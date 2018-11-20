#!/usr/bin/python evn

import re
import sys
import os
from xml.etree import ElementTree as ET

# out_res=open(r'C:\Users\lenovo\Desktop\20181015\clinvar_breast\ret_breast_clinvar4.txt','w',encoding='utf-8')
# out_res.write('#VariationID；VariationName；GeneID；Genename; AlleleID; OMIM; PhenotypeList'+'\n')

"'解析xml文件，提取字段'"
writefile=open(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers\resistance_pub.txt','w',encoding='utf-8')
for i in range(0,4):
    if i ==465:
        pass
    else:
        path=os.path.join(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers',str(i)+'_pubItem.xml')
        print (i)

    # path=os.path.join(r'C:\Users\lenovo\Desktop\20181015\breastcancer_pubmed','0_pubItem.xml')
        tree=ET.parse(path)   #用parse
        root=tree.getroot()   #获得树的根元素

        # print (root.tag, root.attrib)

        child_list=list(root)    #根元素的子元素


        #适用于pubmed 的xml 数据   #研究对象 PubmedArticleSet
        data=root.findall('PubmedArticle')
        count=0

        for inf in data:# print (data)
            count+=1

            pub_item=list()

            for item in inf:
                # print ('~',item.tag,':',item.attrib)
                if item.tag=='MedlineCitation':

                    for child in item:
                        # print ('~*',child.tag,':',child.attrib)
                        if child.tag=='PMID':
                            pmid=child.text       #文章PIMD
                            if pmid=='28153863':
                                print ('-------',i)
                            # print (pmid)
                            pub_item.append(pmid)
                        if child.tag=='Article':
                            for child_child in child:
                                # print ('~**',child_child.tag,':',child_child.attrib)
                                if child_child.tag=='ArticleTitle':
                                    arttitle=child_child.text       #文章题目
                                    # print (arttitle)
                                    pub_item.append(arttitle)

                                if child_child.tag=='Abstract':

                                    pub_item.append('Abstract: ')  #加了一栏提示字串

                                    for subchild_child in child_child:
                                        if subchild_child.tag=='AbstractText': #文章摘要,包括规范格式和不规范格式
                                            abstract=''

                                            if subchild_child.text is None: #AbstractText 中其他标签 通过循环子标签，通过.text以及.tail获得摘要

                                                for abs_ele in subchild_child:
                                                    if abs_ele.text is None:
                                                        pass
                                                    else:
                                                        abs_head=abs_ele.text.replace('\t','').replace('\r','').replace('\n','').strip()
                                                    if abs_ele.tail is None:
                                                        pass
                                                    else:
                                                        abs_tail = abs_ele.tail.replace('\t', '').replace('\r', '').replace('\n', '').strip()
                                                        abstract=abstract+abs_head+abs_tail

                                                pub_item.append(abstract)

                                            else:   #AbstractText 中没有其他标签 可以直接用.text得到摘要

                                                abstract=abstract+subchild_child.text.replace('\t','').replace('\r','').replace('\n','').strip()

                                                pub_item.append(abstract)


                                if child_child.tag=='Journal':

                                    for child_child_child in child_child:

                                        if child_child_child.tag=='Title':
                                            jourtitle=child_child_child.text   #文章期刊
                                            # print (jourtitle)
                                            pub_item.append(jourtitle)

                                        if child_child_child.tag=='ISOAbbreviation':
                                            jourAbb=child_child_child.text      #期刊简写

                                            pub_item.append(jourAbb)

                                        if child_child_child.tag=='JournalIssue':
                                            for child_child_child_child in child_child_child:

                                                if child_child_child_child.tag=='PubDate':
                                                    for y in child_child_child_child:
                                                        if y.tag=='Year':
                                                            pubyear=y.text   #文章发表时间
                                                            # print (pubyear)
                                                            pub_item.append(str(pubyear))


            for ss in pub_item[1:]:

                writefile.write(str(ss)+'\t')
            writefile.write(pub_item[0]+'\n')










#研究VariationReport
# data=root.findall('VariationReport')
# count=0

#适用于clinvar数据
# for inf in data:
#     "'输出格式：Genename; VariationID；VariationName；GeneID；AlleleID; OMIM; PhenotypeList '"
#     count=count+1
#     print (inf.tag," : ",inf.attrib)
#     print ('-------')
#
#     var_item = list()
#
#     variaID=inf.attrib['VariationID']          #第一层，突变ID和突变名称
#     variaName=inf.attrib['VariationName']
#     var_item.append(variaID)
#     var_item.append(variaName)
#
#     for item in inf:
#         print('*',item.tag,' : ',item.attrib)       #第二层
#         if item.tag=='GeneList':                    #元素Genelist中获得基因ID 基因名 ;第三层中获得 OMIM ID
#             for child in item:
#                 # print ('-**',child.tag, ":",child.attrib)
#
#                 if child.tag=='Gene':
#                     # print (child.attrib['Symbol'])
#                     geneID = child.attrib['GeneID']
#                     genename=child.attrib['Symbol']
#                     var_item.append(geneID)
#                     var_item.append(genename)
#                     for child_child in child:
#                         # print ('--**',child_child.tag,":",child_child.attrib)
#                         if child_child.tag=='OMIM':
#                             omim=child_child.text
#                             var_item.append('OMIM='+omim)
#
#         if item.tag=='Allele':                     #等二层
#             alleleID=item.attrib['AlleleID']          #元素Allele 中获得alleleID，
#             var_item.append('AlleleID='+alleleID)
#             # for child in item:
#                 # print ('**',child.tag, ":",child.attrib)
#                 # if child.tag=='Name':
#                 #     print (child.text) #.text 获得标签实际的内容
#                 # for child_child in child:
#                 #     print ('***',child_child.tag,' : ',child_child.attrib)
#
#
#         if item.tag=='ObservationList':     #第二层
#             phenotype_all =''       #元素ObservationList 子元素中获得 phenotype
#             for child in item:
#                 # print ('~**',child.tag, ":",child.attrib)
#                 for child_child in child:
#                     # print ('~~***',child_child.tag,' : ',child_child.attrib)
#                     if child_child.tag=='PhenotypeList':
#                         for child_child_child in child_child:
#                             # print ("~~",child_child_child.tag,":",child_child_child.attrib)
#                             if child_child_child.tag=='Phenotype':
#                                 phenotype=child_child_child.attrib['Name']
#                                 phenotype_all=phenotype+';'+phenotype_all
#
#                         var_item.append(phenotype_all)
#
#     out_res.write('\t'.join(var_item)+'\n')    #将结果输出到文件
#
#     print ('********')
#
# print (count)



