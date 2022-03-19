#!/bin/bash

starttime=`date +'%Y-%m-%d %H:%M:%S'`

/hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/anaconda/envs/nanoplot4_env/bin/NanoPlot --fastq /hwfssz5/ST_BIOINTEL/P17H10200N0325/sunyuhui/thirdGenAsm/correction/long.uncorrected.fq -o fastq-plots --maxlength 270778  -t 10 --plots hex dot

endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次运行时间： "$((end_seconds-start_seconds))"s"
