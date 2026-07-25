import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import jarque_bera

df = pd.read_csv('data/user_level_ai_adoption_enriched.csv')

# Clean industry column name string if needed
df['Industry_Clean'] = df['Industry'].str.replace(' & ', '_').str.replace(' ', '_')

# Formula API with ChatGPT (OpenAI) as Primary_AI_Tool reference and Creative_Design as Industry reference
formula_a = "Productivity_Gain_Percent ~ Daily_Token_Usage + Tasks_Automated_Per_Week + Experience_Years + C(Primary_AI_Tool, Treatment(reference='ChatGPT (OpenAI)')) + C(Industry_Clean, Treatment(reference='Creative_Design'))"

# Fit OLS with HC3 Heteroskedasticity Robust Standard Errors
model_hc3 = smf.ols(formula=formula_a, data=df).fit(cov_type='HC3')

print("=== STATSMODELS OLS INFERENTIAL SUMMARY TABLE (HC3 Robust SE) ===")
print(model_hc3.summary())

# Residual Diagnostics
residuals = model_hc3.resid
bp_test = het_breuschpagan(residuals, model_hc3.model.exog)
jb_test = jarque_bera(residuals)

print("\n=== RESIDUAL DIAGNOSTICS & HETEROSKEDASTICITY TESTS ===")
print(f"Breusch-Pagan LM Stat  : {bp_test[0]:.4f}, p-value: {bp_test[1]:.4e}")
print(f"Jarque-Bera Stat       : {jb_test[0]:.4f}, p-value: {jb_test[1]:.4e}")
print(f"Residual Std Error (RSE): {np.sqrt(model_hc3.mse_resid):.4f}")
print(f"R²                     : {model_hc3.rsquared:.4f}")
print(f"Adjusted R²            : {model_hc3.rsquared_adj:.4f}")
print(f"AIC                    : {model_hc3.aic:.2f}")
print(f"BIC                    : {model_hc3.bic:.2f}")
