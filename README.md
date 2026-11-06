---
license: cc-by-4.0
language:
- en
pretty_name: The B2B SaaS AI Visibility Benchmark 2026
size_categories:
- 1K<n<10K
task_categories:
- tabular-classification
tags:
- ai-search
- generative-engine-optimization
- llm-evaluation
- brand-visibility
- b2b-saas
- chatgpt
- perplexity
- claude
configs:
- config_name: results_aggregate
  data_files: data/citant-benchmark-2026-results-aggregate-v1-5.csv
- config_name: queries
  data_files: data/citant-benchmark-2026-queries.csv
- config_name: overlap_per_prompt
  data_files: data/citant-benchmark-2026-overlap-per-prompt-v1-5.csv
- config_name: summary_metrics
  data_files: data/citant-benchmark-2026-summary-metrics-v1-5.csv
- config_name: cited_domains
  data_files: data/citant-benchmark-2026-cited-domains-v1-5.csv
- config_name: tracker_per_engine
  data_files: data/citant-benchmark-2026-tracker-per-engine-v1-3.csv
- config_name: adjudication
  data_files: data/citant-benchmark-2026-adjudication-v1-5.csv
- config_name: tracker_hand_reads
  data_files: data/citant-benchmark-2026-tracker-hand-reads-v1-3.csv
- config_name: claude_perplexity_recount
  data_files: data/citant-benchmark-2026-claude-perplexity-recount-v1-4.csv
- config_name: chatgpt_prompts_as_sent
  data_files: data/citant-benchmark-2026-chatgpt-prompts-as-sent-v1-5.csv
- config_name: source_domains
  data_files: data/citant-benchmark-2026-source-domains-v1-5.csv
- config_name: chatgpt_funnel_per_question
  data_files: data/citant-benchmark-2026-chatgpt-funnel-per-question-v1-5.csv
- config_name: own_domains
  data_files: data/citant-benchmark-2026-own-domains-v1-5.csv
- config_name: tracker_domains
  data_files: data/citant-benchmark-2026-tracker-domains-v1-5.csv
---

# The B2B SaaS AI Visibility Benchmark 2026 (dataset v1.5)

Which B2B SaaS brands do AI answer engines name when a buyer asks for software? 94 brand entries (93 companies) across five
G2 categories (Project Management, Sales Engagement, Help Desk, Core HR, Vulnerability Scanner), 50 real buying questions
(10 per category, frozen before collection), five AI platforms.

Full report, method and limitations: https://citant.ai/research/b2b-saas-ai-visibility-benchmark-2026/

Check it yourself: `python verify_benchmark.py` reads `data/`, recomputes the main numbers, prints PASS or FAIL for each number it tests, and lists what it cannot check. Python 3 standard library only. `SHA256SUMS.txt` holds the fingerprint of every file in `data/`, and the script checks those too.

## Headline numbers (each recomputable from these files)
- 32 of 94 brands (34%) were named on none of five platforms (ChatGPT, Claude, Perplexity, Google Gemini, Google AI Overviews), on any of their category's questions, in any run we hold.
- Named at least once, of 94: ChatGPT 39, Claude 45, Perplexity 46. ChatGPT names the fewest brands; Claude and Perplexity are one brand apart.
- Of 917 distinct domains consulted by ChatGPT, Claude and Perplexity on the same 50 questions, 71.4% were consulted by exactly one engine and 8.2% by all three, and most of the one-engine domains were consulted just once. Yet the engines largely agree on brands: Claude named 36 of the 39 brands ChatGPT named.
- ChatGPT consulted reddit.com on 27 of 50 questions and cited it on 1.
- Tracked vendors' own domains were 34.4% of ChatGPT's text citations (78 of 227) and 15.8% of what it consulted (183 of 1,161).
- Of the 30 never-named brands we could scan, 24 are AI-ready (AI Access Score 75 or higher); their mean score (82.0) is about the same as the 54 scanned named brands (84.8).

## Files (`data/`)
Files that did not change in v1.5 keep their earlier names and are byte-identical to the earlier release.

