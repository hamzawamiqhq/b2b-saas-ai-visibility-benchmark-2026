---
license: cc-by-4.0
language:
- en
pretty_name: The B2B SaaS AI Visibility Benchmark 2026
size_categories:
- n<1K
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
  data_files: data/citant-benchmark-2026-results-aggregate-v1-4.csv
- config_name: queries
  data_files: data/citant-benchmark-2026-queries.csv
- config_name: overlap_per_prompt
  data_files: data/citant-benchmark-2026-overlap-per-prompt-v1-3.csv
- config_name: summary_metrics
  data_files: data/citant-benchmark-2026-summary-metrics-v1-4.csv
- config_name: cited_domains
  data_files: data/citant-benchmark-2026-cited-domains-v1-3.csv
- config_name: tracker_per_engine
  data_files: data/citant-benchmark-2026-tracker-per-engine-v1-3.csv
- config_name: adjudication
  data_files: data/citant-benchmark-2026-adjudication-v1-4.csv
- config_name: tracker_hand_reads
  data_files: data/citant-benchmark-2026-tracker-hand-reads-v1-3.csv
- config_name: claude_perplexity_recount
  data_files: data/citant-benchmark-2026-claude-perplexity-recount-v1-4.csv
---

# The B2B SaaS AI Visibility Benchmark 2026 (dataset v1.4)

Which B2B SaaS brands do AI answer engines name when a buyer asks for software? 94 brand entries (93 companies) across five
G2 categories (Project Management, Sales Engagement, Help Desk, Core HR, Vulnerability Scanner), 50 real buying questions
(10 per category, frozen before collection), five AI platforms.

Full report, method and limitations: https://citant.ai/research/b2b-saas-ai-visibility-benchmark-2026/

## Headline numbers (each recomputable from these files)
- 32 of 94 brands (34%) were named on none of five platforms (ChatGPT, Claude, Perplexity, Google Gemini, Google AI Overviews), on any of their category's questions, in any run we hold.
- Named at least once, of 94: ChatGPT 39, Claude 45, Perplexity 46. ChatGPT names the fewest brands; Claude and Perplexity are one brand apart.
- Of 940 distinct domains consulted by ChatGPT, Claude and Perplexity on the same 50 questions, 71.6% were consulted by exactly one engine and 8.3% by all three. Yet the engines largely agree on brands: Claude named 36 of the 39 brands ChatGPT named.
- ChatGPT consulted reddit.com on 27 of 50 questions and cited it on 1.
- Tracked vendors' own domains were 30.7% of ChatGPT's answer citations (77 of 251) and 15.1% of what it consulted (177 of 1,176).
- Of the 30 never-named brands we could scan, 24 are AI-ready (AI Access Score 75 or higher); their mean score (82.0) is about the same as the 54 scanned named brands (84.8).

## Files (`data/`)
Files that did not change in v1.4 keep their v1.3 names and are byte-identical to the v1.3 release.

| File | Rows | What it is |
|---|---|---|
| citant-benchmark-2026-queries.csv | 50 | The 50 buying questions, exactly as pasted (unchanged) |
| citant-benchmark-2026-results-aggregate-v1-4.csv | 94 | One row per brand entry: named counts per engine, ChatGPT own-site retrieval and citation, AI Access Scores, tracker visibility, the five-platform flag |
| citant-benchmark-2026-overlap-per-prompt-v1-3.csv | 50 | Per question cross-engine source overlap (domain and page level, Jaccard) (unchanged) |
| citant-benchmark-2026-summary-metrics-v1-4.csv | 54 | Every aggregate in the report as num / den / rate |
| citant-benchmark-2026-cited-domains-v1-3.csv | 242 | Third-party domains ChatGPT cited or retrieved, per category (unchanged) |
| citant-benchmark-2026-tracker-per-engine-v1-3.csv | 282 | Repeated-run figures per brand and engine (3 runs of each question, September 7), own-category denominator (unchanged) |
| citant-benchmark-2026-tracker-hand-reads-v1-3.csv | 32 | Tracker hits read by hand and excluded from the zero-mention test (unchanged) |
| citant-benchmark-2026-adjudication-v1-4.csv | 60 | Hand-read named counts for common-word brand names, before and after |
| citant-benchmark-2026-claude-perplexity-recount-v1-4.csv | 188 | New in v1.4: every brand entry x engine (Claude, Perplexity), named count in v1.3 and v1.4 and the v1.4 question ids |
| citant-benchmark-2026-data-dictionary-v1-4.csv | 40 | Every column defined |

All files are UTF-8, comma-separated, LF line endings, byte-identical to the files linked from the report page.
Charts: `citant-benchmark-2026-charts-v1-4.zip` (10 charts and the share card, CC BY 4.0, with its own README).

