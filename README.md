
![PhonePe Logo](https://mma.prnewswire.com/media/1832286/PhonePe_Logo.jpg?p=twitter)
</br>
</br>

# $${\color{#6739b7}Phonepe \space Pulse \space - Data \space Visualization \space and \space Exploration}$$

### <div align="center"><strong>A User-Friendly Tool Using Streamlit and Plotly</strong></div>


# Introduction
> The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.
</br>


### Table of Contents

- [Overview](#overview)
- [Developer Guide](#developer-guide)
- [User Guide](#user-guide)
- [Conclusion](#conclusion)

</br>

___
# Overview
The PhonePe Pulse Data Visualization and Exploration project is a robust system aimed at enabling the effortless extraction, storage, and analysis of PhonePe Pulse data. Utilizing cutting-edge technologies like SQL, Streamlit, Plotly this project provides users with the capability to efficiently explore and analyze PhonePe Pulse data for actionable insights. This project comprises the following key components:

### 1. Streamlit Application

⠀⠀Built with Streamlit, the application provides an intuitive interface for users to explore and visualize PhonePe Pulse data effortlessly. ⠀⠀Streamlit's interactive widgets enhance the user experience, making data analysis seamless and efficient.

### 2. MySQL Database
⠀⠀MySQL serves as the backbone for storing PhonePe Pulse data securely and efficiently. Data is stored in structured tables within the MySQL ⠀⠀database, facilitating seamless data retrieval and analysis through SQL queries.

### 3. Interactive Data Exploration
⠀⠀Users can interactively explore PhonePe Pulse data using Streamlit's widgets and Plotly visualizations. The application enables users to filter, ⠀⠀group, and analyze data based on various parameters, empowering them to derive actionable insights from the data.

### 4. Data Visualization with Plotly
⠀⠀Plotly is employed to create interactive and visually engaging plots, charts, and maps to visualize PhonePe Pulse data. Users can gain ⠀⠀valuable insights into transaction trends, user behavior, and geographical distribution through Plotly's dynamic visualization features.
</br>
</br>
___
# Developer Guide  
### 1. Tools Installation
   * Visual Studio Code (or other IDE's)
   * Python 3.11.0 or higher
   * MySQL
</br>

### 2. Required Libraries Installation in Visual Studio Code
```python
pip install mysql-connector-python
```
```python
pip install pandas
```
```python
pip install streamlit
```
```python
pip install streamlit_option_menu
```
```python
pip install plotly
```
```python
pip install requests
```
</br>


### 3. Import Libraries
```python
# Pandas library
import pandas as pd

# Dashboard library
import streamlit as st

# Option menu for Streamlit
from streamlit_option_menu import option_menu

# SQL library
import mysql.connector as mySql

# Additional libraries
import requests 
import plotly.express as px
import locale  # to convert number format to indian number format (Optional)
```
</br>

### 4. Project Structure
This project is structured into two distinct Python files, each serving a specific purpose:

* #### <ins>JSON to CSV Conversion and MySQL Migration</ins>
⠀⠀⠀⠀<ins>File:</ins> **_Phonepe_Pulse_DataExtraction.py_**</br>
⠀⠀⠀⠀<ins>Description:</ins> **_This script is responsible for extracting data from a JSON structure, converting it into CSV format, and subsequently ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀migrating it to a MySQL database. It ensures seamless data transformation and storage for further analysis._**
* #### <ins>Streamlit Application for Data Visualization</ins>
⠀⠀⠀⠀<ins>File:</ins> **_Phonepe_Pulse_Explorer.py_**</br>
⠀⠀⠀⠀<ins>Description:</ins> **_This script host a Streamlit application that provides enhanced insights into the data. Leveraging Streamlit's interactive ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀features, it offers geographical map representations and various charts to visualize the data comprehensively._**
</br>
</br>
___
## User Guide
### <ins><em> Analysis Page </em></ins>
![Analysis_Page](https://github.com/BalaKrishnanCodeSpace/Phonepe_Pulse_Data_Extraction_-_Visualization/blob/36ccad82d90bb187b25e17dbfdd97de5f1e0a296/Miscellaneous_Files/Analysis_Page.png)


The Analysis page within the PhonePe Pulse Data Visualization and Exploration application provides users with powerful tools to gain insights into the harvested data. Here's a user guide to navigating through the Analysis page:

*  <b><ins>Selecting Data Parameters:</ins></b>
Users can choose various parameters such as Year, State and highest/lowest using the provided dropdown menus or input fields.

*  <b><ins>Interactive Visualizations:</ins></b>
The application utilizes interactive visualizations powered by Plotly to present data in an intuitive and visually appealing manner. Users can zoom, pan, and interact with the charts to explore specific data points and trends.

*  <b><ins>Data Filters:</ins></b>
Users can filter data based on specific criteria such as Year and State to focus on relevant insights. This allows for a more targeted analysis of the data based on user-defined parameters.

*  <b><ins>Insightful Analysis:</ins></b>
The Analysis page aims to provide users with actionable insights derived from the PhonePe Pulse data. By visualizing transaction and user data across different regions and time periods, users can identify trends, patterns, and outliers to inform business decisions effectively.

*  <b><ins>Exporting Results:</ins></b>
Users have the option to export the analyzed results for further processing or sharing. The application provides functionality to save visualizations as image files or export data tables for offline analysis.
</br>

### <ins><em> Explore Data Page </em></ins>
![](https://github.com/BalaKrishnanCodeSpace/Phonepe_Pulse_Data_Extraction_-_Visualization/blob/36ccad82d90bb187b25e17dbfdd97de5f1e0a296/Miscellaneous_Files/Explore_Data_Page.png)

The Explore Data page within the PhonePe Pulse Data Visualization and Exploration application offers users a comprehensive toolkit to delve into the intricacies of the harvested data. Here's a detailed guide on navigating through the Explore Data page:

*  <b><ins>Selecting Data Filters:</ins></b>
Users can utilize a wide range of filters to narrow down the dataset and focus on specific aspects of interest. These filters include Analyzer (to choose between Transactions and Users), Year, Quarter, and State.

*  <b><ins>Interactive Map Visualization:</ins></b>
The Explore Data page presents geographical insights using an interactive map visualization powered by Plotly. Users can explore transaction or user data across different states of India, allowing for a spatial understanding of transaction trends.
      + <a href="https://plotly.com/python/choropleth-maps/" target="_blank"> Plotly Mapbox Choropleth</a>: 
In the "Explore Data" page of our application, we leverage the Plotly Mapbox Choropleth feature to provide users with an interactive and insightful visualization of geographical data. The Plotly Mapbox Choropleth offers several key functionalities:

          - <b><ins>Geospatial Data Representation</ins>:</b> Visualize geospatial data on an interactive map, with each region shaded or colored based on specific data values, enabling exploration of spatial patterns and variations.

          - <b><ins>Customizable Color Scales</ins>:</b> Flexibility to customize the color scale used in the choropleth map to represent data intensity or magnitude, allowing users to highlight different data ranges or categories.

          - <b><ins>Integration with Mapbox</ins>:</b> Leveraging the Mapbox platform to provide high-quality and customizable maps for data visualization, with options to choose from a variety of Mapbox map styles and themes.

          - <b><ins>Interactive Hover Information</ins>:</b> Interactive hover information for each geographical region, providing additional details about data points upon hovering, enhancing user experience and facilitating deeper exploration.

          - <b><ins>Data Filtering and Aggregation</ins>:</b> Ability to filter and aggregate data based on different parameters such as year, quarter, and state, allowing users to focus on specific subsets of data and analyze them in more detail.

          - <b><ins>Dynamic Updates</ins>:</b> Supports dynamic updates, enabling users to interactively modify data parameters and instantly visualize the changes on the map, enhancing real-time feedback and facilitating exploratory data analysis.

*  <b><ins>Color Scale Customization:</ins></b>
Users have the flexibility to customize the color scale used in the map visualization to represent transaction or user data intensity. By adjusting the color scale, users can emphasize specific data ranges or patterns on the map.

*  <b><ins>Quarterly Analysis:</ins></b>
Users can analyze transaction or user data on a quarterly basis by selecting the desired quarter from the dropdown menu. This allows for a more granular examination of data trends and patterns within specific time periods.

*  <b><ins>State-wise Filtering:</ins></b>
The Explore Data page enables users to filter transaction or user data based on individual states within India. Users can select specific states of interest to focus their analysis and explore regional variations in transaction activity.

*  <b><ins>Dynamic Data Exploration:</ins></b>
With the ability to toggle between Transactions and Users as the chosen analyzer, users can dynamically explore different aspects of the PhonePe Pulse dataset. This flexibility allows for a comprehensive analysis of both transaction and user-related metrics.

*  <b><ins>Exporting Insights:</ins></b>
Users can export the analyzed insights and visualizations from the Explore Data page for further analysis or sharing. The application provides options to save visualizations as image files or export data tables for offline exploration.
