import pandas as pd
import os 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.stats import pearsonr, norm

gdp_data = pd.read_csv('C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Merged_GDP.csv')

investment_data = pd.read_excel('C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Filtered_Debt_Data_2024.xlsx', engine='openpyxl')

infrastructure_sectors = ['Transportation', 'Information and Communication Technology', 'Industry and Trade/Services', 'Public Administration', 'Education', 'Health']
resource_sectors = ['Energy', 'Agriculture', 'Water/Sanitation/Waste']

infrastructure_investment = investment_data[investment_data['Sector'].isin(infrastructure_sectors)]
resource_investment = investment_data[investment_data['Sector'].isin(resource_sectors)]

infrastructure_investment_byear = infrastructure_investment.groupby('Year')['Loan (USD M)'].sum().reset_index()
resource_investment_byear = resource_investment.groupby('Year')['Loan (USD M)'].sum().reset_index()

merged_infrastructure_data = pd.merge(gdp_data, infrastructure_investment_byear, left_on='Year', right_on='Year', how='inner')
merged_resource_data = pd.merge(gdp_data, resource_investment_byear, left_on='Year', right_on='Year', how='inner')

infrastructure_corr, _ = pearsonr(merged_infrastructure_data['Loan (USD M)'], merged_infrastructure_data['Measure'])
resource_corr, _ = pearsonr(merged_resource_data['Loan (USD M)'], merged_resource_data['Measure'])

def fisher_r_to_z(r):
    return np.arctanh(r)

def fisher_z_to_r(z):
    return np.tanh(z)

z_infrastructure = fisher_r_to_z(infrastructure_corr)
z_resource = fisher_r_to_z(resource_corr)
diff_z = z_infrastructure - z_resource

n = len(merged_infrastructure_data)
se_diff_z = np.sqrt(1/(n-3) + 1/(n-3))
p_value = 2 * (1 - norm.cdf(np.abs(diff_z / se_diff_z)))

output_dir = 'C:\\Users\\charl\\Documents\\Python\\Diss_Data\\Diss_hy2_results'
os.makedirs(output_dir, exist_ok=True)
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(merged_infrastructure_data['Loan (USD M)'], merged_infrastructure_data['Measure'], color='grey')
plt.title('Infrastructure Investment vs GDP Growth')
plt.xlabel('Infrastructure Investment (USD M)')
plt.ylabel('GDP Growth')

plt.subplot(1, 2, 2)
plt.scatter(merged_resource_data['Loan (USD M)'], merged_resource_data['Measure'], color='grey')
plt.title('Resource Investment vs GDP Growth')
plt.xlabel('Resource Investment (USD M)')
plt.ylabel('GDP Growth')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'scatter_plots.png'))

correlations = {'Infrastructure': infrastructure_corr, 'Resource': resource_corr}
plt.figure(figsize=(8, 6))
plt.bar(correlations.keys(), correlations.values(), color='grey')
plt.title('Correlation Strengths')
plt.ylabel('Correlation Coefficient')
plt.savefig(os.path.join(output_dir, 'correlation_strengths.png'))

with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
    f.write(f"Infrastructure Investment Correlation with GDP Growth: {infrastructure_corr}\n")
    f.write(f"Resource Investment Correlation with GDP Growth: {resource_corr}\n")
    f.write(f"Difference in Correlations (z): {diff_z}\n")
    f.write(f"P-value for Difference in Correlations: {p_value}\n")

print(f"Analysis complete. Results saved to '{output_dir}'.")
