#!/usr/bin/env python3
"""Recompute the main numbers in The B2B SaaS AI Visibility Benchmark 2026 from the published CSVs.

Usage:  python verify_benchmark.py                 (reads ./data)
        python verify_benchmark.py path/to/data
        python verify_benchmark.py path/to/data --no-hash   (skip the file fingerprints, recompute only)

Standard library only. It does three things and exits 1 if any of them fails:
1. Opens every published file. A missing or empty file is a FAIL.
2. Rebuilds the derived files from the base files: overlap-per-prompt, cited-domains, summary-metrics and the funnel from
   source-domains, own-domains and results-aggregate. Then it compares the main numbers with the values printed on
   https://citant.ai/research/b2b-saas-ai-visibility-benchmark-2026/ , which are typed into this script.
3. Compares each file with the SHA-256 fingerprints in SHA256SUMS.txt. That catches a change to a value nothing can be
   recomputed from, such as a G2 review count, but it only shows the file is the one we published, not that it is right.
What it cannot check is listed at the end of the run.
"""
import collections
import csv
import hashlib
import os
import random
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
DATA = ARGS[0] if ARGS else os.path.join(HERE, "data")
PFX = "citant-benchmark-2026-"
FILES = {
    "adjudication-v1-5.csv": 60, "chatgpt-funnel-per-question-v1-5.csv": 940, "chatgpt-prompts-as-sent-v1-5.csv": 50,
    "claude-perplexity-recount-v1-4.csv": 188, "data-dictionary-v1-5.csv": None, "cited-domains-v1-5.csv": None,
    "own-domains-v1-5.csv": None, "overlap-per-prompt-v1-5.csv": 50, "queries.csv": 50, "results-aggregate-v1-5.csv": 94,
    "source-domains-v1-5.csv": None, "summary-metrics-v1-5.csv": 59, "tracker-domains-v1-5.csv": None,
    "tracker-hand-reads-v1-3.csv": 32, "tracker-per-engine-v1-3.csv": 282,
}
passed = failed = 0


def check(label, page, got):
    global passed, failed
    ok = page == got
    passed += ok
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label}: page {page}" + ("" if ok else f" | data {got}"))


def rows_agree(label, bad, total):
    """A row-by-row comparison: passes only when no row differs."""
    check(f"{label}, rows that differ of {total}", 0, len(bad))
    for b in bad[:3]:
        print("        ", b)


print("-- Files")
data = {}
for name, want in FILES.items():
    path = os.path.join(DATA, PFX + name)
    if not os.path.isfile(path):
        check(f"file present: {name}", True, False)
        continue
    with open(path, encoding="utf-8-sig", newline="") as f:
        data[name] = list(csv.DictReader(f))
    check(f"rows in {name}", want if want is not None else True, len(data[name]) if want is not None else len(data[name]) > 0)
if failed:
    print(f"\n{passed} passed, {failed} failed. Stopped: a published file is missing or the wrong size, so nothing below can be trusted.")
    sys.exit(1)

res = data["results-aggregate-v1-5.csv"]
fun = data["chatgpt-funnel-per-question-v1-5.csv"]
src = data["source-domains-v1-5.csv"]
ovl = data["overlap-per-prompt-v1-5.csv"]
cdm = data["cited-domains-v1-5.csv"]
adj = data["adjudication-v1-5.csv"]
trk = data["tracker-per-engine-v1-3.csv"]
tdm = data["tracker-domains-v1-5.csv"]
qry = data["queries.csv"]
rec = data["claude-perplexity-recount-v1-4.csv"]
hrd = data["tracker-hand-reads-v1-3.csv"]
sm = data["summary-metrics-v1-5.csv"]
own = data["own-domains-v1-5.csv"]
snt = data["chatgpt-prompts-as-sent-v1-5.csv"]
dic = data["data-dictionary-v1-5.csv"]


def pct(n, d, places=1):
    return round(100 * n / d + 1e-9, places)


def i(r, k):
    return int(r[k])


def named(r, e):
    return i(r, e + "_named_questions") > 0


ENG = ("chatgpt", "claude", "perplexity")
inv = [r for r in res if r["named_on_none_of_5_platforms"] == "yes"]
vis = [r for r in res if r["named_on_none_of_5_platforms"] != "yes"]
QIDS = sorted(r["query_id"] for r in qry)
CAT = {r["query_id"]: r["category"] for r in qry}

print("\n-- Sample")
check("brand entries", 94, len(res))
check("distinct companies", 93, len({r["website"] for r in res}))
check("questions", 50, len(qry))
check("questions per category", {10}, set(collections.Counter(r["category"] for r in qry).values()))
check("tier sizes Leader/Challenger/Small", (20, 39, 35), tuple(sum(r["listing_tier"] == t for r in res) for t in ("Leader", "Challenger", "Small")))
check("brands per category PM/SE/HD/HR/VS", (20, 20, 18, 17, 19), tuple(sum(r["category"] == c for r in res) for c in ("Project Management", "Sales Engagement", "Help Desk", "Core HR", "Vulnerability Scanner")))
small = [i(r, "g2_reviews_total") for r in res if r["listing_tier"] == "Small"]
check("Small-tier rows above 1,000 G2 reviews", 15, sum(x > 1000 for x in small))
check("Small-tier rows above 10,000 G2 reviews", 1, sum(x > 10000 for x in small))
check("largest Small-tier review count above 16,000", True, max(small) > 16000)

