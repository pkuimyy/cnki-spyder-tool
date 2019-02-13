import sys
sys.path.append(".")
import tool as cnki
from pprint import pprint as fprint


if __name__ == "__main__":
    tmp = cnki.get_doc_url_set("牛丽慧","南京大学")    
    res_file = open("res.csv","a",encoding="utf-8",newline="")
    for item in tmp:
        cnki.get_doc_bibilo(item,res_file)
    res_file.close()
    
        


        
