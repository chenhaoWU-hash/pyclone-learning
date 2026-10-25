# 02 · The PyClone model

## VAF versus cellular prevalence

VAF is `var_counts / (ref_counts + var_counts)`: the fraction of observed reads carrying the variant. Cellular prevalence (CP) is the model's fraction of cancer cells carrying a mutation. Purity, copy number in reference and variant populations, variant allele multiplicity, and sequencing error connect these quantities.

In a simple pure, diploid, heterozygous setting, VAF is approximately CP/2. That approximation cannot be applied indiscriminately to BB genotypes or altered copy numbers. This healthy-donor mixture was fitted with `tumour_content=1.0`; its fitted CP should not be interpreted directly as clinical tumor burden.

## Model structure

1. Each locus provides read counts and a prior over feasible genotype/copy-number states.
2. A beta-binomial observation model permits extra dispersion relative to a binomial. Higher precision means less extra dispersion.
3. Mutations within a cluster share latent cellular prevalence. A Dirichlet-process mixture permits a variable number of clusters; concentration influences clustering tendency without directly fixing the final K.
4. MCMC samples assignments, prevalence, concentration, and precision. Post-processing uses co-clustering information and MPEAR to produce one hard partition.

The recovered upstream `post_process/clusters.py` calls `pydp.cluster.cluster_with_mpear`. Cluster labels can switch across iterations, so an iteration-specific label of 1 does not identify a persistent biological population. The event `label_i == label_j` is invariant to label permutation.

## Different summaries answer different questions

`tables/loci.tsv` summarizes each locus's CP trace. The mean/std in `tables/cluster.tsv` come from grid-based cluster distributions conditional on the post-processing partition. Their means need not match. A standard deviation is not the Monte Carlo standard error of a mean; a very small grid-based standard deviation does not establish chain convergence.

The final partition has six clusters, while the retained trace has mean cluster counts of 8.435 and 7.575 in its two halves. Single-sample identifiability is limited, and genotype ambiguity and compensation among model parameters may contribute to instability.

References: [official README](https://github.com/Roth-Lab/pyclone), [beta-binomial implementation](https://github.com/Roth-Lab/pyclone/blob/master/pyclone/pyclone_beta_binomial.py), and [post-processing implementation](https://github.com/Roth-Lab/pyclone/blob/master/pyclone/post_process/clusters.py).
