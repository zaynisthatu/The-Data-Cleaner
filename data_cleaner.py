# Data Cleaning Project - Pakistani Contact Database
# Author: Your Name
# Date: July 2025

import pandas as pd
import numpy as np
import re
from io import StringIO

# Sample messy data (same as provided)
messy_data = """Name,Address,Phone,City,Age
Ali Khan,Street 123,03001234567,Karachi,30
Ahmed,Lane 456,923339876543,Lahore,
Sara,,0345-1122334,Islamabad,25
Faiza Khan,Block A,00923015678901,Peshawar,40
Usman,Main Road,0321 9876543,Quetta,35
Aisha,,0300 000 0000,Rawalpindi,
Kamran,Sector B,334-555-1212,Faisalabad,50
Zainab,Gulshan,92-300-1112233,Multan,28
,,03004445555,Sialkot,
Imran,Defence,,Hyderabad,
Mona,DHA,0312-3456789,Lahore,33
Haris,Street 789,0300-1234567,Karachi,29
,Plot 1,03337778888,Islamabad,
Nida,F-7,03009998888,Islamabad,22
Omer,G-9,,Rawalpindi,38
Hina,Johar Town,03221234567,Lahore,
Jawad,Bahria Town,0340-9876543,Rawalpindi,45"""

print("=== DATA CLEANING PROJECT ===")
print("Pakistani Contact Database Cleaner\n")

# Step 1: Load the messy data
print("Step 1: Loading messy data...")
df = pd.read_csv(StringIO(messy_data))
print(f"Original data shape: {df.shape}")
print("\nOriginal data preview:")
print(df.head(10))
print(f"\nMissing values per column:")
print(df.isnull().sum())

# Step 2: Clean Names
print("\nStep 2: Cleaning Names...")
def clean_name(name):
    if pd.isna(name) or name.strip() == "":
        return "Unknown"
    return name.strip().title()

df['Name'] = df['Name'].apply(clean_name)

# Step 3: Clean Addresses
print("Step 3: Cleaning Addresses...")
def clean_address(address):
    if pd.isna(address) or address.strip() == "":
        return "Address Not Provided"
    return address.strip().title()

df['Address'] = df['Address'].apply(clean_address)

# Step 4: Clean and standardize phone numbers
print("Step 4: Cleaning Phone Numbers...")
def clean_phone(phone):
    if pd.isna(phone) or phone.strip() == "":
        return "No Phone"
    
    # Remove all non-digit characters
    digits_only = re.sub(r'[^\d]', '', str(phone))
    
    # Handle different Pakistani phone number formats
    if len(digits_only) == 11 and digits_only.startswith('03'):
        # Standard mobile format: 03XXXXXXXXX
        return f"0{digits_only[1:3]}-{digits_only[3:7]}-{digits_only[7:]}"
    elif len(digits_only) == 13 and digits_only.startswith('923'):
        # International format: 923XXXXXXXXX
        return f"0{digits_only[3:5]}-{digits_only[5:9]}-{digits_only[9:]}"
    elif len(digits_only) == 12 and digits_only.startswith('92'):
        # International without 3: 92XXXXXXXXXXX
        return f"0{digits_only[2:4]}-{digits_only[4:8]}-{digits_only[8:]}"
    elif len(digits_only) == 10 and digits_only.startswith('3'):
        # Missing leading 0: 3XXXXXXXXXX
        return f"03{digits_only[1:3]}-{digits_only[3:7]}-{digits_only[7:]}"
    elif len(digits_only) >= 7:
        # Generic format for other lengths
        if len(digits_only) <= 10:
            mid = len(digits_only) // 2
            return f"{digits_only[:mid]}-{digits_only[mid:]}"
        else:
            return f"{digits_only[:3]}-{digits_only[3:7]}-{digits_only[7:]}"
    else:
        return "Invalid Phone"

df['Phone'] = df['Phone'].apply(clean_phone)

# Step 5: Clean Cities
print("Step 5: Cleaning Cities...")
def clean_city(city):
    if pd.isna(city) or city.strip() == "":
        return "Unknown City"
    return city.strip().title()

df['City'] = df['City'].apply(clean_city)

# Step 6: Clean Ages
print("Step 6: Cleaning Ages...")
def clean_age(age):
    if pd.isna(age):
        return "Unknown"
    try:
        age_int = int(age)
        if 0 <= age_int <= 120:
            return age_int
        else:
            return "Invalid Age"
    except:
        return "Invalid Age"

df['Age'] = df['Age'].apply(clean_age)

# Step 7: Add data quality indicators
print("Step 7: Adding data quality indicators...")
df['Data_Quality_Score'] = 0

# Calculate quality score based on completeness
df.loc[df['Name'] != 'Unknown', 'Data_Quality_Score'] += 1
df.loc[df['Address'] != 'Address Not Provided', 'Data_Quality_Score'] += 1
df.loc[df['Phone'] != 'No Phone', 'Data_Quality_Score'] += 1
df.loc[df['City'] != 'Unknown City', 'Data_Quality_Score'] += 1
df.loc[df['Age'] != 'Unknown', 'Data_Quality_Score'] += 1

df['Data_Quality_Percentage'] = (df['Data_Quality_Score'] / 5) * 100

# Step 8: Generate cleaning report
print("Step 8: Generating cleaning report...")
print("\n" + "="*50)
print("CLEANING REPORT")
print("="*50)
print(f"Total records processed: {len(df)}")
print(f"Records with complete data: {len(df[df['Data_Quality_Score'] == 5])}")
print(f"Records with missing data: {len(df[df['Data_Quality_Score'] < 5])}")
print(f"Average data quality score: {df['Data_Quality_Score'].mean():.2f}/5")
print(f"Phone numbers standardized: {len(df[df['Phone'] != 'No Phone'])}")
print(f"Unknown names filled: {len(df[df['Name'] == 'Unknown'])}")
print(f"Missing addresses filled: {len(df[df['Address'] == 'Address Not Provided'])}")

# Step 9: Display cleaned data
print("\nStep 9: Displaying cleaned data...")
print("\nCleaned data preview:")
print(df.to_string(index=False))

# Step 10: Save cleaned data
print("\nStep 10: Saving cleaned data...")
df.to_csv('cleaned_data.csv', index=False)
print("✅ Cleaned data saved as 'cleaned_data.csv'")

# Additional analysis
print("\n" + "="*50)
print("ADDITIONAL ANALYSIS")
print("="*50)

# City distribution
print("\nCity Distribution:")
city_counts = df['City'].value_counts()
print(city_counts)

# Age statistics (for valid ages only)
valid_ages = df[df['Age'] != 'Unknown']['Age']
if len(valid_ages) > 0:
    print(f"\nAge Statistics:")
    print(f"Average age: {valid_ages.mean():.1f}")
    print(f"Youngest: {valid_ages.min()}")
    print(f"Oldest: {valid_ages.max()}")

# Phone number analysis
valid_phones = len(df[df['Phone'] != 'No Phone'])
print(f"\nPhone Numbers:")
print(f"Valid phone numbers: {valid_phones}/{len(df)} ({valid_phones/len(df)*100:.1f}%)")

print("\n" + "="*50)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("="*50)