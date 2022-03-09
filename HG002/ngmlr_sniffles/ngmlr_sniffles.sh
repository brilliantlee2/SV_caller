#!/bin/bash
starttime=`date +'%Y-%m-%d %H:%M:%S'`
ref_gene=/hwfssz5/ST_BIOINTEL/P17H10200N0325/sunyuhui/database/hs37d5/hs37d5.fa
reads=/hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/SV_Caller/HG002/chr6_reads.fastq


ngmlr -x ont -t 8  -r ${ref_gene} -q ${reads} -o ngmlr_chr6.sam

#sam2bam
samtools view -bS ngmlr_chr6.sam >  ngmlr_chr6.bam
#sort
samtools sort -m 2G  -@ 8  -o ngmlr_sorted.bam     ngmlr_chr6.bam

samtools  rmdup -s  ngmlr_sorted.bam  ngmlr_sorted_rmdup.bam

samtools index -b  ngmlr_sorted_rmdup.bam


#sniffles call sv
sniffles --input  ngmlr_sorted_rmdup.bam  --vcf ngmlr_sniffles.vcf


endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次运行时间： "$((end_seconds-start_seconds))"s"
