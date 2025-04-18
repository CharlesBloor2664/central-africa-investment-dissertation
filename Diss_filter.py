import pandas as pd 
## Code was altered for the use case of each dataset filter ##

eccas_countries = [ "Angola", "Burundi", "Cameroon", "Central African Republic", "Chad", 
    "Republic of the Congo", "Democratic Republic of the Congo", "Equatorial Guinea", 
    "Gabon", "Rwanda", "São Tomé and Príncipe"]

file1_path = "C:/Users/charl/Documents/Python/Diss_Data/Africa (All) Contracts/ContractData_Mar2024.xlsx"
file2_path = "C:/Users/charl/Documents/Python/Diss_Data/Africa (All) Debt/CLA-Database-Raw-Data-Public-2024-FIN.xlsx"

df1 = pd.read_excel(file1_path, sheet_name="Gross Revenue data", header=0)

country_names = df1.iloc[0, 1:].tolist()
df1 = df1.iloc[2:] 
df1.columns = ["Year"] + country_names
df1 = df1.reset_index(drop=True)

df1_filtered = df1[["Year"] + [col for col in country_names if col in eccas_countries]]

output_file1 = "C:/Users/charl/Documents/Python/Diss_Data/Filtered_Contract_Data_2024.xlsx"
df1_filtered.to_excel(output_file1, index=False)
print("Filtered Contract Data saved successfully.")

df2 = pd.read_excel(file2_path, sheet_name="2000-2023", header=0)

country_column2 = "Unnamed: 4" if "Country" not in df2.columns else "Country"

df2_filtered = df2[df2[country_column2].isin(eccas_countries)]

output_file2 = "C:/Users/charl/Documents/Python/Diss_Data/Filtered_Debt_Data_2024.xlsx"
df2_filtered.to_excel(output_file2, index=False)
print("Filtered Debt Data saved successfully.")