## Method in brief
- Brands: G2 category listings sampled September 2 to 3, 2026; first 4 per category labelled Leader, then Challenger, then Small (a listing-position label, not company size).
- ChatGPT (web search on, full conversation payloads), Claude and Perplexity: one manual run per question from a clean US profile, September 4 to 9, 2026.
- Google Gemini, Google AI Overviews and repeated ChatGPT runs: a third-party AI answer tracking platform, 3 runs of each question on September 7, 2026, with each brand's own category as the denominator. The zero-mention test also checks every daily run held through September 14.
- Named = whole-word brand name, alias or domain match in the final answer text; every common-word brand mention read by hand. Source cards and citation links shown beside an answer do not count: a brand that appears only there was cited, not named.
- Consulted (what an engine read) and cited (what it credited in the answer) are separate layers throughout.
- AI Access Score: Citant's AI Crawler Access Report (21 automated checks across 15 named AI crawlers), September 26, 2026 rescan; September 5 scores kept for transparency.

## Limitations
Single manual runs on three engines; answers vary run to run (the report's Finding 7 measures how much). One country (US), one month,
five categories. Tracker text matching runs high for common-word names. Correlation only: nothing here shows what causes a brand to be named.

## Changes in v1.4 (2026-10-12)
- What changed: every Claude and Perplexity named count was recounted on the answer text alone, with each match checked in its sentence and every common-word name read by hand.
- Cause: the transcript counter used for v1.0 to v1.3 skipped every transcript paragraph that carried a citation link, so it missed brands named in those paragraphs, and it counted source-card labels and citation text that sat on a line of their own, so it credited brands whose websites were only listed as sources.
- Fix: a hand recount on the answer text only; source cards, citation links and the pasted question do not count; common-word names read by hand. Every Claude and Perplexity cell, with the questions counted, is in `citant-benchmark-2026-claude-perplexity-recount-v1-4.csv` (51 cells changed; 13 flip between named and not named).
- Effect: brands named at least once moved from 46 to 45 (Claude) and from 52 to 46 (Perplexity); ChatGPT, counted from full conversation payloads, is unchanged at 39. Two non-leader brands whose only Perplexity appearance was a source card or a citation link joined the invisible group, now 32 of 94 (34%), up from 30 of 94; no brand left it.
- Figures that follow: 16 of the 32 invisible brands carry 1,000 or more G2 reviews; 24 of the 30 scored invisible brands are AI-ready (was 23 of 28); mean AI Access Scores 82.0 (invisible) and 84.8 (visible), previously 83.7 and 83.9 (both medians 91). Claude named 36 of the 39 brands ChatGPT named (was 35); 34 of the 54 brands named by at least one manual engine were named by all three (was 33 of 60); 40 brands were named by none of the three manual engines (was 34); the rank correlation of named counts across engines is 0.84 to 0.89 (was 0.78 to 0.85).
- Unchanged: every ChatGPT figure, every source, overlap, Reddit, YouTube, tracker, Google Gemini and Google AI Overviews figure.
- Files changed: results-aggregate, summary-metrics, adjudication, data-dictionary; new: claude-perplexity-recount. The other five files are unchanged from v1.3.

## Changelog
- v1.4 (2026-10-12): recount of every Claude and Perplexity named count on the answer text (see "Changes in v1.4"). The count moves to 32 of 94; two non-leader brands join; nobody leaves.
- v1.3 (2026-10-08): repeated-run visibility recomputed with each brand's own category as denominator (two tracking projects had pooled two categories, halving those rates); sample date corrected to September 7; zero-mention test extended to every tracker run held (Sept 7-14), in category, common-word hits hand-read. The count stayed 30 of 94; two brands left (named on later runs, among them Smartsheet) and two non-leader brands joined.
- v1.2 (2026-10-08): hand adjudication of common-word brand names; front.com counted as Front's own domain; crawler-access figures moved to the corrected September 26 scan. The 30-of-94 headline did not change.
- v1.0 (2026-10-07): first publication.

## License and citation
CC BY 4.0. Reuse freely, with credit and a link.
Citant.ai (2026). The B2B SaaS AI Visibility Benchmark 2026 (dataset v1.4). DOI: 10.5281/zenodo.23350790. https://citant.ai/research/b2b-saas-ai-visibility-benchmark-2026/

DOI (this version): https://doi.org/10.5281/zenodo.23350790 | DOI (all versions): https://doi.org/10.5281/zenodo.23350789

Raw ChatGPT conversation payloads and per-run screenshots are available to researchers and journalists: hamza@citant.ai
