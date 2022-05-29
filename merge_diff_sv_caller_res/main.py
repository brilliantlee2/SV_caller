import argparse
import numpy as pd 
import pandas as pd 
from args_parser import set_parser

args = set_parser()

def read_vcf(vcf1,vcf2):       #vcf1(2)为前缀
	#1
	with open(vcf1 + ".vcf", "r", encoding="utf-8") as f1:
		lines1 = f1.readlines()
	for line in lines1:
		if not  line.startswith(("##")):
			with open(vcf1 + "_body.vcf","a+",encoding="utf-8") as f_1:
				f_1.write(line)
		else:
			with open(vcf1 + "_head.vcf", "a+", encoding="utf-8") as ff1:
				ff1.write(line)

    #2
	with open(vcf2 + ".vcf", "r", encoding="utf-8") as f2:
		lines2 = f2.readlines()
	for line in lines2:
		if not line.startswith(("##")):
			with open(vcf2 + "_body.vcf", "a+", encoding="utf-8") as f_2:
				f_2.write(line)
		else:
			with open(vcf2 + "_head.vcf", "a+", encoding="utf-8") as ff2:
				ff2.write(line)

	return vcf1, vcf2
    

def proc_vcfs(body1, body2):
	#read vcf1
	body_1 = pd.read_csv(body1 + "_body.vcf", sep= "\t", header=0)
	body_1_bp = body_1
	body_1 = body_1.drop(columns=body_1.columns[[-1,-2]])  #去除不要的列
	body_1 = body_1.drop(columns=["FILTER","QUAL","ID"])

	#read vcf2
	body_2 = pd.read_csv(body2 + "_body.vcf", sep="\t", header=0)
	body_2_bp = body_2
	body_2 = body_2.drop(columns=body_2.columns[[-1,-2]])
	body_2 = body_2.drop(columns=["FILTER","QUAL","ID"])

	body_1["SVTYPE"] = 0
	for i in range(len(body_1)):
		if body_1.INFO[i].split(";")[1].split("=")[0] !=  "SVTYPE" :
			body_1["SVTYPE"][i] = body_1.INFO[i].split(";")[0].split("=")[1]
		else:
			body_1["SVTYPE"][i] = body_1.INFO[i].split(";")[1].split("=")[1]


	body_2["SVTYPE"] = 0
	for i in range(len(body_2)):
		if body_2.INFO[i].split(";")[1].split("=")[0] !=  "SVTYPE" :
			body_2["SVTYPE"][i] = body_2.INFO[i].split(";")[0].split("=")[1]
		else:
			body_2["SVTYPE"][i] = body_2.INFO[i].split(";")[1].split("=")[1]


    #添加SVLEN列 
	SVLEN_list = []
	for i in body_1.INFO:
		ele_i = i.split(";")
		for j in ele_i:
			find = False
			if j.startswith(("SVLEN")):
				SVLEN_list.append(j)
				find = True
				break
        
		if not find :
			SVLEN_list.append("SVLEN=0")
	body_1["SVLEN"] = SVLEN_list


	SVLEN_list = []
	for i in body_2.INFO:
		ele_i = i.split(";")
		for j in ele_i:
			find = False
			if j.startswith(("SVLEN")):
				SVLEN_list.append(j)
				find = True
				break

		if not find :
			SVLEN_list.append("SVLEN=0")
	body_2["SVLEN"] = SVLEN_list


	END_list = []
	for i in body_1.INFO:
		ele_i = i.split(";")
		for j in ele_i:
			find = False
			if j.startswith(("END")):
				END_list.append(j)
				find = True
				break
        
		if not find :
			END_list.append("END=0")
	body_1["END"] = END_list


	END_list = []
	for i in body_2.INFO:
		ele_i = i.split(";")
		for j in ele_i:
			find = False
			if j.startswith(("END")):
				END_list.append(j)
				find = True
				break
        
		if not find :
			END_list.append("END=0")
	body_2["END"] = END_list



	body_1 =body_1.drop(columns=["ALT","INFO","REF"])
	body_2 = body_2.drop(columns=["ALT","INFO","REF"])

	LEN_num = []
	for i in body_1.SVLEN:
		LEN_num.append(int(i.split("=")[1]))

	body_1["LEN"] = LEN_num
	body_1 = body_1.drop(columns=["SVLEN"])

	LEN_num = []
	for i in body_2.SVLEN:
		LEN_num.append(int(i.split("=")[1]))
	body_2["LEN"] = LEN_num
	body_2  = body_2.drop(columns=["SVLEN"])

	END_num = []
	for i in body_1["END"]:
		END_num.append(int(i.split("=")[1]))
	body_1["ENDS"] = END_num
	body_1 = body_1.drop(columns=["END"])


	END_num = []
	for i in body_2["END"]:
		END_num.append(int(i.split("=")[1]))
	body_2["ENDS"] = END_num
	body_2 = body_2.drop(columns=["END"])


	return body_1, body_2, body_1_bp, body_2_bp


