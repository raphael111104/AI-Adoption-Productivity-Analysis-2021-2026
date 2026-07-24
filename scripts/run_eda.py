import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math

# Create output folder for charts
charts_dir = "../charts"
os.makedirs(charts_dir, exist_ok=True)

print("=== STARTING PHASE 2 & 3: EDA, STATISTICAL TESTING & FEATURE ENGINEERING ===")

# Load Datasets
df_macro = pd.read_csv('../data/ai_adoption_productivity_2021_2026.csv')
df_micro = pd.read_csv('../data/user_level_ai_adoption.csv')

# -------------------------------------------------------------
# FEATURE ENGINEERING (Phase 3)
# -------------------------------------------------------------
print("\n[1] Executing Feature Engineering on Micro Dataset...")

# 1. Token Efficiency Ratio (Tokens per task automated)
df_micro['Token_Per_Task'] = np.where(
    df_micro['Tasks_Automated_Per_Week'] > 0,
    df_micro['Daily_Token_Usage'] / df_micro['Tasks_Automated_Per_Week'],
    np.nan
)

# 2. Experience Group
bins_exp = [-1, 3, 8, 15, 100]
labels_exp = ['Junior (0-3 yrs)', 'Mid-Level (4-8 yrs)', 'Senior (9-15 yrs)', 'Veteran (>15 yrs)']
df_micro['Experience_Group'] = pd.cut(df_micro['Experience_Years'], bins=bins_exp, labels=labels_exp)

# 3. Productivity Tier
bins_prod = [-1, 10, 25, 100]
labels_prod = ['Low Gain (<10%)', 'Moderate Gain (10-25%)', 'High Gain (>25%)']
df_micro['Productivity_Tier'] = pd.cut(df_micro['Productivity_Gain_Percent'], bins=bins_prod, labels=labels_prod)

# 4. Adoption Cohort Year
df_micro['Adoption_Date'] = pd.to_datetime(df_micro['Adoption_Date'])
df_micro['Adoption_Year'] = df_micro['Adoption_Date'].dt.year

print("Created features: 'Token_Per_Task', 'Experience_Group', 'Productivity_Tier', 'Adoption_Year'")

# Save enriched dataset
enriched_file = '../data/user_level_ai_adoption_enriched.csv'
df_micro.to_csv(enriched_file, index=False)
print(f"Saved enriched micro dataset to '{enriched_file}'")

# -------------------------------------------------------------
# STATISTICAL HYPOTHESIS TESTING (Phase 2)
# -------------------------------------------------------------
print("\n[2] Executing Statistical Hypothesis Testing...")

def calc_p_value_pearson(r, n):
    if abs(r) >= 1.0:
        return 0.0
    t_stat = r * math.sqrt((n - 2) / (1 - r**2))
    # Approximation for large n
    return 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))

n = len(df_micro)

# Hypothesis 1: Token Usage vs Productivity Gain
corr_token = df_micro['Daily_Token_Usage'].corr(df_micro['Productivity_Gain_Percent'])
p_val_token = calc_p_value_pearson(corr_token, n)
print(f"H1 - Pearson Correlation (Token Usage vs Productivity Gain): r = {corr_token:.4f}, p-val = {p_val_token:.4e}")

# Hypothesis 2: Tasks Automated vs Productivity Gain
corr_task = df_micro['Tasks_Automated_Per_Week'].corr(df_micro['Productivity_Gain_Percent'])
p_val_task = calc_p_value_pearson(corr_task, n)
print(f"H2 - Pearson Correlation (Tasks Automated vs Productivity Gain): r = {corr_task:.4f}, p-val = {p_val_task:.4e}")

# Hypothesis 3: Experience Years vs Productivity Gain
corr_exp = df_micro['Experience_Years'].corr(df_micro['Productivity_Gain_Percent'])
p_val_exp = calc_p_value_pearson(corr_exp, n)
print(f"H3 - Pearson Correlation (Experience Years vs Productivity Gain): r = {corr_exp:.4f}, p-val = {p_val_exp:.4e}")

# Group summaries
print("\nSummary Productivity Gain by Experience Group:")
print(df_micro.groupby('Experience_Group', observed=False)['Productivity_Gain_Percent'].agg(['count', 'mean', 'std', 'median']))

print("\nSummary Productivity Gain by AI Tool:")
print(df_micro.groupby('Primary_AI_Tool')['Productivity_Gain_Percent'].agg(['count', 'mean', 'std', 'median']))

# -------------------------------------------------------------
# GENERATING EDA CHARTS (Matplotlib)
# -------------------------------------------------------------
print("\n[3] Generating Visualizations...")

