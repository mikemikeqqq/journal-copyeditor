# Statistics and Numbers Consistency Pass

Use this reference for the statistics/numbers portion of proofreading. The goal is to flag likely inconsistencies and reporting gaps, not to recalculate analyses unless the user provides data.

## Core Rule

Do not change statistical values unless the correction is obvious from the document and low risk. Otherwise, comment or list the issue in the report.

## What To Check

### P Values

Check:

- consistent format: `p = .032`, `p = 0.032`, or `P < 0.001`, depending on style;
- no impossible values such as `p > 1`;
- `p < 0.05` should not be described as exact;
- `p = 0.000` should usually be `p < 0.001`;
- significance language should match the reported threshold.

### Confidence Intervals

Check:

- confidence level is stated, usually `95% CI`;
- lower and upper bounds are both present;
- CI syntax is consistent: `[1.20, 2.31]`, `(1.20-2.31)`, or journal style;
- effect direction matches the text.

### Sample Sizes and Replicates

Check:

- `n`, `N`, sample size, participants, observations, datasets, and replicates are consistently reported;
- subgroup counts sum to total when obvious;
- exclusions and missing data are described when mentioned.

### SD, SE, SEM, IQR

Check:

- the manuscript does not mix SD and SE/SEM without explanation;
- figure legends identify error bars;
- tables define abbreviations in notes.

### Tables, Figures, and Text

Check:

- numbers in text match tables and figures when clearly comparable;
- figure/table numbering is consecutive;
- every figure/table cited in text exists;
- captions do not report values that conflict with the main text.

### Significant / Non-Significant Language

Flag when:

- `significant` is used without a statistical test or citation;
- `no difference` is claimed from a non-significant test without equivalence or power support;
- small non-significant trends are overstated.

Safer language:

- `did not differ significantly`;
- `showed no statistically significant difference`;
- `was numerically higher, although the difference was not statistically significant`.

## Report Categories

Use these labels in the final report:

- `format issue`: inconsistent but likely easy to fix;
- `verification needed`: value may be wrong or unsupported;
- `reviewer risk`: issue may affect interpretation or credibility.

Example:

`[verification needed] Results section: The text reports p = 0.04 but Table 2 reports p = 0.40 for the same comparison. Please verify the correct value.`
