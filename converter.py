import mysql.connector
import pandas as pd
import numpy as np
mydb = mysql.connector.connect(
    host="2e5.h.filess.io",
    user="streamlit_voyagetorn",
    password="56e624bbb5d95587735bc18de2f01507bf2103d6",
    database="streamlit_voyagetorn",
    port="3307"
)
 
data=pd.read_csv(f"E:\\streamtugas\\books.csv")

cursor = mydb.cursor()
excute="CREATE TABLE buku ("
dicthash={
    "int64":"BIGINT(255)",
    "float64":"FLOAT(30,15)",
    "object":"TEXT"
}
column_bad={

}

conv_hash={
    np.int64 : lambda x : int(x),
    np.float64 : lambda x : float(x),
    str  : lambda x : x,
    float : lambda x : float(x)
}
data.isna()
for i in data.keys():
    column_bad[i]=i
column_bad["key"]="key_1"
column_bad["Sat.Fat"]="Sat_Fat"
INSERT_sql="INSERT INTO buku ("

for i in data.keys()[:-1]:
    INSERT_sql+="{},".format(column_bad[str(i)])
INSERT_sql+="{}) VALUES (".format(column_bad[str(data.keys()[-1:][0])])
for i in data.keys()[:-1]:
    INSERT_sql+="%s,"
INSERT_sql+="%s)"
for i in data.keys()[:-1]:
    excute+="{} {},".format(column_bad[str(i)],dicthash[str(data[i].dtypes)])
excute+="{} {})".format(column_bad[str(data.keys()[-1:][0])],dicthash[str(data[data.keys()[-1:][0]].dtypes)])

# for i in data.keys():
#     data[i].fillna("", inplace=True)
print(excute)
cursor.execute(excute)
mydb.commit()

for i in data.iloc():
    temp=[]
    for z in i :
        temp.append(conv_hash[type(z)](z))
    print(temp)
    cursor.execute(INSERT_sql,tuple(temp))
    mydb.commit()
cursor.close()
mydb.close()