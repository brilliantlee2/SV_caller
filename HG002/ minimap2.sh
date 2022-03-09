#!/bin/bash
ref_gene=/hwfssz5/ST_BIOINTEL/P17H10200N0325/sunyuhui/database/hs37d5/hs37d5.fa
ONT_reads=/hwfssz5/ST_BIOINTEL/P17H10200N0325/sunyuhui/thirdGenAsm/correction/long.uncorrected.fq
#minimap2 -d hs37d5.nmi ${ref_gene}
#minimap2 -ax map-ont  ${ref_gene} ${ONT_reads} > aln.sam

#nohup samtools view -bS aln.sam > aln.bam 2> errconver.log &
#排序
samtools sort -m 2G  -@ 8  -o aln_sorted.bam aln.bam

samtools index -b aln_sorted.bam
