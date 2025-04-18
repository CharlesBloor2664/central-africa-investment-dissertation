import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, chi2_contingency, ttest_rel, norm
import statsmodels.api as sm
import seaborn as sns
import os

output_dir = 'C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Diss_hy3_results'
os.makedirs(output_dir, exist_ok=True)

eccas_exports_china = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_China.csv")
eccas_exports_global = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_Global.csv")
eccas_export_destinations = pd.read_csv("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_Exports_Des.csv")
eccas_debt_china = pd.read_excel("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Filtered_Debt_Data_2024.xlsx")
eccas_contracts_china = pd.read_excel("C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Filtered_Contract_Data_2024.xlsx")

eccas_trade = eccas_exports_china.merge(eccas_exports_global, on=["Year", "HS2 ID"], suffixes=("_China", "_Global"))
eccas_trade["China_Trade_Share"] = eccas_trade["Trade Value_China"] / eccas_trade["Trade Value_Global"]

eccas_trade_summary = eccas_trade.groupby("Year")["China_Trade_Share"].mean().reset_index()
eccas_trade_summary["Year"] = eccas_trade_summary["Year"].astype(int)  # Ensure Year is an integer

sns.set_style("whitegrid")
sns.set_palette("gray")

plt.figure(figsize=(10, 5))
sns.lineplot(data=eccas_trade_summary, x="Year", y="China_Trade_Share", marker="o", color="black")
plt.title("China's Share of ECCAS Exports (2000-2020)")
plt.xlabel("Year")
plt.ylabel("Trade Share (%)")
plt.savefig(os.path.join(output_dir, "trade_dependency.png"))

eccas_debt_summary = eccas_debt_china.groupby("Year")["Loan (USD M)"].sum().reset_index()
eccas_debt_summary["Year"] = eccas_debt_summary["Year"].astype(int)  # Ensure Year is an integer

plt.figure(figsize=(10, 5))
sns.lineplot(data=eccas_debt_summary, x="Year", y="Loan (USD M)", marker="o", color="black")
plt.title("ECCAS Debt to China (2000-2020)")
plt.xlabel("Year")
plt.ylabel("Debt (Million USD)")
plt.savefig(os.path.join(output_dir, "debt_sustainability.png"))

eccas_merged = eccas_trade_summary.merge(eccas_debt_summary, on="Year")
X = sm.add_constant(eccas_merged["Loan (USD M)"])
y = eccas_merged["China_Trade_Share"]
model = sm.OLS(y, X).fit()

eccas_merged.to_csv(os.path.join(output_dir, "trade_debt_results.csv"), index=False)

X2 = sm.add_constant(eccas_merged[["Loan (USD M)"]])
model2 = sm.OLS(eccas_merged["China_Trade_Share"], X2).fit()
eccas_corr = eccas_merged.corr()
eccas_corr.to_csv(os.path.join(output_dir, "correlation_matrix.csv"))

eccas_contracts_china["Total Revenue"] = eccas_contracts_china.iloc[:, 1:].sum(axis=1)  # Sum revenues across all countries
eccas_revenue_summary = eccas_contracts_china[["Year", "Total Revenue"]]
eccas_revenue_summary["Year"] = eccas_revenue_summary["Year"].astype(int)  # Ensure Year is an integer

plt.figure(figsize=(10, 5))
sns.lineplot(data=eccas_revenue_summary, x="Year", y="Total Revenue", marker="o", color="black")
plt.title("Annual Revenues of Chinese Construction Projects in Africa")
plt.xlabel("Year")
plt.ylabel("Revenue (Million USD)")
plt.savefig(os.path.join(output_dir, "construction_revenue.png"))

revenue_merged = eccas_trade_summary.merge(eccas_revenue_summary, on="Year")
X3 = sm.add_constant(revenue_merged["Total Revenue"])
y3 = revenue_merged["China_Trade_Share"]
model3 = sm.OLS(y3, X3).fit()
revenue_merged.to_csv(os.path.join(output_dir, "revenue_trade_results.csv"), index=False)

with open(os.path.join(output_dir, "regression_results.txt"), "w") as f:
    f.write("Debt vs. Trade Share Regression:\n")
    f.write(model2.summary().as_text() + "\n\n")
    f.write("Revenue vs. Trade Share Regression:\n")
    f.write(model3.summary().as_text() + "\n")

print(f"Analysis complete. Results saved to '{output_dir}'.")
