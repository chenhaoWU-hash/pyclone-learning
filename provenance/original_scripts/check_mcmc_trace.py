from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

root = Path("results/pyclone/single_test")
trace = root / "trace"

# 1. Read trace files
alpha = pd.read_csv(
    trace / "alpha.tsv.bz2",
    sep="\t", header=None
).iloc[:, 0]

precision = pd.read_csv(
    trace / "precision.tsv.bz2",
    sep="\t", header=None
).iloc[:, 0]

labels = pd.read_csv(
    trace / "labels.tsv.bz2",
    sep="\t"
)

cp = pd.read_csv(
    trace / "SRR385938.cellular_prevalence.tsv.bz2",
    sep="\t"
)

cluster_count = labels.nunique(axis=1)

# 2. Select two mutations
m1 = "NA18507:BB:chr2:113737630"
m2 = "NA19240:BB:chr15:50399138"

# 3. Plot
fig, axes = plt.subplots(
    4, 1, figsize=(12, 11), sharex=True
)

axes[0].plot(alpha)
axes[0].set_ylabel("DP concentration")

axes[1].plot(precision)
axes[1].set_ylabel("BB precision")

axes[2].plot(cluster_count)
axes[2].set_ylabel("Number of clusters")

axes[3].plot(cp[m1], label="NA18507")
axes[3].plot(cp[m2], label="NA19240", alpha=0.7)
axes[3].set_ylabel("Cellular prevalence")
axes[3].set_xlabel("MCMC iteration")
axes[3].legend()

# Mark our previous burn-in cutoff
for ax in axes:
    ax.axvline(
        x=200,
        linestyle="--",
        color="red",
        label="Burn-in = 200"
    )

fig.tight_layout()

output = root / "mcmc_trace.png"
fig.savefig(output, dpi=160)
plt.close(fig)

print("Saved plot:", output)

# 4. Compare first and second halves after burn-in
print("\n=== Post-burnin comparison ===")

series = {
    "alpha": alpha,
    "precision": precision,
    "cluster_count": cluster_count,
    "CP_NA18507": cp[m1],
    "CP_NA19240": cp[m2],
}

for name, values in series.items():
    first = values.iloc[200:600]
    second = values.iloc[600:1000]

    print(
        name,
        "first_half=", round(first.mean(), 4),
        "second_half=", round(second.mean(), 4),
        "lag1_autocorr=", round(
            values.iloc[200:].autocorr(lag=1), 4
        )
    )

# 5. How often are the two mutations clustered together?
same_cluster = (labels[m1] == labels[m2])

print("\n=== Co-clustering frequency ===")
print("After burn-in:",
      round(same_cluster.iloc[200:].mean(), 4))
print("Iterations 200-599:",
      round(same_cluster.iloc[200:600].mean(), 4))
print("Iterations 600-999:",
      round(same_cluster.iloc[600:1000].mean(), 4))