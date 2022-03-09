f_chr6 = open("/hwfssz1/ST_BIOCHEM/P18Z10200N0032/liyiyan/SV_Caller/HG002/chr6_reads.fastq")
liness = f_chr6.readlines()
reads_list = []
for i in range(1,len(liness),4):
    reads_list.append(liness[i])
res = min(reads_list, key=len,default='')
print(len(res)-1)
