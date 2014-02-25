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

def _clawer_queue(namenumber):
    '''抓取好友进入队列函数'''
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
        tempname = row[0]        
        try:
            fans = api.get.friends__user_fanslist(format="json",reqnum=25,startindex=0,name=tempname,install=0,mode=0)
            N = N+1
            while fans.data.hasnext==0:
                for i in range(0,25):
                    tname = [fans.data.info[i].name]   #注意加上方括号，序列形式
                    cu.execute('select * from queue where name=?',tname)
                    if cu.fetchone():
                        continue
                    else:
                        canshu = [(fans.data.info[i].name,tempname)]
                        cu.executemany('insert into queue values(?,?)',canshu)
                        cx.commit()
                page = page + 1
                print page    
                fans = api.get.friends__user_fanslist(format="json",reqnum=25,startindex=25*page,name=tempname,install=0,mode=0)
                N = N+1
            else:
                if fans.data.has_key('curnum'):
                    num = fans.data.curnum
                else:
                    num = len(fans.data.info)
                for i in range(0,num):
                    tname = [fans.data.info[i].name]
                    cu.execute('select * from queue where name=?',tname)
                    if cu.fetchone():
                        continue
                    else:
                        canshu = [(fans.data.info[i].name,tempname)]
                        cu.executemany('insert into queue values(?,?)',canshu)
                        cx.commit()
                print "--finalpage--"
        except:
            print "!!!!!!!!!!!!!!!!!!!!!!!Error comes up########################"
            filename = "FriendQueueError"
            fp = open(filename,'a')
            output = "no.%d"%(namenumber)+"    name="+tempname+"\n"
            fp.write(output.encode('utf-8'))
            fp.close()
        print tempname
        print namenumber
        namenumber = namenumber + 1
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
    beginnumber = 2324             #初始的抓取值
    _clawer_queue(beginnumber)
                












            
    
