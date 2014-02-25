import matplotlib.pyplot as plt
import sqlite3


cx=sqlite3.connect("txwbfans.db")
cu=cx.cursor()
i=0
j=0
error=0
cu.execute("select * from informationtable")
row=cu.fetchone()
while row:
    temp=row[12]
    x=temp.find('sex')          #在处理text文本时候，利用find定位可以很方便
    y=temp[x+6]                
    if y =='1':                   #返回值为字符串，比较时要注意
        i +=1
    elif y=='2':
        j +=1
    else:
        error +=1
    row=cu.fetchone()
    
print i,j,error
plt.title('sex figure')
plt.xlabel(u'Sex')
plt.ylabel(u'Number')
plt.xticks((0,1,2),(u'boy'+str(i),u'girl'+str(j),u'error'+str(error)))
plt.bar(left=(0,1,2),height=(i,j,error),width=0.5,align="center")
plt.show()
        
    
    

