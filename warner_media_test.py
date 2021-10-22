import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import regex as re

max_width = 1500
padding_top = 5
padding_right = 10
padding_left = 10
padding_bottom = 50
COLOR =  "white"
BACKGROUND_COLOR = "" 

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Warner Media Assignment')

st.sidebar.title('Navigation Page') 
sidebar_selection = st.sidebar.radio('',('Explaratory Analysis','Model Results','Model Evaluation'))


def pmf(x,p): 
    f = p**x*(1-p)**(1-x)
    return f


df = pd.read_csv(os.getcwd()+'/wm_project.csv',sep=",") 
conditions = [
              (df['decade'] == "60s"),
              (df['decade'] == "70s"),
              (df['decade'] == "80s"),
              (df['decade'] == "90s"),
              (df['decade'] == "00s"),
              (df['decade'] == "10s")
        ]

   
values = ['1960','1970','1980','1990','2000','2010']  
df['artist'] = df['artist'].astype('string')  

###TODO 
### ONE Hot Encoding for Categorical variables

cm = sns.light_palette("green", as_cmap=True) 

df['year_in_decade'] = np.select(conditions,values) 
target_col = df['hit']
#features = [col for col in df.columns if col not in target_col]
features = ['danceability','energy','key','loudness','mode','speechiness',
            'instrumentalness','liveness','valence','tempo',
            'duration_ms','chorus_hit','time_signature'] 

#p = sns.countplot(data=df, x="year_in_decade",hue='hit')

if sidebar_selection == 'Explaratory Analysis':
    st.write('This page shows explaratory data analysis')
    if st.checkbox('Show Data'):
        st.dataframe(df.style.apply(lambda x: "background-color: red")) 
    st.write('Data Summary Stats')
    st.write(df.describe())
    st.write(df.hit.value_counts())
    st.write('Artists with the most hits across all decades')
    st.write(df.artist.value_counts())
    st.subheader('Visualize relationship between Features,Decades & Hit')
    st.write('')
    st.subheader('Number of Hits by Decades')
    sns.countplot(data=df, x="year_in_decade",hue='hit')
    st.pyplot()
    st.subheader('Heatmap of Hit and Features')
    plt.figure(figsize=(24,20))
    sns.heatmap(df[features+['hit']].corr(),square=True,  annot=True, vmax=1, vmin=-1, cmap='RdBu')
    st.pyplot()
    st.header('Observations')
    st.write('There doesnt seem to be a consistent pattern across decades and artists with hits')
elif sidebar_selection == 'Model Results': 
    st.write('This page shows explaratory model results')
elif sidebar_selection == 'Model Evaluation': 
    st.write('This page shows Model Evaluation metrics')
