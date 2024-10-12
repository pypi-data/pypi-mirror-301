#########################################################
# title:get barcode seqence
# author:dawang
# date:20230915
#########################################################

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file")
    parser.add_argument("-o", "--output_prefix", type=str, required=True, help="Output file prefix")
    parser.add_argument("-b","--barcode", type=str, required=True,  help='barcode fasta')

    return parser.parse_args()


def main():
    
    args = parse_args()
    input= args.input
    output = args.output_prefix
    bc=args.barcode

    os.system("cut -f 3 {} > {}.label.all.txt".format(input,output))
    os.system("sort {}.label.all.txt | uniq > {}.label.txt".format(output,output))
    os.system("sed -i '1d' {}.label.txt".format(output))
    os.system("cat {} | seqkit grep -f {}.label.txt > {}.fa".format(bc,output,output))
    os.system("sed -n '2~2p' {}.fa > {}.seq.txt".format(output,output))



if __name__ == "__main__":
    main()