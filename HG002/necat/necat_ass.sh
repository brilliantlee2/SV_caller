#!/bin/bash
starttime=`date +'%Y-%m-%d %H:%M:%S'`

necat.pl correct SV_Caller_config.txt
necat.pl assemble SV_Caller_config.txt
necat.pl bridge SV_Caller_config.txt

endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次运行时间： "$((end_seconds-start_seconds))"s"
