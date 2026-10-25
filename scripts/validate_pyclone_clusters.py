
from pathlib import Path
import pandas as pd

# Adapted original script; strict join, configurable paths, ARI added.
from _common import options, annotated
from sklearn.metrics import adjusted_rand_score
args = options('Validate clusters against known mixture donors')
df = annotated(args)
print('ARI:', adjusted_rand_score(df['donor'], df['cluster_id']))
pd.crosstab(df['cluster_id'], df['donor']).to_csv(args.output_dir / 'confusion_matrix.tsv', sep='\t')

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
output_file = args.output_dir / 'annotated_mutations.tsv'

df.to_csv(output_file, sep="\t", index=False)

print("\nSaved:", output_file)
