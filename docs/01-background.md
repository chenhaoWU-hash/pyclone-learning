# 01 · Background and data provenance

This project studies how original PyClone combines read counts, copy-number information, and cellular prevalence to cluster mutations, then examines the reliability of that clustering. PyClone estimates prevalence and clusters; it does not reconstruct a phylogeny. Pairtree was part of the broader learning context but was not run in this experiment.

## The input is a healthy-donor mixture

The included input is a local copy of the official `examples/mixing/tsv/SRR385938.tsv`. According to the upstream data README, the mixing examples were generated from healthy tissue from four individuals in different proportions. They correspond to the Cal-A–Cal-D MiSEQ experiments described in *Detection of low prevalence somatic mutations in solid tumors with ultra-deep targeted sequencing*.

The exact donor proportions for SRR385938 were not independently verified and are not invented here. These are not ground-truth tumor clones.

`mutation_id` encodes donor, genotype, chromosome, and position, for example `NA18507:BB:chr2:113737630`. Donor labels provide known mixture-source annotations. AB/BB describe genotype, not cancer stages. Genotype affects expected variant allele frequency (VAF).

Core input fields are `mutation_id`, `ref_counts`, `var_counts`, `normal_cn`, `minor_cn`, and `major_cn`. Extra fields such as `variant_case`, `variant_freq`, and `genotype` provide annotations; the genotype annotation is not itself a donor label supplied to the clustering model.

## Sources

- [Official PyClone repository](https://github.com/Roth-Lab/pyclone)
- [Official mixing input directory](https://github.com/Roth-Lab/pyclone/tree/master/examples/mixing/tsv)
- [Upstream data README](https://github.com/Roth-Lab/pyclone/blob/master/examples/mixing/tsv/README.txt)
- [Original PyClone paper](https://doi.org/10.1038/nmeth.2883)

## Recovery record

The initial workspace had no original data. The original project was subsequently located on the local machine, where four scripts, the example input, generated YAML/configuration, tables, figures, and all four compressed trace files were found. Private absolute paths are replaced by `/path/to/pyclone-project` in this public version. The original data, docs, and notebooks directories had no files.

The conversation retrieval interface exposed five recent exchanges and an image attachment path. Older assistant responses were content-reference markers rather than readable explanations. Consequently, these notes rely on the recovered files and recomputed values, and do not claim to recover missing historical commands or environment details.

The local upstream `cli.py` declares a 0.13.1 interface. Its Git metadata could not be read, so the exact upstream commit and any local source changes remain unknown. The original runtime package versions and random seed were not recovered. Checksums in `provenance/manifest.json` establish the distributed file bytes; original SHA-256 values are also retained for the three archived files whose paths were sanitized. They do not prove equality to a particular upstream commit. Only filesystem paths were changed in those archived files; mutation data, traces, model parameters, and analysis logic are unchanged.