plt.style.use('ggplot')

# Chart 1: AI Tool Market Share & Avg Productivity Gain
fig, ax1 = plt.subplots(figsize=(10, 5))
tool_stats = df_micro.groupby('Primary_AI_Tool').agg(
    User_Count=('User_ID', 'count'),
    Avg_Productivity=('Productivity_Gain_Percent', 'mean')
).sort_values('User_Count', ascending=False)

bars = ax1.bar(tool_stats.index, tool_stats['User_Count'], color='#3498db', alpha=0.85, label='User Count')
ax1.set_title('AI Tool Adoption: Active User Count & Avg Productivity Gain (%)', fontsize=13, fontweight='bold', pad=15)
ax1.set_ylabel('Total Active Users (Sample)', color='#2980b9', fontweight='bold')
ax1.set_xlabel('Primary AI Tool', fontweight='bold')
plt.xticks(rotation=25)

ax2 = ax1.twinx()
ax2.plot(tool_stats.index, tool_stats['Avg_Productivity'], color='#e74c3c', marker='o', linewidth=2.5, label='Avg Productivity %')
ax2.set_ylabel('Avg Productivity Gain (%)', color='#c0392b', fontweight='bold')
ax2.grid(False)

plt.tight_layout()
chart1_path = os.path.join(charts_dir, 'chart1_ai_tools_adoption.png')
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"Saved: {chart1_path}")

# Chart 2: Daily Token Usage vs Productivity Gain (Scatter plot)
plt.figure(figsize=(9, 5))
plt.scatter(df_micro['Daily_Token_Usage'], df_micro['Productivity_Gain_Percent'], alpha=0.15, color='#2c3e50', edgecolors='none', s=20)
# Trend line
z = np.polyfit(df_micro['Daily_Token_Usage'], df_micro['Productivity_Gain_Percent'], 1)
p = np.poly1d(z)
plt.plot(df_micro['Daily_Token_Usage'], p(df_micro['Daily_Token_Usage']), color='#e74c3c', linewidth=2.5, label=f'Trend Line (r={corr_token:.2f})')

plt.title('Daily Token Usage vs. Productivity Gain (%)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Daily Token Usage', fontweight='bold')
plt.ylabel('Productivity Gain (%)', fontweight='bold')
plt.legend()
plt.tight_layout()
chart2_path = os.path.join(charts_dir, 'chart2_token_vs_productivity.png')
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"Saved: {chart2_path}")

# Chart 3: Productivity Gain by Industry
plt.figure(figsize=(10, 5))
ind_stats = df_micro.groupby('Industry')['Productivity_Gain_Percent'].mean().sort_values(ascending=False)
plt.barh(ind_stats.index, ind_stats.values, color='#2ecc71', alpha=0.85)
plt.title('Average Productivity Gain (%) by Industry', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Average Productivity Gain (%)', fontweight='bold')
plt.ylabel('Industry', fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
chart3_path = os.path.join(charts_dir, 'chart3_productivity_by_industry.png')
plt.savefig(chart3_path, dpi=300)
plt.close()
print(f"Saved: {chart3_path}")

# Chart 4: Macro Trend (2021 - 2026)
df_macro['YearMonth_Dt'] = pd.to_datetime(df_macro['YearMonth'])
macro_trend = df_macro.groupby('YearMonth_Dt').agg({
    'Global Active Users (Millions)': 'sum',
    'Productivity Gain (%)': 'mean'
}).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(macro_trend['YearMonth_Dt'], macro_trend['Global Active Users (Millions)'], color='#2980b9', linewidth=2.5, label='Global Users (M)')
ax1.set_title('Macro Trend: Global Active Users & Productivity Gain (2021–2026)', fontsize=13, fontweight='bold', pad=15)
ax1.set_ylabel('Global Active Users (Millions)', color='#2980b9', fontweight='bold')
ax1.set_xlabel('Period', fontweight='bold')

ax2 = ax1.twinx()
ax2.plot(macro_trend['YearMonth_Dt'], macro_trend['Productivity Gain (%)'], color='#27ae60', linewidth=2, linestyle='--', label='Avg Productivity %')
ax2.set_ylabel('Avg Productivity Gain (%)', color='#27ae60', fontweight='bold')
ax2.grid(False)

plt.tight_layout()
chart4_path = os.path.join(charts_dir, 'chart4_macro_trend.png')
plt.savefig(chart4_path, dpi=300)
plt.close()
print(f"Saved: {chart4_path}")

print("\n=== EDA & STATISTICAL ANALYSIS COMPLETED SUCCESSFULLY ===")
