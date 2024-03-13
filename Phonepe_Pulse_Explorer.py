# Importing required libraries
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as mySql
import pandas as pd
import requests 
import plotly.express as px
import locale
import plotly.graph_objects as go


# ___*___*___*___*___*___ Format Numbers In Indian Style ___*___*___*___*___*___ #
def indianNumberFormat(number):
    """
    Format numbers in Indian style.
    Args:
        number (int): Number to be formatted.
    Returns:
        str: Formatted number string.
    """
    locale.setlocale(locale.LC_NUMERIC, 'en_IN')
    formattedNumber = locale.format_string("%d", number, grouping=True)
    return formattedNumber


# ___*___*___*___*___*___ Establish connection to MySQL database ___*___*___*___*___*___ #
def connectToMySql():
    """
    Establish connection to MySQL database.
    Returns:
        object: MySQL connection object.
    """
    myConnection = mySql.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'phonepe_pulse'
    )
    return myConnection

    
# ___*___*___*___*___*___ Load data from MySQL tables into Pandas DataFrames ___*___*___*___*___*___ #
def dataFrameLoader():
    """
    Load data from MySQL tables into Pandas DataFrames.
    Returns:
        tuple: DataFrames containing data from MySQL tables.
    """
    mySqlConnection = connectToMySql()
    myCursor = mySqlConnection.cursor()

    # Query to retreive Aggregated Transaction data
    myCursor.execute('SELECT * FROM aggtrans')
    aggTransTable = myCursor.fetchall()
    df_aggTrans = pd.DataFrame(aggTransTable,columns = ['State','Year','Quarter','Transaction Type','Transaction Count', 'Transaction Amount'])
        
    # Query to retreive Aggregated User data
    myCursor.execute('SELECT * FROM agguser')
    aggUserTable = myCursor.fetchall()
    df_aggUser = pd.DataFrame(aggUserTable, columns = ['State', 'Year', 'Quarter', 'Brand Name', 'User Count', 'User Percentage'])
    
    # Query to retreive Map Transaction data
    myCursor.execute('SELECT * FROM maptrans')
    mapTransTable = myCursor.fetchall()
    df_mapTrans = pd.DataFrame(mapTransTable, columns = ['State', 'Year', 'Quarter', 'District', 'Transaction Count', 'Transaction Amount'])
    
    # Query to retreive Map User data
    myCursor.execute('SELECT * FROM mapuser')
    mapUserTable = myCursor.fetchall()
    df_mapUser = pd.DataFrame(mapUserTable, columns = ['State', 'Year', 'Quarter', 'District', 'Registered Users', 'App Opens'])
    
    # Query to retreive Top Transaction data
    myCursor.execute('SELECT * FROM toptrans')
    topTransTable = myCursor.fetchall()
    df_topTrans = pd.DataFrame(topTransTable, columns = ['State', 'Year', 'Quarter', 'Pincode', 'Transaction Count', 'Transaction Amount'])
    df_topTrans['Pincode'] = df_topTrans['Pincode'].astype(str)

    # Querty to retreive Top User data
    myCursor.execute('SELECT * FROM topuser')
    topUserTable = myCursor.fetchall()
    df_topUser = pd.DataFrame(topUserTable, columns = ['State', 'Year', 'Quarter', 'Pincode', 'Registered Users'])
    df_topUser['Pincode'] = df_topUser['Pincode'].astype(str)
    
    mySqlConnection.close()
    myCursor.close()

    return df_aggTrans, df_aggUser, df_mapTrans, df_mapUser, df_topTrans, df_topUser



# ___*___*___*___*___*___ Setting up the page configuration ___*___*___*___*___*___ #

# Define the logo image in base64 encoded format
logo_image = "data:image/png;base64,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"

# Set the page configuration using Streamlit's set_page_config function
st.set_page_config(page_title= "Phonepe Pulse | Data Visualization",
                   page_icon= logo_image,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )

