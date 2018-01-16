import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import os

def pagedownloader(url,page,keyword):
    keyword=urllib.parse.quote(keyword)
    keyword={
        'keyword':keyword,
        'enc':'utf-8',
        'page':str(page)
    } 
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            
        }
    refkeyword={
        'keyword':keyword,
        'enc':'utf-8',
        'page':str(page-1)
    } 
    if page%2:
        headers['Referer']=requests.get(url=url,params=refkeyword).url
       
    content=requests.get(url=url,params=keyword)
    content.encoding='utf-8'
    bscontent=BeautifulSoup(content.text,'lxml')
    shoplist=bscontent.find_all(attrs={"class":"gl-item"})

    for i in shoplist:
        url=i.img.get('src')
        if not url:
            url=i.img.get('data-lazy-img')
        urllib.request.urlretrieve('https:'+url,os.path.basename(url))

url='https://search.jd.com/Search'
keyword=input("请输入你需要爬取的搜索关键词")
endpage=int(input('请输入爬取的终止页面'))
for page in range(1,endpage):
    pagedownloader(url=url,page=page,keyword=keyword)