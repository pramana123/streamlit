import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import re
import streamlit as st
from datetime import datetime,timedelta

def convert_slide_value_to_datetime(x):
    datetimes =  datetime.strptime(str(x), f'%Y-%m-%d %H:%M:%S')
    return datetimes


def fix_change_date(x):
    pattern=r"(\d+)\/(\d+)\/(\d+)"
    matches=re.match(pattern=pattern,string=str(x))#split the date into 3 different group
    group=matches.group(2).zfill(2)
    group_1=int(matches.group(1))
    if ((group_1%2==0 and group_1<=7) or (group_1%2>0 and group_1>7)) and int(group)>=30:#detect if date are correct or not
        group="30"
    string="{}/{}/{}".format(matches.group(1).zfill(2),group,matches.group(3))
    return string

def find_word(string_series,searched):
    data=[]
    for string in string_series:
        matches=re.match(pattern=searched,string=string)
        if matches:
            data.append(True)
        else:
            data.append(False)
    series=np.array(data)
    return series
# Initialize connection.
conn = st.experimental_connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from buku;', ttl=600)

#about section
st.title("Data buku")
st.header("About Datasets")
st.caption("The dataset includes information about books, such as titles, authors, publication dates, ratings, reviews, and popularity metrics, to help analyze and understand book-related data.")
st.dataframe(df.iloc[:50],hide_index=True)

#start the cleaning data section
st.header("Data cleaning")
st.subheader("check data type")
st.caption("we need to check if the column is in the correct datatype")
types=df.dtypes
types_table=pd.DataFrame({'Column_Name': types.index, 'Data_Type': types.values})
st.dataframe(types_table)
st.caption("as we can see the publication is in the wrong format we change the format by converting it to datetime format.")
df["publication_date"]=df["publication_date"].apply(fix_change_date)#apply data cleaning for date that have incorrect date
df["publication_date"]=pd.to_datetime(df['publication_date'], infer_datetime_format=True)
st.subheader("check null value")
st.caption("then we need to check to the null value for it")
miss_value=df.isna().sum()
miss_value_table=pd.DataFrame({'Column_Name': miss_value.index, 'missing_value': miss_value.values})
st.dataframe(miss_value_table)
unique={}
st.subheader("check duplicated value")
st.caption("then we need to check to the duplicated value for it")
for i in df.keys():
    unique[i]=[x for x in df[i].unique()]
option = st.selectbox("Choose Data:",df.keys())
st.data_editor(pd.DataFrame(unique[str(option)],columns=["unique data of : {}".format(str(option))]), width=800, height=400,hide_index=True)

#start the data Explainatory Data Analysis section
st.header("Data EDA")
st.subheader("Checking data by relase date")
st.caption("we could check if there is an effect of date in any of the column in the data.")
#change data type to datetime instead of pandas.datetime
max_date=df["publication_date"].max()
min_date=df["publication_date"].min()
max_date=datetime.fromtimestamp(max_date.timestamp())
min_date=datetime.fromtimestamp(0)+timedelta(seconds=min_date.timestamp())
appointment = st.slider(
    "Select a date range",
    min_value=max_date,
    max_value=min_date,
    value=(max_date, min_date),
    step=timedelta(days=1)
)
option2 = st.selectbox("Choose Data the data:",types_table.loc[(types_table["Data_Type"]=="int64") | (types_table["Data_Type"]=="float64")])
st.bar_chart(df.loc[(df["publication_date"] >= convert_slide_value_to_datetime(appointment[0])) & (df["publication_date"] <= convert_slide_value_to_datetime(appointment[1]))],x="publication_date",y=option2)
st.subheader("Checking the top 10 most book author")
st.caption("Checking the top 10 author who have written the most book in the datasets")
most_written_author=df[["authors","title"]].groupby(["authors"]).count().sort_values(by=["title"],ascending=False)
st.dataframe(most_written_author[:10], width=800, height=400)

st.subheader("Checking the most rated book")
st.caption("We can check the book that was rated by sorting in descending than see the few of the first row")
most_reviewed_book=df[["ratings_count","title"]].sort_values(by=["ratings_count"],ascending=False)
st.dataframe(most_reviewed_book, width=800, height=400)

st.subheader("Serching book with the most rated")
st.caption("We want to add a input box that able to search the table and find the output that we wanted")
search_box = st.text_input("Search :")
searched_data=df.loc[find_word(df["title"],r".*"+search_box+r".*")]
most_reviewed_book=searched_data[["ratings_count","title"]].sort_values(by=["ratings_count"],ascending=False)
st.dataframe(most_reviewed_book, width=800,hide_index=True)