# Define custom CSS to hide default formatting elements
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """

# Apply the custom CSS using Streamlit's markdown function
st.markdown(hide_default_format, unsafe_allow_html=True)


# Define column layout for the streamlit app
col1, col2,  col3, = st.columns([1, 2, 6])

# Column 1: Logo
with col1:
    # Define logo image
    logo_image = "data:image/png;base64,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"
    # Display logo image
    st.image(logo_image, use_column_width=False, width=100)


# Column 2: Title
with col2:
    # Define title text
    title_text = ":violet[PhonePe | Pulse]" 
    additional_text = ""
    combined_text = f"{title_text} {additional_text}"
    # Display title with styled markdown
    st.markdown('<h2 style="color:#6739b7">Phonepe | Pulse</h2><hr style="height:2px;border:none;color:#6739b7;background-color:#6739b7;width:6cm;margin:0;padding:0;" /><b style="color:#6739b7; font-size: 16px;">The beat of </b><b style="color:#6739b7; font-size: 25px;">progress</b>', unsafe_allow_html=True)


# Column 3: Navigation Menu
with col3:
    # Create an option menu for navigation
    selected = option_menu(
        menu_title = None,
        options=["Home","Data API's","Analysis","Explore Data","Contact Us"],
        default_index= 0,
        icons =["house","gear","graph-up-arrow","map","card-heading"],
        orientation="horizontal",
        styles={
        "icon": {"color": "black", "font-size": "12px"},
        "nav-link": { "--hover-color": "#834da0","color": "black","width":"140px",
                        "text-align":"center","padding":"5px 0",
                        "border-bottom":"4px solid transparent","transition":"border-bottom 0.5 ease","font-size":"14px"},
        "nav-link:hover": {"color":"black"},
        "nav-link-selected": {"background-color": "#473480", "width":"140px","border-bottom":"4px solid #bc8c8c","color":"white"}
        }           
    )

        


if selected == "Home":
    st.write("")
    st.write("")
    st.write("")
    st.markdown("## :violet[Data Visualization and Exploration]")
    st.markdown("##### :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("##### :violet[Domain :]")
        st.write("<h5>Fintech</h5>",unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.markdown("##### :violet[Technologies used :]")
        st.write("<h5>Our tool leverages cutting-edge technologies including GitHub Cloning, Python, Pandas, MySQL, Streamlit, and Plotly.</h5>",unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.markdown("##### :violet[Overview :]")
        st.write("<h5>Our Streamlit web application offers an intuitive interface to explore and analyze PhonePe Pulse data comprehensively. Gain valuable insights into transaction trends, user demographics, top 10 state distributions, district analyses, pincode insights, and identify leading brands based on user engagement. We employ sophisticated visualizations such as Bar charts, Pie charts, and Geo maps to deliver actionable insights effectively.</h5>",unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.markdown(
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/Yy03rjSUIB8" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )

    with col2:
        video_url = "https://github.com/BalaKrishnanCodeSpace/Phonepe_Pulse_Data_Extraction_-_Visualization/blob/main/Miscellaneous_Files/Pulse_Video.mp4?raw=true"
        st.markdown(f'<video src="{video_url}" autoplay muted loop width="100%">', unsafe_allow_html=True)
        st.write("")
        st.image("https://github.com/BalaKrishnanCodeSpace/Phonepe_Pulse_Data_Extraction_-_Visualization/blob/main/Miscellaneous_Files/Know%20More%20About.JPG?raw=true")
        

if selected== "Data API's":
    col1,col2 = st.columns(2)
    
    # Column 1: Introduction
    with col1:
        st.write("")
        st.write("")
        st.title (":violet[Introduction]")
        st.markdown("""
                        - ##### **The Indian digital payments story has truly captured the world's imagination.**
                        - ##### **From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government.**
                        - ##### **Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India.**
                        - ##### **When we started, we were constantly looking for granular and definitive data sources on digital payments in India.**
                        - ##### **PhonePe Pulse is our way of giving back to the digital payments ecosystem.**
                """)
    
    # Add horizontal line
    st.write("""<hr style="height:3px;border:none;color:#6739b7;background-color:#6739b7;margin:0;padding:0;"/>""",unsafe_allow_html=True)

    st.title(":violet[GUIDE]")
    st.markdown("#### This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab.")
    
    st.subheader(":violet[1. Aggregated]")
    st.markdown("#####   Aggregated values of various payment categories as shown under Categories section")

    st.subheader(":violet[2. Map]")
    st.markdown("#####   Total values at the State and District levels")      

    st.subheader(":violet[3. Top]")
    st.markdown("#####   Totals of top States / Districts / Postal Codes")   

    # Column 2: Display PhonePe logo with a link
    with col2:
            img = "https://pbs.twimg.com/media/D4QJf0bUYAA-UL_.png"
            link = "https://www.phonepe.com/"
            st.markdown(f'<a href="{link}"><img src="{img}" style="max-width:100%; cursor:pointer;"></a>', unsafe_allow_html=True)
    #col3,col14,col5 = st.columns([5,1,1])
    
if selected == "Analysis":
    st.write("")
    st.write("")
    st.write("")
    mySqlConnection = connectToMySql()
    myCursor = mySqlConnection.cursor()
    myCursor.execute("""select concat(t.month,', ',t.year) as maxmonth from (select year, quarter, 
                    CASE
                    WHEN quarter = 1 then 'March'
                    WHEN quarter = 2 then 'June'
                    WHEN quarter = 3 then 'September'
                    else 'December'
                    end as 'month'
                    from aggTrans order by year desc, quarter desc LIMIT 1) as t;""")
    dataAvailableTill = myCursor.fetchone()[0]
    myCursor.execute("SELECT * FROM lastrefreshed")
    lastRefreshedOn = myCursor.fetchone()[0]
    lastRefreshedOn = lastRefreshedOn.strftime("%d-%m-%Y")
    col1,col2 = st.columns([11,3], gap="large")
    with col1:
        st.header(":violet[Analyse Phonepe pulse data]")
    with col2:
        st.write(f"<p style='font-size: 13px; color:#6739b7'><b><i>Data is available upto:</b> {dataAvailableTill}</p></i>", unsafe_allow_html=True)
        st.write(f"<p style='font-size: 13px; color:#6739b7'><b><i>Data last refreshed on:</b> {lastRefreshedOn}</p></i>", unsafe_allow_html=True)

  
    options = ["--select a query--",
        "1. Identify the top-performing states annually, based on transaction amounts.",
        "2. Evaluate the least-performing states based on both transaction type and volume.",
        "3. Analyze leading states categorized by transaction type and corresponding transaction count.",
        "4. Highlight top-performing States, Year and Pincode alongside their respective transaction values and registered user count.",
        "5. Discover districts with the lowest and highest transaction counts and amounts, considering both states and transaction volumes.",
        "6. Ascertain the least and most engaged registered users based on their districts and states.",
        "7. Mobile brands based on user percentage.",
        "8. Identify the top 10 pin codes based on transaction count and amount.",
        "9. What are the top 10 cities per pincode, considering the total number of registered users, categorized by state and year?",
        "10. What are the top 10 districts in terms of transaction count and amount, categorized by year?",
        "11. What are the top 10 districts in terms of App open count?"
    ]
    
    query = st.selectbox("Select the option",options)
 

    if query == "1. Identify the top-performing states annually, based on transaction amounts.":
        col1,col2 = st.columns([3,8], gap="large")
        with col1:
            options1 = ["All","2018","2019","2020","2021","2022","2023"]
            selected_year = st.selectbox("Select Year", options1)
        with col2:
            st.write("")
        
        if selected_year == "All":
            myCursor.execute('''
                SELECT State, Year, SUM(Transaction_amount) AS Transaction_amount
                from aggtrans 
                GROUP BY State, Year
                ORDER BY Transaction_amount DESC
                LIMIT 10'''
            )
            df = pd.DataFrame(myCursor.fetchall(),columns=['State','Year','Transaction Amount'])
            myCursor.close()
            mySqlConnection.close()
            df['Year'] = df['Year'].astype(str)
            fig = px.bar(df, x='State', y='Transaction Amount', color='Year', title='Top States by Transaction Amount')
            fig.update_layout(coloraxis_colorbar=dict(
                tickmode='linear',
                dtick=1
            ))
            col1,col2 = st.columns([3,3], gap="large")
            with col1:    
                df.index += 1
                df.index.name = 'S No.'
                st.write(df)
            with col2:
                st.plotly_chart(fig)
            st.write('#### :violet[Aggregated Transaction Data: ]')
            goldIcon = "🥇"
            silverIcon = "🥈"
            bronzeIcon = "🥉"
            st.write(f"<span style='color:purple'>{goldIcon} Among all the years <b>{df.iloc[0]['State']}</b> is in </span>"
                    f"<span style='color:goldenrod'><b>1st top</b></span>"
                    f"<span style='color:purple'> in the year {df.iloc[0]['Year']} with transaction amount {int(round(df.iloc[0]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)

            st.write(f"<span style='color:purple'>{silverIcon} Among all the years <b>{df.iloc[1]['State']}</b> is in </span>"
                    f"<span style='color:#C0C0C0'><b>2nd top</b></span>"
                    f"<span style='color:purple'> in the year {df.iloc[1]['Year']} with transaction amount {int(round(df.iloc[1]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)

            st.write(f"<span style='color:purple'>{bronzeIcon} Among all the years <b>{df.iloc[2]['State']}</b> is in </span>"
                    f"<span style='color:#CD7F32'><b>3rd top</b></span>"
                    f"<span style='color:purple'> in the year {df.iloc[2]['Year']} with transaction amount {int(round(df.iloc[2]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)

        else:
            myCursor.execute(f'''
                SELECT State, Year, SUM(Transaction_amount) AS Transaction_amount
                from aggtrans WHERE Year = {int(selected_year)}
                GROUP BY State, Year
                ORDER BY Transaction_amount DESC
                LIMIT 10'''
            )
            df = pd.DataFrame(myCursor.fetchall(),columns=['State','Year','Transaction Amount'])
            myCursor.close()
            mySqlConnection.close()
            df['Year'] = df['Year'].astype(str)
            fig = px.bar(df, x='State', y='Transaction Amount', color='Year', title='Top States by Transaction Amount')
            fig.update_layout(coloraxis_colorbar=dict(
                tickmode='linear',
                dtick=1
            ))
            col1,col2 = st.columns([3,3], gap="large")
            with col1:    
                df.index += 1
                df.index.name = 'S No.'
                st.write(df)
            with col2:
                st.plotly_chart(fig)
            goldIcon = "🥇"
            silverIcon = "🥈"
            bronzeIcon = "🥉"
            st.write('#### :violet[Aggregated Transaction Data Analysis: ]')
            st.write(f"<span style='color:purple'>{goldIcon} In the year {df.iloc[0]['Year']}, <b>{df.iloc[0]['State']}</b> is in </span>"
                    f"<span style='color:goldenrod'><b>1st top</b></span>"
                    f"<span style='color:purple'> with transaction amount {int(round(df.iloc[0]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)

            st.write(f"<span style='color:purple'>{silverIcon} In the year {df.iloc[1]['Year']}, <b>{df.iloc[1]['State']}</b> is in </span>"
                    f"<span style='color:#C0C0C0'><b>2nd top</b></span>"
                    f"<span style='color:purple'> with transaction amount {int(round(df.iloc[1]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)

            st.write(f"<span style='color:purple'>{bronzeIcon} In the year {df.iloc[2]['Year']}, <b>{df.iloc[2]['State']}</b> is in </span>"
                    f"<span style='color:#CD7F32'><b>3rd top</b></span>"
                    f"<span style='color:purple'> with transaction amount {int(round(df.iloc[2]['Transaction Amount']/1000000,0))} million</span>",
                    unsafe_allow_html=True)
            
    if query == "2. Evaluate the least-performing states based on both transaction type and volume.":
        col1,col2 = st.columns([3,8], gap="large")
        with col1:
            options1 = ["All","2018","2019","2020","2021","2022","2023"]
            selected_year = st.selectbox("Select Year", options1)
        with col2:
            st.write("")

        mySqlConnection = connectToMySql()
        myCursor = mySqlConnection.cursor()
        if selected_year == "All":
            myCursor.execute('''
                SELECT State, Year, SUM(Transaction_amount) AS Transaction_amount
                from aggtrans 
                GROUP BY State, Year
                ORDER BY Transaction_amount ASC
                LIMIT 10'''
            )
            df = pd.DataFrame(myCursor.fetchall(),columns=['State','Year','Transaction Amount'])
            myCursor.close()
            mySqlConnection.close()
            df['Year'] = df['Year'].astype(str)
            fig = px.bar(df, x='State', y='Transaction Amount', color='Year', title='Top States by Transaction Amount')
            fig.update_layout(coloraxis_colorbar=dict(
                tickmode='linear',
                dtick=1
            ))
            col1,col2 = st.columns([3,3], gap="large")
            with col1:    
                df.index += 1
                df.index.name = 'S No.'
                st.write(df)
            with col2:
                st.plotly_chart(fig)
            st.write('#### :violet[Aggregated Transaction Data: ]')
            st.write(f"► <span style='color:purple'>Among all the years {df.iloc[0]['State']} has recorded the lowest transaction amount among all states, with {int(round(df.iloc[0]['Transaction Amount']/1000000,0))} million (year {df.iloc[0]['Year']})</span>", unsafe_allow_html=True)
            st.write(f"► <span style='color:purple'>Among all the years {df.iloc[1]['State']} has recorded the second lowest transaction amount among all states, with {int(round(df.iloc[1]['Transaction Amount']/1000000,0))} million (year {df.iloc[1]['Year']})</span>", unsafe_allow_html=True)
            st.write(f"► <span style='color:purple'>Among all the years {df.iloc[2]['State']} has recorded the third lowest transaction amount among all states, with {int(round(df.iloc[2]['Transaction Amount']/1000000,0))} million (year {df.iloc[2]['Year']})</span>", unsafe_allow_html=True)

        else:
            myCursor.execute(f'''
                SELECT State, Year, SUM(Transaction_amount) AS Transaction_amount
                from aggtrans WHERE Year = {int(selected_year)}
                GROUP BY State, Year
                ORDER BY Transaction_amount ASC
                LIMIT 10'''
            )
            df = pd.DataFrame(myCursor.fetchall(),columns=['State','Year','Transaction Amount'])
            myCursor.close()
            mySqlConnection.close()
            df['Year'] = df['Year'].astype(str)
            fig = px.bar(df, x='State', y='Transaction Amount', color='Year', title='Top States by Transaction Amount')
            fig.update_layout(coloraxis_colorbar=dict(
                tickmode='linear',
                dtick=1
            ))
            col1,col2 = st.columns([3,3], gap="large")
            with col1:    
                df.index += 1
                df.index.name = 'S No.'
                st.write(df)
            with col2:
                st.plotly_chart(fig)
            st.write('#### :violet[Aggregated Transaction Data Analysis: ]')
            st.write(f"► <span style='color:purple'>In {df.iloc[0]['Year']}, {df.iloc[0]['State']} recorded the lowest transaction amount among all states, with {int(round(df.iloc[0]['Transaction Amount']/1000000,0))} million</span>", unsafe_allow_html=True)
            st.write(f"► <span style='color:purple'>In {df.iloc[1]['Year']}, {df.iloc[1]['State']} had the second lowest transaction amount after {df.iloc[0]['State']}, with {int(round(df.iloc[1]['Transaction Amount']/1000000,0))} million</span>", unsafe_allow_html=True)
            st.write(f"► <span style='color:purple'>In {df.iloc[2]['Year']}, {df.iloc[2]['State']} had the third lowest transaction amount after {df.iloc[1]['State']}, with {int(round(df.iloc[2]['Transaction Amount']/1000000,0))} million</span>", unsafe_allow_html=True)

    if query == "3. Analyze leading states categorized by transaction type and corresponding transaction count.":
        myCursor.execute('''
            SELECT State, Transaction_Type, SUM(Transaction_Count) AS Transaction_count
            FROM aggtrans
            GROUP BY State, Transaction_Type
            ORDER BY Transaction_Count DESC''')
        df = pd.DataFrame(myCursor.fetchall(), columns=['State', 'Transaction_Type', "Transaction_Count"])
        myCursor.close()
        mySqlConnection.close()

        # Filter by transaction type
        all_types = df['Transaction_Type'].unique()
        selected_types = st.multiselect('Select Transaction Types', all_types, default=all_types)

        # Filter by state
        all_states = df['State'].unique()
        selected_states = st.multiselect('Select States', all_states, default=all_states)

        filtered_df = df[df['Transaction_Type'].isin(selected_types) & df['State'].isin(selected_states)]
        filtered_df.reset_index(drop=True, inplace=True)
        filtered_df.index += 1
        col1, col2 = st.columns(2)
        with col1:
            filtered_df.index.name = 'S No.'
            st.write(filtered_df)
        with col2:
            fig = px.line(filtered_df, x='State', y='Transaction_Count', color='Transaction_Type',
                        title='Transaction Type Distribution by State')
            st.plotly_chart(fig)
        st.write('#### :violet[Aggregated Transaction Data Analysis: ]')
        st.write(f"► <span style='color:purple'>{df.iloc[0]['State']} state recorded top in {df.iloc[0]['Transaction_Type']} transaction type with count of {int(round(df.iloc[0]['Transaction_Count']/1000000,0))} million</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[1]['State']} state recorded second top in {df.iloc[1]['Transaction_Type']} transaction type with count of {int(round(df.iloc[1]['Transaction_Count']/1000000,0))} million</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[2]['State']} state recorded third top in {df.iloc[1]['Transaction_Type']} transaction type with count of {int(round(df.iloc[2]['Transaction_Count']/1000000,0))} million</span>", unsafe_allow_html=True)



    if query == "4. Highlight top-performing States, Year and Pincode alongside their respective transaction values and registered user count.":
        myCursor.execute('''
                        WITH toptrans_topuser
                        AS
                        (
                            SELECT tt.State, tt.Year, tt.Quarter, tt.pincode, cast(tt.Transaction_Count as unsigned) AS Transaction_Count,
                            cast(tt.Transaction_Amount as unsigned) AS Transaction_Amount, tu.Registered_User FROM toptrans tt JOIN topuser tu ON 
                            tt.State = tu.State AND tt.Year = tu.Year AND tt.Quarter = tu.Quarter AND tt.pincode=tu.pincode ORDER BY Transaction_Count DESC
                        )
                        SELECT State, Year, Pincode, (sum(Transaction_Amount)/1000000) AS Transaction_Amount, SUM(Registered_User) AS Registered_User FROM toptrans_topuser GROUP BY State, Year, Pincode ORDER BY Transaction_Amount DESC LIMIT 10;'''
        )
        df = pd.DataFrame(myCursor.fetchall(),columns = ["State", "Year", "Pincode", "Transaction Amount (In Millions)", "Registered User"])
        myCursor.close()
        mySqlConnection.close()
        df.index += 1
        df.index.name = 'S No.'

        col1, col2 = st.columns([3,3], gap="large")
        with col1:
            st.write(df)
        with col2:
            fig1 = px.pie(df, names='State', values='Transaction Amount (In Millions)', title='Top States by Transaction Amount')
            fig2 = px.pie(df, names='State', values='Registered User', title='Top States by Registered User')
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)


    if query == "5. Discover districts with the lowest and highest transaction counts and amounts, considering both states and transaction volumes.":
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        selection = st.radio("Select criteria:", ("Lowest", "Highest"))
        if selection == "Highest":
            transaction_function = "MAX"
            transaction_function1 = "highest"
            order_by = "DESC"
        else:
            transaction_function = "MIN"
            transaction_function1 = "lowest"
            order_by = "ASC"
        myCursor.execute(f'''
        SELECT State, District, {transaction_function}(Transaction_Count) AS Transaction_Count, {transaction_function}(Transaction_Amount) AS Transaction_Amount
        FROM maptrans 
        GROUP BY State, District 
        ORDER BY Transaction_Count {order_by}, Transaction_Amount {order_by}
        LIMIT 10'''
        )
        df = pd.DataFrame(myCursor.fetchall(),columns=['State',"District","Transaction Count","Transaction Amount"])
        myCursor.close()
        mySqlConnection.close()

        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:

            st.write(df)
        with col2:        

            fig = px.bar(df, x='State', y=['Transaction Count','Transaction Amount'], color='District', title=f'Districts with {selection} Transaction Count and Amounts')
            st.plotly_chart(fig)
        st.write('#### :violet[Map Transaction Data Analysis: ]')
        st.write(f"► <span style='color:purple'>{df.iloc[0]['District']} in {df.iloc[0]['State']} state recorded {transaction_function1} with transaction count of {df.iloc[0]['Transaction Count']} and transaction amount of {'{:.2f}'.format(df.iloc[0]['Transaction Amount']/1000000) if df.iloc[0]['Transaction Amount'] >= 1000000 else df.iloc[0]['Transaction Amount']} million</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[1]['District']} in {df.iloc[1]['State']} state recorded 2nd {transaction_function1} with transaction count of {df.iloc[1]['Transaction Count']} and transaction amount of {'{:.2f}'.format(df.iloc[1]['Transaction Amount']/1000000) if df.iloc[1]['Transaction Amount'] >= 1000000 else df.iloc[1]['Transaction Amount']} million</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[2]['District']} in {df.iloc[2]['State']} state recorded 3rd {transaction_function1} with transaction count of {df.iloc[2]['Transaction Count']} and transaction amount of {'{:.2f}'.format(df.iloc[2]['Transaction Amount']/1000000) if df.iloc[2]['Transaction Amount'] >= 1000000 else df.iloc[2]['Transaction Amount']} million</span>", unsafe_allow_html=True)

    if query == "6. Ascertain the least and most engaged registered users based on their districts and states.":
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        selection = st.radio("Select criteria:", ("Lowest", "Highest"))
        if selection == "Highest":
            transaction_function = "MAX"
            transaction_function1 = "highest"
            order_by = "DESC"
        else:
            transaction_function = "MIN"
            transaction_function1 = "lowest"
            order_by = "ASC"

        myCursor.execute(f'''
        SELECT State, District, {transaction_function}(RegisteredUsers) As Registered_Users
        FROM mapuser
        GROUP BY State, District
        ORDER BY Registered_Users {order_by}
        LIMIT 10''')
        df = pd.DataFrame(myCursor.fetchall(), columns=["State", "District", "Registered Users"])
        myCursor.close()
        mySqlConnection.close()

        df['Registered Users'] = pd.to_numeric(df['Registered Users'])

        df.index += 1
        df.index.name = 'S No.'

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            fig = px.bar(df, x='State', y='Registered Users', color='District', title=f'{transaction_function1.capitalize()}-Engaged Registered Users')
            st.plotly_chart(fig)
        st.write('#### :violet[Map User Data Analysis: ]')
        st.write(f"► <span style='color:purple'>{df.iloc[0]['District']} in {df.iloc[0]['State']} state recorded {transaction_function1} with registered users count of {df.iloc[0]['Registered Users']}</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[1]['District']} in {df.iloc[1]['State']} state recorded 2nd {transaction_function1} with registered users count of {df.iloc[1]['Registered Users']}</span>", unsafe_allow_html=True)
        st.write(f"► <span style='color:purple'>{df.iloc[2]['District']} in {df.iloc[2]['State']} state recorded 3rd {transaction_function1} with registered users count of {df.iloc[2]['Registered Users']}</span>", unsafe_allow_html=True)

    if query == "7. Mobile brands based on user percentage.":
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        selection = st.radio("Select:", ("All", "Highest", "Lowest"), key='select', 
                         help="Select option for limiting the number of records")
    
        if selection != "All":
            cola,colb,colc = st.columns([5,5,5])
            with cola:
                limit = st.text_input("Enter limit number:", key='limit', 
                                    help="Enter the number of records to display")

        if selection == "All":
            limit_clause = ""
            selection_text = "All"
        else:
            if limit:
                limit_clause = f"LIMIT {int(limit)}"
            else:
                limit_clause = ""

            if selection == "Highest":
                order_by = "DESC"
                selection_text = "Highest"
            else:
                order_by = "ASC"
                selection_text = "Lowest"

            limit_clause = f"ORDER BY User_Count {order_by} {limit_clause}"


        myCursor.execute(f'''
            SELECT State, Year, Brand_Name, User_Count, User_Percentage
            FROM agguser {limit_clause}''')
        df = pd.DataFrame(myCursor.fetchall(),columns=['State',"Year","Brand Name","User Count","User Percentage"])
        myCursor.close()
        mySqlConnection.close()
        df['User Count'] = df['User Count'].astype(int)  # Convert User Count to int
        df['Year'] = df['Year'].astype(str)
        df['User Percentage'] = df['User Percentage'].astype(float)
        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            fig = px.scatter(df, x='State', y='User Count', size='User Percentage',
                            color='Brand Name', title=f'Mobile Brands in {selection_text} {limit if selection!="All" else ""} category')
            st.plotly_chart(fig)

    if query == "8. Identify the top 10 pin codes based on transaction count and amount.":
        myCursor.execute('''SELECT tt.State, tt.Year, p.City, tt.Pincode, sum(CAST(tt.Transaction_Count AS UNSIGNED)) AS Transaction_Count, 
                            (sum(tt.Transaction_Amount)/1000000) FROM phonepe_pulse.TopTrans tt JOIN (SELECT DISTINCT Pincode, City FROM pincode.pincode) p 
                            ON tt.Pincode = p.Pincode GROUP BY tt.State, tt.Year, p.City, tt.Pincode ORDER BY Transaction_Count DESC LIMIT 10
        ''')
        df = pd.DataFrame(myCursor.fetchall(),columns=["State", "Year", "City", "Pincode", "Transaction Count", "Transaction Amount (In Million)"])
        myCursor.close()
        mySqlConnection.close()
        df['Year'] = df['Year'].astype(str)
        df['Pincode'] = df['Pincode'].astype(str)
        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            df['Transaction Count'] = df['Transaction Count'].astype(int)
            fig = px.scatter(df, x='Pincode', y='Transaction Amount (In Million)', size='Transaction Count',
                            color='City', title="Pincode wise Top Transaction")
            st.plotly_chart(fig)


    if query == "9. What are the top 10 cities per pincode, considering the total number of registered users, categorized by state and year?":
        myCursor.execute('''SELECT tu.State, tu.Year, p.City, tu.Pincode, SUM(tu.Registered_User) AS Total_Registered_Users
                            FROM TopUser tu
                            JOIN (SELECT DISTINCT Pincode, City FROM pincode.pincode) p ON tu.Pincode = p.Pincode
                            GROUP BY tu.State, tu.Year, p.City, tu.Pincode
                            ORDER BY Total_Registered_Users DESC
                            LIMIT 10
        ''')
        df = pd.DataFrame(myCursor.fetchall(),columns=["State", "Year", "City", "Pincode", "Registered User"])
        myCursor.close()
        mySqlConnection.close()
        df['Year'] = df['Year'].astype(str)
        df['Pincode'] = df['Pincode'].astype(str)
        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            fig = px.bar(df, x='Pincode', y='Registered User',
                            color='City', title="Top 10 Pincode wise Registered Users")
            st.plotly_chart(fig)

    if query == "10. What are the top 10 districts in terms of transaction count and amount, categorized by year?":
        myCursor.execute('''SELECT Year, District, SUM(Transaction_Count) AS Total_Transaction_Count, SUM(Transaction_Amount) AS Total_Transaction_Amount
                        FROM maptrans GROUP BY Year, District ORDER BY Year, Total_Transaction_Count DESC, Total_Transaction_Amount DESC limit 10;
        ''')
        df = pd.DataFrame(myCursor.fetchall(),columns=["Year", "District", "Transaction Count", "Transaction Amount"])
        myCursor.close()
        mySqlConnection.close()
        df['Year'] = df['Year'].astype(str)
        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            fig = px.bar(df, x='District', y='Transaction Amount',
                             title="Top 10 District in year wise Registered Users")
            st.plotly_chart(fig)


    if query == "11. What are the top 10 districts in terms of App open count?":
        myCursor.execute('''SELECT State, District, Year, SUM(AppOpens) AS AppOpens FROM mapuser
                         GROUP BY State, District, Year ORDER BY AppOpens DESC LIMIT 10''')
        df = pd.DataFrame(myCursor.fetchall(),columns=["State", "District", "Year", "App Open Count"])
        myCursor.close()
        mySqlConnection.close()
        df['Year'] = df['Year'].astype(str)
        df.index += 1
        df.index.name = 'S No.'

        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:        
            fig = px.bar(df, x='District', y='App Open Count', color = 'Year',
                             title="Top 10 District in year wise App Open Count",
                             labels={'District': 'District', 'App Open Count': 'App Open Count', 'Year': 'Year'},
                     color_discrete_sequence=px.colors.qualitative.Set1)
            st.plotly_chart(fig)



    
if selected == "Explore Data":
    df_aggTrans, df_aggUser, df_mapTrans, df_mapUser, df_topTrans, df_topUser = dataFrameLoader()
    st.write("")
    st.write("")
    st.write("")
    col1,col2,col3,col4,col5 = st.columns([3,3,3,6,3])
    
    with col1:
        with st.container():
            analyser = st.selectbox(
                '**Choose the Analyzer**',
                options=["Transactions", "Users"],
                index=0,
            )
    with col2:
        Year = st.selectbox(
            '**Choose the Year**',
            ('2018', '2019', '2020', '2021', '2022', '2023'),
            key='side1'
        )
    with col3:
        Quarter = st.selectbox(
            '**Choose the Quarter**',
            ('Q1 (Jan - Mar)', 'Q2 (Apr - Jun)', 'Q3 (Jul - Sep)', 'Q4 (Oct - Dec)'),
            key='side2'
        )
    with col4:
        State = st.selectbox(
            '**Choose the State**',
            (
                'All', 'Andhra Pradesh', 'Arunachal Pradesh', 
                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadara & Nagar Havelli', 
                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 
                'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
                'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 
                'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman & Nicobar Island'
            ),
            key='side3'
        )
    with col5:
        colorScales = [
                        "Inferno", "Plasma", "Magma", "Turbo", "Cividis",
                        "Rainbow", "Portland", "Jet", "Hot", "Cool", "Electric",
                        "Picnic", "Blackbody", "Earth", "YlOrRd", "YlOrBr", "YlGnBu",
                        "YlGn", "Reds", "RdBu", "PuRd", "PuBuGn", "PuBu", "OrRd", "Oranges",
                        "Inferno", "Greys", "Greens", "GnBu", "BuPu", "BuGn", "Blues", "Viridis"
                    ]
        desiredColorScale = st.selectbox("**Choose Color Scale for the map**", colorScales)

    subcol1,subcol2,subcol3 = st.columns([4.5,3,10])
    with subcol1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(
            """
            <style>
            .purple-container {
                background-color: #372961; /* Purple color */
                padding: 20px;
                margin-bottom: 100px;
                color: white;
                width: 400px;
                height: 623px;
                overflow: hidden; /* Hide overflow content */
            }
            .purple-header {
                margin-bottom: 10px; /* Add margin to separate header and content */
            }
            .purple-scrollable {
                max-height: 450px; /* Adjust max height for scrolling area */
                overflow-y: auto; /* Enable vertical scrolling */
            }
            .purple-scrollable::-webkit-scrollbar {
                display: none; /* Hide scrollbar for Chrome/Safari/Opera */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        
        qtr = int(Quarter[1])
        if analyser == "Transactions":
            if State == 'All':
                filteredDfAggTrans = df_aggTrans[
                    (df_aggTrans['Year'] == int(Year)) &
                    (df_aggTrans['Quarter'] == qtr)            
                ]
                filteredDfMapTrans = df_mapTrans[
                    (df_mapTrans['Year'] == int(Year)) &
                    (df_mapTrans['Quarter'] == qtr)
                ]
                filteredDftopTrans = df_topTrans[
                    (df_topTrans['Year'] == int(Year)) &
                    (df_topTrans['Quarter'] == qtr)
                ]
                
                filteredDfAggTrans = filteredDfAggTrans.groupby(['Year', 'Quarter','Transaction Type'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfAggTrans = filteredDfAggTrans.sort_values(by='Transaction Amount', ascending=False)
                filteredDfMapTrans = filteredDfMapTrans.groupby(['Year','Quarter','District'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfMapTrans = filteredDfMapTrans.sort_values(by = 'Transaction Amount', ascending = False)
                filteredDfTopTrans = filteredDftopTrans.groupby(['Year', 'Quarter','Pincode'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfTopTrans =  filteredDfTopTrans.sort_values(by = 'Transaction Amount', ascending = False)

                
            else:
                filteredDfAggTrans = df_aggTrans[
                    (df_aggTrans['Year'] == int(Year)) &
                    (df_aggTrans['State'] == State) &
                    (df_aggTrans['Quarter'] == qtr)            
                ]
                filteredDfMapTrans = df_mapTrans[
                    (df_mapTrans['Year'] == int(Year)) &
                    (df_mapTrans['Quarter'] == qtr) &
                    (df_mapTrans['State'] == State)
                ]
                filteredDfTopTrans = df_topTrans[
                    (df_topTrans['Year'] == int(Year)) &
                    (df_topTrans['Quarter'] == qtr) &
                    (df_topTrans['State'] == State)
                ]

                filteredDfAggTrans = filteredDfAggTrans.groupby(['Year', 'State', 'Quarter', 'Transaction Type'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfAggTrans = filteredDfAggTrans.sort_values(by='Transaction Amount', ascending=False)
                filteredDfMapTrans = filteredDfMapTrans.groupby(['Year','State', 'Quarter','District'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfMapTrans = filteredDfMapTrans.sort_values(by = 'Transaction Amount', ascending = False)
                filteredDfTopTrans = filteredDfTopTrans.groupby(['Year','State', 'Quarter','Pincode'])['Transaction Amount'].sum().reset_index()
                sortedfilteredDfTopTrans =  filteredDfTopTrans.sort_values(by = 'Transaction Amount', ascending = False)

            totalTransactionAmount = filteredDfAggTrans['Transaction Amount'].sum()
            totalTransactionAmount = int(totalTransactionAmount)
            formatted_amount = indianNumberFormat(totalTransactionAmount)
            try:
                st.markdown(f"""
                    <div class='purple-container'> 
                        <div class='purple-header'>
                            <strong style='font-size: 28px; color: #05C3DE;'> {analyser} </strong> <br><br>
                            All Phonepe transactions (UPI + Cards + Wallets)</br> <strong style='font-size: 40px; color: #05C3DE;'> {formatted_amount} </strong>
                            </br><hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                        </div>
                        <div class='purple-scrollable'>
                            <strong style='font-size: 28px; color: #fafcfa;'> Categories </strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfAggTrans.iloc[0]['Transaction Type']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfAggTrans.iloc[0]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfAggTrans.iloc[1]['Transaction Type']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfAggTrans.iloc[1]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfAggTrans.iloc[2]['Transaction Type']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfAggTrans.iloc[2]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfAggTrans.iloc[3]['Transaction Type']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfAggTrans.iloc[3]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfAggTrans.iloc[4]['Transaction Type']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfAggTrans.iloc[4]['Transaction Amount'])/10000000)} Cr</strong></br>
                            <hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                            <strong style='font-size: 28px; color: #fafcfa;'>Top 10 Districts</strong></br></br> 
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[0]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[0]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[1]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[1]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[2]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[2]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[3]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[3]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[4]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[4]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[5]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[5]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[6]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[6]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[7]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[7]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[8]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[8]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapTrans.iloc[9]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfMapTrans.iloc[9]['Transaction Amount'])/10000000)} Cr</strong></br>
                            <hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                            <strong style='font-size: 28px; color: #fafcfa;'>Top 10 Postal Codes</strong></br></br> 
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[0]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[0]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[1]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[1]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[2]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[2]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[3]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[3]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[4]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[4]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[5]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[5]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[6]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[6]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[7]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[7]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[8]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[8]['Transaction Amount'])/10000000)} Cr</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopTrans.iloc[9]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #05C3DE;'>{indianNumberFormat(int(sortedfilteredDfTopTrans.iloc[9]['Transaction Amount'])/10000000)} Cr</strong>
                            </br>
                            </br>
                            </br>
                            </br>
                            </br>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True)
            except:
                st.markdown(f"""
                    <div class='purple-container'> 
                        <div class='purple-header'>
                            <strong style='font-size: 28px; color: #05C3DE;'> {analyser} </strong> <br><br>
                            All Phonepe transactions (UPI + Cards + Wallets)</br> <strong style='font-size: 40px; color: #05C3DE;'> {formatted_amount} </strong>
                            </br><hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True)
        else:
            if State == 'All':
                filteredDfAggUser = df_aggUser[
                    (df_aggUser['Year'] == int(Year)) &
                    (df_aggUser['Quarter'] == qtr)            
                ]
                filteredDfMapUser = df_mapUser[
                    (df_mapUser['Year'] == int(Year)) &
                    (df_mapUser['Quarter'] == qtr)
                ]
                filteredDftopUser = df_topUser[
                    (df_topUser['Year'] == int(Year)) &
                    (df_topUser['Quarter'] == qtr)
                ]
                
                filteredDfAggUser = filteredDfAggUser.groupby(['Year', 'Quarter'])['User Count'].sum().reset_index()
                sortedfilteredDfAggUser = filteredDfAggUser.sort_values(by='User Count', ascending=False)
                filteredDfMapUser = filteredDfMapUser.groupby(['Year','Quarter','District'])['Registered Users'].sum().reset_index()
                sortedfilteredDfMapUser = filteredDfMapUser.sort_values(by = 'Registered Users', ascending = False)
                filteredDfTopUser = filteredDftopUser.groupby(['Year', 'Quarter','Pincode'])['Registered Users'].sum().reset_index()
                sortedfilteredDfTopUser =  filteredDfTopUser.sort_values(by = 'Registered Users', ascending = False)
            else:
                filteredDfAggUser = df_aggUser[
                    (df_aggUser['Year'] == int(Year)) &
                    (df_aggUser['State'] == State) &
                    (df_aggUser['Quarter'] == qtr)            
                ]
                filteredDfMapUser = df_mapUser[
                    (df_mapUser['Year'] == int(Year)) &
                    (df_mapUser['Quarter'] == qtr) &
                    (df_mapUser['State'] == State)
                ]
                filteredDfTopUser = df_topUser[
                    (df_topUser['Year'] == int(Year)) &
                    (df_topUser['Quarter'] == qtr) &
                    (df_topUser['State'] == State)
                ]
                filteredDfAggUser = filteredDfAggUser.groupby(['Year', 'State', 'Quarter'])['User Count'].sum().reset_index()
                sortedfilteredDfAggUser = filteredDfAggUser.sort_values(by='User Count', ascending=False)
                filteredDfMapUser = filteredDfMapUser.groupby(['Year','State', 'Quarter','District'])['Registered Users'].sum().reset_index()
                sortedfilteredDfMapUser = filteredDfMapUser.sort_values(by = 'Registered Users', ascending = False)
                filteredDfTopUser = filteredDfTopUser.groupby(['Year','State', 'Quarter','Pincode'])['Registered Users'].sum().reset_index()
                sortedfilteredDfTopUser =  filteredDfTopUser.sort_values(by = 'Registered Users', ascending = False)

            totalTransactionAmount = filteredDfAggUser['User Count'].sum()
            totalTransactionAmount = int(totalTransactionAmount)
            formatted_amount = indianNumberFormat(totalTransactionAmount)

            try:
                st.markdown(f"""
                    <div class='purple-container'> 
                        <div class='purple-header'>
                            <strong style='font-size: 28px; color: #C98BDB;'> {analyser} </strong> <br><br>
                            Registered PhonePe users during {Year} {Quarter}</br> <strong style='font-size: 40px; color: #C98BDB;'> {formatted_amount} </strong>
                            </br><hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                        </div>
                        <div class='purple-scrollable'>
                            <strong style='font-size: 28px; color: #fafcfa;'>Top 10 Districts</strong></br></br> 
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[0]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[0]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[1]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[1]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[2]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[2]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[3]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[3]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[4]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[4]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[5]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[5]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[6]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[6]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[7]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[7]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[8]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[8]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfMapUser.iloc[9]['District']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfMapUser.iloc[9]['Registered Users']))}</strong></br>
                            <hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                            <strong style='font-size: 28px; color: #fafcfa;'>Top 10 Postal Codes</strong></br></br> 
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[0]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[0]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[1]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[1]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[2]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[2]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[3]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[3]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[4]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[4]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[5]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[5]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[6]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[6]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[7]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[7]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[8]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[8]['Registered Users']))}</strong></br></br>
                            <strong style='font-size: 16px; color: #fafcfa;'>{sortedfilteredDfTopUser.iloc[9]['Pincode']}</strong>: {"⠀" * 3}<strong style='font-size: 25px; color: #C98BDB;'>{indianNumberFormat(int(sortedfilteredDfTopUser.iloc[9]['Registered Users']))}</strong>
                            </br>
                            </br>
                            </br>
                            </br>
                            </br>
                            </br>   
                            </br>   
                            </br>   
                        </div>
                    </div>
                """,
                unsafe_allow_html=True)
            except:
                st.markdown(f"""
                    <div class='purple-container'> 
                        <div class='purple-header'>
                            <strong style='font-size: 28px; color: #C98BDB;'> {analyser} </strong> <br><br>
                            Registered PhonePe users during {Year} {Quarter}</br> <strong style='font-size: 40px; color: #C98BDB;'> {formatted_amount} </strong>
                            </br><hr style='height:1px;border:none;color:#e4f0e4;background-color:#fcfcfc;width:8.43cm;margin:0;padding:0;opacity:0.3;'/>
                            </br>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True)

    with subcol2:
        st.write()
    with subcol3:
        indianstate = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        if State == "All":
            if analyser == "Transactions":
                result_df = df_aggTrans[(df_aggTrans['Year'] == int(Year)) & (df_aggTrans['Quarter'] == qtr)].groupby(['State', 'Quarter']).agg({
                    'Transaction Amount': ['mean', 'sum'],
                    'Transaction Count': 'sum'
                }).reset_index()
                result_df.columns = ['State',"Quarter", 'Avg_transaction_amount', 'Total_transaction_amount', 'Total_transaction_count']
                base_map = go.Figure()
                base_map.update_layout(
                mapbox=dict(
                    style="carto-positron",
                    center=dict(lat=23, lon=83),
                    zoom=3.5,
                    bearing=0,
                    pitch=0,
                ),
                width = 650,
                height = 800 )

                # Create choropleth figure with go
                choropleth_map = go.Figure()
                hover_text = (
                    result_df['State'] + '<br>' + 
                    'Transactions Amount: ' + (result_df['Total_transaction_amount'] // 1000000).astype(str) + 'M' + '</br>' +
                    'Avg_transaction_amount: ' + (result_df['Avg_transaction_amount'] // 1000000).astype(str) + 'M' +
                    '<br>Transactions Count: ' + result_df['Total_transaction_count'].astype(str)
                )
                # indianstate = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(indianstate)   
                choropleth_map.add_trace(go.Choroplethmapbox(
                geojson = indianstate,
                locations=result_df['State'],
                z=result_df['Total_transaction_amount'],
                featureidkey="properties.ST_NM",
                colorscale = desiredColorScale,
                colorbar=dict(title="Total Transactions"),
                hovertext=hover_text,
                ))
                # Overlay choropleth map on base map
                base_map.add_trace(choropleth_map.data[0])


                # Show the combined map
                st.plotly_chart(base_map)
            else:
                result_df = df_aggUser[(df_aggUser['Year'] == int(Year)) & (df_aggUser['Quarter'] == qtr)].groupby(['State', 'Quarter']).agg({
                    'User Count': 'sum',
                    'User Percentage': 'sum'
                }).reset_index()
                result_df.columns = ['State',"Quarter", 'User Count', 'User Percentage']
                base_map = go.Figure()
                base_map.update_layout(
                mapbox=dict(
                    style="carto-positron",
                    center=dict(lat=23, lon=83),
                    zoom=3.5,
                    bearing=0,
                    pitch=0,
                ),
                width = 650,
                height = 800 )

                # Create choropleth figure with go
                choropleth_map = go.Figure()
                hover_text = (
                    result_df['State'] + '<br>' + 
                    'User Count: ' + (result_df['User Count'] // 1000).astype(str) + 'K' + '</br>' +
                    'User Percentage: ' + result_df['User Percentage'].astype(str)
                )
                # indianstate = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(indianstate)   
                choropleth_map.add_trace(go.Choroplethmapbox(
                geojson = indianstate,
                locations=result_df['State'],
                z=result_df['User Count'],
                featureidkey="properties.ST_NM",
                colorscale = desiredColorScale,
                colorbar=dict(title="Total User"),
                hovertext=hover_text,
                ))
                base_map.add_trace(choropleth_map.data[0])
                st.plotly_chart(base_map)
        else:
            if analyser == "Transactions":
                result_df = df_aggTrans[(df_aggTrans['Year'] == int(Year)) & (df_aggTrans['Quarter'] == qtr) & (df_aggTrans['State'] == State)].groupby(['State', 'Quarter']).agg({
                    'Transaction Amount': ['mean', 'sum'],
                    'Transaction Count': 'sum'
                }).reset_index()
                result_df.columns = ['State',"Quarter", 'Avg_transaction_amount', 'Total_transaction_amount', 'Total_transaction_count']
                base_map = go.Figure()
                base_map.update_layout(
                mapbox=dict(
                    style="carto-positron",
                    center=dict(lat=23, lon=83),
                    zoom=3.5,
                    bearing=0,
                    pitch=0,
                ),
                width = 650,
                height = 800 )

                choropleth_map = go.Figure()
                hover_text = (
                    result_df['State'] + '<br>' + 
                    'Transactions Amount: ' + (result_df['Total_transaction_amount'] // 1000000).astype(str) + 'M' + '</br>' +
                    'Avg_transaction_amount: ' + (result_df['Avg_transaction_amount'] // 1000000).astype(str) + 'M' +
                    '<br>Transactions Count: ' + result_df['Total_transaction_count'].astype(str)
                )
                # indianstate = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(indianstate)   
                choropleth_map.add_trace(go.Choroplethmapbox(
                geojson = indianstate,
                locations=result_df['State'],
                z=result_df['Total_transaction_amount'],
                featureidkey="properties.ST_NM",
                colorscale = desiredColorScale,
                colorbar=dict(title="Total Transactions"),
                hovertext=hover_text,
                ))
                base_map.add_trace(choropleth_map.data[0])
                st.plotly_chart(base_map)
            else:
                result_df = df_aggUser[(df_aggUser['Year'] == int(Year)) & (df_aggUser['Quarter'] == qtr) & (df_aggUser['State'] == State)].groupby(['State', 'Quarter']).agg({
                    'User Count': 'sum',
                    'User Percentage': 'sum'
                }).reset_index()
                result_df.columns = ['State',"Quarter", 'User Count', 'User Percentage']
                base_map = go.Figure()
                base_map.update_layout(
                mapbox=dict(
                    style="carto-positron",
                    center=dict(lat=23, lon=83),
                    zoom=3.5,
                    bearing=0,
                    pitch=0,
                ),
                width = 650,
                height = 800 )

                # Create choropleth figure with go
                choropleth_map = go.Figure()
                hover_text = (
                    result_df['State'] + '<br>' + 
                    'User Count: ' + (result_df['User Count'] // 1000).astype(str) + 'K' + '</br>' +
                    'User Percentage: ' + result_df['User Percentage'].astype(str)
                )
                # indianstate = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(indianstate)   
                choropleth_map.add_trace(go.Choroplethmapbox(
                geojson = indianstate,
                locations=result_df['State'],
                z=result_df['User Count'],
                featureidkey="properties.ST_NM",
                colorscale = desiredColorScale,
                colorbar=dict(title="Total User"),
                hovertext=hover_text,
                ))
                # Overlay choropleth map on base map
                base_map.add_trace(choropleth_map.data[0])
                # Show the combined map
                st.plotly_chart(base_map)


            

if selected == "Contact Us":
    col1, col2 = st.columns([6,5])
    with col1:
        st.write('')
        st.write('')
        st.header(":violet[Contact Us]")
        st.write('')
        st.subheader('*:red[Balakrishnan Ravikumar]*')
        st.write('*:red[Mylapore, Chennai, Tamil Nadu, India]*')
        st.write('')
        st.write('')
        st.markdown('<img src="https://static-00.iconduck.com/assets.00/linkedin-icon-1024x1024-net2o24e.png" width="25" height="25">&nbsp;&nbsp;[Click here to visit our LinkedIn page](https://www.linkedin.com/in/balakrishnan-ravikumar-8790732b6/)', unsafe_allow_html=True)
        st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="25" height="25">&nbsp;&nbsp;[Click here to visit our Github page](https://github.com/BalaKrishnanCodeSpace)', unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.markdown("<iframe src='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3890.3743995180666!2d80.26730301482026!3d13.032550190796538!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5266b6f4de2397%3A0x39d2ffdb6a48ec92!2sThirumayilai%2C%20Mylapore%2C%20Chennai%2C%20Tamil%20Nadu%2C%20India!5e0!3m2!1sen!2sca!4v1647159863087!5m2!1sen!2sca' width='600' height='450' style='border:0;' allowfullscreen='' loading='lazy'></iframe>", unsafe_allow_html=True)
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        
        # Function to validate email format
        def is_valid_email(email):
            # check for '@' and '.com' in email 
            if "@" in email and ".com" in email:
                return True # Return True if conditions met
            return False    # Return False otherwise

        
        # Function to validate phone number format
        def is_valid_phone(phone_number):
            # Check if only digits and length is 10
            if phone_number.isdigit() and len(phone_number) == 10:
                return True # Return True if conditions met
            return False    # Return False otherwise
                
        
        st.write("**_:violet[Please fill out the form below to contact us.]_**")
        name = st.text_input("**Name**")
        email = st.text_input("**Email ID**")
        phone_number = st.text_input("**Phone Number**")
        remarks = st.text_area("**Remarks**")
        
        if st.button("Submit"):
            if name.strip() == "":
                st.error("Please enter your name.")
            elif email.strip() == "":
                st.error("Please enter your email ID.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email ID.")
            elif phone_number.strip() == "":
                st.error("Please enter your phone number.")
            elif not is_valid_phone(phone_number):
                st.error("Please enter a valid phone number.")
            else:
                st.success("Your details have been submitted successfully!")