import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

output_dir = r"C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Diss_hy4_results"
os.makedirs(output_dir, exist_ok=True)

eccas_exports_china = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_China.csv")
eccas_exports_global = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_Global.csv")
eccas_export_destinations = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_Des.csv")
eccas_debt_china = pd.read_excel("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Filtered_Debt_Data_2024.xlsx")
eccas_contracts_china = pd.read_excel("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Filtered_Contract_Data_2024.xlsx")

eccas_trade = eccas_exports_china.merge(eccas_exports_global, on=["Year", "HS2 ID"], suffixes=("_China", "_Global"))
eccas_trade["China_Trade_Share"] = eccas_trade["Trade Value_China"] / eccas_trade["Trade Value_Global"]

eccas_trade_summary = eccas_trade.groupby("Year")["China_Trade_Share"].mean().reset_index()
eccas_trade_summary["Year"] = eccas_trade_summary["Year"].astype(int)

sns.set_style("whitegrid")
sns.set_palette("gray")

eccas_sector_summary = eccas_debt_china.groupby(["Year", "Sector"])["Loan (USD M)"].sum().unstack().fillna(0)
eccas_sector_summary["Year"] = eccas_sector_summary.index

eccas_sector_summary.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="Greys")
plt.title("Chinese Investment by Sector in Central Africa")
plt.xlabel("Year")
plt.ylabel("Total Loan (Million USD)")
plt.legend(title="Sector")
plt.savefig(os.path.join(output_dir, "investment_by_sector.png"))
plt.show()

eccas_exports_summary = eccas_exports_china.groupby("Section")["Trade Value"].sum().sort_values(ascending=False)
eccas_exports_summary.plot(kind="bar", figsize=(12, 6), color="black")
plt.title("ECCAS Exports to China by Product Type (2000-2020)")
plt.xlabel("Product Section")
plt.ylabel("Total Trade Value (Million USD)")
plt.savefig(os.path.join(output_dir, "exports_to_china.png"))
plt.show()

eccas_merged = eccas_trade_summary.merge(eccas_debt_china.groupby("Year")["Loan (USD M)"].sum().reset_index(), on="Year")
X = sm.add_constant(eccas_merged["Loan (USD M)"])
y = eccas_merged["China_Trade_Share"]
model = sm.OLS(y, X).fit()

eccas_merged.to_csv(os.path.join(output_dir, "investment_trade_correlation.csv"), index=False)

eccas_gdp_trade = eccas_export_destinations.groupby("Year")["Trade Value"].sum().reset_index()
eccas_gdp_trade = eccas_gdp_trade.merge(eccas_debt_china.groupby("Year")["Loan (USD M)"].sum().reset_index(), on="Year")

X_gdp = sm.add_constant(eccas_gdp_trade["Loan (USD M)"])
y_gdp = eccas_gdp_trade["Trade Value"]
model_gdp = sm.OLS(y_gdp, X_gdp).fit()

eccas_gdp_trade.to_csv(os.path.join(output_dir, "gdp_investment_analysis.csv"), index=False)


with open(os.path.join(output_dir, "hypothesis_4_results.txt"), "w") as f:
    f.write("Investment vs. Trade Share Regression:\n")
    f.write(model.summary().as_text() + "\n\n")
    f.write("Investment vs. GDP Growth Regression:\n")
    f.write(model_gdp.summary().as_text() + "\n")

print(f"Analysis complete. Results saved to '{output_dir}'.")