print("\n-- Question wording")
listed = {r["query_id"]: r["query_text"] for r in qry}
rows_agree("prompts file repeats the list", [r["query_id"] for r in snt if listed.get(r["query_id"]) != r["query_text_as_listed"]], 50)
rows_agree("overlap file repeats the list", [r["prompt_id"] for r in ovl if listed.get(r["prompt_id"]) != r["question"]], 50)
check("ChatGPT prompts that end in the year", 50, sum(r["chatgpt_prompt_as_sent"].endswith("2026") for r in snt))
rows_agree("ChatGPT prompt = listed question plus the year", [r["query_id"] for r in snt if re.sub(r"\s*2026$", "", r["chatgpt_prompt_as_sent"]).strip().lower() != r["query_text_as_listed"].strip().lower().rstrip("?")], 50)
check("chats that hold two attempts", ["P12", "P16"], sorted(r["query_id"] for r in snt if i(r, "attempts_in_chat") == 2))
check("first attempts carried no year", 2, sum(bool(r["chatgpt_first_attempt"]) and "2026" not in r["chatgpt_first_attempt"] for r in snt))

print("\n-- Finding 1: invisibility")
check("named on none of 5 platforms", 32, len(inv))
check("share", 34, round(100 * len(inv) / 94))
check("invisible with 1,000+ G2 reviews", 16, sum(i(r, "g2_reviews_total") >= 1000 for r in inv))
for b, n in (("ServiceNow", 6876), ("Adobe Workfront", 1234)):
    row = next(r for r in res if r["brand"] == b)
    check(f"{b} reviews, invisible, Leader", (n, "yes", "Leader"), (i(row, "g2_reviews_total"), row["named_on_none_of_5_platforms"], row["listing_tier"]))
check("named at least once ChatGPT/Claude/Perplexity", (39, 45, 46), tuple(sum(named(r, e) for r in res) for e in ENG))
check("invisible by category PM/HD/HR", (6, 10, 4), tuple(sum(r["category"] == c for r in inv) for c in ("Project Management", "Help Desk", "Core HR")))
check("zero test agrees with its columns", True, all((all(not named(r, e) for e in ENG) and i(r, "tracker_mentions_in_category_sep7_14") == 0) == (r in inv) for r in res))
rows_agree("named_by_none_of_3_manual agrees with the counts", [r["brand"] for r in res if (r["named_by_none_of_3_manual"] == "yes") != (not any(named(r, e) for e in ENG))], 94)

print("\n-- Finding 2: reviews and tiers (ChatGPT)")
band = lambda lo, hi: [r for r in res if lo <= i(r, "g2_reviews_total") < hi]
for lab, lo, hi, a, b in (("1,000+", 1000, 10**9, 31, 58), ("100 to 999", 100, 1000, 8, 32), ("10 to 99", 10, 100, 0, 4)):
    x = band(lo, hi)
    check(f"{lab} band named/size", (a, b), (sum(named(r, "chatgpt") for r in x), len(x)))
big = band(1000, 10**9)
check("1,000+ band never named by ChatGPT", 27, sum(not named(r, "chatgpt") for r in big))
check("1,000+ band named on at least one of 5 platforms", 42, sum(r["named_on_none_of_5_platforms"] != "yes" for r in big))
check("tier ladder", (14, 17, 8), tuple(sum(named(r, "chatgpt") for r in res if r["listing_tier"] == t) for t in ("Leader", "Challenger", "Small")))

print("\n-- Base files agree with each other")


def hm(h, b):
    return h == b or h.endswith("." + b)


UGC = ("g2.com", "capterra.com", "reddit.com", "youtube.com", "trustradius.com")
ED = ("forbes.com", "techrepublic.com")
owndoms = {r["domain"] for r in own}


def classify(d):
    if any(hm(d, b) or hm(b, d) for b in owndoms):
        return "own_vendor"
    if any(hm(d, x) for x in UGC):
        return "review_ugc"
    if any(hm(d, x) for x in ED):
        return "editorial"
    return "institutional" if re.search(r"\.(org|edu)(\.[a-z]{2})?$", d) else "other"


rows_agree("source class follows the stated rule", [(r["query_id"], r["engine"], r["domain"], r["class"]) for r in src if r["class"] != classify(r["domain"])], len(src))
rows_agree("source category follows the question", [r["domain"] for r in src if CAT.get(r["query_id"]) != r["category"]], len(src))
rows_agree("every brand has its website in own-domains", [r["brand"] for r in res if not any(o["brand"] == r["brand"] and o["category"] == r["category"] and o["basis"] == "website" for o in own)], 94)
layer = collections.defaultdict(set)
for r in src:
    layer[(r["engine"], r["layer"], r["query_id"])].add(r["domain"])
consulted = {e: {q: layer[(e, "consulted", q)] for q in QIDS} for e in ENG}
cited = {q: layer[("chatgpt", "cited", q)] for q in QIDS}
image = {q: layer[("chatgpt", "image_only", q)] for q in QIDS}

