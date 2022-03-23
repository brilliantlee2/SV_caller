#!/bin/bash
startTime=`date +"%Y-%m-%d %H:%M:%S"`
ONT_reads=/hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/SV_Caller/HG002/chr6_reads.fastq
flye  --nano-raw  ${ONT_reads} --out-dir HG200 --genome-size 171000000  --threads 4

endTime=`date +"%Y-%m-%d %H:%M:%S"`
st=`date -d  "$startTime" +%s`
et=`date -d  "$endTime" +%s`
sumTime=$(($et-$st))
echo "Total time is : $sumTime second."


##ok
