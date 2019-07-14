#!/usr/bin/evn python
#coding:utf-8

import os
import re
import requests
import time
import random
from optparse import OptionParser
print(time.ctime())

#创建时间：2019-7-14
"'获得uid，下载xml,每次运行需要修改保存文件路径，以及读取文件的路径'"

def get_udi(url):# 获得pubmed文献的uid
    # 参数说明：url:构建的用于检索的url; i：检索关键词； basepath:保存的根目录
    docsums = requests.get(url).text
    # print(docsums)
    ids = re.findall(r'<Id>(\d+)</Id>', docsums)
    return ids
   

def get_xml(uidlist, base_url, basepath):   #根据uid下载xml
    count = len(uidlist)
    rem = count % 200  # 余数
    intrger = count // 200  # 整数
    for n in range(0, intrger+1):    #循环下载，每次200篇文献
        xrange = n * 200 + 1
        yrange = (n + 1) * 200

        out_file = open(os.path.join(basepath, str(n) + '_pubItem.xml'), 'w', encoding='utf-8')
        cur_ids = ','.join(uidlist[xrange:yrange])

        cur_url = base_url + '&id=' + cur_ids + '&rettype=abstract&retmode=xml'
        cur_data = requests.get(cur_url).text

        for string in cur_data:
            out_file.write(string)
        t = random.uniform(10, 20)   #random sleep time
        time.sleep(t)
        print(n)
    print('complete')
    print(time.ctime())


def makedirfile(root): #创建文件夹
    if os.path.exists(root):
        pass
    else:
        os.makedirs(root)
        print('创建新文件夹：', root)


def downloadXML(basepath, query):
    #参数说明： basepath:保存路径； query:构成的检索字符串
    makedirfile(basepath)

    db = 'pubmed'
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url = base + 'esearch.fcgi?db=' + db + '&term=' + query + '&usehistory=y'
    print(url)

    output = requests.get(url).text
    web = re.findall(r'<WebEnv>(.*?)</WebEnv>', output)[0]
    key = re.findall(r'<QueryKey>(\d+)</QueryKey>', output)[0]
    count = re.findall(r'<Count>(\d+?)</Count>', output)[0]
    print(count)

    if int(count) > 0:
        cur_url = base + 'esearch.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web + '&retmax=' + str(count)
        uidlist=get_udi(cur_url)            #1、获得uid

        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' + 'efetch.fcgi?' + 'db=' + db + '&WebEnv=' + web + '&query_key=' + query
        get_xml(uidlist, base_url, basepath)         #2、下载xml
    else:
        print ('检索结果为0！！')
        

parser=OptionParser()
parser.add_option('-q', '--query', action='store')
parser.add_option('-r', '--root', action='store')
(options, args) = parser.parse_args()

if __name__=='__main__':
    # example:
    # keywords = ['lung',]
    #
    # for i in keywords:
    #     query = '(((' + i + '+cancer)+AND+gene[Title/Abstract])+AND+("2010"[Date - Publication] : "2020"[Date - Publication])'
    #     basepath = os.path.join(r'C:\Users\lenovo\Desktop\tmp\taoping', i)
    #
    #     downloadXML(basepath, query)

    downloadXML(options.root, options.query)



        
        
       



