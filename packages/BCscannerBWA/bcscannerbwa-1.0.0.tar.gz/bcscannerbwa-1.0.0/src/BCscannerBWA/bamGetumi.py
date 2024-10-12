#########################################################
# title:bam generate barcode umi list
# author:dawang
# date:20230915
#########################################################


import argparse
import pysam


def parse_args():
    parser = argparse.ArgumentParser(description="Extract reference sequences and UMIs from a BAM file")
    parser.add_argument("-i", "--bam", type=str, required=True, help="Input BAM file")
    parser.add_argument("-o", "--output_prefix", type=str, required=True, help="Output file prefix")
    parser.add_argument("-t","--type", choices=['longread', 'shortread'], default="longread")

    
    return parser.parse_args()

def main():
    
    args = parse_args()
    input_bam = args.bam
    output_prefix = args.output_prefix
    type = args.type


    bam = pysam.AlignmentFile(input_bam, "rb")

    refseq_umi_file = f"{output_prefix}_refseq_umi.txt"

    with  open(refseq_umi_file, "w") as ru_out:
        ru_out.write("barcode\tumi\n")
        barcode = "CB" if type=='longread' else "DB"
        umi = "UR" if type=='longread' else "UB"
        for read in bam.fetch():
            if type=="longread":
                if read.has_tag('GX'):
                    CB = read.get_tag(barcode)
                    UB = read.get_tag(umi)
                else:
                    continue
            else:
                if read.mapq==255:
                    if read.has_tag('GN'):
                        CB = read.get_tag(barcode)
                        UB = read.get_tag(umi)   
                    else:
                         continue
                else:
                    continue
            ru_out.write(f"{CB}\t{UB}\n")

    bam.close()

if __name__ == "__main__":
    main()