| File | Rows | What it is |
|---|---|---|
| citant-benchmark-2026-queries.csv | 50 | The 50 buying questions as listed; ChatGPT received them with the year added, see chatgpt-prompts-as-sent (unchanged) |
| citant-benchmark-2026-chatgpt-prompts-as-sent-v1-5.csv | 50 | New in v1.5: the wording ChatGPT received on each question, read from the payloads |
| citant-benchmark-2026-results-aggregate-v1-5.csv | 94 | One row per brand entry: named counts per engine, ChatGPT own-site retrieval and citation, AI Access Scores, tracker visibility, the five-platform flag |
| citant-benchmark-2026-chatgpt-funnel-per-question-v1-5.csv | 940 | New in v1.5: one row per brand entry and question: named, own site retrieved, cited, image only |
| citant-benchmark-2026-overlap-per-prompt-v1-5.csv | 50 | Per question cross-engine source overlap (domain and page level, Jaccard) |
| citant-benchmark-2026-source-domains-v1-5.csv | 2,409 | New in v1.5: one row per question, engine, layer and registrable domain, with its class |
| citant-benchmark-2026-own-domains-v1-5.csv | 105 | New in v1.5: every domain counted as a tracked brand's own, and why |
| citant-benchmark-2026-summary-metrics-v1-5.csv | 59 | Summary metrics behind the main aggregates in this report as num / den / rate |
| citant-benchmark-2026-cited-domains-v1-5.csv | 801 | Every registrable domain ChatGPT cited, showed only in images, or retrieved, per category, no cap |
| citant-benchmark-2026-tracker-per-engine-v1-3.csv | 282 | Repeated-run figures per brand and engine (3 runs of each question, September 7), own-category denominator (unchanged) |
| citant-benchmark-2026-tracker-domains-v1-5.csv | 48 | New in v1.5: the tracker source rows the report quotes |
| citant-benchmark-2026-tracker-hand-reads-v1-3.csv | 32 | Tracker hits read by hand and excluded from the zero-mention test (unchanged) |
| citant-benchmark-2026-adjudication-v1-5.csv | 60 | Hand-read named counts for common-word brand names, before and after, beside the count in force today |
| citant-benchmark-2026-claude-perplexity-recount-v1-4.csv | 188 | Every brand entry x engine (Claude, Perplexity), named count in v1.3 and v1.4 and the v1.4 question ids (unchanged) |
| citant-benchmark-2026-data-dictionary-v1-5.csv | 71 | Every column defined |

All files are UTF-8, comma-separated, LF line endings, except queries.csv, which keeps its earlier CRLF line endings and byte order mark. SHA256SUMS.txt hashes each file with CRLF changed to LF, so use verify_benchmark.py and not sha256sum -c.
The repo also holds `panel-fingerprints/`, hashes of Citant's daily AI answer panel. It is a separate log, and no number in this dataset uses it.
Charts: `citant-benchmark-2026-charts-v1-5.zip` (10 charts and the share card, CC BY 4.0, with its own README).

