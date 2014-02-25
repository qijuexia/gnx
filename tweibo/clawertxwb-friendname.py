#! /usr/bin/env python
#-*-coding:utf-8-*-


import sqlite3
import time
import sys
from oauth import *
from tweibo import *
from key import *

def _authon(J):
    ''' 参数认证函数'''
    oauth = OAuth2Handler()
    oauth.set_app_key_secret(appkey[J],appsecret[J],CALLBACK_URL)  #这一步开始传递认证参数，可以在此循环
    oauth.set_access_token(accesstoken[J])
    oauth.set_openid(openid[J])
    api = API(oauth)
    print"appkey%s"%(J)

def _clawer_friendname(namenumber):
    '''根据列表抓取全部好友名称'''
    J=0
    _authon(J)           #认证    
    cx=sqlite3.connect("txwbfans.db")
    cu=cx.cursor()
    N = 0
    i=1
    cu.execute("select * from queue")
    row = cu.fetchone()
    while i<namenumber:
        i = i+1
        row = cu.fetchone()
    while row:
        page = 0
        temp=" "
        overpage = 0
        tempname = row[0]
        errornumber = 0
        try:
            fans = api.get.friends__user_fanslist(format="json",reqnum=25,startindex=0,name=tempname,install=0,mode=0)
            N = N+1
            while fans.data.hasnext==0:
                for i in range(0,25):
                    temp = temp + " " +fans.data.info[i].name
                page = page +1
                print page
                if page<150 or overpage==1:
                    try:
                        fans = api.get.friends__user_fanslist(format="json",reqnum=25,startindex=25*page,name=tempname,install=0,mode=0)
                        N = N+1
                    except:
                        print "nothing wrong!"
                        errornumber = errornumber+1
                        if errornumber >10:                 #当一个人的错误出现过多跳出循环抓下一个
                            break
                else:
                    canshu = [(namenumber+500000,tempname,temp)]                       #好友过多的数据存储在对应的记录
                    cu.executemany('insert into fntable values(?,?,?)',canshu)       
                    cx.commit()
                    temp= " "
                    overpage = 1
            else:
                if fans.data.has_key('curnum'):
                    num = fans.data.curnum
                else:
                    num = len(fans.data.info)
                for i in range(0,num):
                    temp = temp + " " +fans.data.info[i].name
                print "--finalpage--"
                canshu = [(namenumber,tempname,temp)]
                cu.executemany('insert into fntable values(?,?,?)',canshu)
                cx.commit()
        except:
            print "!!!!!!!!!!!!!!!!!!!!!!!Error comes up########################"
            filename = "FriendErrorRecord"                 #出错写记录到文档
            fp = open(filename,'a')
            output = "no.%d"%(namenumber)+"    name="+tempname+"\n"
            fp.write(output.encode('utf-8'))
            fp.close()
        print tempname
        print namenumber
        namenumber +=1
        if N<200:
            cu.execute('select * from queue')
            row = cu.fetchone()
            i = 1
            while i<namenumber:
                i = i+1
                row = cu.fetchone()
        else:
            N=N-200
            J=(J+1)%22
            _authon(J)
            cu.execute('select * from queue')
            row = cu.fetchone()
            i = 1
            while i<namenumber:
                i = i+1
                row=cu.fetchone()

        
            
if __name__=='__main__':
    beginnumber = 47562         #初始的抓取值
    _clawer_friendname(beginnumber)

                




                
