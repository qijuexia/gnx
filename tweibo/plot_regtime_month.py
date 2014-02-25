import matplotlib.pyplot as plt
import sqlite3
import time

cx=sqlite3.connect("txwbfans.db")
cu=cx.cursor()

N=0
Time=[0]*12
cu.execute("select * from informationtable")
row=cu.fetchone()
while row:
    temp = row[11]
    value = time.localtime(float(temp))
    if value.tm_year==2013:
        N+=1
        for i in range(12):
            if value.tm_mon ==(i+1):
                Time[i] +=1
    row=cu.fetchone()

print N
for i in range(12):
    print Time[i]

plt.title('Regtime_2013 Figure\n'+'total number:'+str(N))
plt.xlabel(u'Month')
plt.ylabel(u'Number')
plt.xticks((0,1,2,3,4,5,6,7,8,9,10,11),(u'/1/'+str(Time[0]),u'/2/'+str(Time[1]),u'/3/'+str(Time[2]),u'/4/'+str(Time[3]),u'/5/'+str(Time[4]),u'/6/'+str(Time[5]),u'/7/'+str(Time[6]),u'/8/'+str(Time[7]),u'/9/'+str(Time[8]),u'/10/'+str(Time[9]),u'/11/'+str(Time[10]),u'/12/'+str(Time[11])))
plt.bar(left=(0,1,2,3,4,5,6,7,8,9,10,11),height=(Time[0],Time[1],Time[2],Time[3],Time[4],Time[5],Time[6],Time[7],Time[8],Time[9],Time[10],Time[11]),width=0.5,align="center")
plt.show()
    
        