## Method in brief
- Brands: G2 category listings sampled September 2 to 3, 2026; first 4 per category labelled Leader, then Challenger, then Small (a listing-position label, not company size).
- ChatGPT (web search on, full conversation payloads), Claude and Perplexity: one manual run per question from research accounts over a US VPN, one new chat per question: Claude September 3 to 4, ChatGPT September 4, Perplexity September 8, 2026. On ChatGPT each question was pasted with the year added; on Claude and Perplexity it was pasted as listed in `queries`. Two ChatGPT questions (P12 and P16) were first sent without the year and then edited in the same chat; counts use the final attempt. Memory was switched off on all three before the runs (settings screenshots held). Payload metadata cannot confirm this either way: the `memory_scope` tag is a constant label, and three ChatGPT answers carry an internal marker named memcite whose meaning we could not establish. The ChatGPT profile's occupation field still read Gastroenterologist during the runs. Exports do not show profile context, so we cannot prove it had no effect. None of the 50 search queries or answers mentions anything medical, apart from HIPAA in two security answers.
- Google Gemini, Google AI Overviews and repeated ChatGPT runs: a third-party AI answer tracking platform, 3 runs of each question on September 7, 2026, with each brand's own category as the denominator. The zero-mention test also checks every daily run held through September 14.
- Named = whole-word brand name, alias or domain match in the final answer text; every common-word brand mention read by hand. Source cards and citation links shown beside an answer do not count: a brand that appears only there was cited, not named.
- Consulted (what an engine's search surfaced; the exports do not show which pages a model opened) and cited (what it credited in the answer text) are separate layers throughout. ChatGPT's consulted count is raw search hits and the other two are source lists, so pool sizes are not like for like. Domains that appeared only in an image carousel or thumbnail are published apart as image_only.
- The year appeared in ChatGPT's prompts only, so it may account for part of the source gap between ChatGPT and the other two engines. The only same-engine check is the two ChatGPT re-asks: P12 and P16 overlapped their own first attempts at 0.18 and 0.56, against pairwise means of 0.07 to 0.10 between engines.
- 15 of the 50 questions name a tracked brand (for example, Asana alternatives for small teams), so a brand's count can include answers that repeat its name: 18 of the named pairs on each manual engine sit on a question naming that brand. No brand's at-least-once result depends on those pairs. Without all 15 questions, Claude named 34 of the 36 brands ChatGPT named and the rank correlations are 0.83 to 0.88.
- Claude's bare "Monday" on P04 and P10 refers to monday.com. It affects brand-question pairs only and no at-least-once figure.
- AI Access Score: Citant's AI Crawler Access Report (21 automated checks across 15 named AI crawlers), September 26, 2026 rescan; September 5 scores kept for transparency.

## Limitations
Single manual runs on three engines; answers vary run to run (the report's Finding 7 measures how much). One country (US), one month,
five categories. Tracker text matching runs high for common-word names. Correlation only: nothing here shows what causes a brand to be named.

## Changes in v1.5 (2026-11-07)
We recounted every consulted, retrieved and cited figure from the raw captures and fixed what did not hold. Named counts, tracker figures and crawler scores carry over from v1.4. Three headline figures moved: the one-engine share (71.6% to 71.4%), the vendor share of citations (30.7% to 34.4%) and the retrieved-to-cited rate (43.5% to 40.7%). Unchanged: 32 of 94; 39, 45 and 46 brands named; 36 of 39; Reddit 27 and 1; YouTube 21 and 0; every crawler-access, tracker and rank-correlation figure.
- Question wording: all 50 ChatGPT prompts carried the year at the end; the Claude and Perplexity prompts did not. Earlier editions said identical questions, pasted verbatim. That was wrong. The wording ChatGPT received is now in chatgpt-prompts-as-sent.
- Two ChatGPT chats (P12, P16) held two attempts at the same question. Counts now use the final attempt only: ChatGPT's research pool 1,176 to 1,161, pages shared by ChatGPT and Perplexity 66 to 65.
- Retrieved-to-cited rate: 43.5% (77 of 177) divided every cited pair by the retrieved pairs, though 3 cited pairs were not in that question's search results. On the v1.4 data the right figure was 41.8% (74 of 177); v1.5 is 40.7% (72 of 177).
- Cited now means cited in the answer text. 24 of 251 prompt-domain incidences were image carousels or thumbnails; they move to the image_only layer. Citation base 227. Vendor-own 30.7% to 34.4%, review and UGC 3.6% to 4.0%, .org and .edu 2.0% to 2.2%, all other domains 63.3% to 59.0%, the two-domain editorial list (forbes.com, techrepublic.com) 0.4% unchanged. Brand-question pairs cited 77 to 75 (Zendesk, Freshworks).
- Six vendor domains counted as third parties moved to own: fin.ai, intercom.help, zendesk.nl, freshdesk.com, letsdeel.com, outreach.ai. Retrieved stays at 177: Outreach gains one pair here and lemlist loses one under the final-attempt rule. Vendor share of ChatGPT's research pool 15.1% to 15.8%. Sister products stay in other domains: slack.com (Salesforce), bolddesk.com (Syncfusion).
- Text in the Claude and Perplexity transcripts that was not a source had been read as a domain. With the final-attempt rule, consulted total 940 to 917; one engine 673 to 655 (71.6% to 71.4%); two engines 189 to 187 (20.1% to 20.4%); all three 78 to 75 (8.3% to 8.2%). Perplexity pool 703 to 664, Claude 336 to 333. Mean Jaccard 0.022 to 0.021, pairwise 0.072 to 0.098 becomes 0.068 to 0.097; on the 43 questions 0.025 to 0.024 and 0.077 to 0.114 becomes 0.072 to 0.113. All-other share of the research pools 74.9 to 85.9% becomes 74.0 to 86.3%.
- cited-domains was capped at 25 rows per category, left out tracked vendors and listed hosts unmerged. It now lists every registrable domain with class and question ids.
- adjudication: v1.4 had written the recount over the v1.1 hand read. The file now holds both, side by side, and agrees with the flag in results-aggregate.
- Dates: manual runs were September 3 to 8, not September 4 to 9.
- Wording: quoted is now cited (a citation here is a link in the answer); causal phrases are gone, because the study shows association; the overlap finding now states the long tail; the limitations state that 15 of the 50 questions name a tracked brand.
- New: chatgpt-prompts-as-sent, source-domains, chatgpt-funnel-per-question, own-domains, tracker-domains, verify_benchmark.py, SHA256SUMS.txt. Unchanged: queries, tracker-per-engine, tracker-hand-reads, claude-perplexity-recount.

## Changes in v1.4 (2026-10-12)
- What changed: every Claude and Perplexity named count was recounted on the answer text alone, with each match checked in its sentence and every common-word name read by hand.
- Cause: the transcript counter used for v1.0 to v1.3 skipped every transcript paragraph that carried a citation link, so it missed brands named in those paragraphs, and it counted source-card labels and citation text that sat on a line of their own, so it credited brands whose websites were only listed as sources.
- Fix: a hand recount on the answer text only; source cards, citation links and the pasted question do not count; common-word names read by hand. Every Claude and Perplexity cell, with the questions counted, is in `citant-benchmark-2026-claude-perplexity-recount-v1-4.csv` (51 cells changed; 13 flip between named and not named).
- Effect: brands named at least once moved from 46 to 45 (Claude) and from 52 to 46 (Perplexity); ChatGPT, counted from full conversation payloads, is unchanged at 39. Two non-leader brands whose only Perplexity appearance was a source card or a citation link joined the invisible group, now 32 of 94 (34%), up from 30 of 94; no brand left it.
- Figures that follow: 16 of the 32 invisible brands carry 1,000 or more G2 reviews; 24 of the 30 scored invisible brands are AI-ready (was 23 of 28); mean AI Access Scores 82.0 (invisible) and 84.8 (visible), previously 83.7 and 83.9 (both medians 91). Claude named 36 of the 39 brands ChatGPT named (was 35); 34 of the 54 brands named by at least one manual engine were named by all three (was 33 of 60); 40 brands were named by none of the three manual engines (was 34); the rank correlation of named counts across engines is 0.84 to 0.89 (was 0.78 to 0.85).
- Unchanged: every ChatGPT figure, every source, overlap, Reddit, YouTube, tracker, Google Gemini and Google AI Overviews figure.
- Files changed: results-aggregate, summary-metrics, adjudication, data-dictionary; new: claude-perplexity-recount. The other five files are unchanged from v1.3.

## Changelog
- v1.5 (2026-11-07): every consulted, retrieved and cited figure recounted from the raw captures (see "Changes in v1.5"); question wording stated, final attempt used on P12 and P16, retrieved-to-cited rate corrected, text citations separated from images, six vendor domains reclassed, transcript parsing fixed, public verification script added. Three headline figures moved.
- v1.4 (dataset 2026-10-12, report page 2026-10-13): recount of every Claude and Perplexity named count on the answer text (see "Changes in v1.4"). The count moves to 32 of 94; two non-leader brands join; nobody leaves.
- v1.3 (2026-10-08): repeated-run visibility recomputed with each brand's own category as denominator (two tracking projects had pooled two categories, halving those rates); sample date corrected to September 7; zero-mention test extended to every tracker run held (Sept 7-14), in category, common-word hits hand-read. The count stayed 30 of 94; two brands left (named on later runs, among them Smartsheet) and two non-leader brands joined.
- v1.2 (2026-10-08): hand adjudication of common-word brand names; front.com counted as Front's own domain; crawler-access figures moved to the corrected September 26 scan. The 30-of-94 headline did not change.
- v1.0 (2026-10-07): first publication.

## License and citation
CC BY 4.0. Reuse freely, with credit and a link.
Citant.ai (2026). The B2B SaaS AI Visibility Benchmark 2026 (dataset v1.5). DOI: 10.5281/zenodo.23350789. https://citant.ai/research/b2b-saas-ai-visibility-benchmark-2026/

DOI (all versions, resolves to the latest): https://doi.org/10.5281/zenodo.23350789 | DOI (v1.4): https://doi.org/10.5281/zenodo.23350790

Full ChatGPT conversation payloads, the Claude and Perplexity transcripts and the memory-setting screenshots are available to researchers and journalists: hamza@citant.ai
