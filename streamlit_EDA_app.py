import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
# Page title
st.set_page_config(page_title='Interactive Data Explorer', page_icon='📊')
st.title('📊 Interactive Data Explorer')

# define tabs
tab1,tab2=st.tabs(['Data Exploration & Visualization','Box Office Analysis'])


with tab1:
    
    # Load data
    st.subheader('Top 5 Samples')
    df = pd.read_csv('movies_genres_summary.csv')
    st.write(df.head())
    
    st.subheader('Stats')
    st.write(df.describe().T)
    
    st.subheader('Exploratory Data Analysis')
    # Option to choose EDA feature via selectbox
    st.sidebar.subheader('EDA Options')
    option = st.sidebar.selectbox(
        'Choose EDA option',
        ['Histogram', 'Box Plot', 'Violin Plot', 'Correlation Heatmap','Pie Plot']
    )
    
    # Histogram
    if option == 'Histogram':
        col = st.selectbox('Choose column for Histogram', df.select_dtypes(include=['float', 'int']).columns)
        fig, ax = plt.subplots()
        sns.histplot(df[col].dropna(), bins=30, kde=True, ax=ax)  # Adding KDE for a smooth curve
        plt.tight_layout()
        st.pyplot(fig)
    
    # Box Plot
    elif option == 'Box Plot':
        col = st.selectbox('Choose column for Box Plot', df.select_dtypes(include=['float', 'int']).columns)
        
        fig, ax = plt.subplots()
        sns.boxplot(data=df, y=col, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Violin Plot
    elif option == 'Violin Plot':
        col = st.selectbox('Choose column for Violin Plot', df.select_dtypes(include=['float', 'int']).columns)
        fig, ax = plt.subplots()
        sns.violinplot(data=df, y=col, ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
    

    # Correlation Heatmap
    elif option == 'Correlation Heatmap':
        fig, ax = plt.subplots()
        sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax, cmap='coolwarm')
        plt.tight_layout()
        st.pyplot(fig)

    elif option == 'Pie Plot':
        st.subheader('Gross Earnings Distribution by Genre')
        pie_data = df.groupby('genre')['gross'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 5))  # Larger figure size
     
        ax.pie(pie_data['gross'], labels=pie_data['genre'], autopct='%1.0f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        st.pyplot(fig)
    
with tab2:
    # App description - Explain functionalities in an expander box
    with st.expander('About this Tab'):
        st.markdown('**What can this app do?**')
        st.info('This app shows the use of Pandas for data wrangling, Altair for chart creation and editable dataframe for data interaction.')
        st.markdown('**How to use the app?**')
        st.warning('To engage with the app, 1. Select genres of your interest in the drop-down selection box and then 2. Select the year duration from the slider widget. As a result, this should generate an updated editable DataFrame and line plot.')

    # Question header
    st.subheader('Which Movie Genre performs ($) best at the box office?')

    # reading csv file
    

    # selecting Genre
    genres_list=df.genre.unique()
    genres_selection = st.multiselect('Select genres', genres_list, ['Action', 'Adventure', 'Biography', 'Comedy', 'Drama', 'Horror'])

    # selecting Year values
    df_years=df['year'].astype(int)
    year_list=df_years.unique()
    year_selection = st.slider('Select year duration', 1986, 2006, (2000, 2016))
    year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

    # filtering dataset
    df_selection=df[df['genre'].isin(genres_selection) & df['year'].isin(year_selection_list)]
    reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
    reshaped_df = reshaped_df.sort_values(by='year', ascending=False)
    st.write(reshaped_df)

    # making data editable
    # Editable DataFrame - Allow users to made live edits to the DataFrame
    df_editor = st.data_editor(reshaped_df, 
        height=212, use_container_width=True,   
        column_config={"year": st.column_config.TextColumn("Year")}, num_rows="dynamic")

    # Data preparation - Prepare data for charting
    df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

    # Display line chart
    chart = alt.Chart(df_chart).mark_line().encode(
                x=alt.X('year:N', title='Year'),
                y=alt.Y('gross:Q', title='Gross earnings ($)'),
                color='genre:N'
                ).properties(height=320)
    st.altair_chart(chart, use_container_width=True)