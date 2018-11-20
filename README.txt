

目的：ncbi API批量下载文献- E-utilities，并根据期刊名增加影响因子


第一步：download_clinvar_data.py   导出文献的ID,下载文献摘要

第二步：parser XML.py  解析xml格式-标准格式

第三步：merge.py  根据期刊名称增加影响因子，并筛选出title和abstract中的gene name

运行脚本前需要修改文件路径，检索关键词等





