#########################################################
# title:bam to fastq
# author:dawang
# date:20230915
#########################################################


import argparse
import pysam

def calculate_values(offset, original_list, bc_len):
    first_elements = [item[0] for item in original_list]
    second_elements = [item[1] for item in original_list]

    first_zero_index = first_elements.index(0)
    last_zero_index = len(first_elements) - first_elements[::-1].index(0) - 1

    first_elements = first_elements[first_zero_index:last_zero_index+1]
    second_elements = second_elements[first_zero_index:last_zero_index+1]

    first_elements.insert(0, 4)
    second_elements.insert(0, offset)

    indices = [index for index, value in enumerate(first_elements) if value != 0]
    values = sum([second_elements[i] for i in indices])
    length = sum(second_elements)

    if length != bc_len:
        values += abs(length - bc_len)

    return values
    

def parse_args():
    parser = argparse.ArgumentParser(description="Extract reference sequences and UMIs from a BAM file")
    parser.add_argument("-i", "--bam", type=str, required=True, help="Input BAM file")
    parser.add_argument("-o", "--output_prefix", type=str, required=True, help="Output file prefix")
    parser.add_argument("-u","--umi_length", type=int, default=10, help="Length of UMI")
    parser.add_argument("-b","--bc_len", type=int, default=26, help='barcode length (default: 26)')
    parser.add_argument("-e","--error_num", type=int, default=4, help='maximum error number (default: 4)')
    
    return parser.parse_args()

def main():
    
    args = parse_args()
    input_bam = args.bam
    output_prefix = args.output_prefix
    umi_length = args.umi_length
    bc_len=args.bc_len
    err_num=args.error_num

    bam = pysam.AlignmentFile(input_bam, "rb")

    fastq_file = f"{output_prefix}.fq"
    refseq_umi_file = f"{output_prefix}_refseq_umi.txt"

    with open(fastq_file, "w") as fq_out, open(refseq_umi_file, "w") as ru_out:
        ru_out.write("qname\torientation\tref_name\tumi\tcigar\toffset\tmissmatch\tsequance_length\n")
        for read in bam.fetch():
            if read.flag in [0, 16]:
                ref_name = read.reference_name
                cigar= read.cigartuples

                if read.flag == 0:
                    orientation = "F"  # Forward strand
                else:
                    orientation = "R"  # Reverse strand

                offset = read.reference_start
                end_pos = read.query_alignment_end
                cor_pos = end_pos  + offset + umi_length + 5

                # ptimize error
                if offset <= err_num:
                    missmatch=calculate_values(offset,cigar,bc_len)
                    if missmatch <=err_num:
                        sequence = read.query_sequence[cor_pos:]
                        quality = read.qual[cor_pos:]
                        sequence = read.query_sequence[end_pos:]
                        quality = read.qual[end_pos:]
                        sequance_length=len(sequence)
                        umi = read.query_sequence[cor_pos-umi_length:cor_pos]
                        description = f"{read.qname}|||CB:Z:{ref_name}|||UR:Z:{umi}"
                        fastq_record = f"@{description}\n{sequence}\n+\n{quality}\n"
                        fq_out.write(fastq_record)

                        ru_out.write(f"{read.qname}\t{orientation}\t{ref_name}\t{umi}\t{cigar}\t{offset}\t{missmatch}\t{sequance_length}\n")

    bam.close()

if __name__ == "__main__":
    main()