# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 16:09:19 2018

@author: HP
"""
'''
4点注意，对于防扒措施的建议：
1.设置socket响应时间
2.模拟用户代理，设置header
3.每次response = urllib.request.urlopen()后，需要response.close()
4.每次爬完需要,time.sleep(2)线程休息两秒
'''
import urllib 
from bs4 import BeautifulSoup  
import time  
import socket
import re
import random
import json
#from lxml import etree
def get_urllist(url):
    socket.setdefaulttimeout(20)
    header_all =["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
              "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"]
    #"User-Agent":用户代理
    userlist_lenth = len(header_all)
    random_number = random.randint(0,userlist_lenth-1)
    header ={}
    header["User-Agent"] = header_all[random_number]#随机选取一名用户代理  
    request1 = urllib.request.Request(url,headers = header)#发送请求
    try:
        response = urllib.request.urlopen(request1)#相应请求
        html = response.read()                     #网页读取，
        html = str(html,encoding='utf-8',errors = 'ignore')#编码字符串转化，正常网页读取
        response.close()
    except urllib.error.URLError as e:
        print(e.reason)
    reg = r'createPageHTML\((\d+), 0, "index", "html"\);'#\(\)字符转义
    reg = re.compile(reg)
    page_number = re.findall(reg,html)#获得总页数
    urllist = []
    last_url = []
    page_url = []#页面网址
    date_list = []
    for i in range(int(page_number[0])):
        if i==0:
            str1 = url+"index.html"
            urllist.append(str1)
        else:
            str1 = url+"index_"+str(i)+".html"
            urllist.append(str1)#获得页数的url地址
    for i in urllist:
        random_number = random.randint(0,userlist_lenth-1)
        header["User-Agent"] = header_all[random_number]
        request2 = urllib.request.Request(i,headers = header)#发送请求
        try:
            response = urllib.request.urlopen(request2)#相应请求
            html2 = response.read()
            html2 = str(html2,encoding='utf-8',errors = 'ignore')#正常网页读取
            response.close()
        except urllib.error.URLError as e:
            print(e.reason)     
        reg1 = r'<li  style="width:700px;">\s+?<span>(.*?)</span>\s+?<a href="./(.*?)" target="_blank">.*?</a>\s+?</li>'
        reg1 = re.compile(reg1)#正则匹配获得这个信息发布的日期和网址的后半部分
        urllist1 = re.findall(reg1,html2)
        last_url.append(urllist1)
#        time.sleep()
#    print(last_url)
    for i in range(len(last_url)):
        for j,k in last_url[i]:
            str2 = url+k
#            print(str2)
            page_url.append(str2)
            date_list.append(j)
    time.sleep(2)
    return page_url,date_list
def get_massage(url):
    socket.setdefaulttimeout(20)
    header_all =["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
              "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
              "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)"]
    #"User-Agent":用户代理
    userlist_lenth = len(header_all)
    random_number = random.randint(0,userlist_lenth-1)
    header ={}
    header["User-Agent"] = header_all[random_number]#随机选取一名用户代理
    request = urllib.request.Request(url,headers = header)
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
        html = str(html,encoding='utf-8',errors = 'ignore')#正常网页读取
        response.close()
    except urllib.error.URLError as e:
        print(e.reason)
    return gettitle(html),gettender(html),getwinbid(html),getmoney(html),getmessage(html),getdate(html)
    time.sleep(2)
def gettitle(html):    
    reg1 = r'<h1>\s*?(\S*?)\s*</h1>'#正则表达式获取标题
    reg1 = re.compile(reg1)
    urllist1 = re.findall(reg1,html) #把获得的标题取出
    #print html
    urllist1 = ''.join(urllist1)
    if urllist1 == '':
        urllist1 ='无'
    return urllist1
def gettender(html):#获得招标单位
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)#findall的返回结果是一个数组
    urllist = ''.join(urllist)#数组转化为字符串    
    reg1 = re.compile(r'</?[^>]+>')#找到所有的html标签
    urllist1 = reg1.sub('',urllist)#去除所有的HTML标签
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub('',urllist1)
    key1 = '受'
    key2 = '委托'
    p1 = urllist1.find(key1)+1
    p2 = urllist1.find(key2)
    if p2 != -1:
        if urllist1[p2-1]=='的':       
            urlx = urllist1[p1:p2-1]
        else :
            urlx = urllist1[p1:p2]
    else:
        p3 = urllist1.find('号')+1
        p4 = urllist1.find('就')
        p5 = urllist1.find('一、')
        if p4 == -1:
            urlx = '无'
        elif p5 < p4:
            urlx = '无'
        else :        
            urlx = urllist1[p3:p4]
    return urlx 
def getwinbid(html):#获得中标单位
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    urllist = ''.join(urllist)   
    reg1 = re.compile(r'</?[^>]+>')
    urllist1 = reg1.sub('',urllist)
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub(' ',urllist1)  
    key0 = '一、'
    key =['成 交 单 位','成交供应商名称','中标供应商名称','预中标社会资本合作方','预中标社会资本名称','中标（成交）社会资本的名称','社会资本的名称','中标候选人','预成交供应商名称','预成交人','中标供应商','成交供应商','中标（成交）单位名称','中标人名称','中标单位名称','中标单位单位名称','中标单位：','中标单位','中标人名称','单位','名称']
    key2 = ['二、','三、','四、','五、','六、','七、','八、','联系事项']
    a = 0
    p0=urllist1.find(key0)
    if p0 != -1:
        urllist1 = urllist1[p0:-1]
    for i in key:
        p1=urllist1.find(i)        
        if p1 != -1:
            p = p1
            break
        else :
            a += 1
            if a == len(key):
                p = -1
                a = 0
    list1 = []
    if p != -1:
        html1 = urllist1[p:-1]
        for i in key2:
            p2 = html1.find(i)
            if p2 != -1:
                break 
        html1 = html1[:p2]
        reg = r'[：|\s|:|-|、]([\u4E00-\u9FA5|（|）|-]+公司)'
        reg = re.compile(reg)
        company = re.findall(reg,html1)#返回公司名称
        if len(company)!=0:
            return company
        else :
            reg = r'[：|\s|:|-]([\u4E00-\u9FA5]+[院|馆|所|厂])'
            reg = re.compile(reg)
            company = re.findall(reg,html1)#返回公司名称
            if len(company)!=0:
                return company
            else:
                company.append("无")
                return (company)
                
    else:
        list1.append("无")
        return list1
def getmoney(html):#获取中标金额
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    urllist = ''.join(urllist)   
    reg1 = re.compile(r'</?[^>]+>')
    urllist1 = reg1.sub('',urllist)
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub(' ',urllist1)
    key1 = ['预中标金额','中标折扣率','合同金额','中标金额','中标价','总价','成交价','金 额','金额']
    key2 = ['二、','三、','四、','五、','六、','七、','八、','九、','联系事项','联系人']
    a = 0
    for i in key1:
        p1=urllist1.find(i)
        if p1 != -1:
            p = p1
            break
        else :
            a += 1
            if a ==len(key1):
                p = -1
                a = 0
    if p != -1:
        urllist1 = urllist1[p:-1]
        for i in key2:
            p2 = urllist1.find(i)
            if p2 != -1:
                break           
        html1 = urllist1[:p2]
        reg3 = r'[\s|：|、]+([萬|人|民|币|零|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|佰|仟|万|（|）|(|)|\d|元|圆|角|分|整|。|￥|￥|.|&|y|e|n|;|''|小写|大写|：|,|每年|RMB|%|//|吨|时]+)'
        reg3 = re.compile(reg3)
        money = re.findall(reg3,html1)
        return money
    else:
        return "无" 
def getmessage(html):#获取主要信息
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    urllist = ''.join(urllist)   
    reg1 = re.compile(r'</?[^>]+>')
    urllist1 = reg1.sub('',urllist)
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub(' ',urllist1)
    key1 = ['谈判备忘录内容：','简要说明','项目概况','项目内容']
    key2 = ['二、','三、','四、','五、','六、','七、','八、','九、','联系事项','联系人']
    a = 0
    for i in key1:
        p1=urllist1.find(i)
        if p1 != -1:
            p = p1
            break
        else :
            a += 1
            if a ==len(key1):
                p = -1
                a = 0
    if p != -1:
        urllist1 = urllist1[p:-1]
        for i in key2:
            p2 = urllist1.find(i)
            if p2 != -1:
                html1 = urllist1[:p2]
                break 
            else:
                html1 = urllist1[:-1]
        reg3 = r'[：|\s]+(\S*?)\s'
        reg3 = re.compile(reg3)
        message = re.findall(reg3,html1)
        message = ''.join(message)
        if message == '':
            message = "无"
        return message        
    else:
        return "无"
def getdate(html):#获取日期
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    urllist = ''.join(urllist)   
    reg1 = re.compile(r'</?[^>]+>')
    urllist1 = reg1.sub('',urllist)
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub(' ',urllist1)
    key1 = ['采购公告媒体及日期','公告日期','信息发布日期','公告媒体']
    key2 = ['二、','三、','四、','五、','六、','七、','八、','九、','联系人']
    a = 0
    for i in key1:
        p1=urllist1.find(i)
        if p1 != -1:
            p = p1
            break
        else :
            a += 1
            if a ==len(key1):
                p = -1
                a = 0
    if p != -1:
        urllist1 = urllist1[p:-1]
        for i in key2:
            p2 = urllist1.find(i)
            if p2 != -1:                
                html1 = urllist1[:p2]                
                break
            else:
                html1 = urllist1[:-1]                
                #break
        reg3 = r'[：|\s|；|:|\u4E00-\u9FA5|，|（]+([\d+|\s]+?[.|年][\d+|\s]+?[.|月][\d+|\s]+?日)'
        reg3 = re.compile(reg3)
        message = re.findall(reg3,html1)
        if len(message)==0:
            return "无"
        else:
            message = ''.join(message)
        return message
    else:
        return "无"
if __name__=='__main__':
    url = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/shengji/'#按照市爬取效率更高，不容易被墙
    url_list,date = get_urllist(url)
    print("总数据条数：%d"%url_list)
#    url1 = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/shengji/201806/t20180601_316347.html'
    dic1 = {}
    a = 0
    list1 = ['网址','标题','招标单位','中标单位','中标金额','主要内容','公告日期']
    for url1 in url_list[0:500]:
        list2 = []
        title,tender,winbid,money,message,date = get_massage(url1)
        list2.append(url1)
        list2.append(title)
        list2.append(tender)
        list2.append(winbid)
        list2.append(money)
        list2.append(message)
        list2.append(date)
        dic =dict(zip(list1,list2))
        dic1[a] = dic
        a += 1
        print(a)
#        dic3 = sorted(dic1.items())[-1]
    with open("record2.json","w",encoding="UTF-8") as f:
        json.dump(dic1,f,ensure_ascii=False)
        print("加载入文件完成...")
    '''
    for i in url_list:
        get_massage(i)
    '''