# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 09:41:10 2018

@author: Administrator
"""
import urllib
import re
import json
import pdb
#import sys 
#from bs4 import BeautifulSoup
def geturl1(url):
    html = urllib.request.urlopen(url).read() 
    html = html.decode()
    #print (html)
    url1 = []
    url2 = []
    url3 = []
    reg = r' <li id=""><span><nobr><a href="./(.*?)" target="fram" title=".*?">.*?</a></nobr></span></li>'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    for i in urllist:
        url1.append(url+i)
    for i in url1:
        html2 = urllib.request.urlopen(i).read() 
        html2=html2.decode('utf-8')
        reg2 = r'createPageHTML\((.*?), 0, "index", "html"\);'
        reg2 = re.compile(reg2)
        urllen = re.findall(reg2,html2)
        url3.append(urllen[0])     
        
    return url1,url3
def geturl(url):
    url1 = []
    url2 = []
    url3 = []
    url4 = []
    url1,url2 = geturl1(url)
    print (url1,url2)
    n = 0 
    for i in range(len(url1)):
        j = url2[i]
        for k in range(int(j)):
            if k == 0:
                url3.append(url1[i]+'index.html')
            else:
                url3.append(url1[i]+'index_'+str(k)+'.html')
    print (len(url3))
    for i in range(len(url2)):
        url2[i] = int(url2[i])
        print (url2[i])
    for i in range(len(url3)):
         html = urllib.request.urlopen(url3[i]).read() 
         html = html.decode()
         reg = r'<a href="./(.*?)" target="_blank">.*?</a>'
         reg = re.compile(reg)
         urllist = re.findall(reg,html)
         for k in urllist:
             url4.append(url1[n]+k)         
         if i == url2[n]:
             url2[n+1] += url2[n]
             n += 1
             print (n,url1[n])
    print (len(url4))
    return url4
'''    
         html = urllib.request.urlopen(url3[i]).read() 
         html = html.decode()
         reg = r'<a href="./(.*?)" target="_blank">.*?</a>'
         reg = re.compile(reg)
         urllist = re.findall(reg,html)
         for k in urllist:
             url4.append(url1[n]+k)
    print (url4)
'''
         #url4.append(url3)  
    #url = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/changzhou/'
    #url1 = url+'index_1.html'
'''
    html = urllib.request.urlopen(url).read() 
    html = html.decode()
    reg = r'<a href="./(.*?)" target="_blank">.*?</a>'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
'''    
    
def gettitle(url):    
    html = urllib.request.urlopen(url).read()   
    #print (html)
    #print (type(html))
    
    html = html.decode()
    #print(type(html))
    reg1 = r'<h1>\s*?(\S*?)\s*</h1>'#正则表达式获取标题
    reg1 = re.compile(reg1)
    urllist1 = re.findall(reg1,html) #把获得的标题取出
    #print html
    urllist1 = ''.join(urllist1)
    if urllist1 == '':
        urllist1 ='无'
    return urllist1
    
def gettender(url):#获得招标单位
    html = urllib.request.urlopen(url).read()  #数据类型class 'bytes'
    #print html
    #bsobj =  BeautifulSoup(html)
    #print bsobj.body.h1
    html = html.decode()
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
    #d = re.compile(r'</?[^>]+>')#去除所有的HTML标签
    #dd = d.sub('',html)#所有的HTML标签用空白符代替
    #d = re.compile()
    #d1 = re.compile(r'[^\x00-\xff]')#汉字的匹配
    #dd1 = re.findall(d1,dd)

def getwinbid(url):#获得中标单位
    html = urllib.request.urlopen(url).read()
    html = html.decode()
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
               # print(company)
                return (company)
                
    else:
        list1.append("无")
        return list1
        #regex_str = r'/s*?:*?([\u4E00-\u9FA5]+公司)'
        #match_obj = re.match(regex_str, html1)
        #if match_obj:
            #print(match_obj.group(1))
        #    return match_obj.group()
        #else:
         #   return -1
def getmoney(url):#获取中标金额
    html = urllib.request.urlopen(url).read()
    html = html.decode()
    reg = r'<!--正文-->([\s\S]*?)<!--endprint1-->'
    reg = re.compile(reg)
    urllist = re.findall(reg,html)
    urllist = ''.join(urllist)   
    reg1 = re.compile(r'</?[^>]+>')
    urllist1 = reg1.sub('',urllist)
    reg2 = re.compile(r'&nbsp;')
    urllist1 = reg2.sub(' ',urllist1)
    key1 = ['预中标金额','中标折扣率','合同金额','中标金额','中标价','总价','成交价','金 额','金额']
    key2 = ['二、','三、','四、','五、','六、','七、','联系事项','联系人']
    a = 0
    for i in key1:
        p1=urllist1.find(i)
        #print (urllist1[p1:p1+6])
        if p1 != -1:
            p = p1
            break
        else :
            a += 1
            if a ==len(key1):
                p = -1
                a = 0
    #print (p)
    if p != -1:
        urllist1 = urllist1[p:-1]
        for i in key2:
            p2 = urllist1.find(i)
            if p2 != -1:
                #print (p2)
                break           
        html1 = urllist1[:p2]
        #print (html1)
        #reg3 = r'[：|\s]+(\S*?)\s'
        reg3 = r'[\s|：|、]+([萬|人|民|币|零|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|佰|仟|万|（|）|(|)|\d|元|圆|角|分|整|。|￥|￥|.|&|y|e|n|;|''|小写|大写|：|,|每年|RMB|%|//|吨|时]+)'
        reg3 = re.compile(reg3)
        money = re.findall(reg3,html1)
        #print (money[0])
        return money
    else:
        return "无"
def getmessage(url):#获取主要信息
    html = urllib.request.urlopen(url).read()
    html = html.decode()
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
                #print (p2)
                html1 = urllist1[:p2]
                #return html1
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
        #html1 = urllist1[:p2]        
    else:
        return "无"
def getdate(url):#获取日期
    html = urllib.request.urlopen(url).read()
    html = html.decode()
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
    list1 = ['网址','标题','招标单位','中标单位','中标金额','主要内容','公告日期']
    list2 = []
    dic2 = {}
    a = 0
    '''以下为测试案例
    i = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/nanjing/201806/t20180608_318768.html'
    print (i)
    print ('标题为：',gettitle(i))   
    print ('招标单位：',gettender(i))
    print ('中标单位:',getwinbid(i))
    print ('中标金额:',getmoney(i))
    print ('主要内容：',getmessage(i))                    
    print ('公告日期：',getdate(i))

    '''
    url = 'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/'
    for i in geturl(url)[1]:
        list2 = []
        list2.append(i)
        list2.append(gettitle(i))
        list2.append(gettender(i))
        list2.append(getwinbid(i))
        list2.append(getmoney(i))
        list2.append(getmessage(i))
        list2.append(getdate(i))
        dic =dict(zip(list1,list2))
        dic2[a] = dic
        a += 1
        print(a)  
   
    #print (dic2)
    #print (dic2[9999])
    
    with open("record1.json","w",encoding="UTF-8") as f:
        json.dump(dic2,f,ensure_ascii=False)
        print("加载入文件完成...")
       
    #geturl(url)
          
    '''
    for i in url1:
        print (i)
        print ('标题为：',gettitle(i))   
        print ('招标单位：',gettender(i))
        print ('中标单位:',getwinbid(i))
        print ('中标金额:',getmoney(i))
        print ('主要内容：',getmessage(i))
        print ('公告日期：',getdate(i))
    '''       
    #print (sys.getdefaultencoding())#获得系统的默认编码
       