#!/bin/bash
starttime=`date +'%Y-%m-%d %H:%M:%S'`
ref_gene=/hwfssz5/ST_BIOINTEL/P17H10200N0325/sunyuhui/database/hs37d5/hs37d5.fa
reads=/hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/SV_Caller/HG002/chr6_reads.fastq

#建立index
minimap2 -d hs37d5.nmi ${ref_gene}

#map
minimap2 -ax map-ont  ${ref_gene} ${reads} > aln_chr6.sam
#sam2bam
samtools view -bS aln_chr6.sam >  aln_chr6.bam
#sort
samtools sort -m 2G  -@ 8  -o aln_sorted.bam    aln_chr6.bam

samtools  rmdup -s  aln_sorted.bam  aln_sorted_rmdup.bam

samtools index -b aln_sorted_rmdup.bam

#sniffles call sv
sniffles --input aln_sorted_rmdup.bam --vcf sniffles.vcf

endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次运行时间： "$((end_seconds-start_seconds))"s"
