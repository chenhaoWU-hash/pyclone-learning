
import pandas as pd
from pathlib import Path

# Adapted original script; rebuild annotations directly, no execution-order dependency.
from _common import options, annotated
args = options('Examine cluster 1 donor/genotype composition')
df = annotated(args)

# Select Cluster 1
c1 = df[df["cluster_id"] == 1].copy()

# Express frequencies as percentages
c1["VAF_pct"] = c1["variant_allele_frequency"] * 100
c1["CP_pct"] = c1["cellular_prevalence"] * 100

# 1. Compare donor and genotype together
print("\n=== Donor × Genotype ===")
print(pd.crosstab(c1["donor"], c1["genotype"]))

# 2. Calculate frequency statistics
print("\n=== Frequency statistics ===")
print(
    c1.groupby(["donor", "genotype"])[
        ["VAF_pct", "CP_pct"]
    ]
    .agg(["count", "mean", "median"])
    .round(2)
)

# 3. Inspect mutations ordered by VAF
print("\n=== Individual mutations ===")
print(
    c1[
        ["mutation_id", "donor", "genotype",
         "VAF_pct", "CP_pct"]
    ]
    .sort_values("VAF_pct")
    .to_string(index=False)
)
