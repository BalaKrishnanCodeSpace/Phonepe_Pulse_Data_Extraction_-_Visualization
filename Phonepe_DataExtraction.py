# Importing required libraries
import os
import pandas as pd
import json
import mysql.connector as mySql


# ___*___*___*___*___*___ Data Extraction Process ___*___*___*___*___*___ #

# Define paths for aggregated transaction data
aggTransPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\aggregated\transaction\country\india\state"
aggTransPathList = os.listdir(aggTransPath) # The list stores the folder names, which are represented as states."

# Define paths for aggregated user data
aggUserPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\aggregated\user\country\india\state"
aggUserPathList = os.listdir(aggUserPath) # The list stores the folder names, which are represented as states."

# Define paths for map transaction data
mapTransPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\map\transaction\hover\country\india\state"
mapTransPathList = os.listdir(mapTransPath) # The list stores the folder names, which are represented as states."

# Define paths for map user data
mapUserPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\map\user\hover\country\india\state"
mapUserPathList = os.listdir(mapUserPath) # The list stores the folder names, which are represented as states."

# Define paths for top transaction data
topTransPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\top\transaction\country\india\state"
topTransPathList = os.listdir(topTransPath) # The list stores the folder names, which are represented as states."

# Define paths for top user data
topUserPath = r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\pulse-master\data\top\user\country\india\state"
topUserPathList = os.listdir(topUserPath) # The list stores the folder names, which are represented as states."


def dataExtraction(path,states):
    """
    Extracts data from JSON files located in the specified path for each state and organizes it into lists.

    Args:
    - path (str): The directory path containing state-wise JSON files.
    - states (list of str): A list of state names.

    Returns:
    - stateList (list of str): A list containing state names corresponding to the extracted data.
    - yearList (list of str): A list containing years corresponding to the extracted data.
    - quarterList (list of str): A list containing quarters corresponding to the extracted data.
    - processedDataList (list): A list containing processed JSON data extracted from the files.
    """  
    processedDataList = []    # List to store processed data from JSON files
    stateList = []            # List to store states
    yearList = []             # List to store years
    quarterList = []          # List to store quarters
    
    # Loop through each state provided in the 'states' list
    for state in states:
        statePath = os.path.join(path, state)   # Construct the path for the state
        years = os.listdir(statePath)           # List all years in the state directory

        # Loop through each year found in the state directory
        for year in years:
            yearPath = os.path.join(statePath, year)    # Construct the path for the year
            quarters = os.listdir(yearPath)             # List all quarters in the year directory

            # Loop through each quarter found in the year directory
            for quarter in quarters:
                quarterPath = os.path.join(yearPath, quarter)     # Construct the path for the quarter
                fileHandle = open(quarterPath, 'r')               # Open the JSON file
                response = json.load(fileHandle)                  # Load JSON data from the file

                # Append state, year, quarter, and JSON data to their respective lists
                stateList.append(state)
                yearList.append(year)
                quarterList.append(quarter)
                processedDataList.append(response)

    # Return lists containing extracted data
    return stateList, yearList, quarterList, processedDataList

# Extract aggregated transaction data from the specified path and list of files
aggTransState, aggTransYear, aggTransQuarter, aggTransProData = dataExtraction(aggTransPath,aggTransPathList)

# Extract aggregated user data from the specified path and list of files
aggUserState, aggUserYear, aggUserQuarter, aggUserProData = dataExtraction(aggUserPath,aggUserPathList)

# Extract map transaction data from the specified path and list of files
mapTransState, mapTransYear, mapTransQuarter, mapTransProData = dataExtraction(mapTransPath,mapTransPathList)

# Extract map user data from the specified path and list of files
mapUserState, mapUserYear, mapUserQuarter, mapUserProData = dataExtraction(mapUserPath,mapUserPathList)

# Extract top transaction data from the specified path and list of files
topTransState, topTransYear, topTransQuarter, topTransProData = dataExtraction(topTransPath,topTransPathList)

# Extract top user data from the specified path and list of files
topUserState, topUserYear, topUserQuarter, topUserProData = dataExtraction(topUserPath,topUserPathList)


