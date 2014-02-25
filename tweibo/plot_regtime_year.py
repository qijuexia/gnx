import matplotlib.pyplot as plt
import sqlite3
import time

cx=sqlite3.connect("txwbfans.db")
cu=cx.cursor()

Time=[0,0,0,0,0]
cu.execute("select * from informationtable")
row=cu.fetchone()
while row:
    temp=row[11]
    value = time.localtime(float(temp))
    if value.tm_year==2010:
        Time[0] +=1
    elif value.tm_year==2011:
        Time[1] +=1
    elif value.tm_year==2012:
        Time[2] +=1
    elif value.tm_year==2013:
        Time[3] +=1
    else:
        Time[4] +=1
    row=cu.fetchone()

print Time[0],Time[1],Time[2],Time[3],Time[4]

plt.title('Regtime Figure')
plt.xlabel(u'Year')
plt.ylabel(u'Number')
plt.xticks((0,1,2,3,4),(u'/2010/'+str(Time[0]),u'/2011/'+str(Time[1]),u'/2012/'+str(Time[2]),u'/2013/'+str(Time[3]),u'/null/'+str(Time[4])))
plt.bar(left=(0,1,2,3,4),height=(Time[0],Time[1],Time[2],Time[3],Time[4]),width=0.5,align="center")
plt.show()
