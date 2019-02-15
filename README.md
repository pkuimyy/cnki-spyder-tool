# cnki-spyder-tool
一个中国知网的爬虫工具，给定作者，可以获得该作者的所有文献的题录

### 范例
使用时需要将文件tool.py放在正确的位置
```
import sys
sys.path.append(".")
import tool as cnki
from pprint import pprint as fprint


if __name__ == "__main__":
    tmp = cnki.get_doc_url_set("牛丽慧","南京大学") 
    fprint(tmp)
    res_file = open("res.csv","a",encoding="utf-8",newline="")
    for item in tmp:
        cnki.get_doc_bibilo(item,res_file)
    res_file.close()

```
### 文档
```
Help on module tool:

NAME
    tool

DESCRIPTION
    Eng:
    This module is written for scraping bibilograph of literature from cnki.
    It relies on python modules below:
    1. requests
    2. bs4
    you can easily get them using tool like pip.
    
    中文：
    这个模块用来爬取中国知网的文献题录。
    它依赖于以下的Python模块：
    1.requests
    2.bs4
    你可以使用像pip这样的工具容易地获取它们。

FUNCTIONS
    get_doc_bibilo(doc_url, res_file)
        this function return bibliograph of the specified doc url by writting into the specified file
        
        Args:
            doc_url: specified doc url
            res_file: target res file
    
    get_doc_url_set(author_name, unit_name)
        This function simulates the behavior that you open the website:
        http://yuanjian.cnki.com.cn/
        and enter the dictionary:
        {"作者":"foo","作者单位":"bar"}
        and click the search button
        as you get the response page, you can get url set of all the page,
        it needs support of function:
        def get_next_page_doc_url_set(author_name,page_num,unit_name):
        to deal with the demond of page turning
        
        Args:
            author_name:  author's name
            unit_name: author's unit name
           
        Returns:
            return set of doc urls
    
    get_next_page_doc_url_set(author_name, page_num, unit_name)
        this function support the function:
        def get_doc_url_set(author_name,unit_name):
        get urls of specified page.
        
        Args:
            author_name: author's name
            page_num: specified page number
            unit_name: author's unit name
            
        Return:
            return set of doc urls

FILE
    /root/workbench/cnki-spyder-tool/tool.py
```