def aggregatedTransaction(aggTransState, aggTransYear, aggTransQuarter, aggTransProData):
  """
  Extracts aggregated transaction data from the provided parameters and returns a DataFrame.

  Parameters:
  - aggTransState (list): List of states corresponding to the aggregated transaction data.
  - aggTransYear (list): List of years corresponding to the aggregated transaction data.
  - aggTransQuarter (list): List of quarters corresponding to the aggregated transaction data.
  - aggTransProData (list): List of aggregated transaction data.

  Returns:
  - dfAggTrans (pandas.DataFrame): DataFrame containing the aggregated transaction data.
  """
  
  aggTrans = []   # List to store extracted aggregated transaction data
  
  try:
    # Iterate through each item in the list of aggregated transaction data
    for index, items in enumerate(aggTransProData):
      if 'transactionData' in items['data'] and items['data']['transactionData'] is not None:
        
        # Extract transaction details from each item
        for itemData in items['data']['transactionData']:
          name = itemData['name']
          count = itemData['paymentInstruments'][0]['count']
          amount = itemData['paymentInstruments'][0]['amount']
          
          # Append extracted data to the 'aggTrans' list
          aggTrans.append({
              'State': aggTransState[index],
              'Year' : aggTransYear[index],
              'Quarter' : aggTransQuarter[index].rstrip('.json'),
              'Transaction_Type' : name,
              'Transaction_Count' : count,
              'Transaction_Amount' : amount

          })
  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass
  
  # Create a DataFrame from the 'aggTrans' list
  dfAggTrans = pd.DataFrame(aggTrans)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfAggTrans['State'] = dfAggTrans['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfAggTrans['State'] = dfAggTrans['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfAggTrans['State'] = dfAggTrans['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  
  dfAggTrans['State'] = dfAggTrans['State'].str.title()
  
  return dfAggTrans


def aggregatedUser(aggUserState, aggUserYear, aggUserQuarter, aggUserProData):
  """
  Extracts aggregated user data from the provided parameters and returns a DataFrame.

  Parameters:
  - aggUserState (list): List of states corresponding to the aggregated user data.
  - aggUserYear (list): List of years corresponding to the aggregated user data.
  - aggUserQuarter (list): List of quarters corresponding to the aggregated user data.
  - aggUserProData (list): List of aggregated user data.

  Returns:
  - dfAggUser (pandas.DataFrame): DataFrame containing the aggregated user data.
  """
  
  aggUser = []  # List to store extracted aggregated user data
  try:
    # Iterate through each item in the list of aggregated user data
    for index, items in enumerate(aggUserProData):
        if 'usersByDevice' in items['data'] and items['data']['usersByDevice'] is not None:
          # Extract user details from each item
          for itemData in items['data']['usersByDevice']:
              brandName = itemData['brand']
              count = itemData['count']
              percentage = itemData['percentage']

              # Append extracted data to the 'aggUser' list
              aggUser.append({
                  'State': aggUserState[index],
                  'Year': aggUserYear[index],
                  'Quarter': aggUserQuarter[index].rstrip('.json'),
                  'Brand_Name': brandName,
                  'User_Count': count,
                  'User_Percentage': percentage
              })

  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass
  
  # Create a DataFrame from the 'aggUser' list
  dfAggUser = pd.DataFrame(aggUser)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfAggUser['State'] = dfAggUser['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfAggUser['State'] = dfAggUser['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfAggUser['State'] = dfAggUser['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  dfAggUser['State'] = dfAggUser['State'].str.title()
  return dfAggUser


def mapTransaction(mapTransState, mapTransYear, mapTransQuarter, mapTransProData):
  """
  Extracts map transaction data from the provided parameters and returns a DataFrame.

  Parameters:
  - mapTransState (list): List of states corresponding to the map transaction data.
  - mapTransYear (list): List of years corresponding to the map transaction data.
  - mapTransQuarter (list): List of quarters corresponding to the map transaction data.
  - mapTransProData (list): List of map transaction data.

  Returns:
  - dfmapTrans (pandas.DataFrame): DataFrame containing the map transaction data.

  """
  mapTrans = []   # List to store extracted map transaction data
  try:
    # Iterate through each item in the list of map transaction data
    for index, items in enumerate(mapTransProData):
        if 'hoverDataList' in items['data'] and items['data']['hoverDataList'] is not None:
          # Extract transaction details from each item
          for itemData in items['data']['hoverDataList']:
              district = itemData['name'].rstrip('district').rstrip()
              count = itemData['metric'][0]['count']
              amount = itemData['metric'][0]['amount']

              # Append extracted data to the 'mapTrans' list
              mapTrans.append({
                  'State': mapTransState[index],
                  'Year': mapTransYear[index],
                  'Quarter': mapTransQuarter[index].rstrip('.json'),
                  'District': district,
                  'Transaction_Count': count,
                  'Transaction_Amount': amount
              })

  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass

  # Create a DataFrame from the 'mapTrans' list
  dfmapTrans = pd.DataFrame(mapTrans)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfmapTrans['State'] = dfmapTrans['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfmapTrans['State'] = dfmapTrans['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfmapTrans['State'] = dfmapTrans['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  dfmapTrans['State'] = dfmapTrans['State'].str.title()
  dfmapTrans['District'] = dfmapTrans['District'].str.title()
  
  return dfmapTrans


def mapUser(mapUserState, mapUserYear, mapUserQuarter, mapUserProData):
  """
  Extracts map user data from the provided parameters and returns a DataFrame.

  Parameters:
  - mapUserState (list): List of states corresponding to the map user data.
  - mapUserYear (list): List of years corresponding to the map user data.
  - mapUserQuarter (list): List of quarters corresponding to the map user data.
  - mapUserProData (list): List of map user data.

  Returns:
  - dfmapUser (pandas.DataFrame): DataFrame containing the map user data.
  """
  mapUser = []  # List to store extracted map user data
  try:
    # Iterate through each item in the list of map user data
    for index, items in enumerate(mapUserProData):
        if 'hoverData' in items['data'] and items['data']['hoverData'] is not None:
          # Extract user details for each district
          for district, districtData in items['data']['hoverData'].items():
              registeredUsers = districtData.get('registeredUsers')
              appOpens = districtData.get('appOpens')
              district = district.rstrip('district').rstrip()
              mapUser.append({
                  'State' : mapUserState[index],
                  'Year' : mapUserYear[index],
                  'Quarter' : mapUserQuarter[index].rstrip('.json'),
                  'District' : district,
                  'RegisteredUsers' : registeredUsers,
                  'AppOpens' : appOpens
              })

  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass

  # Create a DataFrame from the 'mapUser' list
  dfmapUser = pd.DataFrame(mapUser)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfmapUser['State'] = dfmapUser['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfmapUser['State'] = dfmapUser['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfmapUser['State'] = dfmapUser['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  dfmapUser['State'] = dfmapUser['State'].str.title()
  dfmapUser['District'] = dfmapUser['District'].str.title()
  return dfmapUser


def topTransaction(topTransState, topTransYear, topTransQuarter, topTransProData):
  """
  Extracts top transaction data from the provided parameters and returns a DataFrame.

  Parameters:
  - topTransState (list): List of states corresponding to the top transaction data.
  - topTransYear (list): List of years corresponding to the top transaction data.
  - topTransQuarter (list): List of quarters corresponding to the top transaction data.
  - topTransProData (list): List of top transaction data.

  Returns:
  - dfTopTrans (pandas.DataFrame): DataFrame containing the top transaction data.
  """
  
  topTrans = [] # List to store extracted top transaction data
  
  try:
    # Iterate through each item in the list of top transaction data
    for index, items in enumerate(topTransProData):
      if 'data' in items and 'pincodes' in items['data']:
        # Extract transaction details for each pincode
        for pincodeData in items['data']['pincodes']:
            pincode = pincodeData['entityName']
            count = pincodeData['metric']['count']
            amount = pincodeData['metric']['amount']

            # Append extracted data to the 'topTrans' list
            topTrans.append({
                'State': topTransState[index],
                'Year': topTransYear[index],
                'Quarter': topTransQuarter[index].rstrip('.json'),
                'Pincode': pincode,
                'Transaction_Count': count,
                'Transaction_Amount': amount
            })

  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass

  # Create a DataFrame from the 'topTrans' list
  dfTopTrans = pd.DataFrame(topTrans)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfTopTrans['State'] = dfTopTrans['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfTopTrans['State'] = dfTopTrans['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfTopTrans['State'] = dfTopTrans['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  dfTopTrans['State'] = dfTopTrans['State'].str.title()
  return dfTopTrans


def topUser(topUserState, topUserYear, topUserQuarter, topUserProData):
  """
  Extracts top user data from the provided parameters and returns a DataFrame.

  Parameters:
  - topUserState (list): List of states corresponding to the top user data.
  - topUserYear (list): List of years corresponding to the top user data.
  - topUserQuarter (list): List of quarters corresponding to the top user data.
  - topUserProData (list): List of top user data.

  Returns:
  - dfTopUser (pandas.DataFrame): DataFrame containing the top user data.
  """
  
  topUser = []  # List to store extracted top user data
  try:
    # Iterate through each item in the list of top user data
    for index, items in enumerate(topUserProData):
        if 'data' in items and 'pincodes' in items['data']:
          # Extract user details for each pincode
          for pincodeData in items['data']['pincodes']:
              pincode = pincodeData['name']
              registeredUser = pincodeData['registeredUsers']

              # Append extracted data to the 'topUser' list
              topUser.append({
                  'State': topUserState[index],
                  'Year': topUserYear[index],
                  'Quarter': topUserQuarter[index].rstrip('.json'),
                  'Pincode': pincode,
                  'Registered_User': registeredUser
              })

  except (KeyError, TypeError) as e:
    print(f"Error: {e}")
    pass

  # Create a DataFrame from the 'topUser' list
  dfTopUser = pd.DataFrame(topUser)
  
  # Clean the 'State' column by replacing characters and converting to title case in order to align with geojson
  dfTopUser['State'] = dfTopUser['State'].str.replace('-',' ')
  
  # Replace occurrences of 'andaman & nicobar islands' with 'andaman & nicobar island' 
  # to match the naming convention used in the geojson file, which likely represents 
  # the geographical entity as singular rather than plural.
  dfTopUser['State'] = dfTopUser['State'].str.replace('andaman & nicobar islands','andaman & nicobar island')
  
  # Replace occurrences of 'dadra & nagar haveli & daman & diu' with 'dadara & nagar havelli'
  # to align with the expected naming format or representation, ensuring consistency 
  # across the data and making it easier to work with and understand.
  dfTopUser['State'] = dfTopUser['State'].str.replace('dadra & nagar haveli & daman & diu','dadara & nagar havelli')
  dfTopUser['State'] = dfTopUser['State'].str.title()
  
  return dfTopUser



# Export aggregated transaction data to a CSV file
aggTransToCSV = aggregatedTransaction(aggTransState, aggTransYear, aggTransQuarter  , aggTransProData)
aggTransToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Aggregate_Transaction.csv',index = False, mode = 'w')

# Export aggregated user data to a CSV file
aggUserToCSV = aggregatedUser(aggUserState, aggUserYear, aggUserQuarter, aggUserProData)
aggUserToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Aggregate_User.csv',index = False, mode = 'w')

# Export map transaction data to a CSV file
mapTransToCSV = mapTransaction(mapTransState, mapTransYear, mapTransQuarter, mapTransProData)
mapTransToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Map_Transaction.csv',index = False, mode = 'w')

# Export map user data to a CSV file
mapUserToCSV = mapUser(mapUserState, mapUserYear, mapUserQuarter, mapUserProData)
mapUserToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Map_User.csv',index = False, mode = 'w')

# Export top transaction data to a CSV file
topTransToCSV = topTransaction(topTransState, topTransYear, topTransQuarter, topTransProData)
topTransToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Top_Transaction.csv',index = False, mode = 'w')

# Export top user data to a CSV file
topUserToCSV = topUser(topUserState, topUserYear, topUserQuarter, topUserProData)
topUserToCSV.to_csv(r'C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Top_User.csv',index = False, mode = 'w')


# ___*___*___*___*___*___ Data Transfer to MySQL ___*___*___*___*___*___ #

# Establish a connection to MySQL database
myConnection = mySql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root'
)


# Create a cursor object to interact with the MySQL database
myCursor = myConnection.cursor()


# Execute SQL commands to drop and create a new database if it does not exist
myCursor.execute("Drop Database IF EXISTS PhonePe_Pulse")
myCursor.execute("Create Database PhonePe_Pulse")

# Switch to the newly created database for subsequent operations
myCursor.execute("Use PhonePe_Pulse")


# Execute SQL command to create a table named 'AggTrans' in the database
myCursor.execute("""
                 CREATE TABLE AggTrans(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     Transaction_Type Varchar(255),
                     Transaction_Count Int,
                     Transaction_Amount Float
                     )
                 """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Aggregate_Transaction.csv")

# Convert DataFrame rows into a list of tuples
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'AggTrans' table
myCursor.executemany("INSERT INTO AggTrans (State, Year, Quarter, Transaction_Type, Transaction_Count, Transaction_Amount) VALUES (%s, %s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'AggUser' in the database
myCursor.execute("""
                 CREATE TABLE AggUser(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     Brand_Name Varchar(255),
                     User_Count Int,
                     User_Percentage Float
                     )
                 """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Aggregate_User.csv")

# Convert DataFrame rows into a list of tuples for database insertion
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'AggUser' table
myCursor.executemany("INSERT INTO AggUser (State, Year, Quarter, Brand_Name, User_Count, User_Percentage) VALUES (%s, %s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'MapTrans' in the database
myCursor.execute("""
                 CREATE TABLE MapTrans(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     District Varchar(255),
                     Transaction_Count Int,
                     Transaction_Amount Float
                     )
                     """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Map_Transaction.csv")

# Convert DataFrame rows into a list of tuples for database insertion
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'MapTrans' table
myCursor.executemany("INSERT INTO MapTrans (State, Year, Quarter, District, Transaction_Count, Transaction_Amount) VALUES (%s, %s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'MapUser' in the database
myCursor.execute("""
                 CREATE TABLE MapUser(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     District Varchar(255),
                     RegisteredUsers Int,
                     AppOpens Int
                     )
                     """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Map_User.csv")

# Convert DataFrame rows into a list of tuples for database insertion
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'MapUser' table
myCursor.executemany("INSERT INTO MapUser (State, Year, Quarter, District, RegisteredUsers, AppOpens) VALUES (%s, %s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'TopTrans' in the database
myCursor.execute("""
                 CREATE TABLE TopTrans(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     Pincode Int,
                     Transaction_Count Long,
                     Transaction_Amount Double
                     )
                     """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Top_Transaction.csv")

# Fill any missing values with 0 in the DataFrame
df.fillna(0, inplace = True)

# Convert DataFrame rows into a list of tuples for database insertion
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'TopTrans' table
myCursor.executemany("INSERT INTO TopTrans (State, Year, Quarter, Pincode, Transaction_Count, Transaction_Amount) VALUES (%s, %s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'TopUser' in the database
myCursor.execute("""
                 CREATE TABLE TopUser(
                     State Varchar(255),
                     Year Int,
                     Quarter Int,
                     Pincode Int,
                     Registered_User Int
                     )
                     """)

# Read data from the CSV file into a DataFrame
df = pd.read_csv(r"C:\My Folder\Tuts\Python\Project\Project 2 - Phonepe Pulse Data Visualization\Top_User.csv")

# Convert DataFrame rows into a list of tuples for database insertion
values = df.values.tolist()

# Execute SQL command to insert the data from the DataFrame into the 'TopUser' table
myCursor.executemany("INSERT INTO TopUser (State, Year, Quarter, Pincode, Registered_User) VALUES (%s, %s, %s, %s, %s)", values)


# Execute SQL command to create a table named 'lastrefreshed' in the database
myCursor.execute("""
                 CREATE TABLE lastrefreshed(
                     date date
                     )
                     """)
# Execute SQL command to insert the current date into the 'lastrefreshed' table
myCursor.execute("INSERT INTO lastrefreshed (date) VALUES (CURRENT_DATE)")



# Commit the changes made to the database
myConnection.commit()

# Close the cursor used to interact with the database
myCursor.close()

# Close the connection to the database
myConnection.close()

