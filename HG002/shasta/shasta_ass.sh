#!/bin/bash
startTime=`date +"%Y-%m-%d %H:%M:%S"`
shasta --input /hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/SV_Caller/HG002/chr6_reads.fastq --config Nanopore-Oct2021

endTime=`date +"%Y-%m-%d %H:%M:%S"`
st=`date -d  "$startTime" +%s`
et=`date -d  "$endTime" +%s`
sumTime=$(($et-$st))
echo "Total time is : $sumTime second."
