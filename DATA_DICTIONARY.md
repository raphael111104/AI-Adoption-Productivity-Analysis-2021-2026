# 📚 Data Dictionary & Schema Specification

This document provides a comprehensive data dictionary and technical schema specification for all micro user-level and macro global datasets used in the **AI Adoption & Productivity Analysis (2021–2026)** project.

---

## 🔬 1. Micro User-Level Dataset (`data/user_level_ai_adoption.csv`)

- **Primary Scale**: Micro (Individual User Level)
- **Total Records**: 15,000 synthetic user profiles
- **Missing Value Ratio**: 0.00% across all columns (100% complete)
- **Primary Key**: `User_ID` (100% Unique)

| Field Name | Data Type | Range / Allowed Values | Description | Constraints & Business Rules |
|:-----------|:---------:|:----------------------:|:------------|:-----------------------------|
| `User_ID` | String | `USR_00001` - `USR_15000` | Unique identifier for each synthetic user record | Must be non-null and unique primary key |
| `Adoption_Date` | Date String | `2021-01-01` to `2026-06-30` | Date when the user adopted AI tools | Format: `YYYY-MM-DD`. Must fall within project timeline |
| `Industry` | Categorical | 6 sectors | Industry sector of the user's employer | Values: `Software Development`, `Finance`, `Healthcare`, `Marketing`, `Education`, `Creative & Design` |
| `Job_Role` | Categorical | 22 roles | Specific job title of the user | Strictly nested inside `Industry` (e.g. `Software Engineer` $\in$ `Software Development`) |
| `Daily_Token_Usage` | Integer | `411` to `58,989` | Average number of LLM/AI tokens consumed daily | Non-negative integer. Positive skewed (Power users in tail) |
| `Tasks_Automated_Per_Week` | Integer | `1` to `12` | Number of distinct work tasks automated weekly | Integer between 1 and 12 |
| `Productivity_Gain_Percent` | Float | `0.30%` to `84.90%` | Self-reported or measured percentage productivity gain | Non-negative float |
| `Experience_Years` | Float | `1.0` to `25.0` | Total professional work experience in years | Non-negative float |
| `Primary_AI_Tool` | Categorical | 7 tools | Primary AI software/tool utilized by the user | Values: `ChatGPT (OpenAI)`, `Claude (Anthropic)`, `Perplexity`, `Gemini (Google)`, `GitHub Copilot`, `Midjourney`, `DeepSeek` |
| `Satisfaction_Score` | Float | `1.0` to `5.0` | User satisfaction score with AI tooling | Likert scale float (1.0 to 5.0) |

---

## 🧪 2. Enriched Micro Dataset (`data/user_level_ai_adoption_enriched.csv`)

Includes all 10 columns from `user_level_ai_adoption.csv` plus 4 engineered features generated during Phase 3 feature engineering:

| Field Name | Data Type | Range / Allowed Values | Description | Derivation Logic |
|:-----------|:---------:|:----------------------:|:------------|:-----------------|
| `Token_Per_Task` | Float | `62.0` to `14,845.0` | Token efficiency ratio (tokens per task automated) | `Daily_Token_Usage / Tasks_Automated_Per_Week` |
| `Experience_Group` | Categorical | 4 tiers | Binned seniority group | Bins: `Junior (0-3 yrs)`, `Mid-Level (4-8 yrs)`, `Senior (9-15 yrs)`, `Veteran (>15 yrs)` |
| `Productivity_Tier` | Categorical | 3 tiers | Categorical gain tier | Bins: `Low Gain (<10%)`, `Moderate Gain (10-25%)`, `High Gain (>25%)` |
| `Adoption_Year` | Integer | `2021` to `2026` | Calendar year of AI adoption | `Year(Adoption_Date)` |

---

## 📈 3. Macro Global Dataset (`data/ai_adoption_productivity_2021_2026.csv`)

- **Primary Scale**: Macro (Global Monthly Timeline)
- **Total Records**: 402 timeline points (67 monthly periods across 6 sectors)
- **Timeline Range**: January 2021 to June 2026

| Field Name | Data Type | Range / Allowed Values | Description |
|:-----------|:---------:|:----------------------:|:------------|
| `YearMonth` | String | `2021-01` to `2026-06` | Monthly timeline identifier (`YYYY-MM`) |
| `Industry` | Categorical | 6 macro sectors | Values: `Software Development`, `Marketing & Content`, `Customer Support`, `Healthcare`, `Education`, `Finance & Legal` |
| `Primary Use Case` | String | Various text | Main application scenario (e.g. `Code Generation`, `Data Analysis`) |
| `Global Active Users (Millions)` | Float | `0.50` to `485.00` | Estimated global active user base in millions |
| `Average Tokens/User/Day` | Integer | `1,200` to `45,000` | Estimated global average daily token consumption per user |
| `Productivity Gain (%)` | Float | `1.5%` to `48.2%` | Aggregated global average productivity gain |
