import requests
import os
from bs4 import BeautifulSoup
import json

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
s=requests.Session()


def login(username,password):
    LoginUrl='https://accounts.pixiv.net/api/login?lang=zh'
    headers={
            'Referer':'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent':user_agent
            # 'cookies':'PHPSESSID=bfd27fbba83948b6ac0e26c6f1ecaefb; p_ab_id=4; p_ab_id_2=4; __utma=235335808.314879822.1515933739.1515933739.1515933739.1; __utmc=235335808; __utmz=235335808.1515933739.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=no=1^9=p_ab_id=4=1^10=p_ab_id_2=4=1^11=lang=zh=1; __utmt=1; __utmb=235335808.1.10.1515933739; _td=f18a31bd-622f-4a9a-933b-ee4c72179fbe; login_bc=1; _ga=GA1.2.314879822.1515933739; _gid=GA1.2.15696380.1515933745; _ga=GA1.3.314879822.1515933739; _gid=GA1.3.15696380.1515933745'
        }
    loginpage=s.get(url='https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',headers=headers)
    soup=BeautifulSoup(loginpage.text,'lxml')
    post_key=soup.input['value']



    data={
            'pixiv_id':username,
            'password':password,
            'captcha':'',
            'g_recaptcha_response':'',
            'post_key':post_key,
            'source':'android',
            'ref':'wwwtop_accounts_index',
            'return_to':'https://www.pixiv.net/'
        }
    r=s.post(url=LoginUrl,headers=headers,data=data)
    print(r.text)

def getimgurl():
    headers={
        'Referer':'https://www.pixiv.net/discovery?mode=safe',
        'User-Agent':user_agent
    }
    data={
        'type':'illust',
        'sample_illusts':'auto',
        'num_recommendations':1000,
        'page':'discovery',
        'mode':'safe',
        'tt':'da9700eb87b296e2162f9c27c54ed893'
        }
    url1='https://www.pixiv.net/rpc/recommender.php'
    jsondata=s.get(url=url1,headers=headers,params=data)
    # print(jsondata.text)
    dict=json.loads(jsondata.text)
    list=dict.get('recommendations')
    # print(list)
    url2='https://www.pixiv.net/rpc/illust_list.php'
    data1={
        'page':'discover',
        'exclude_muted_illusts':1,
        'tt':'da9700eb87b296e2162f9c27c54ed893'
        }
    imglist={}
    print(len(list))
    for i in range(20):
        list1=list[i*50:50*(i+1)]
        illust_ids=''
        # print(len(list1))

        for j in list1:
            illust_ids=illust_ids+','+j
        data1['illust_ids']=illust_ids[1:]
        # print(data1)
        jsondata1=s.get(url=url2,headers=headers,params=data1)
        # print(jsondata1.status_code)
        imginfodict=json.loads(jsondata1.text)
        # print(imginfodict)
        for i in imginfodict:
            # print(i)
            imglist[i['illust_id']]=i['url']
    # print(imglist)
    return imglist


def imgdownloader(imglist):
    for id,url in imglist.items():
        headers={
            'referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+id,
            'user-agent':user_agent
        }
        urllist=url.split('c/240x240/img-master')
    
        url=urllist[0]+'img-original'+urllist[1].split('_master1200')[0]+urllist[1].split('_master1200')[1]
        # print(url)
        r=s.get(url=url,headers=headers)
        print(r.status_code)
        if r.status_code==404:
            url=urllist[0]+'img-original'+urllist[1].split('_master1200')[0]+'.png'
            r=s.get(url=url,headers=headers)
        path=r'pixiv/'
        with open(path+id+'.'+url.split('.')[-1],'wb') as f:
            f.write(r.content)
login()

imgdownloader(getimgurl())