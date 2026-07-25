import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm

df = pd.read_csv('data/user_level_ai_adoption_enriched.csv')
df['Industry_Clean'] = df['Industry'].str.replace(' & ', '_').str.replace(' ', '_')

# Formula with Interaction Terms: Experience_Years * C(Primary_AI_Tool)
formula_int = "Productivity_Gain_Percent ~ Daily_Token_Usage + Tasks_Automated_Per_Week + Experience_Years * C(Primary_AI_Tool, Treatment(reference='ChatGPT (OpenAI)')) + C(Industry_Clean, Treatment(reference='Creative_Design'))"

model_int = smf.ols(formula=formula_int, data=df).fit(cov_type='HC3')

print("=== INTERACTION MODEL OLS REGRESSION SUMMARY (HC3 Robust SE) ===")
print(model_int.summary())

# F-test for joint significance of interaction terms
interaction_terms = [col for col in model_int.params.index if ':' in col]
f_test_int = model_int.f_test(interaction_terms)
print("\n=== JOINT HYPOTHESIS TEST FOR INTERACTION TERMS (Experience x Tool) ===")
print(f"F-statistic: {float(f_test_int.fvalue):.4f}, p-value: {float(f_test_int.pvalue):.4e}")
print(f"R² (Interaction Model): {model_int.rsquared:.6f} vs Baseline Model A: 0.807399")
print(f"Adjusted R²           : {model_int.rsquared_adj:.6f} vs Baseline Model A: 0.807219")
print(f"AIC                   : {model_int.aic:.2f} vs Baseline Model A: 91363.57")
