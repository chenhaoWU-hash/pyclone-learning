"""Shared paths and validation; reconstructed packaging helper."""
import argparse
from pathlib import Path
import pandas as pd
REPO=Path(__file__).resolve().parents[1]
def options(description, trace=False):
    p=argparse.ArgumentParser(description=description)
    p.add_argument('--data-root',type=Path,default=REPO,help='Original project root, or this repository')
    p.add_argument('--result-dir',type=Path,help='Override results directory')
    p.add_argument('--input',type=Path,help='Override raw TSV')
    p.add_argument('--output-dir',type=Path,default=REPO/'results/review')
    p.add_argument('--sample',default='SRR385938')
    if trace:
        p.add_argument('--burnin',type=int,default=200)
        p.add_argument('--thin',type=int,default=1)
        p.add_argument('--mutation1',default='NA18507:BB:chr2:113737630')
        p.add_argument('--mutation2',default='NA19240:BB:chr15:50399138')
    a=p.parse_args()
    root=a.data_root.resolve()
    a.result_dir=(a.result_dir or (root/'evidence/single_test' if (root/'evidence/single_test').exists() else root/'results/pyclone/single_test')).resolve()
    a.input=a.input or (root/'data/SRR385938.tsv' if (root/'data/SRR385938.tsv').exists() else root/'pyclone/examples/mixing/tsv/SRR385938.tsv')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    return a
def annotated(a):
    raw=pd.read_csv(a.input,sep='\t')
    df=pd.read_csv(a.result_dir/'tables/loci.tsv',sep='\t')
    if df.sample_id.nunique()!=1 or str(df.sample_id.iloc[0])!=a.sample:
        raise ValueError('Expected one sample matching --sample')
    if raw.mutation_id.duplicated().any() or df.mutation_id.duplicated().any():
        raise ValueError('Duplicate mutation_id')
    raw['donor']=raw.mutation_id.str.split(':').str[0]
    df=df.merge(raw[['mutation_id','donor','genotype']],on='mutation_id',how='left',validate='one_to_one')
    if df[['donor','genotype']].isna().any().any(): raise ValueError('Unmatched mutation IDs')
    return df
