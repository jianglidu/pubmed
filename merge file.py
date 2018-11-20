#!/usr/bin/python evn

import re

"'将多个文件写入一个文件'"
# ret_file=open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\total_breast_clinvar.txt','w',encoding='utf-8')
#
# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\ret_breast_clinvar1.txt',encoding='utf-8') as file:
#     for line in file:
#         ret_file.write(line)
#
#
# with open (r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\ret_breast_clinvar2.txt',encoding='utf-8') as file2:
#     for line2 in file2:
#         ret_file.write(line2)
#
#
# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\ret_breast_clinvar3.txt',encoding='utf-8') as file3:
#     for line3 in file3:
#         ret_file.write(line3)


# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\total_breast_clinvar.txt',encoding='utf-8') as file4:
#     count=0
#     for line4 in file4:
#         count+=1
# print (count)

# genefile=open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\gene_total_breast.txt','w',encoding='utf-8')
# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\total_breast_clinvar.txt',encoding='utf-8') as infile:
#     gene_total=set()
#     for line in infile:
#         if not line.startswith("#"):
#             a=line.split('\t')
#             geneName=a[3]
#             if 'Breast-ovarian cancer, familial 2;' in geneName :
#                 print (line)
#             if 'C16orf74' in geneName:
#                 print (line)
#             gene_total.add(geneName)
# for n in gene_total:
#     genefile.write(n+'\n')
# print (len(gene_total))

# new_file=open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\withoutSNP_breast_clinvar.txt','w',encoding='utf-8',)
# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\total_breast_clinvar.txt',encoding='utf-8') as infile2:
#     for line in infile2:
#         if not line.startswith("#"):
#             a=line.split('\t')
#             mutation=a[1]
#             geneName=a[3]
#             list1=['+','-','dup','ins','del']
#             count=0
#             for i in list1:
#                 if i in mutation:
#                     count+=1
#             if count>0:
#                 new_file.write(line)

# ret_file=open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\withoutSNP_add1list.txt','w',encoding='utf-8',)
# with open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\withoutSNP_breast_clinvar.txt',encoding='utf-8') as infile3:
#     for line in infile3:
#         if not line.startswith('#'):
#             a=line.split('\t')
#             string=''
#             for item in a[2:]:
#                 if 'breast' in item:
#                     b=item.split(';')
#                     for child_item in b:
#                         if 'breast' in child_item:
#                             string=child_item+';'+string
#             ret_file.write(string+'\t'+line)


"'根据关键词过滤数据，增加影响  因子'"

dict1=dict()
with open(r'C:\Users\lenovo\Desktop\期刊汇总\新建文件夹\2018国际期刊全称和简称对应表.txt') as file:   #影响因子
    count=0
    for line in file:
        count+=1
        line=line.strip()

        a=line.split('\t')
        if len(a)>1:  #过滤空行

            journalN=a[0].lower()
            abbN=a[1].lower()

            if a[2]=='Not Available' or a[2]=='-':
                pass
            else:
                jourIF=a[2]
                if journalN not in dict1.keys():
                    dict1[journalN]=jourIF
                if abbN not in dict1.keys():
                    dict1[abbN]=jourIF
print (count)
print (len(dict1))

#基因表
geneList=set()
with open(r'E:\NCBI_human aliases\Hs_gene_Aliases.txt') as file2:
    for li in file2:
        if not li.startswith("#"):
            c=li.split('\t')
            geneNum=c[0]
            geneN=c[1]

            alleN=c[2].split('|')
            geneList.add(geneN)
            for n in alleN:
                geneList.add(n)

print (len(geneList))
print('----')
#
#
#
out=open(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers\resistance_pub-2.txt', 'w',encoding='utf-8')
with open(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers\resistance_pub.txt', encoding='utf-8') as infile:
    ct = 0
    for lines in infile:
        b=lines.strip('\n').split('\t')
        if len(b)>4:
            cur_abs = ''
            for i in b[5:-1]:
                cur_abs=cur_abs+i

            jouN=b[1].lower()      #期刊全称
            jouAbb=b[2].lower().replace('.','')   #期刊简称
            title=b[3]

            inf1=dict1.get(jouN,0)
            inf2=dict1.get(jouAbb,0)
            print (inf1,inf2)
            if float(inf2)>=float(inf1):
                influence=inf2
            else:
                influence=inf1


            # for j in (jouN,jouAbb):
            #
            #     if j in dict1.keys():
            "' 增加全称和简称影响因子查找  '"

            if float(influence)>0.0 :

                string_set=set()
                get_strx=re.findall(r'[A-Z]+-?\d*?',cur_abs)   #截取可能的基因名称,全大写或者|-|数字或者字母

                flag=0
                flag2=0

                if 'ALK' in title or 'ALK' in cur_abs:
                     #要求标题或者摘要中含有关键字

                    if 'ALK' in title :
                        flag=flag+1
                    if 'ALK' in cur_abs :
                        flag2=flag2+1
                    if flag >0 or flag2>0:
                        print ('true')

                        string = '*'  # 大写字母字段
                        if len(get_strx)>0:
                            for i in get_strx :
                                if len(i)>1 and i in geneList:   #限制了基因长度大于1bp
                                    string_set.add(i)

                        if len(string_set)<1:    #当没有获得基因名称时，直接过滤
                            pass
                        else:
                            print (string_set)
                            for s in list(string_set):

                                string =string+','+s          #所有可能的基因字串集合
                            print (string)
                            new_line=lines.replace('\r','').replace('\n','')
                            out.write(influence+'\t'+new_line+'\t'+string+'\n')

                            # out.write(influence+'\t'+'PMID:'+b[-1]+'\t'+b[0]+'\t'+b[1]+'\t'+b[2]+'\t'+b[3]+'\t'+b[4]+'\t'+cur_abs+'\t'+string+'\n')
                            # out.write('\n')



