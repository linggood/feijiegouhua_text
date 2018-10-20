#!/usr/bin/env python

import os
from time import sleep
from tkinter import *
import webbrowser
import json
import jieba
class DirList(object):
    def __init__(self, initdir=None):
        self.top = Tk()
        self.top.title("非结构化文本处理系统")
        self.label = Label(self.top,
            text='非结构化文本处理软件V1.0',font=('Helvetica', 12, 'bold'),fg='blue')
        self.label.pack()

        self.cwd1 = StringVar(self.top)
        self.cwd2 = StringVar(self.top)
        self.cwd3 = StringVar(self.top)
        '''
        self.dirl = Label(self.top, fg='blue',
            font=('Helvetica', 12, 'bold'))
        self.dirl.pack()
        '''
        self.dirfm = Frame(self.top)
        self.dirsb = Scrollbar(self.dirfm)#上面插入一 插入一个滚动条
        self.dirsb.pack(side=RIGHT, fill=Y)#设置滚动条的位置
        self.dirs = Listbox(self.dirfm, height=15,
            width=100, yscrollcommand=self.dirsb.set)#滚动条必然要配合listbox列表框，内容 控制滚动条
        self.dirs.bind('<Double-Button-1>', self.select)#双击鼠标事件
        self.dirsb.config(command=self.dirs.yview)#滑动滚动条控制Scrollbar的滚动
        self.dirs.pack(side=LEFT, fill=BOTH)
        self.dirfm.pack()
        
        self.frame1 = Frame(self.top)     
        self.dirn1 = Entry(self.frame1, width=50,#输入文本域，textvariable是文本域的默认值
            textvariable=self.cwd1)
        self.cwd1.set("输入公司名称，例如：江苏第二师范学院")
        self.dirn1.bind('<Return>', self.certain1)#按下回车，调用函数dols
        self.dirs.delete(0,END)
        self.top.update()
        self.dirn1.pack(side=RIGHT)
        #self.dirn1.grid(row = 0,column = 0,padx = 5,pady = 5)
        self.label1 = Label(self.frame1,text = "精准查询：",font=('Helvetica', 12, 'bold'))
        self.label1.pack(side=LEFT)
        #self.button1.grid(row = 0,column = 1,padx = 5,pady = 5)
        self.frame1.pack()
        
        self.frame2 = Frame(self.top)  
        self.dirn2 = Entry(self.frame2, width=50,#输入文本域，textvariable是文本域的默认值
            textvariable=self.cwd2)
        self.cwd2.set("医院")
        self.dirn2.bind('<Return>', self.certain2)#按下回车，调用函数dols
        self.label2 = Label(self.frame2,text = "模糊查询：",font=('Helvetica', 12, 'bold'))
        self.label2.pack(side=LEFT)
        self.dirn2.pack(side = RIGHT)
        self.frame2.pack()
        
        self.frame3 = Frame(self.top)  
        self.dirn3 = Entry(self.frame3, width=50,#输入文本域，textvariable是文本域的默认值
            textvariable=self.cwd3)
        self.cwd3.set("人民")
        self.dirn3.bind('<Return>', self.certain3)#按下回车，调用函数dols
        self.label3 = Label(self.frame3,text = "限制查询：",font=('Helvetica', 12, 'bold'))
        self.label3.pack(side=LEFT)
        self.dirn3.pack(side = RIGHT)
        self.frame3.pack()
        
        self.quit = Button(self.top, text='退出',
            command=self.top.quit,
            activeforeground='white')
        #self.quit.bind("<ButtonRelease-1>")
            #activebackground='red'
        self.quit.pack()
        #self.cwd1.set()
    def get_entry(self,x = 0):
        self.string1 = self.cwd1.get()#把输入的参数传入string字符串
    def get_entry2(self,x = 0):
        self.string2 = self.cwd2.get()
    def get_entry3(self,x = 0):
        self.string3 = self.cwd3.get()
    def load_json(self,x = 0):
        with open("record2.json","r",encoding="UTF-8") as f:
            self.data = json.load(f)        
        #DirList        
       # pass
    def certain1(self,x = 0):
        self.list1 = []
        self.load_json()
        self.get_entry()
        self.dirs.config(selectbackground='red')
        self.dict = {}
        self.dirs.delete(0,END)#清除列表
        self.top.update()#更新列表
        #print (self.cwd1.get())
        #self.list1.append(self.cwd1)
        #print (self.data.values())
        a = 1
        for self.key,self.value in self.data.items():          
            
            #print(type(self.value["中标单位"]))
            if (self.value["招标单位"] == self.string1):                
                #print(self.value["标题"])
                self.value1 =  str(a)+'、'+self.value["标题"]                            
                self.list1.append(self.value1)  
                #print (self.key)
                self.dict[self.value1] = self.key
                a = int(a)   #加入序号防止有相同标题             
                a += 1
               # print (a)
            else :
                #print (self.value["中标单位"])                
                for company in self.value["中标单位"]:
                    if(company == self.string1):
                        self.value1 =  str(a)+'、'+self.value["标题"]                                              
                        self.list1.append(self.value1)
                        self.dict[self.value1] = self.key#
                        a = int(a)   #加入序号防止有相同标题             
                        a += 1               
            
        for i in self.list1:
            self.dirs.insert(END,i)
            #print (i)
            self.top.update()        
           
        #pass
    def certain2(self,x = 0):
        self.dirs.bind('<Double-Button-1>', self.select3)
        self.list2 = []
        self.list3 = []#标题集合
        self.load_json()
        self.get_entry2()
        self.dirs.config(selectbackground='red')
        self.dict = {}
        self.dirs.delete(0,END)#清除列表
        self.top.update()#更新列表
        a = 1
       # b = 0
        for self.key,self.value in self.data.items():          
            self.seg_list1 = jieba.cut(self.value["招标单位"], cut_all=True, HMM=False)#使用结巴分词做模糊查询
            self.seg_list3 = jieba.cut(self.value["主要内容"], cut_all=True, HMM=False)
            self.seg_list4 = jieba.cut(self.value["标题"], cut_all=True, HMM=False)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式
            for i in self.seg_list1:#招标单位的模糊查询
                #print (i)            
                if (i == self.string2):                
                    #print(self.value["标题"])
                    self.value2 =  str(a)+'、'+self.value["标题"]
                    self.list3.append(self.value["标题"])                            
                    self.list2.append(self.value2)  
                    #print (self.key)
                    self.dict[self.value2] = self.key
                    a = int(a)   #加入序号防止有相同标题             
                    a += 1
                    break            
               # print (a)
               #print (self.value["中标单位"])                
            for self.company in self.value["中标单位"]:#中标单位的模糊查询
                seg_list2 = jieba.cut(self.company, cut_all=True, HMM=False)
                for i in seg_list2:
                    if(i == self.string2):
                        if self.value["标题"] not in self.list3:
                            self.value2 =  str(a)+'、'+self.value["标题"] 
                            self.list3.append(self.value["标题"])                                              
                            self.list2.append(self.value2)
                            self.dict[self.value2] = self.key#
                            a = int(a)   #加入序号防止有相同标题             
                            a += 1
                            break
            for i in self.seg_list3:#主要内容的模糊查询
                if(i == self.string2):
                    if self.value["标题"] not in self.list3:
                        self.value3 =  str(a)+'、'+self.value["标题"]                                              
                        self.list2.append(self.value3)
                        self.dict[self.value3] = self.key#
                        a = int(a)   #加入序号防止有相同标题             
                        a += 1
                        break
            for i in self.seg_list4:#标题的模糊查询
                if(i == self.string2):
                    if self.value["标题"] not in self.list3:
                        self.value4 =  str(a)+'、'+self.value["标题"]                                              
                        self.list2.append(self.value4)
                        self.dict[self.value4] = self.key#
                        a = int(a)   #加入序号防止有相同标题             
                        a += 1
                    break               
            
        for i in self.list2:
            self.dirs.insert(END,i)
            #print (i)
            self.top.update()     
        
    def certain3(self,x = 0):
        self.dirs.bind('<Double-Button-1>', self.select5)
        #self.list2 = []
        self.list4 = []        
        self.load_json()
        self.get_entry3()
        self.dirs.config(selectbackground='red')
        self.dict = {} 
        self.dirs.delete(0,END)#清除列表
        self.top.update()#更新列表
       # print ("2")
       # print (self.list2)   
       
        for i in range(len(self.list3)):  
            #print (self.list3[0])             
            #print (i)                      
            self.seg_list5 = jieba.cut_for_search(self.list3[i], HMM=True)
            for j in self.seg_list5:
                if j == self.string3:
                    #print (self.list3[i]) 
                    self.list3[i] = ''
                    break
                    
        a = 1
        for i in self.list3:
            if i != '': 
                self.value5 = str(a)+'、'+i
                self.dirs.insert(END,self.value5)
                a = int(a)
                a += 1
                #print (i)
                self.top.update() 
                for self.key,self.value in self.data.items():
                     if (i == self.value["标题"]):
                             #print (type(i),type(self.value5))
                             self.list4.append(i)
                             self.dict[self.value5] = self.key
                                                                   
            
        
        
    def select(self,x = 0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        #print (self.get_value)
        self.key1 = self.dict[self.get_value]
        self.dirs.delete(0,END)
        self.top.update()
        self.dirs.insert(END,"上一页")
        #print (self.dict[self.get_value])
        for self.key,self.value in self.data.items():  
            if self.key == self.key1:
                for item in self.value.items():
                    self.dirs.insert(END,item)
                    self.top.update()
        self.dirs.bind('<Double-Button-1>', self.select2)
        
       # pass
    def select2(self,x = 0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        #print(type(self.get_value))
        if self.get_value == "上一页":
            self.dirs.delete(0,END)
            self.top.update()            
            self.certain1()  
           # self.certain2()
            self.dirs.bind('<Double-Button-1>', self.select)
        elif self.get_value[0]=="网址":            
            webbrowser.open(self.get_value[1]) 
        
    def select3(self,x = 0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        #print (self.get_value)
        self.key1 = self.dict[self.get_value]
        self.dirs.delete(0,END)
        self.top.update()
        self.dirs.insert(END,"上一页")
        #print (self.dict[self.get_value])
        for self.key,self.value in self.data.items():  
            if self.key == self.key1:
                for item in self.value.items():
                    self.dirs.insert(END,item)
                    self.top.update()
        self.dirs.bind('<Double-Button-1>', self.select4)        
    def select4(self,x = 0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        if self.get_value == "上一页":
            self.dirs.delete(0,END)
            self.top.update()            
            #self.certain1()  
            self.certain2()
            self.dirs.bind('<Double-Button-1>', self.select3)
        elif self.get_value[0]=="网址":            
            webbrowser.open(self.get_value[1])
    def select5(self,x =0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        #print (self.get_value)
        self.key1 = self.dict[self.get_value]
        self.dirs.delete(0,END)
        self.top.update()
        self.dirs.insert(END,"上一页")
        #print (self.dict[self.get_value])
        for self.key,self.value in self.data.items():  
            if self.key == self.key1:
                for item in self.value.items():
                    self.dirs.insert(END,item)
                    self.top.update()
        self.dirs.bind('<Double-Button-1>', self.select6)
    def select6(self,x = 0):
        self.get_value = self.dirs.get(self.dirs.curselection())
        if self.get_value == "上一页":
            self.dirs.delete(0,END)
            self.top.update()            
            #self.certain1()  
            self.certain3()
            self.dirs.bind('<Double-Button-1>', self.select5)  
        elif self.get_value[0]=="网址":            
            webbrowser.open(self.get_value[1])
    def event1(self,x=0):
        pass
    def event2(self):
        pass
        
        '''
        
        '''
    

def main():
    d = DirList(os.curdir)
    mainloop()

if __name__ == '__main__':
    main()
