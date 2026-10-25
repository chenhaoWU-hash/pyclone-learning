from pathlib import Path
import pandas as pd

# Adapted original diagnostics; samples are indexed by saved trace row.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from _common import options
args = options('Inspect saved MCMC trace', trace=True)
root = args.output_dir
trace = args.result_dir / 'trace'

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
    trace / f"{args.sample}.cellular_prevalence.tsv.bz2",
    sep="\t"
)

cluster_count = labels.nunique(axis=1)

# 2. Select two mutations
m1 = args.mutation1
m2 = args.mutation2

n = len(labels)
if not (len(alpha)==len(precision)==len(cp)==n): raise ValueError('Trace lengths differ')
if not labels.columns.equals(cp.columns): raise ValueError('Trace mutation columns differ')
if not 0 <= args.burnin < n-3 or args.thin < 1: raise ValueError('Invalid burnin/thin')
if m1 not in labels or m2 not in labels: raise ValueError('Requested mutation missing')
cut = args.burnin + (n-args.burnin)//2

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
        x=args.burnin,
        linestyle="--",
        color="red",
        label=f"Burn-in = {args.burnin}"
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
    first = values.iloc[args.burnin:cut:args.thin]
    second = values.iloc[cut:n:args.thin]

    print(
        name,
        "first_half=", round(first.mean(), 4),
        "second_half=", round(second.mean(), 4),
        "lag1_autocorr=", round(
            values.iloc[args.burnin::args.thin].autocorr(lag=1), 4
        )
    )

# 5. How often are the two mutations clustered together?
same_cluster = (labels[m1] == labels[m2])

print("\n=== Co-clustering frequency ===")
print("After burn-in:",
      round(same_cluster.iloc[args.burnin::args.thin].mean(), 4))
print("First post-burnin half:",
      round(same_cluster.iloc[args.burnin:cut:args.thin].mean(), 4))
print("Second post-burnin half:",
      round(same_cluster.iloc[cut:n:args.thin].mean(), 4))
# Reconstructed extension: joint event counts and transparent approximate ESS.
import numpy as np
def approximate_ess(values):
    x=np.asarray(values,dtype=float)
    if np.var(x)==0: return float('nan')
    correlations=[pd.Series(x).autocorr(lag=k) for k in range(1,len(x)//2)]
    total=0.0
    for k in range(0,len(correlations)-1,2):
        pair=correlations[k]+correlations[k+1]
        if not np.isfinite(pair) or pair<=0: break
        total+=pair
    return min(len(x),len(x)/(1+2*total))
rows=[]
for name, values in series.items():
    post=values.iloc[args.burnin::args.thin]
    rows.append(dict(parameter=name,first_half=values.iloc[args.burnin:cut:args.thin].mean(),second_half=values.iloc[cut:n:args.thin].mean(),lag1=post.autocorr(),approx_ESS=approximate_ess(post)))
pd.DataFrame(rows).to_csv(root/'diagnostics.tsv',sep='\t',index=False)
same=same_cluster.iloc[args.burnin::args.thin]
low=(cp[m1]<0.4).iloc[args.burnin::args.thin]
joint=pd.crosstab(same,low,rownames=['Same cluster'],colnames=['NA18507 CP < 0.4']).reindex(index=[False,True],columns=[False,True],fill_value=0)
print('Co-clustering count:', int(same.sum()), '/', len(same))
print(joint)
joint.to_csv(root/'coclustering_vs_low_cp.tsv',sep='\t')
for lo,hi in [(args.burnin,cut),(cut,n),(args.burnin,n)]:
    print(f'Rows {lo}-{hi-1}: same={same_cluster.iloc[lo:hi:args.thin].mean():.4f}, low_CP={(cp[m1].iloc[lo:hi:args.thin]<0.4).mean():.4f}')
print('Approximate ESS is a descriptive single-chain estimate; drift invalidates stationary interpretations. R-hat requires multiple independent chains.')
