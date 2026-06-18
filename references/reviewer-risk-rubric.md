# Reviewer-Risk Audit Rubric

Use this reference when writing the `Potential Reviewer Challenges` section of the copy editing report.

## Severity Labels

Use three labels:

- `minor`: likely easy to fix with wording, citation, definition, or local clarification.
- `moderate`: may require author judgment, added explanation, stronger support, or limited manuscript revision.
- `serious`: may affect credibility, novelty, reproducibility, interpretation, or reviewer confidence.

Do not overstate certainty. Phrase as likely reviewer concerns, not guaranteed rejection reasons.

## Risk Categories

### Claim-Evidence Mismatch

Signals:

- strong claim in Abstract/Introduction but evidence appears only weakly reported;
- conclusion goes beyond Results;
- citation is attached to a sentence but may support only part of the claim.

Report pattern:

`[moderate] The claim that ... may need tighter evidence because ...`

### Causality Overclaim

Signals:

- `leads to`, `drives`, `causes`, `determines`, or `proves` used for observational/correlational data;
- mechanism language appears without mechanistic experiment, mediation analysis, or theory support;
- temporal wording implies causation where design does not.

Default fix:

- hedge in manuscript;
- ask author to confirm causal evidence;
- note in report if the design appears correlational.

### Novelty Overclaim

Signals:

- `first`, `novel`, `unprecedented`, `groundbreaking`, `unique`, `for the first time`;
- novelty not scoped by population, method, setting, dataset, or field;
- prior work is summarized too weakly.

Default fix:

- bound novelty: `to our knowledge`, `in this setting`, `among studies of...`;
- request citation support.

### Missing Limitations

Signals:

- Discussion contains broad implications but few limits;
- sample, setting, measurement, generalizability, bias, or data constraints are not acknowledged;
- limitations appear only as generic boilerplate.

Default report:

`[moderate] Reviewers may ask for a clearer limitation on ... because the claim currently appears broader than the design supports.`

### Methods Not Reproducible

Signals:

- vague methods: `standard procedure`, `routine analysis`, `optimized`, `validated`, `statistically analyzed`;
- missing software versions, parameters, inclusion/exclusion criteria, randomization, blinding, data preprocessing, model settings, or threshold definitions;
- results depend on a method not described.

Severity is often `serious` if a central result cannot be reproduced from the description.

### Weak or Missing Citations

Signals:

- background claims without citation;
- reliance on secondary sources where primary sources are expected;
- outdated support for a fast-moving field;
- citation does not appear to match the claim;
- reference list has missing or inconsistent metadata.

Use the output of `scripts/audit_citations.py` when available.

### Inconsistent Constructs, Variables, or Terms

Signals:

- the same construct is named differently across Abstract, Methods, Results, and Discussion;
- abbreviations are defined more than once or inconsistently;
- variables in text do not match tables/figures;
- theory labels shift across sections.

Default fix:

- standardize terminology where safe;
- comment or report when the author must choose the intended term.

## Report Format

Each item should include:

- severity;
- issue;
- location if known, using section/paragraph rather than invented line numbers;
- why a reviewer may challenge it;
- suggested author action.

Example:

`[serious] Methods reproducibility, Methods section: The preprocessing threshold is not specified. Reviewers may be unable to reproduce the analysis. Please add the threshold, selection rationale, and software/version details.`