def group_vcfs(body_1, body_2):

	vcf_1 = body_1.groupby('SVTYPE')
	vcf_2 = body_2.groupby('SVTYPE')
	
	vcf_1_list = []
	for i in vcf_1:
		vcf_1_list.append(i[0])
    
	#储存各个类型的sv dataframe 
	vcf_1_dict = {}
	for  ele in vcf_1_list:
		vcf_1_dict[ele] = vcf_1.get_group(ele)

	vcf_2_list = []
	for i in vcf_2:
		vcf_2_list.append(i[0])
    
	vcf_2_dict = {}
	for  ele in vcf_2_list:
		vcf_2_dict[ele] = vcf_2.get_group(ele)


	return vcf_1_dict, vcf_2_dict   #返回两个.vcf的按svtype分类的dict

def merge_vcf(sv_df1, sv_df2):

	#assert sv_df1["SVTYPE"][0] == sv_df2["SVTYPE"][0], "The sv type is different between sv_df1 and sv_df2"
	#svtype = sv_df1[0]
	tmp_list = []
	for i in range(len(sv_df1)):
		for j in range(len(sv_df2)):   
			if abs(sv_df1.iloc[i]["POS"] - sv_df2.iloc[j]["POS"]) + abs(sv_df1.iloc[i]["ENDS"] - sv_df2.iloc[j]["ENDS"]) <= args.errlen :
				#print(i)
				tmp_list.append(i)   #录入交集index   #这点不对,改了
				break

	return sv_df1.iloc[tmp_list].index.tolist()

def merge_vcfs(vcf_1_dict, vcf_2_dict):
	final_loc = []
	for key_1, value1 in vcf_1_dict.items():
		for key_2, value2 in vcf_2_dict.items():
			if key_1 == key_2 :
				final_loc.extend(merge_vcf(value1, value2))

				break

	return final_loc                #最终的交集的坐标





def merge_header_body(header): 
	with open("./final.vcf", "a+", encoding="utf-8") as f:
		f1 = open(header + "_head.vcf", "r", encoding="utf-8")                    
		f2 = open("./intersection.vcf", "r", encoding="utf-8")
		for i in f1:
			f.write(i)
		for j in f2:
			f.write(j)


	#f.close()



def generate_intersection_vcf(prev_vcf_df,final_loc):

	final_vcf_df = prev_vcf_df.iloc[final_loc]
	final_vcf_df.to_csv("./intersection.vcf", sep = "\t", index=False, header=True)





if __name__ == "__main__":
	
	vcf1, vcf2 = read_vcf(args.vcf1, args.vcf2)
	body_1, body_2, body_1_bp, body_2_bp = proc_vcfs(vcf1, vcf2)
	vcf_1_dict, vcf_2_dict = group_vcfs(body_1, body_2)
	final_loc = merge_vcfs(vcf_1_dict, vcf_2_dict)

	generate_intersection_vcf(body_1_bp,final_loc)

	merge_header_body(vcf1)