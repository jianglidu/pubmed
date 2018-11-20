#!/usr/bin/evn python


import os
import re
import requests
import time
print (time.time())


"'获得uid，下载xml,每次运行需要修改保存文件路径，以及读取文件的路径'"

def get_udi(url,i):     #获得pubmed文献的uid

    # cur_url=base+'esearch.fcgi?db='+db+'&query_key='+key+'&WebEnv='+web+'&retmax='+str(count)
    docsums=requests.get(url).text

    ids=re.findall(r'<Id>(\d+)</Id>',docsums)

    path=os.path.join(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers',i+'_pubID.txt')
    outfile=open(path,'w',encoding='utf-8')

    for s in ids:
        outfile.write(s+'\n')




def uid_list(baseroot,filename):   #将文件中所有的ID列在list中
    idlist = list()
    cur_path = os.path.join(baseroot, filename)
    with open(cur_path) as filein:
        for id in filein:
            id = id.split('\n')
            b = id[0]
            idlist.append(b)
        print(len(idlist))
    return idlist



def get_xml(uidlist,base_url):   #根据uid下载xml

    count = len(uidlist)
    rem = count % 200  # 余数
    intrger = count // 200  # 整数

    writefile = open(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers\alk_cliItem.xml', 'w', encoding='utf-8')

    for n in range(0, intrger+2):    #循环下载，每次200篇文献
        xrange = n * 200 + 1
        yrange = (n + 1) * 200

        out_file = open(os.path.join(r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers', str(n) + '_pubItem.xml'), 'w',encoding='utf-8')
        cur_ids = ','.join(uidlist[xrange:yrange])

        cur_url = base_url + '&id=' + cur_ids + '&rettype=abstract&retmode=xml'
        cur_data = requests.get(cur_url).text

        for string in cur_data:
            out_file.write(string)
        time.sleep(30)
        print(n)

    print('complete')
    print(time.time())




db = 'pubmed'
genelist = ['ALK',]
for i in genelist:
    query = 'resistance[Title/Abstract]+AND+' + i + '[Title/Abstract]+AND+cancer[Title/Abstract]+AND+("2010"[Date - Publication] : "2019"[Date - Publication])'
    base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url = base + 'esearch.fcgi?db=' + db + '&term=' + query + '&usehistory=y'
    print(url)

    output = requests.get(url).text

    web = re.findall(r'<WebEnv>(.*?)</WebEnv>', output)[0]
    key = re.findall(r'<QueryKey>(\d+)</QueryKey>', output)[0]
    count = re.findall(r'<Count>(\d+?)</Count>', output)[0]
    print(count)

    cur_url = base + 'esearch.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web + '&retmax=' + str(count)
    get_udi(cur_url,i)            #1、uid

    filename=i+'_pubID.txt'
    baseroot=r'C:\Users\lenovo\Desktop\肺癌-遗传变异\papers'
    uidlist=uid_list(baseroot,filename)   #2、计算每个文件uidshumu


    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' + 'efetch.fcgi?' + 'db=' + db + '&WebEnv=' + web + '&query_key=' + query
    get_xml(uidlist,base_url)         #3、下载xml



