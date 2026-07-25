import os
import pandas as pd
import numpy as np
from scipy.stats import f_oneway
import statsmodels.formula.api as smf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def test_micro_dataset_integrity():
    micro_path = os.path.join(DATA_DIR, 'user_level_ai_adoption.csv')
    assert os.path.exists(micro_path), "Micro dataset file user_level_ai_adoption.csv missing"
    
    df = pd.read_csv(micro_path)
    assert len(df) == 15000, f"Expected 15,000 rows, got {len(df)}"
    assert df.isnull().sum().sum() == 0, "Micro dataset contains missing values"
    assert df['User_ID'].duplicated().sum() == 0, "Duplicate User_IDs found in micro dataset"
    assert df['Daily_Token_Usage'].min() > 0, "Daily token usage must be positive"
    assert df['Productivity_Gain_Percent'].min() >= 0, "Productivity gain must be non-negative"

def test_macro_dataset_integrity():
    macro_path = os.path.join(DATA_DIR, 'ai_adoption_productivity_2021_2026.csv')
    assert os.path.exists(macro_path), "Macro dataset file ai_adoption_productivity_2021_2026.csv missing"
    
    df = pd.read_csv(macro_path)
    assert len(df) == 402, f"Expected 402 macro rows, got {len(df)}"
    assert df.isnull().sum().sum() == 0, "Macro dataset contains missing values"
    assert df['YearMonth'].nunique() == 67, "Expected 67 unique timeline points"

def test_feature_engineering_outputs():
    enriched_path = os.path.join(DATA_DIR, 'user_level_ai_adoption_enriched.csv')
    assert os.path.exists(enriched_path), "Enriched dataset file missing"
    
    df = pd.read_csv(enriched_path)
    required_cols = ['Token_Per_Task', 'Experience_Group', 'Productivity_Tier', 'Adoption_Year']
    for col in required_cols:
        assert col in df.columns, f"Engineered column {col} missing in enriched dataset"
    
    # Token_Per_Task ratio sanity check
    expected_ratio = df['Daily_Token_Usage'] / df['Tasks_Automated_Per_Week']
    np.testing.assert_allclose(df['Token_Per_Task'].values, expected_ratio.values, rtol=1e-5)

def test_model_a_full_rank():
    enriched_path = os.path.join(DATA_DIR, 'user_level_ai_adoption_enriched.csv')
    df = pd.read_csv(enriched_path)
    
    X_df = pd.get_dummies(df[['Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years', 'Primary_AI_Tool', 'Industry']], drop_first=True).astype(float)
    X_df.insert(0, 'Intercept', 1.0)
    
    matrix_rank = np.linalg.matrix_rank(X_df.values)
    expected_cols = X_df.shape[1]
    
    assert matrix_rank == expected_cols, f"Model A matrix rank deficiency detected: Rank {matrix_rank} vs {expected_cols} cols"
    assert expected_cols == 15, f"Expected 15 columns in Model A, got {expected_cols}"

def test_anova_and_eta_squared():
    enriched_path = os.path.join(DATA_DIR, 'user_level_ai_adoption_enriched.csv')
    df = pd.read_csv(enriched_path)
    
    exp_groups = ['Junior (0-3 yrs)', 'Mid-Level (4-8 yrs)', 'Senior (9-15 yrs)', 'Veteran (>15 yrs)']
    group_data = [df[df['Experience_Group'] == eg]['Productivity_Gain_Percent'].values for eg in exp_groups]
    
    f_stat, p_val = f_oneway(*group_data)
    assert round(f_stat, 4) == 0.6962, f"Expected ANOVA F-stat 0.6962, got {f_stat:.4f}"
    assert round(p_val, 4) == 0.5542, f"Expected ANOVA p-val 0.5542, got {p_val:.4f}"
    
    overall_mean = df['Productivity_Gain_Percent'].mean()
    ss_between = sum(len(g) * (np.mean(g) - overall_mean)**2 for g in group_data)
    ss_within = sum(sum((x - np.mean(g))**2 for x in g) for g in group_data)
    eta_sq = ss_between / (ss_between + ss_within)
    
    assert round(eta_sq, 6) == 0.000139, f"Expected Eta-squared 0.000139, got {eta_sq:.6f}"

def test_ols_hc3_regression():
    enriched_path = os.path.join(DATA_DIR, 'user_level_ai_adoption_enriched.csv')
    df = pd.read_csv(enriched_path)
    df['Industry_Clean'] = df['Industry'].str.replace(' & ', '_').str.replace(' ', '_')
    
    formula = "Productivity_Gain_Percent ~ Daily_Token_Usage + Tasks_Automated_Per_Week + Experience_Years + C(Primary_AI_Tool, Treatment(reference='ChatGPT (OpenAI)')) + C(Industry_Clean, Treatment(reference='Creative_Design'))"
    model = smf.ols(formula=formula, data=df).fit(cov_type='HC3')
    
    assert round(model.rsquared, 4) == 0.8074, f"Expected R2 0.8074, got {model.rsquared:.4f}"
    assert round(model.rsquared_adj, 4) == 0.8072, f"Expected Adj R2 0.8072, got {model.rsquared_adj:.4f}"
    assert round(model.params['Daily_Token_Usage'], 6) == 0.001071