print("\n-- Finding 3: funnel (940 brand-question pairs on ChatGPT)")
N = sum(i(r, "named") for r in fun)
R = sum(i(r, "own_site_retrieved") for r in fun)
C = sum(i(r, "own_site_cited") for r in fun)
RC = sum(i(r, "own_site_retrieved") and i(r, "own_site_cited") for r in fun)
check("pairs", 940, len(fun))
check("named, retrieved, cited", (200, 177, 75), (N, R, C))
check("percent", (21.3, 18.8, 8.0), (pct(N, 940), pct(R, 940), pct(C, 940)))
check("retrieved pairs also cited", (72, 40.7), (RC, pct(RC, R)))
check("cited pairs not in search results", 3, C - RC)
check("image-only pairs, kept apart", 2, sum(i(r, "own_site_image_only") for r in fun))
doms = collections.defaultdict(set)
for r in own:
    doms[(r["brand"], r["category"])].add(r["domain"])


def hit(sets, r):
    return int(any(hm(x, d) or hm(d, x) for x in sets[r["query_id"]] for d in doms[(r["brand"], r["category"])]))


rows_agree("funnel retrieved rebuilt from own-domains and source-domains", [(r["brand"], r["query_id"]) for r in fun if hit(consulted["chatgpt"], r) != i(r, "own_site_retrieved")], 940)
rows_agree("funnel cited rebuilt from own-domains and source-domains", [(r["brand"], r["query_id"]) for r in fun if hit(cited, r) != i(r, "own_site_cited")], 940)
rows_agree("funnel image-only rebuilt", [(r["brand"], r["query_id"]) for r in fun if int(not i(r, "own_site_cited") and hit(image, r)) != i(r, "own_site_image_only")], 940)
per = collections.Counter()
fn = collections.Counter()
for r in fun:
    per[(r["brand"], r["category"])] += i(r, "own_site_retrieved") * 1000 + i(r, "own_site_cited")
    fn[(r["brand"], r["category"])] += i(r, "named")
rows_agree("funnel agrees with results file", [r["brand"] for r in res if per[(r["brand"], r["category"])] != i(r, "chatgpt_own_site_retrieved_questions") * 1000 + i(r, "chatgpt_own_site_cited_questions")], 94)
rows_agree("funnel named agrees with results file", [r["brand"] for r in res if fn[(r["brand"], r["category"])] != i(r, "chatgpt_named_questions")], 94)

print("\n-- Finding 4: source overlap and shortlists")
sets = {e: set().union(*consulted[e].values()) for e in ENG}
union = set().union(*sets.values())
hits = collections.Counter(sum(d in sets[e] for e in ENG) for d in union)
check("distinct domains consulted", 917, len(union))
check("on one, two, three engines", (655, 187, 75), (hits[1], hits[2], hits[3]))
check("one engine, two engines, all three percent", (71.4, 20.4, 8.2), (pct(hits[1], len(union)), pct(hits[2], len(union)), pct(hits[3], len(union))))


def jac(a, b):
    return round(len(a & b) / len(a | b), 3) if a | b else 0.0


bad = []
for r in ovl:
    q = r["prompt_id"]
    s = [consulted[e][q] for e in ENG]
    u = set().union(*s)
    n = collections.Counter(sum(d in x for x in s) for d in u)
    allp = s[0] & s[1] & s[2]
    want = {"chatgpt_consulted": len(s[0]), "claude_consulted": len(s[1]), "perplexity_consulted": len(s[2]), "chatgpt_cited": len(cited[q]), "chatgpt_image_only": len(image[q]),
            "union_domains": len(u), "on_exactly_one": n[1], "on_exactly_two": n[2], "on_all_present": len(allp)}
    for k, v in want.items():
        if i(r, k) != v:
            bad.append((q, k, r[k], v))
    if r["claude_listed_web_sources"] != ("yes" if s[1] else "no"):
        bad.append((q, "claude_listed_web_sources"))
    if set(filter(None, r["domains_on_all_present"].split(";"))) != allp:
        bad.append((q, "domains_on_all_present"))
    for k, v in (("jaccard_chatgpt_claude", jac(s[0], s[1])), ("jaccard_chatgpt_perplexity", jac(s[0], s[2])), ("jaccard_claude_perplexity", jac(s[1], s[2]))):
        if r[k] != "" and abs(float(r[k]) - v) > 0.0011:
            bad.append((q, k, r[k], v))
    if abs(float(r["jaccard_all_present"]) - round(len(allp) / len(u), 3)) > 0.0011:
        bad.append((q, "jaccard_all_present", r["jaccard_all_present"]))
