"""
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
"""


import requests
from bs4 import BeautifulSoup
#ensure that you have installed python modules as above

import time
import csv
import math

    
def get_doc_url_set(author_name,unit_name):
    """
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
    """
    
    #http messsage' header 
    headers = {
        "Host":"yuanjian.cnki.com.cn",
    "Connection":"keep-alive",
    "Content-Length":"63",
    "Cache-Control":"max-age=0",
    "Origin":"http://yuanjian.cnki.com.cn",
    "Upgrade-Insecure-Requests":"1",
    "DNT":"1",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer":"http://yuanjian.cnki.com.cn/",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
    }

    cookies = {
        "UM_distinctid":"168ae2b533519-0c21eda9d60a5f-57b143a-ea600-168ae2b533827",
    "KEYWORD":"%E5%BC%A0%E4%B9%85%E7%8F%8D%24%E7%89%9B%E4%B8%BD%E6%85%A7%24%E7%9F%AD%E5%B0%8F%E8%8A%BD%E5%AD%A2%E6%9D%86%E8%8F%8C%E8%A1%A8%E8%BE%BE%E7%B3%BB%E7%BB%9F%E7%9A%84%E4%BC%98%E5%8C%96%E7%A0%94%E7%A9%B6",
    "SID":"110105",
    "CNZZDATA1257838124":"249878561-1549106680-%7C1549701224"
    }
    
    base_url = "http://yuanjian.cnki.net/Search/Result"

    #can easily be extended in the future
    data = {
        "searchType":"MulityTermsSearch",
        "Author":author_name,
        "Unit":unit_name
    }

    r = requests.post(base_url,cookies = cookies,headers = headers,data = data)

    bs = BeautifulSoup(r.text,"html.parser")
    
    total_count = int(bs.find("input",{"id":"hidTotalCount"})["value"])
    count_per_page = 20
    page_count = math.ceil(total_count/count_per_page)

    print(author_name,page_count)

    doc_url_set = list()
    for i in range(1,page_count+1):
        #turn page and add urls of each page to doc_url_set
        doc_url_set.extend(get_next_page_doc_url_set(author_name,i,unit_name))  
    
    return doc_url_set

def get_next_page_doc_url_set(author_name,page_num,unit_name):
    """
    this function support the function:
    def get_doc_url_set(author_name,unit_name):
    get urls of specified page.
    
    Args:
        author_name: author's name
        page_num: specified page number
        unit_name: author's unit name
        
    Return:
        return set of doc urls  
    """
    headers = {
        "Host":"yuanjian.cnki.com.cn",
        "Connection":"keep-alive",
        "Content-Length":"473",
        "Accept":"text/html, */*; q=0.01",
        "Origin":"http://yuanjian.cnki.com.cn",
        "X-Requested-With":"XMLHttpRequest",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        "DNT":"1",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Referer":"http://yuanjian.cnki.com.cn/Search/Result",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
    }

    cookies = {
        "UM_distinctid":"168ae2b533519-0c21eda9d60a5f-57b143a-ea600-168ae2b533827",
    "KEYWORD":"%E5%BC%A0%E4%B9%85%E7%8F%8D%24%E7%89%9B%E4%B8%BD%E6%85%A7%24%E7%9F%AD%E5%B0%8F%E8%8A%BD%E5%AD%A2%E6%9D%86%E8%8F%8C%E8%A1%A8%E8%BE%BE%E7%B3%BB%E7%BB%9F%E7%9A%84%E4%BC%98%E5%8C%96%E7%A0%94%E7%A9%B6",
    "SID":"110105",
    "CNZZDATA1257838124":"249878561-1549106680-%7C1549701224"
    }

    base_url = "http://yuanjian.cnki.net/Search/Result"

    data = {
        "searchType":"MulityTermsSearch",
        "Author":author_name,
        "ParamIsNullOrEmpty":"true",
        "Islegal":"false",
        "Order":"1",
        "Page":page_num,
        "Unit":unit_name
    }

    r = requests.post(base_url,cookies = cookies,headers = headers,data = data)

    bs = BeautifulSoup(r.text,"html.parser")
    doc_url_set = [item["href"] for item in bs.find_all("a",{"target":"_blank","class":"left"})]
    
    return doc_url_set

def get_doc_bibilo(doc_url,res_file):

    """
    this function return bibliograph of the specified doc url by writting into the specified file
    
    Args:
        doc_url: specified doc url
        res_file: target res file
    """
    csv_writer = csv.writer(res_file,delimiter="\t")

    try:
        r = requests.get(doc_url,allow_redirects=False,timeout = 10)
    except:
        print(doc_url)
    bs = BeautifulSoup(r.text,"html.parser")

    #journal
    try:
        journal = bs.find("b").text.strip()
    except:
        journal = " "

    #title
    try:
        title = bs.find("h1").text.strip()
    except:
        title = " "
        
    #author
    author_list = list()
    try:
        res = bs.find("div",{"style":"text-align:center; width:740px; height:30px;"})
        for item in res.find_all("a"):
            author_list.append(item.string.strip())
    except:
        pass
    #abstract
#         try:
#             abstract = bs.find("div",{"style":"text-align:left;word-break:break-all"}).font.next_sibling.string.strip()
#         except:
#             abstract = " "

    #address
    try:
        address = bs.find("div",{"style":"text-align:left;"}).a.string.strip()
    except:
        address = " "

    #keywords
    try:
        keyword_list = bs.find("meta",{"name":"keywords"})["content"].split()
    except:
        keyword_list = []

    #year
    try:
        year = bs.find("font",{"color":"#0080ff"}).string.strip()[:4]
    except:
        year = " "

    tmp = (title,";".join(author_list),journal,address,year,";".join(keyword_list))
    csv_writer.writerow(tmp)       


if __name__ == "__main__":
    start_time = time.time()
    tmp = get_doc_url_set("牛丽慧","南京大学")    
    res_file = open("res_test.csv","a",encoding="utf-8",newline="")
    get_doc_bibilo(tmp[0],res_file)
    stop_time = time.time()
    print("total:",stop_time - start_time)
    

    
    
