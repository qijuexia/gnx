import matplotlib.pyplot as plt
import sqlite3
import time

cx=sqlite3.connect("txwbfans.db")
cu=cx.cursor()
Time=[0]*5
n=0
cu.execute("select * from informationtable")
row = cu.fetchone()
while row:    
    temp = row[3]
    if temp[0]=="1" and temp[1]=="9":
        if temp[2]=="6":
            Time[0]+=1
        elif temp[2]=="7":
            Time[1]+=1
        elif temp[2]=="8":
            Time[2]+=1
        elif temp[2]=="9":
            Time[3]+=1
        else:
            n+=1
            print temp[2],temp[3]
    elif temp[0]=="2":
        Time[4]+=1

    row =cu.fetchone()
print "no number is:%d"%(n)      
print Time[0],Time[1],Time[2],Time[3],Time[4]
plt.title('Birthday Figure')
plt.xlabel(u'Years')
plt.ylabel(u'Number')
plt.xticks((0,1,2,3,4),(u'/1960s/'+str(Time[0]),u'/1970s/'+str(Time[1]),u'/1980s/'+str(Time[2]),u'/1990s/'+str(Time[3]),u'/2000s/'+str(Time[4])))
plt.bar(left=(0,1,2,3,4),height=(Time[0],Time[1],Time[2],Time[3],Time[4]),width=0.5,align="center")
plt.show()
