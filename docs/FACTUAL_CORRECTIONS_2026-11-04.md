# Factual corrections — November 4, 2026

This note accompanies dataset **v0.4.1** and the corrected author reading manuscript. It records corrections to our descriptions, not new experimental results. Collection membership remains **318 papers and 11 resources**; the dataset remains **145 category-source records, 113 works and 45 scoped observations**.

| Item | Correction and primary evidence |
| --- | --- |
| RSI-Env benchmark identities | The evaluated arithmetic set is **AIME 2026**, not AIME 2025. The factual QA set is a **500-question subset of original SimpleQA**, not SimpleQA Verified. GPQA Diamond has 198 questions; the three QA/math metrics use avg@3, whereas Terminal-Bench 2.1 uses pass@3. [v1, Section 4, Table 1 and Appendix B.3](https://arxiv.org/html/2611.01736v1). |
| Masked Erosion model swap | The signal concerns **AppWorld**. OpsSim remains a separate study-level membership but is removed from this signal's benchmark join. [v1, Section 4.5](https://arxiv.org/html/2610.38392v1). |
| HCL interactive acceptance | Minecraft/ALFWorld use an **LLM judgment of historical task records instead of strict historical replay**, because replay can change environment state. Our previous Minecraft wording overstated direct retained-skill testing. Corrected QA and visual ablation locators refer to Section 4.2 and Appendix F.2/Table 7. [v2, Appendix C.1](https://arxiv.org/html/2608.19013v2). |
| ModularRSI version alignment | The current v2 author list includes **Xudong Ma**. Its Go repair case is Appendix **K.4**, not D.4; method comparison is Section **6.5**/Appendix F. The reported 36-to-25 interaction comparison remains a combined-edit case, not isolated causal evidence for dispatch. [v2](https://arxiv.org/html/2609.14857v2). |
| VideoWeaver transfer | The inspected v2 unseen-category evaluation uses a **frozen merged creator**, without target-category adaptation feedback. Removed a stale bibliography phrase suggesting limited-example target adaptation. [v2, Section 4.2](https://arxiv.org/html/2606.08091v2). |
| MoMHa metric interpretation | The 0.611/0.584 aggregation combines seven capability and three safety domains. It is an **overall capability-and-safety score**, not pure mean task accuracy. The corresponding token means are 572/667. Removed a misidentified second comparison. [v1, Appendix K](https://arxiv.org/html/2609.30967v1). |
| Thinkingbox locator | The 65.36% pass@1 and 30.62% estimated pass^20 pair is in **Table 15**, not Table 5. Appendix C.7 specifies the plug-in estimator; it is not an observed all-20-success fraction. [v4](https://arxiv.org/html/2608.19741v4). |
| Representation and maintenance | Unified the Terminal-Bench 2.1 join key, repaired tau-squared title markup and removed four leaked TeX category commands. Maintenance documentation now distinguishes a target schedule from a verified active scheduler. |

## How to use old and current versions

Published dataset v0.1.0–v0.4.0 and the original 95-record October 1 atlas remain immutable historical artifacts. Their preservation is not an endorsement of every old statement. Use **v0.4.1** and its machine-readable `corrections.json` for the corrected records. The historical benchmark explorer may still display the earlier HCL wording; this note and the current dataset supersede it. Manuscript locators and the selected ModularRSI website finding are corrected independently.

The posted Preprints.org version and any submitted manuscript are separate objects; this correction does not submit or replace a platform version.

## Verification boundary

The audit combined bibliographic identity checks, targeted primary-text comparisons of dataset narratives and signals, and inspection of website/manuscript claims. Abstract-level checks are not full-text adjudication. Source-version changes, inaccessible sources, and unpublished implementation details remain limitations. No independent experimental reproduction, dual human annotation, agreement score, exhaustive literature recall, or zero-error guarantee is claimed. Existing review labels are preserved; this audit does not automatically promote legacy records.
