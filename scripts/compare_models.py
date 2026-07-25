import pandas as pd
import numpy as np

df = pd.read_csv('data/user_level_ai_adoption_enriched.csv')

def fit_ols(X_df, y):
    X = X_df.values.astype(float)
    feature_names = X_df.columns
    n, k = X.shape
    
    beta, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ beta
    res = y - y_pred
    rss = np.sum(res**2)
    tss = np.sum((y - np.mean(y))**2)
    
    r2 = 1 - (rss / tss)
    r2_adj = 1 - ((1 - r2) * (n - 1) / (n - k))
    rmse = np.sqrt(rss / n)
    
    # Log-likelihood under normality
    log_lh = -0.5 * n * (np.log(2 * np.pi) + np.log(rss / n) + 1)
    aic = 2 * k - 2 * log_lh
    bic = k * np.log(n) - 2 * log_lh
    cond_num = np.linalg.cond(X)
    
    # VIF for key numerical predictors
    vifs = {}
    num_cols = ['Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years']
    for col in num_cols:
        if col in X_df.columns:
            col_idx = X_df.columns.get_loc(col)
            y_vif = X[:, col_idx]
            X_other = np.delete(X, col_idx, axis=1)
            beta_vif, _, _, _ = np.linalg.lstsq(X_other, y_vif, rcond=None)
            r2_vif = 1 - (np.sum((y_vif - X_other @ beta_vif)**2) / np.sum((y_vif - np.mean(y_vif))**2))
            vifs[col] = 1 / (1 - r2_vif) if (1 - r2_vif) > 1e-10 else np.inf
            
    return {
        'n': n, 'k': k, 'rank': rank, 'rank_deficiency': k - rank,
        'r2': r2, 'r2_adj': r2_adj, 'rss': rss, 'rmse': rmse,
        'log_lh': log_lh, 'aic': aic, 'bic': bic, 'cond_num': cond_num,
        'vifs': vifs, 'beta': dict(zip(feature_names, beta))
    }

y = df['Productivity_Gain_Percent'].values

# Model A (Industry, excluding Job_Role)
X_a = pd.get_dummies(df[['Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years', 'Primary_AI_Tool', 'Industry']], drop_first=True).astype(float)
X_a.insert(0, 'Intercept', 1.0)

# Model B (Job_Role, excluding Industry)
X_b = pd.get_dummies(df[['Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years', 'Primary_AI_Tool', 'Job_Role']], drop_first=True).astype(float)
X_b.insert(0, 'Intercept', 1.0)

res_a = fit_ols(X_a, y)
res_b = fit_ols(X_b, y)

print("=== MODEL COMPARISON SUMMARY ===")
print(f"Metric                      | Model A (Industry)       | Model B (Job_Role)")
print("-" * 75)
print(f"Design Matrix Shape (n x k) | {res_a['n']} x {res_a['k']:2d}                 | {res_b['n']} x {res_b['k']:2d}")
print(f"Matrix Rank (Full Rank)     | {res_a['rank']:2d} (Deficiency: {res_a['rank_deficiency']})        | {res_b['rank']:2d} (Deficiency: {res_b['rank_deficiency']})")
print(f"Condition Number            | {res_a['cond_num']:.2e}               | {res_b['cond_num']:.2e}")
print(f"R²                          | {res_a['r2']:.6f}                 | {res_b['r2']:.6f}")
print(f"Adjusted R²                 | {res_a['r2_adj']:.6f}                 | {res_b['r2_adj']:.6f}")
print(f"RMSE                        | {res_a['rmse']:.6f}                 | {res_b['rmse']:.6f}")
print(f"AIC                         | {res_a['aic']:.2f}             | {res_b['aic']:.2f}")
print(f"BIC                         | {res_a['bic']:.2f}             | {res_b['bic']:.2f}")

print("\n=== VIF (VARIANCE INFLATION FACTORS) ===")
for col in ['Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years']:
    print(f"  {col:30s} | Model A VIF: {res_a['vifs'][col]:.4f} | Model B VIF: {res_b['vifs'][col]:.4f}")

print("\n=== COEFFICIENT STABILITY COMPARISON ===")
print(f"Feature                        | Model A Beta             | Model B Beta")
print("-" * 75)
shared_features = ['Intercept', 'Daily_Token_Usage', 'Tasks_Automated_Per_Week', 'Experience_Years'] + [c for c in X_a.columns if 'Primary_AI_Tool_' in c]
for f in shared_features:
    print(f"  {f:30s} | {res_a['beta'][f]:10.6f}               | {res_b['beta'][f]:10.6f}")
