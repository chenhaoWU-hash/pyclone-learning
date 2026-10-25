
from pathlib import Path
import pandas as pd
import matplotlib

# Save figures without requiring a graphical Linux display
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 1. Define the project directory
project_dir = Path(__file__).resolve().parents[1]

input_file = (
    project_dir
    / "results/pyclone/single_test/tables/loci.tsv"
)

output_dir = (
    project_dir
    / "results/pyclone/single_test/figures"
)
output_dir.mkdir(parents=True, exist_ok=True)

# 2. Read the PyClone output
df = pd.read_csv(input_file, sep="\t")

# Convert proportions into percentages
df["VAF_pct"] = df["variant_allele_frequency"] * 100
df["CP_pct"] = df["cellular_prevalence"] * 100

# 3. Summarize mutations by cluster
summary = (
    df.groupby("cluster_id")
    .agg(
        mutations=("mutation_id", "count"),
        mean_VAF_pct=("VAF_pct", "mean"),
        mean_CP_pct=("CP_pct", "mean"),
    )
    .sort_index()
)

print("\nCluster summary:")
print(summary.round(3))

summary.to_csv(output_dir / "cluster_summary.csv")

# 4. Plot VAF vs Cellular Prevalence
fig, ax = plt.subplots(figsize=(9, 6))

for cluster_id, group in df.groupby("cluster_id"):
    ax.scatter(
        group["VAF_pct"],
        group["CP_pct"],
        s=35,
        alpha=0.75,
        label=f"Cluster {cluster_id} (n={len(group)})",
    )

ax.set_xlabel("Variant Allele Frequency (%)")
ax.set_ylabel("Cellular Prevalence (%)")
ax.set_title("PyClone: VAF vs Cellular Prevalence")
ax.legend(fontsize=9)
ax.grid(alpha=0.2)

fig.tight_layout()
fig.savefig(
    output_dir / "vaf_vs_cellular_prevalence.png",
    dpi=200,
)
plt.close(fig)

# 5. Compare within-cluster distributions
clusters = sorted(df["cluster_id"].unique())

vaf_data = [
    df.loc[df["cluster_id"] == c, "VAF_pct"]
    for c in clusters
]

cp_data = [
    df.loc[df["cluster_id"] == c, "CP_pct"]
    for c in clusters
]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for ax, data, ylabel, title in [
    (axes[0], vaf_data, "VAF (%)", "VAF distribution"),
    (axes[1], cp_data, "Cellular Prevalence (%)",
     "Cellular Prevalence distribution"),
]:
    ax.boxplot(data, positions=range(1, len(clusters) + 1))
    ax.set_xticks(range(1, len(clusters) + 1))
    ax.set_xticklabels(clusters)
    ax.set_xlabel("Cluster ID")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.2)

fig.tight_layout()
fig.savefig(
    output_dir / "cluster_distributions.png",
    dpi=200,
)
plt.close(fig)

print("\nFigures saved in:", output_dir)