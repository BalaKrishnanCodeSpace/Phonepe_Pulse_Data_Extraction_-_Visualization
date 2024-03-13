
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

# Overview
The PhonePe Pulse Data Visualization and Exploration project is a robust system aimed at enabling the effortless extraction, storage, and analysis of PhonePe Pulse data. Utilizing cutting-edge technologies like SQL, Streamlit, Plotly this project provides users with the capability to efficiently explore and analyze PhonePe Pulse data for actionable insights. This project comprises the following key components:

### 1. Streamlit Application

Built with Streamlit, the application provides an intuitive interface for users to explore and visualize PhonePe Pulse data effortlessly. Streamlit's interactive widgets enhance the user experience, making data analysis seamless and efficient.

### 2. MySQL Database
MySQL serves as the backbone for storing PhonePe Pulse data securely and efficiently. Data is stored in structured tables within the MySQL database, facilitating seamless data retrieval and analysis through SQL queries.

### 3. Interactive Data Exploration
Users can interactively explore PhonePe Pulse data using Streamlit's widgets and Plotly visualizations. The application enables users to filter, group, and analyze data based on various parameters, empowering them to derive actionable insights from the data.

### 4. Data Visualization with Plotly
Plotly is employed to create interactive and visually engaging plots, charts, and maps to visualize PhonePe Pulse data. Users can gain valuable insights into transaction trends, user behavior, and geographical distribution through Plotly's dynamic visualization features.



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
# SQL libraries
import mysql.connector

# Pandas
import pandas as pd

# Dashboard libraries
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

* #### JSON to CSV Conversion and MySQL Migration
##### File: Phonepe_Pulse_DataExtraction.py
<p>Description: This script is responsible for extracting data from a JSON structure, converting it into CSV format, and subsequently migrating it to a MySQL database. It ensures seamless data transformation and storage for further analysis.
* #### Streamlit Application for Data Visualization
##### File: Phonepe_Pulse_Explorer.py
Description: The streamlit_app.py script hosts a Streamlit application that provides enhanced insights into the data. Leveraging Streamlit's interactive features, it offers geographical map representations and various charts to visualize the data comprehensively.

Features
Data Cloning: Clone data from the PhonePe Pulse repository on GitHub.
Data Extraction: Extract data to CSV files for further processing.
Database Integration: Store extracted data in a MySQL database for efficient retrieval and analysis.
Interactive Visualization: Visualize PhonePe Pulse data in various formats, including graphs and maps, using Streamlit.
Contact Form: Easily reach out for further inquiries through the built-in contact form.
Installation
Clone the Repository:

git clone https://github.com/your-username/phonepe-pulse-visualization.git
Install Dependencies:

pip install -r requirements.txt
Set Up MySQL Database:

Create a MySQL database and user.
Update the MySQL connection details in the code.
Run the Streamlit App:

streamlit run app.py
Usage
Access the Streamlit App: Open the Streamlit app in your browser.
Explore Data: Utilize the intuitive interface to select desired analysis options.
Visualize Data: View PhonePe Pulse data visualizations, including graphs and maps, generated dynamically.
Contact: Use the contact form to reach out for further inquiries or support.
Contributing
Contributions to this project are welcome! If you'd like to contribute, please follow these steps:

Fork the Repository
Create a Feature Branch: git checkout -b feature/YourFeature
Commit Changes: git commit -am 'Add some feature'
Push to Your Branch: git push origin feature/YourFeature
Submit a Pull Request
Credits
This project was developed by [Your Name] and [Contributors], inspired by the PhonePe Pulse data.
