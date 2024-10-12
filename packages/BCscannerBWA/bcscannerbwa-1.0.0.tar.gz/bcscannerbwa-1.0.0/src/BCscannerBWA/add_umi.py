"""
extract umi and add it to fastq sequence name
"""

import pandas as pd
import argparse
import datetime
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def read_fastq(fq_path):
    fastq_data = pd.read_csv(fq_path, sep='\t', header=None)
    fastq_data2 = pd.DataFrame()
    fastq_data2['seqname'] = fastq_data.iloc[::4, 0].values
    fastq_data2['seq'] = fastq_data.iloc[1::4, 0].values
    fastq_data2['info'] = fastq_data.iloc[2::4, 0].values
    fastq_data2['quality'] = fastq_data.iloc[3::4, 0].values

    return fastq_data2


def write_fastq(fq_path, df):
    fq = df[['seqname', 'seq', 'info', 'quality']].applymap(lambda x:x+'\n').values.flatten()
    with open(fq_path, 'w') as file:
        file.writelines(fq)


def addumi(row):
    seq = row['seq'][10:]
    quality = row['quality'][10:]
    name = row['seqname'].replace('#', '_'+row['seq'][:10]+'#')
    return [name, seq, quality]


def process_file(fq_path, fq_out):
    fq = read_fastq(fq_path)
    fq[['seqname', 'seq', 'quality']] = fq.apply(addumi, axis=1, result_type='expand').values
    write_fastq(fq_out, fq)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fq_file", type=str, required=True, help="Path to the fastq file")
    parser.add_argument("--fq_out", type=str, required=True, help="Path to the output fastq file")
    args = parser.parse_args()
    print("Args:", args)
    print(f"process start: {datetime.datetime.now()}")
    process_file(args.fq_file, args.fq_out)
    print(f"process end: {datetime.datetime.now()}")


