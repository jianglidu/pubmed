#!/usr/bin/evn python


import os
import re
import requests
import time
print (time.time())


"'获得uid，下载xml,每次运行需要修改保存文件路径，以及读取文件的路径'"

def get_uid(url, i, basepath):     #获得pubmed文献的uid
    docsums=requests.get(url).text
    ids=re.findall(r'<Id>(\d+)</Id>',docsums)
    path=os.path.join(basepath, i+'_pubID.txt')
    outfile=open(path,'w',encoding='utf-8')
    if len(ids) > 0:
        for s in ids:
            outfile.write(s+'\n')
    else:
        print('Errors: there is no uids!')
        return

    
def uid_list(baseroot,filename):   #将文件中所有的ID列在list中
    idlist = list()
    cur_path = os.path.join(baseroot, filename)
    with open(cur_path) as filein:
        for id in filein:
            id = id.strip()
            idlist.append(id)
    print(len(idlist))
    print('complete uid_list!') 
    return idlist


def get_xml(uidlist,base_url):   #根据uid下载xml
    count = len(uidlist)
    rem = count % 200  # 余数
    intrger = count // 200  # 整数
    for n in range(0, intrger+2):    #循环下载，每次200篇文献
        xrange = n * 200
        yrange = (n + 1) * 200
        cur_ids = ''
        if yrange <= count:
            out_file = open(os.path.join(basepath, str(n) + '_pubItem.xml'), 'w', encoding='utf-8')
            cur_ids = ','.join(uidlist[xrange:yrange])
        else:
            out_file = open(os.path.join(basepath, str(intrger+1) + '_pubItem.xml'), 'w', encoding='utf-8')
            cur_ids = ','.join(uidlist[xrange:count])
        cur_url = base_url + '&id=' + cur_ids + '&rettype=abstract&retmode=xml'
        cur_data = requests.get(cur_url).text

        for string in cur_data:
            out_file.write(string)
        t = random.uniform(10, 20)   #random sleep time
        time.sleep(t)
        print(n)
    print('all complete!')
    print(time.time())


def running():
    db = 'pubmed'       #默认数据库：pubmed
    genelist = ['ALK',]      #检索关键词
    for i in genelist:
        basepath = os.path.join(r'C:\Users\lenovo\Desktop\tmp\xiao', i) #保存路径
        cur_dirfile = ''
        if os.path.exists(basepath):
            cur_dirfile = basepath
            print('path is exit.')
        else:
            try:
                cur_dirfile = os.makedirs(basepath)
            except:
                print('fail to make dirpath!')
    
        query='((('+i+'[Title/Abstract])+AND+resistance[Title/Abstract])+AND+cancer)+AND+("2010"[Date - Publication] : "2020"[Date - Publication])'
        base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        url = base + 'esearch.fcgi?db=' + db + '&term=' + query + '&usehistory=y'
        print(url)

        output = requests.get(url).text
        web = re.findall(r'<WebEnv>(.*?)</WebEnv>', output)[0]
        key = re.findall(r'<QueryKey>(\d+)</QueryKey>', output)[0]
        count = re.findall(r'<Count>(\d+?)</Count>', output)[0]

        if int(count) > 0:
            cur_url = base + 'esearch.fcgi?db=' + db + '&query_key=' + key + '&WebEnv=' + web + '&retmax=' + str(count)
            get_uid(cur_url, i, cur_dirfile)            #1、uid

            filename = i+'_pubID.txt'
            baseroot = cur_dirfile
            uidlist = uid_list(baseroot, filename)   #2、计算每个文件uidshumu

            base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' + 'efetch.fcgi?' + 'db=' + db + '&WebEnv=' + web + '&query_key=' + query
            get_xml(uidlist, base_url, cur_dirfile)         #3、下载xml
running()


        
        
       



