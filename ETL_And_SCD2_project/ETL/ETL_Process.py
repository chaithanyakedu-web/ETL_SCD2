import json
import pandas as pd
import pyodbc
from config import *
import os

"""important note:
  inplace=True/False 
  -->if you want to chage the main data frame use inplace=True
     it will modify the original data frame
 -->you don't want to chage the orginal df use inplace=False
    it will return the new dataframe     
 
"""

from config.db_connection import db_connection
from data_extraction.extraction_json_xml import verify_file_extension_and_read_data


def transform_data(filename):

    """creating the database connection"""
    conn = db_connection()

#source layer validations:

    #file existance check
    if os.path.exists(filename):
        print("file exists")
    else:
        print("file does not exist")

    #file format validations
    df=verify_file_extension_and_read_data(filename)
    # print(df_data)
    count_columns=len(df.columns)
    print("number of headers:",count_columns)


# curated validations::


    #creating csv file before transformation for better readablity
    output_file0= r'K:\ETL_And_SCD2_project\before_cleaned.csv'
    df.to_csv(output_file0, index=False)
    print(f"before Cleaned data saved to: {output_file0}")

    #remove the duplicated data
    #show the duplicate rows before deleting them
    duplicates=df[df.duplicated(subset=['org_nk','org_name'])]
    print(f"Duplicates: {duplicates}")

    #drop the duplicates
    df.drop_duplicates(subset=['org_nk','org_name'], inplace=True)

    """ RULE x :remove the all the coumns that has null values"""
    df.dropna(how='all', inplace=True)

    # #date type conversion
    # date_columns=['created_date_dmy','turnover_evaluation_date','valid_till']
    #
    # for col in date_columns:
    #      df[col]=pd.to_datetime(df[col], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
    #if the date is 31-12-9999 it is out of range so it will give error outofboundsdatetime



    # sql_query='select * from source.organization_day_data'
    # df = pd.read_sql(sql_query, conn)
    # print(df)
    # print(df.columns) -->it retuns the all the column names
    # print(df.columns[0])-->it returns the column name at index 0


    """RULE 1: 'org_nk' and 'org_name' must not have null data """
    df.dropna(subset=['org_nk', 'org_name'],inplace=True)

    """RULE 2: 'address_line1' trim this column it removes the white spaces"""

    df['org_name'].str.strip().inplace=True
    df['address_line1'].str.strip().inplace=True

    #if you want to strip the multiple col use lambda expression

    # print(df)

    """RULE 3: capitalize the city and the state"""
    df['city'].str.upper().inplace=True
    df['state'].str.upper().inplace=True


    """RULE 4 postal code must have olny 6 digits with numbers only"""
    # df.dropna(df['postal_code'].str.match(r'^\d{6}$'),inplace=True)
    df.drop(df[~df['postal_code'].str.match(r'^\d{6}$', na=False)].index, inplace=True)

    """RULE 5 :change the email address to the lowercase and must ends with email.com"""
    df['contact_email']=df['contact_email'].str.lower()

    """RULE 6: to check weather phone number is valid or not if not drop it"""
    df.drop(df[~df['phone'].astype(str).str.match(r'^(?:\+91|91)?\d{10}$',na=False)].index, inplace=True)

    """RULE 8 : check weather the status is in between(valid/invalid) if not drop the row"""
    df.drop(df[df['status'].isin(['active','inactive'])].index, inplace=True)
    df['status']=df['status'].str.upper()
    # print(df['status'].dtype)


    """RULE 9 : strip the data and titlecase if any null left fill it to unknown"""
    df['org_name']=df['org_name'].str.strip().str.title().fillna("unknown")

    """RULE 10 : concat the address,city,state"""
    df['address_line1']=df['address_line1'].str.strip()+","+df['city'].str.strip()+","+df['state'].str.strip()

    """RULE 11:: validate the email id if not matched it will be dropped"""
    df=df[df["contact_email"].str.endswith('@gmail.com',na=False)]

#domain layer validations:
    #dump the data into the json file update the previous record and change the dates respectively

    #adding the data into the json data
    # Save the DataFrame back to JSON
    # data_to_write = df.to_dict(orient='records')
    # with open(r'K:\ETL_And_SCD2_project\SOURCE_DATA\json\day0_orgs.json', 'w') as f:
    #     json.dump(data_to_write, f, indent=4)

    #reading the data and comparing the data
    get_data=conn.execute("select * from domain.organization")
    df_sql_data=pd.DataFrame(get_data)
    print(df_sql_data)
    # data=get_data.fetchall()
    # print(data)
    #or
    for row in get_data:
        print(row)
    # print(df.columns)
    #compare the your data and the database data to check yournot uploading the duplicate data

    output_file1 = r'K:\ETL_And_SCD2_project\after_cleaned.csv'
    df.to_csv(output_file1, index=False)
    print(f" Cleaned data saved to: {output_file1}")

transform_data(r'K:\ETL_And_SCD2_project\SOURCE_DATA\json\day0_orgs.json')





