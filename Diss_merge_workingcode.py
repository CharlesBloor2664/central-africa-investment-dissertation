import os
import pandas as pd
## Code was altered for the use case of each dataset merge ##

extract_folder = "C:/Users/charl/Documents/Python/Diss_Data/Extracted_GDP"
output_file = "C:/Users/charl/Documents/Python/Diss_Data/Merged_GDP.csv"

os.makedirs(extract_folder, exist_ok=True)

data_frames = []

if not os.path.exists(extract_folder):
    print(f"Error: Folder not found - {extract_folder}")
    exit()

files = os.listdir(extract_folder)
print(f"Files found: {files}")

for file in files:
    file_path = os.path.join(extract_folder, file)
    
    if file.endswith(".xls") or file.endswith(".xlsx"):
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    elif file.endswith(".csv"):
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
    else:
        continue  
    
    if df.empty:
        print(f"Warning: {file} is empty or could not be read correctly.")
        continue
    
    found_year = False
    for year in range(2000, 2021):
        if str(year) in file:
            df["Year"] = year
            found_year = True
            break  
    
    if not found_year:
        print(f"Warning: No valid year found in filename {file}.")
    
    df = df.rename(columns=lambda x: x.strip())  
    
    expected_columns = ['Year', 'Continent ID', 'Continent', 'Country ID', 'Country', 'Trade Value', 'ECI', 'Measure']
    df = df[[col for col in expected_columns if col in df.columns]]
    
    if not df.empty:
        data_frames.append(df)
      
if data_frames:
    merged_df = pd.concat(data_frames, ignore_index=True)
    merged_df.drop_duplicates(inplace=True)
    merged_df.dropna(inplace=True)
    merged_df.to_csv(output_file, index=False)
    print(f"Merged dataset saved to {output_file}")
else:
    print("No valid data files found for merging.")
