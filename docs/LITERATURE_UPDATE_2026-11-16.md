# Literature update · November 16, 2026

The collection now contains 339 papers and 11 resources. One paper appeared in the November 16 arXiv announcements. Two earlier papers came from the screening backlog.

## Three contrasts

### ModHarness-RL

Learns a compression program before policy training and periodically revises a separate steering program during GRPO. On CodeSearch with Qwen3-8B and limited history, repeatedly refitting compression scored 0.279 validation localization F1. The default with compression held fixed scored 0.412. Steering still evolves during training.

The endpoint measures file, module and entity localization. Policy weights are trained. Cost estimates in Table 2 have a separate scope and include scaled quantities. [Full text](https://arxiv.org/html/2611.18533v1). Sections 3.2 and 4.1–4.3, Table 3, Limitations, Appendix C.3.

### FinAcumen

Distills useful strategies and cautions from graded trajectories into a persistent memory bank. A similarity threshold governs retrieval. Test queries have read-only access. Adding the frozen memory bank to the tool-equipped agent raised FinMMR Easy accuracy from 74.08% to 81.67% (+7.59 percentage points).

This ablation covers the memory module as a whole in one benchmark split. It does not isolate the retrieval threshold. Appendix K reports a higher average inference cost with memory in a separate sampled comparison. [Full text](https://arxiv.org/html/2606.17642v6). Sections 3, 4.2, 5.1 and 5.3, Table 2, Appendix K.

### HarnessPro

Uses execution feedback, generated validation tests and performance–cost preferences to select executable harness variants for a fixed model and coding scaffold. On SWE-Bench Pro, HarnessPro-Medium reported a 79.0% pass rate and $1.26 mean cost per task. RHO reported 80.0% and $2.68, respectively.

This comparison applies to one model, benchmark and budget profile. The cost is per test task. It does not give a break-even point after the cost of searching for the harness. [Full text](https://arxiv.org/html/2610.26770v2). Sections 3–5.2, Table 2 and Appendix A.

## Bibliographic correction

The 17 authors and title of the Evo-Harness proceedings paper match the August 15 preprint. Its first-release date moves from the earlier October proceedings-month estimate to August 15. The collection first added it on November 15. [arXiv version history](https://arxiv.org/abs/2608.15071) · [EMNLP proceedings](https://aclanthology.org/2026.emnlp-main.969/).

For FinAcumen, the publisher's BibTeX and arXiv metadata spell the third author's name Yucheng Jian. Both full-text title pages spell it Yuchen Jian. The bibliography uses the publisher's metadata spelling and records the discrepancy. [ACL bibliographic record](https://aclanthology.org/2026.findings-emnlp.2357/) · [Proceedings PDF](https://aclanthology.org/2026.findings-emnlp.2357.pdf).

## Coverage and evidence versions

The four standing arXiv API queries for November 8–16 returned service or rate-limit errors. The last completed standard search ends November 15. On November 16 we searched the recent cs.AI, cs.CL and cs.LG announcement titles, covering 2,711 distinct identifiers and 80 title matches. These counts refer to titles, not eligible papers. We followed references from Evo-Harness and the Two Perspectives survey. The cumulative queue contains 349 candidates.

The arXiv OAI feed returned 2,179 metadata-change identifiers for November 15–16. None matched the 119 previously registered arXiv evidence sources. Separate submission-history checks confirmed the previously recorded versions of MemSkill, RSI-Dojo and Multi-Task Self-Harness. The latest complete Atom version audit was November 15.

Dataset v0.6.0 contains 162 records from 129 works, including 77 AI-assisted primary checks and 62 scoped observations. Human adjudication is pending. The historical October atlas contains 95 records. [Versioned data](dataset/v0.6.0/dataset.json) · [Previous release](dataset/v0.5.0/DATASET_CARD.md).
