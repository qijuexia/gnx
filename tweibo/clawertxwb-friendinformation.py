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
    return api

def _clawer_information(namenumber):
    '''抓取好友信息'''
    J = 0
    api = _authon(J)           #认证    
    cx = sqlite3.connect("txwbfans.db")
    cu = cx.cursor()
    N = 0
    i = 1
    cu.execute("select * from queue")
    row = cu.fetchone()
    while i < namenumber:
        i = i + 1
        row = cu.fetchone()
    while row:
        page = 0
        tempname = row[0]        
        try:
            information = api.get.user__other_info(format="json",name=tempname)
            N =  N + 1
            temp1 = information.data.nick
            temp2 = str(information.data.birth_year) + '.' + str(information.data.birth_month) + '.' + str(information.data.birth_day)
            temp3 = json.dumps(information.data.city_code)
            temp4 = json.dumps(information.data.comp).decode('unicode-escape')
            temp5 = json.dumps(information.data.edu).decode('unicode-escape')
            temp6 = json.dumps(information.data.country_code)
            temp7 = information.data.fansnum
            temp8 = information.data.favnum
            temp9 = information.data.idolnum
            if information.data.has_key('regtime'):
                temp10 = json.dumps(information.data.regtime)
            else:
                temp10 = 0
            temp11= json.dumps(information.data).decode('unicode-escape')
            canshu = [(namenumber,tempname,temp1,temp2,temp3,temp4,temp5,temp6,temp7,temp8,temp9,temp10,temp11)]
            cu.executemany('insert into informationtable values(?,?,?,?,?,?,?,?,?,?,?,?,?)',canshu)
            cx.commit()
            print namenumber
            print tempname
            print "nextone is:"
        except TWeiboError:
            print namenumber
            print "-------------------error comes up---------------"
            filename = "InformationErrorRecord"
            fp = open(filename,'a')
            output = "no.%d" % (namenumber) + "    name=" + tempname + "\n"
            fp.write(output.encode('utf-8'))
            fp.close()
        namenumber += 1
        if N >= 200:
            N = N - 200
            J = (J + 1) % 22
            api = _authon(J)
        f=open('informationnumber.txt','w')
        f.write(str(namenumber))
        f.close()
        cu.execute('select * from queue')
        row = cu.fetchone()
        i = 1
        while i< namenumber:
            i = i + 1
            row = cu.fetchone()
        
            
if __name__=='__main__':
    f=open('informationnumber.txt','r')
    beginnumber =int(f.read())            #初始的抓取值
    f.close()                                #设置初始值
    _clawer_information(beginnumber)

