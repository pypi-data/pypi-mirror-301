import argparse
import subprocess

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='BWA-MEM alignment script')
parser.add_argument('input_fastq', type=str, help='Path to the input FASTQ file')
parser.add_argument('barcode_fa', type=str, help='Path to the barcode.fa file')
parser.add_argument('output_sam', type=str, help='Path to the output SAM file')
parser.add_argument('-k', '--seed_length', type=int, default=13, help='Seed length (default: 13)')
parser.add_argument('-W', '--band_width', type=int, default=5, help='Band width (default: 5)')
parser.add_argument('-r', '--reseed_rate', type=int, default=8, help='Reseeding rate (default: 8)')
parser.add_argument('-T', '--score_threshold', type=int, default=22, help='Score threshold (default: 22)')

# 解析命令行参数
args = parser.parse_args()

# 执行bwa mem命令
bwa_command = [
    '${bwa}',
    'mem',
    f'-k{args.seed_length}',
    f'-W{args.band_width}',
    f'-r{args.reseed_rate}',
    '-A1', '-B1', '-O1', '-E1', '-L0',
    f'-T{args.score_threshold}',
    '-t', '10',
    args.barcode_fa,
    args.input_fastq
]

try:
    with open(args.output_sam, 'w') as output_file:
        subprocess.run(bwa_command, stdout=output_file, check=True)
    print(f"Alignment completed. SAM file saved to: {args.output_sam}")
except subprocess.CalledProcessError:
    print("Alignment failed.")