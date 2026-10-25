
from pathlib import Path
import pandas as pd

# Project location
root = Path("/path/to/pyclone-project")

raw_file = root / "pyclone/examples/mixing/tsv/SRR385938.tsv"
result_file = root / "results/pyclone/single_test/tables/loci.tsv"

# 1. Read original data and PyClone results
raw = pd.read_csv(raw_file, sep="\t")
results = pd.read_csv(result_file, sep="\t")

# 2. Extract the known donor from mutation_id
# Example: NA12156:BB:chr11:118178007
raw["donor"] = raw["mutation_id"].str.split(":").str[0]

# The original dataset also contains a genotype column
# with information such as AB and BB.

# 3. Merge the original labels with PyClone's output
df = results.merge(
    raw[["mutation_id", "donor", "genotype"]],
    on="mutation_id",
    how="left",
    validate="one_to_one"
)

print("Total mutations:", len(df))
print("Missing donor labels:", df["donor"].isna().sum())

# 4. Compare clusters with original DNA donors
print("\n=== Cluster vs donor ===")
print(pd.crosstab(df["cluster_id"], df["donor"]))

# 5. Compare clusters with genotype
print("\n=== Cluster vs genotype ===")
print(pd.crosstab(df["cluster_id"], df["genotype"]))

# 6. Focus on Cluster 1
cluster1 = df[df["cluster_id"] == 1].copy()

cluster1["VAF_pct"] = (
    cluster1["variant_allele_frequency"] * 100
)
cluster1["CP_pct"] = (
    cluster1["cellular_prevalence"] * 100
)

print("\n=== Cluster 1 by genotype ===")
print(
    cluster1.groupby("genotype")
    .agg(
        mutations=("mutation_id", "count"),
        mean_VAF=("VAF_pct", "mean"),
        mean_CP=("CP_pct", "mean"),
    )
    .round(2)
)

# 7. Save annotated data for later analysis
output_file = (
    root / "results/pyclone/single_test/"
    "annotated_mutations.tsv"
)

df.to_csv(output_file, sep="\t", index=False)

print("\nSaved:", output_file)