rows_agree("overlap file rebuilt from source-domains", bad, 50)
mean = lambda rows, k: round(statistics.mean(float(r[k] or 0) for r in rows), 3)
PAIRS = ("jaccard_chatgpt_claude", "jaccard_chatgpt_perplexity", "jaccard_claude_perplexity")
check("mean per-question Jaccard, all 50", 0.021, round(statistics.mean(float(r["jaccard_all_present"]) if r["claude_listed_web_sources"] == "yes" else 0.0 for r in ovl), 3))
check("pairwise means, all 50 (low, high)", (0.068, 0.097), (min(mean(ovl, k) for k in PAIRS), max(mean(ovl, k) for k in PAIRS)))
q43 = [r for r in ovl if r["claude_listed_web_sources"] == "yes"]
check("questions where Claude listed no source", 7, 50 - len(q43))
check("three-way Jaccard on the 43", 0.024, mean(q43, "jaccard_all_present"))
check("pairwise on the 43 (low, high)", (0.072, 0.113), (min(mean(q43, k) for k in PAIRS), max(mean(q43, k) for k in PAIRS)))
check("pages shared by ChatGPT and Perplexity", 65, sum(i(r, "page_shared_chatgpt_perplexity") for r in ovl))
both = [r for r in res if named(r, "chatgpt")]
check("Claude named of ChatGPT's 39", 36, sum(named(r, "claude") for r in both))
any3 = [r for r in res if any(named(r, e) for e in ENG)]
check("named by any manual engine, by all three", (54, 34), (len(any3), sum(all(named(r, e) for e in ENG) for r in res)))


