---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-26"
status: current
tags:
  - meta
---

> [!tldr]
> Hierarchical taxonomy of supplement categories and functional groupings. Used for cross-cutting discovery and stack design.

See also: [[index]], [[lint-rules]], [[ingest-checklist]]

## How This Works

Supplements are grouped by shared mechanism, function, or category. During ingest, tag new supplements with the relevant taxonomy groups. This enables queries like "show me all Nrf2 activators" or "which adaptogens overlap with anti-inflammatories?"

## By Mechanism and Basic Biology

### Nrf2 Activators
<!-- Supplements that activate the Nrf2 signaling pathway -->
<!-- e.g., Sulforaphane, Curcumin -->

### mTOR Inhibitors
<!-- Supplements that inhibit the mTOR pathway -->

### AMPK Activators
<!-- Supplements that activate AMPK -->

### Sirtuin Activators
<!-- Supplements that activate sirtuins -->

### Sirtuin Biology
<!-- Basic-biology process pages about SIRT1-7, NAD+ dependence, and aging biology -->

### NAD+ Boosters
<!-- Supplements that increase NAD+ levels -->

### Anti-Inflammatories
<!-- Supplements with primary anti-inflammatory mechanisms -->

### Antioxidants
<!-- Supplements that directly scavenge free radicals or upregulate antioxidant enzymes -->

### Mitochondrial Support
<!-- Supplements that enhance mitochondrial function or biogenesis -->

### Cellular Senescence
<!-- Supplements or hypotheses involving senescent-cell burden, SASP, or senolytic/senomorphic effects -->

### Adaptogens
<!-- Supplements that help the body adapt to stress -->

## By Function

### Longevity Fundamentals
<!-- Supplements with the broadest evidence for healthspan -->

### Cognitive Enhancement
<!-- Supplements targeting cognitive outcomes -->

### Cardiovascular Support
<!-- Supplements targeting cardiovascular outcomes -->

### Cancer Chemoprevention
<!-- Supplements with evidence for cancer prevention -->

### Metabolic Health
<!-- Supplements targeting metabolic outcomes (glucose, insulin, lipids) -->

### Immune Support
<!-- Supplements targeting immune function -->

### Bone and Joint Health
<!-- Supplements targeting musculoskeletal outcomes -->

## By Condition or Risk Domain

### Osteoarthritis and Joint Pain
<!-- Condition-specific evidence for symptom relief, function, and structural outcomes -->

### Mood Disorders
<!-- Depression, anxiety, irritability, stress resilience -->

### Cognitive Aging
<!-- Memory, attention, processing speed, neurodegeneration risk -->

### Cancer Risk and Chemoprevention
<!-- Prevention/risk framing; distinguish from established cancer treatment -->

### Cardiometabolic Risk
<!-- Blood pressure, lipids, glucose, insulin resistance, metabolic syndrome -->

## By Population

### Healthy Adults
<!-- Evidence from generally healthy adult participants -->

### Older Adults
<!-- Evidence specific to older adults -->

### Clinical Populations
<!-- Disease-specific populations such as T2D, OA, heart failure, depression -->

## By Genetics

### Genes
<!-- Gene pages such as MTHFR, APOE, or COMT when they affect supplement relevance, dose, risk, or interpretation -->

### Variants and SNPs
<!-- Variant pages such as rsIDs, functional polymorphisms, or clinically named variants -->

### Genotypes and Carrier States
<!-- Genotype context such as APOE e4 carrier, MTHFR C677T homozygous, or compound heterozygous states -->

### Pharmacogenomic and Nutrigenomic Markers
<!-- Markers that plausibly change supplement response, adverse effects, or dosing -->

## By Category

### Minerals
<!-- Elemental minerals (magnesium, zinc, selenium, etc.) -->

### Vitamins
<!-- Essential vitamins (D3, K2, B-complex, etc.) -->

### Amino Acids and Derivatives
<!-- Amino acid supplements (taurine, NAC, creatine, etc.) -->

### Polyphenols and Botanicals
<!-- Plant-derived compounds (curcumin, resveratrol, quercetin, etc.) -->

### Peptides and Proteins
<!-- Peptide-based supplements -->

### Lipids
<!-- Fat-soluble compounds (omega-3, etc.) -->

## Cross-Cutting Queries

```dataview
TABLE WITHOUT ID
  file.link AS "Supplement",
  filter(file.tags, (t) => startswith(t, "#pathway/")) AS "Pathways",
  filter(file.tags, (t) => startswith(t, "#outcome/")) AS "Outcomes",
  filter(file.tags, (t) => startswith(t, "#condition/")) AS "Conditions",
  filter(file.tags, (t) => startswith(t, "#population/")) AS "Populations",
  filter(file.tags, (t) => startswith(t, "#gene/") or startswith(t, "#variant/") or startswith(t, "#genotype/")) AS "Genetics"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT file.name ASC
```
