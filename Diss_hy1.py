import pandas as pd
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt 
import seaborn as sns 
import os 

eccas_global = pd.read_csv("Diss_Data/Merged_Exports_Global.csv")
eccas_china = pd.read_csv("Diss_Data/Merged_Exports_China.csv")
eccas_debts = pd.read_excel("Diss_Data/Filtered_Debt_Data_2024.xlsx")

china_sector_investment = eccas_china.groupby("Section")["Trade Value"].sum().reset_index()
global_sector_investment = eccas_global.groupby("Section")["Trade Value"].sum().reset_index()

debt_sector_investment = eccas_debts.groupby(["Lender Type","Sector"])["Loan (USD M)"].sum().reset_index()

dfi_debt = debt_sector_investment[debt_sector_investment["Lender Type"] == "Development Finance Institutions"]
commercial_bank_debt = debt_sector_investment[debt_sector_investment["Lender Type"] == "Commercial Banks"]
govt_debt = debt_sector_investment[debt_sector_investment["Lender Type"] == "Other CN Gov"]
contractor_debt = debt_sector_investment[debt_sector_investment["Lender Type"] == "Contractors"]

print("Chinese Investments by Sector:")
print(china_sector_investment.describe())
print("\nDebt by Lender Type:")
print(debt_sector_investment.describe())

contingency_table = pd.pivot_table(debt_sector_investment, values="Loan (USD M)", index="Sector", columns="Lender Type", aggfunc=np.sum, fill_value=0)
observed = contingency_table.values

chi2, p, dof, expected = stats.chi2_contingency(observed)

n = observed.sum()
phi2 = chi2 / n 
r, k = observed.shape
cramers_v = np.sqrt(phi2 / min(r-1, k-1))

output_dir =  "Diss_Data\\Diss_hy1_results"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "hy1_results.txt"), "w") as f:
	f.write("Chi-Squared Test result: \n")
	f.write(f"Chi-Squared Statisitics: {chi2}\n")
	f.write(f"P-Value: {p}\n")
	f.write(f"Degrees of Freedom: {dof}\n\n")
	f.write("Expected Frequencie Table: {\n}")
	f.write(f"Cramers V: {cramers_v}\n")

plt.figure(figsize=(15,10))
contingency_table.plot(kind="bar", stacked=True, colormap="Greys", figsize=(15,10))
plt.xticks(rotation=45)
plt.title("Sectoral Debt Allocation by Lender Type")
plt.ylabel("Loan (USD M)")
plt.legend(title="Lender Type")
plt.savefig(os.path.join(output_dir, "sector_lender_relationship.png"))
plt.show()