def ranks(v):
    o = sorted(range(len(v)), key=lambda j: v[j])
    out = [0.0] * len(v)
    a = 0
    while a < len(o):
        b = a
        while b + 1 < len(o) and v[o[b + 1]] == v[o[a]]:
            b += 1
        for j in range(a, b + 1):
            out[o[j]] = (a + b) / 2 + 1
        a = b + 1
    return out


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return num / (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5


cnt = {e: [i(r, e + "_named_questions") for r in res] for e in ENG}
rho = [spearman(cnt[a], cnt[b]) for a, b in (("chatgpt", "claude"), ("chatgpt", "perplexity"), ("claude", "perplexity"))]
check("rank correlation (low, high)", (0.84, 0.89), (round(min(rho), 2), round(max(rho), 2)))

print("\n-- Finding 4: the long tail")
inc = collections.Counter(d for e in ENG for s in consulted[e].values() for d in s)
one = {d for d in union if sum(d in sets[e] for e in ENG) == 1}
pairs = collections.Counter((q, d) for e in ENG for q, s in consulted[e].items() for d in s)
nq = collections.Counter(d for _, d in pairs)  # distinct questions per domain, any engine
seen2 = [d for d in union if nq[d] >= 2]
check("consulted incidences, all three engines", 2158, sum(inc.values()))
check("one-engine domains consulted once", 524, sum(inc[d] == 1 for d in one))
check("domains consulted on two or more questions, those on one engine, percent", (357, 131, 36.7), (len(seen2), sum(d in one for d in seen2), pct(sum(d in one for d in seen2), len(seen2))))
big = [d for d in union if nq[d] >= 8]
check("domains consulted on eight or more questions, those on all three", (26, 13), (len(big), sum(all(d in sets[e] for e in ENG) for d in big)))
two_up = sum(n >= 2 for n in pairs.values())
check("question-domain pairs, on two or more engines, percent, on all three", (1892, 232, 12.3, 34), (len(pairs), two_up, pct(two_up, len(pairs)), sum(n == 3 for n in pairs.values())))
pg = {e: sum(int(r[e + "_pages"] or 0) for r in ovl) for e in ENG}
sh = {k: sum(int(r["page_shared_" + k] or 0) for r in ovl) for k in ("chatgpt_perplexity", "chatgpt_claude", "claude_perplexity")}
check("page pairs shared, ChatGPT and Perplexity", (65, 2517), (sh["chatgpt_perplexity"], pg["chatgpt"] + pg["perplexity"] - sh["chatgpt_perplexity"]))
check("page pairs shared, ChatGPT and Claude", (74, 2125), (sh["chatgpt_claude"], pg["chatgpt"] + pg["claude"] - sh["chatgpt_claude"]))
check("page pairs shared, Claude and Perplexity", (71, 1018), (sh["claude_perplexity"], pg["claude"] + pg["perplexity"] - sh["claude_perplexity"]))

print("\n-- Finding 5: hand lists")
ct = collections.Counter(d for s in cited.values() for d in s)
ed = sum(ct[d] for d in ("forbes.com", "techrepublic.com", "businessinsider.com", "techradar.com", "business.com", "fitsmallbusiness.com"))
rv = sum(ct[d] for d in ("g2.com", "capterra.com", "reddit.com", "youtube.com", "trustradius.com", "softwareadvice.com", "peerspot.com"))
check("editorial with example publishers (not a complete list), percent", (6, 2.6), (ed, pct(ed, sum(ct.values()))))
check("review sites with Software Advice and PeerSpot (not a complete list), percent", (12, 5.3), (rv, pct(rv, sum(ct.values()))))
check("cited rows not in that question's search results", 11, sum(len(s - consulted["chatgpt"].get(q, set())) for q, s in cited.items()))

print("\n-- Limitations: questions that name a tracked brand")
OWNQ = {"Asana": ["P03"], "Atlassian": ["P04"], "monday.com": ["P07"], "Outreach": ["P13", "P14"], "Salesloft": ["P14"], "Apollo.io": ["P17"], "HubSpot": ["P19"], "Zendesk": ["P23", "P24"], "Intercom": ["P24"],
        "Freshworks": ["P27"], "BambooHR": ["P33"], "Rippling": ["P34"], "Gusto": ["P34"], "Deel": ["P37"], "Tenable": ["P43"], "Intruder": ["P44"]}
BQ = {q for v_ in OWNQ.values() for q in v_}
key = lambda r: (r["brand"], r["category"])
ids = lambda s: set(filter(None, re.split(r"[;, ]+", s)))
NQ = {e: {key(r): set() for r in res} for e in ENG}
for r in fun:
    if r["named"] == "1":
        NQ["chatgpt"][key(r)].add(r["query_id"])
for r in rec:
    NQ[r["engine"].lower()][key(r)] = ids(r["named_question_ids_v1_4"])
for r in adj:
    e = r["engine"].lower()
    if e in NQ and r["current_count_from"].strip() and len(ids(r["current_question_ids"])) == int(r["current_named_questions"] or 0):
        NQ[e][key(r)] = ids(r["current_question_ids"])
rows_agree("named question ids agree with the results file", [(key(r), e) for r in res for e in ENG if len(NQ[e][key(r)]) != i(r, e + "_named_questions")], 94)
check("questions naming a tracked brand", 15, len(BQ))
check("named pairs on a question naming that brand, per engine", {18}, {sum(len(NQ[e][k] & set(OWNQ.get(k[0], []))) for k in NQ[e]) for e in ENG})
ks = list(NQ["chatgpt"])
wo = {e: {k: NQ[e][k] - set(OWNQ.get(k[0], [])) for k in ks} for e in ENG}
check("at-least-once without those pairs", (39, 45, 46), tuple(sum(bool(wo[e][k]) for k in ks) for e in ENG))
wq = {e: {k: NQ[e][k] - BQ for k in ks} for e in ENG}
cg = {k for k in ks if wq["chatgpt"][k]}
check("without all 15 questions: ChatGPT named, Claude shares", (36, 34), (len(cg), sum(bool(wq["claude"][k]) for k in cg)))
rq = [spearman([len(wq[a][k]) for k in ks], [len(wq[b][k]) for k in ks]) for a, b in (("chatgpt", "claude"), ("chatgpt", "perplexity"), ("claude", "perplexity"))]
check("without all 15 questions: rank correlation (low, high)", (0.83, 0.88), (round(min(rq), 2), round(max(rq), 2)))

T = {(r["brand"], r["category"], r["engine"]): r for r in trk}
sent = []
for r in res:
    a, b = T[(r["brand"], r["category"], "AI Overview")]["sentiment_project_level"], T[(r["brand"], r["category"], "ChatGPT")]["sentiment_project_level"]
    if a and b:
        sent.append((float(a), float(b)))
check("sentiment: AI Overviews above ChatGPT", (24, 25), (sum(a > b for a, b in sent), len(sent)))
check("sentiment: median gap", 18, statistics.median(a - b for a, b in sent))


def t(b, e):
    r = next(x for x in trk if x["brand"] == b and x["engine"] == e)
    return i(r, "chats_mentioning_brand"), i(r, "chats_in_category")


for b, x, y in (("Apollo.io", 77, 54), ("ClickUp", 75, 57), ("Asana", 73, 55)):
    g = lambda e: int(float(next(r for r in trk if r["brand"] == b and r["engine"] == e)["sentiment_project_level"]))
    check(f"{b} sentiment", (x, y), (g("AI Overview"), g("ChatGPT")))
check("Aikido AIO/Gemini/ChatGPT chats", ((13, 30), (8, 30), (1, 30)), (t("Aikido Security", "AI Overview"), t("Aikido Security", "Gemini"), t("Aikido Security", "ChatGPT")))
check("Aikido G2 reviews", 260, i(next(r for r in res if r["brand"] == "Aikido Security"), "g2_reviews_total"))

print("\n-- Finding 5: citation mix")


def mix(engine, lay):
    c = collections.Counter(r["class"] for r in src if r["engine"] == engine and r["layer"] == lay)
    return c, sum(c.values())


c, n = mix("chatgpt", "cited")
check("ChatGPT text citations", 227, n)
check("own/ugc/editorial/institutional/other", (78, 9, 1, 5, 134), tuple(c[k] for k in ("own_vendor", "review_ugc", "editorial", "institutional", "other")))
check("percent", (34.4, 4.0, 0.4, 2.2, 59.0), tuple(pct(c[k], n) for k in ("own_vendor", "review_ugc", "editorial", "institutional", "other")))
forms = collections.Counter(r["citation_form"] for r in src if r["layer"] == "cited")
check("primary, supporting, plain links", (170, 49, 8), (forms["primary"], forms["supporting"], forms["plain_link"]))
check("image-only incidences, kept apart", 24, mix("chatgpt", "image_only")[1])
c1, n1 = mix("chatgpt", "consulted")
c2, n2 = mix("claude", "consulted")
c3, n3 = mix("perplexity", "consulted")
check("consulted incidences", (1161, 333, 664), (n1, n2, n3))
check("own-vendor share of ChatGPT consulted", (183, 15.8), (c1["own_vendor"], pct(c1["own_vendor"], n1)))
check("ChatGPT consulted ugc/institutional/editorial percent", (6.5, 2.8, 0.9), tuple(pct(c1[k], n1) for k in ("review_ugc", "institutional", "editorial")))
check("other-domain share, low and high", (74.0, 86.3), (min(pct(x["other"], y) for x, y in ((c1, n1), (c2, n2), (c3, n3))), max(pct(x["other"], y) for x, y in ((c1, n1), (c2, n2), (c3, n3)))))


def qs(domain, lay, cat=None):
    return len({r["query_id"] for r in src if r["engine"] == "chatgpt" and r["domain"] == domain and r["layer"] == lay and (cat is None or r["category"] == cat)})


check("Reddit consulted/cited", (27, 1), (qs("reddit.com", "consulted"), qs("reddit.com", "cited")))
check("YouTube consulted/cited", (21, 0), (qs("youtube.com", "consulted"), qs("youtube.com", "cited")))
check("Reddit Sales Engagement", (8, 1), (qs("reddit.com", "consulted", "Sales Engagement"), qs("reddit.com", "cited", "Sales Engagement")))
check("YouTube Core HR", (8, 0), (qs("youtube.com", "consulted", "Core HR"), qs("youtube.com", "cited", "Core HR")))
check("getmacha.com Help Desk consulted/cited", (7, 3), (qs("getmacha.com", "consulted", "Help Desk"), qs("getmacha.com", "cited", "Help Desk")))
check("arxiv.org, detectify.com, snyk.io, g2.com in Vulnerability Scanner", (4, 3, 3, 2), tuple(qs(d, "cited", "Vulnerability Scanner") for d in ("arxiv.org", "detectify.com", "snyk.io", "g2.com")))
check("owasp.org cited in Vulnerability Scanner", True, qs("owasp.org", "cited", "Vulnerability Scanner") > 0)
check("toolradar.com tops third parties in Core HR", 3, max(i(r, "questions") for r in cdm if r["category"] == "Core HR" and r["layer"] == "cited" and r["class"] != "own_vendor"))
check("toolradar.com Core HR cited", 3, qs("toolradar.com", "cited", "Core HR"))
inst = collections.Counter(r["category"] for r in src if r["layer"] == "cited" and r["class"] == "institutional")
check("most institutional citations", "Vulnerability Scanner", inst.most_common(1)[0][0])
check("G2 consulted/cited questions", (14, 5), (qs("g2.com", "consulted"), qs("g2.com", "cited")))
want = {}
for r in src:
    if r["engine"] == "chatgpt":
        want.setdefault((r["category"], r["layer"], r["domain"]), []).append(r["query_id"])
got = {(r["category"], r["layer"], r["domain"]): r for r in cdm}
bad = [k for k in want if k not in got or sorted(want[k]) != sorted(got[k]["question_ids"].split(";")) or i(got[k], "questions") != len(want[k]) or got[k]["class"] != classify(k[2]) or got[k]["of_questions"] != "10"]
bad += [k for k in got if k not in want]
rows_agree("cited-domains rebuilt from source-domains", bad, len(got))
board = {}
for cat in dict.fromkeys(r["category"] for r in qry):
    rows = [r for r in cdm if r["category"] == cat and r["layer"] == "cited" and r["class"] != "own_vendor"]
    top = collections.Counter(i(r, "questions") for r in rows)
    board[cat] = sorted(top.items(), reverse=True)
check("top-cited ties (questions: domains)", {
    "Project Management": [(2, 1), (1, 21)], "Sales Engagement": [(4, 1), (3, 1), (2, 2), (1, 19)], "Help Desk": [(3, 1), (2, 3), (1, 25)],
    "Core HR": [(3, 1), (2, 7), (1, 17)], "Vulnerability Scanner": [(4, 1), (3, 2), (2, 2), (1, 14)]}, board)
tr = {(r["project"], r["domain"]): r for r in tdm}
check("stackfyi.com tracker retrieved/cited", (19, 28), (i(tr[("A", "stackfyi.com")], "retrieved_chats"), i(tr[("A", "stackfyi.com")], "citations")))
check("taskrhino.ca tracker retrieved/cited/rate", (7, 25, "3.57"), (i(tr[("A", "taskrhino.ca")], "retrieved_chats"), i(tr[("A", "taskrhino.ca")], "citations"), tr[("A", "taskrhino.ca")]["citation_rate"]))
check("apollo.io tracker retrieved/cited", (34, 86), (i(tr[("A", "apollo.io")], "retrieved_chats"), i(tr[("A", "apollo.io")], "citations")))
ownc = collections.Counter()
for r in fun:
    ownc[r["brand"]] += i(r, "own_site_cited")
check("top own-site cited on the manual run", [("Intercom", 8), ("ClickUp", 7), ("Apollo.io", 6)], ownc.most_common(3))

print("\n-- Finding 6: crawler access")
sc = lambda rows: [float(r["ai_access_score_2026_09_26"]) for r in rows if r["ai_access_score_2026_09_26"].strip()]
si, sv = sc(inv), sc(vis)
check("scored entries", 84, len(si) + len(sv))
check("invisible scored, AI-ready", (30, 24), (len(si), sum(x >= 75 for x in si)))
check("means", (82.0, 84.8), (round(statistics.mean(si), 1), round(statistics.mean(sv), 1)))
check("medians", (91, 91), (statistics.median(si), statistics.median(sv)))
rng = random.Random(2026)
pool, obs, more, RUNS = si + sv, abs(statistics.mean(si) - statistics.mean(sv)), 0, 20000
for _ in range(RUNS):
    rng.shuffle(pool)
    more += abs(sum(pool[:30]) / 30 - sum(pool[30:]) / 54) >= obs - 1e-9
check("permutation p, two-sided, within 0.02 of 0.53", True, abs(more / RUNS - 0.53) <= 0.02)

print("\n-- Finding 7 and categories (repeated runs)")
check("Asana ChatGPT, AI Overviews chats", ((28, 30), (19, 30)), (t("Asana", "ChatGPT"), t("Asana", "AI Overview")))
check("chats per engine per category, low and high", (18, 30), (min(i(r, "chats_in_category") for r in trk), max(i(r, "chats_in_category") for r in trk)))


def comb(b, c_):
    rows = [r for r in trk if r["brand"] == b and r["category"] == c_]
    return sum(i(r, "chats_mentioning_brand") for r in rows), sum(i(r, "chats_in_category") for r in rows)


rows_agree("tracker per-engine visibility = mentions / chats", [(r["brand"], r["engine"]) for r in trk if r["visibility_in_category"] and abs(float(r["visibility_in_category"]) - i(r, "chats_mentioning_brand") / i(r, "chats_in_category")) > 0.0001], len(trk))
rows_agree("results tracking visibility = tracker mentions / chats", [r["brand"] for r in res if r["tracking_visibility_in_category"].strip() and abs(float(r["tracking_visibility_in_category"]) - comb(r["brand"], r["category"])[0] / comb(r["brand"], r["category"])[1]) > 0.0001], 94)
vispct = lambda b, c_: round(100 * comb(b, c_)[0] / comb(b, c_)[1])
check("Project Management top three", (81, 79, 77), tuple(vispct(b, "Project Management") for b in ("Atlassian", "ClickUp", "Asana")))
check("Apollo.io chats", (77, 89), comb("Apollo.io", "Sales Engagement"))
check("Zendesk, Intercom, Freshworks range", (72, 73), (min(vispct(b, "Help Desk") for b in ("Zendesk", "Intercom", "Freshworks")), max(vispct(b, "Help Desk") for b in ("Zendesk", "Intercom", "Freshworks"))))
hr = sorted((vispct(r["brand"], "Core HR") for r in res if r["category"] == "Core HR"), reverse=True)
check("Core HR Rippling, Gusto", (90, 86), (vispct("Rippling", "Core HR"), vispct("Gusto", "Core HR")))
check("Core HR next group and sixth place", (62, 66, 25), (min(hr[2:5]), max(hr[2:5]), hr[5]))
ten = [t("Tenable", e) for e in ("ChatGPT", "Gemini", "AI Overview")]
check("Tenable range", (43, 57), (round(100 * min(a / b for a, b in ten)), round(100 * max(a / b for a, b in ten))))
check("CrowdStrike chats each engine", [(1, 30)] * 3, [t("CrowdStrike", e) for e in ("ChatGPT", "Gemini", "AI Overview")])
avg = lambda c_, k: round(statistics.mean(i(r, k) for r in ovl if r["category"] == c_), 1)
check("Project Management consulted, cited per question", (24.2, 3.9), (avg("Project Management", "chatgpt_consulted"), avg("Project Management", "chatgpt_cited")))
check("Vulnerability Scanner consulted per question, lowest", (15.7, True), (avg("Vulnerability Scanner", "chatgpt_consulted"), avg("Vulnerability Scanner", "chatgpt_consulted") == min(avg(c_, "chatgpt_consulted") for c_ in {r["category"] for r in ovl})))
hd = {c_: round(statistics.mean(float(r["jaccard_chatgpt_claude"]) for r in q43 if r["category"] == c_), 3) for c_ in {r["category"] for r in q43}}
check("Help Desk ChatGPT-Claude Jaccard, lowest", (0.034, "Help Desk"), (hd["Help Desk"], min(hd, key=hd.get)))

print("\n-- Summary file: every row rebuilt")
LBL = {"own vendor": "own_vendor", "review ugc": "review_ugc", "editorial": "editorial", "institutional": "institutional", "all other domains": "other"}


def rebuild(r):
    m = r["metric"]
    if m == "brands named at least once":
        return sum(named(x, r["engine"]) for x in res), 94
    if m == "brands named by none of the 3 manual engines":
        return sum(not any(named(x, e) for e in ENG) for x in res), 94
    if m == "brands named on none of 5 platforms":
        return len(inv), 94
    if m == "brand-question pairs named":
        return N, 940
    if m == "brand-question pairs own site retrieved":
        return R, 940
    if m == "brand-question pairs own site cited":
        return C, 940
    if m == "consulted domains on exactly one engine":
        return hits[1], len(union)
    if m == "consulted domains on exactly two engines":
        return hits[2], len(union)
    if m == "consulted domains on all three engines":
        return hits[3], len(union)
    if m.startswith("source type share: "):
        cc, nn = mix(r["engine"], r["layer"])
        return cc[LBL[m.split(": ")[1]]], nn
    if m in ("reddit.com present", "youtube.com present"):
        cat = None if r["category"] == "ALL" else r["category"]
        return qs(m.split()[0], r["layer"], cat), 50 if cat is None else 10
    if m == "own site retrieved pairs that were also cited":
        return RC, R
    if m == "own site cited pairs not in that question's search results":
        return C - RC, C
    if m == "own site pairs in an image carousel or thumbnail only":
        return sum(i(x, "own_site_image_only") for x in fun), 940
    if m == "image-only domain incidences":
        return mix("chatgpt", "image_only")[1], mix("chatgpt", "image_only")[1] + mix("chatgpt", "cited")[1]
    return None


bad = []
for r in sm:
    w = rebuild(r)
    if w is None or (i(r, "num"), i(r, "den")) != w or abs(float(r["rate"]) - w[0] / w[1]) > 0.00006:
        bad.append((r["metric"], r["engine"], r["layer"], r["category"], r["num"], r["den"], r["rate"], w))
rows_agree("summary rows", bad, len(sm))

print("\n-- Other files")
check("hand read: ChatGPT pairs moved 180 to 200", 20, sum(i(r, "hand_read_after") - i(r, "hand_read_before") for r in adj if r["engine"] == "chatgpt"))
check("hand read: Claude new brands Front, Remote", ["Front", "Remote"], sorted(r["brand"] for r in adj if r["engine"] == "claude" and i(r, "hand_read_before") == 0 and i(r, "hand_read_after") > 0))
rows_agree("hand read count = its question ids", [(r["brand"], r["engine"]) for r in adj if i(r, "hand_read_after") != len(list(filter(None, r["hand_read_question_ids"].split(";"))))], 60)
rr = {(r["brand"], r["category"], r["engine"]): r for r in rec}
rows_agree("recount file agrees with results file", [(r["brand"], e) for r in res for e in ("claude", "perplexity") if i(rr[(r["brand"], r["category"], e)], "named_questions_v1_4") != i(r, e + "_named_questions")], 188)
rows_agree("recount changed flag follows its columns", [(r["brand"], r["engine"]) for r in rec if (r["changed"] == "yes") != (r["named_questions_v1_3"] != r["named_questions_v1_4"])], 188)
rows_agree("adjudication current counts agree with results file", [(a["brand"], a["engine"]) for a in adj if i(a, "current_named_questions") != i(next(r for r in res if r["brand"] == a["brand"] and r["category"] == a["category"]), a["engine"] + "_named_questions")], 60)
rows_agree("tracker hand reads name a tracked brand", [r["brand"] for r in hrd if not any(x["brand"] == r["brand"] and x["category"] == r["category"] for x in res) or not r["decision"].strip()], len(hrd))
meant = collections.defaultdict(set)
for r in dic:
    for c_ in r["column"].split(" / "):
        meant[r["file"]].add(c_.strip())
bad = []
for name, rows in data.items():
    key = re.sub(r"(-v1-\d)?\.csv$", "", name)
    if key == "data-dictionary":
        continue
    known = meant[key]
    for col in rows[0]:
        if col not in known and not any(k.endswith("*") and col.startswith(k[:-1]) or k.startswith("*") and col.endswith(k[1:]) for k in known):
            bad.append((key, col))
rows_agree("every column has a dictionary row", bad, sum(len(v[0]) for k, v in data.items() if k != "data-dictionary-v1-5.csv"))
check("dictionary rows all carry a meaning", True, all(r["meaning"].strip() for r in dic))

if "--no-hash" not in sys.argv:
    print("\n-- File fingerprints")
    sums = os.path.join(HERE, "SHA256SUMS.txt")
    if not os.path.isfile(sums):
        check("SHA256SUMS.txt present", True, False)
    else:
        want = {}
        with open(sums, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    h, name = line.split(None, 1)
                    want[name.strip().lstrip("*")] = h
        check("fingerprints listed", len(FILES), len(want))
        bad = []
        for name in FILES:
            with open(os.path.join(DATA, PFX + name), "rb") as f:
                # line endings are normalised, so a Windows checkout with autocrlf hashes the same
                got = hashlib.sha256(f.read().replace(b"\r\n", b"\n")).hexdigest()
            if want.get(PFX + name) != got:
                bad.append(name)
        rows_agree("files match their published fingerprint", bad, len(FILES))

print(f"\n{passed} passed, {failed} failed")
print("""
What this script does not prove:
- The page itself: expected values are typed in here from the page, so it shows the files agree with those values, not that the live page still prints them.
- The raw captures (50 ChatGPT payloads, the Claude and Perplexity transcripts, screenshots): on request, hamza@citant.ai. This script starts from the published CSVs.
- Source class calls and own-domain calls: it checks that the stated rule was applied, not that the rule or a call is right.
- Word-level hand reads: the files carry each decision, not the sentence read.
- The tracker: tracker-per-engine and tracker-domains are exports from a third-party platform; tracker_mentions cannot be rebuilt from them.
- Question wording on Claude and Perplexity, memory settings, VPN exit, and capture dates: none of these can be seen in the published files. Memory rests on settings screenshots and the US VPN rests on our own record.
- The AI Crawler Access scan: scores are published, the 21 checks and 15 crawlers run in the live tool, not here.
- Page-level overlap columns: only their totals are checked, because page URLs are not published.
- The 15 questions naming a tracked brand are our hand list, not computed.
- G2 review counts and listing order: recorded on September 2 to 3, 2026; the live pages change.
""")
sys.exit(1 if failed else 0)
