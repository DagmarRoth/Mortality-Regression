# The 34% Error: Regression Analysis

**County-level analysis of life expectancy disparities for American Indian and Alaska Native populations**

This repository contains the data analysis supporting the article "The 34% Error: America's Century of Miscounting Indigenous Deaths," which examines whether life expectancy gaps for Native American populations persist after controlling for socioeconomic factors.

## Key Finding

Counties with higher Native American populations have significantly shorter life expectancies than their income, education, poverty rates, age profiles, and population densities would predict. Each percentage-point increase in Native American population share is associated with 0.10 fewer years of life expectancy, independent of these socioeconomic factors (p < 0.001).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Data Sources](#data-sources)
- [Setup](#setup)
- [Running the Analysis](#running-the-analysis)
- [Output Files](#output-files)
- [Key Results](#key-results)
- [Methodology](#methodology)
- [Citation](#citation)

---

## Project Overview

This analysis addresses a critical question: **Is the life expectancy gap for American Indian and Alaska Native (AIAN) people explained by socioeconomic factors, or does something else contribute?**

Using county-level data for 3,062 U.S. counties, we estimate a regression model controlling for:
- Median household income
- Educational attainment (% bachelor's degree or higher)
- Poverty rate
- Median age
- Population density (log-transformed)
- Native American population share

The model explains 65% of variance in county life expectancy (R² = 0.650), and Native American population share remains highly significant even after controlling for all other factors.

---

## Repository Structure

```
├── data/
│   ├── county_outcomes.csv           # Life expectancy by county (from CHR)
│   ├── census_df.csv                 # Socioeconomic variables (from ACS)
│   ├── pop_density.csv              # Land area & density (from Gazetteer)
│   └── merged_df.csv                # Final analysis dataset
│
├── notebooks/
│   ├── 1-download-chr-data.ipynb    # Download County Health Rankings
│   ├── 2-explore-distributions.ipynb # EDA on life expectancy
│   ├── 3-download-census-data.ipynb  # Pull ACS variables via API
│   ├── 4-merge.ipynb                # Join datasets on FIPS codes
│   ├── 5-single-variable-regressions.ipynb  # Bivariate relationships
│   ├── 6-multivariable-regression.ipynb     # Full model estimation
│   └── 7-native-american-gap.ipynb  # Visualizations for article
│
├── scripts/
│   └── build_pop_density.py         # Join Gazetteer + population estimates
│
├── outputs/
│   ├── figures/                     # Charts for publication
│   └── tables/                      # Coefficient tables
│
├── raw_data/                        # Original source files (not in repo)
│   ├── 2025_Gaz_counties_national.txt
│   └── co-est2025-pop.csv
│
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── .env.example                     # Template for API keys
└── methodology.pdf                  # Full methodological documentation
```

---

## Data Sources

All data are publicly available:

### 1. County Health Rankings & Roadmaps (2024)
- **What**: Life expectancy at birth by county
- **Source**: https://www.countyhealthrankings.org
- **Coverage**: ~3,070 U.S. counties
- **Time period**: 2020-2022 mortality data
- **Access**: Download CSV from website (no API key required)

### 2. U.S. Census Bureau, American Community Survey 5-Year Estimates (2018-2022)
- **What**: Demographics and socioeconomic variables
- **Source**: https://api.census.gov/data/2022/acs/acs5
- **Coverage**: All U.S. counties
- **Variables pulled**:
  - B19013_001E: Median household income
  - B15003_*: Educational attainment (bachelor's degree+)
  - B17001_*: Poverty status
  - B03002_*: Race/ethnicity (NH white, NH Native American)
  - B01002_001E: Median age
  - B01003_001E: Total population
- **Access**: Requires free Census API key (get at https://api.census.gov/data/key_signup.html)

### 3. Census Gazetteer Files (2025)
- **What**: Land area by county
- **Source**: https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html
- **File**: `2025_Gaz_counties_national.txt`
- **Access**: Direct download (no API key)

### 4. Population Estimates (2025)
- **What**: Annual population estimates by county
- **Source**: https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html
- **File**: `co-est2025-pop.csv`
- **Access**: Direct download

---

## Setup

### Prerequisites
- Python 3.9+
- Jupyter Notebook or JupyterLab
- Census API key (free, get at https://api.census.gov/data/key_signup.html)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/native-american-life-expectancy-analysis.git
cd native-american-life-expectancy-analysis
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up your Census API key**
```bash
cp .env.example .env
# Edit .env and add your Census API key:
# CENSUS_API_KEY=your_key_here
```

### Python Dependencies
```
pandas>=2.0.0
numpy>=1.24.0
statsmodels>=0.14.0
matplotlib>=3.7.0
seaborn>=0.12.0
requests>=2.28.0
python-dotenv>=1.0.0
jupyter>=1.0.0
altair>=5.0.0  # for interactive visualizations
```

---

## Running the Analysis

The analysis follows a sequential pipeline. Run notebooks in order:

### Step 1: Download Life Expectancy Data
```bash
jupyter notebook notebooks/1-download-chr-data.ipynb
```
- Downloads County Health Rankings data
- Cleans and standardizes FIPS codes
- Outputs: `data/county_outcomes.csv`

### Step 2: Explore Distributions
```bash
jupyter notebook notebooks/2-explore-distributions.ipynb
```
- EDA on life expectancy (histograms, summary stats, outliers)
- Confirms normal distribution (validates OLS regression assumptions)

### Step 3: Download Census Data
```bash
jupyter notebook notebooks/3-download-census-data.ipynb
```
- Pulls ACS 5-year estimates via Census API
- Calculates derived variables (% bachelor's, % poverty, % Native American)
- Outputs: `data/census_df.csv`

**Note**: Requires Census API key in `.env` file.

### Step 4: Build Population Density
```bash
python scripts/build_pop_density.py
```
- Joins Census Gazetteer (land area) with population estimates
- Calculates population density (persons per square mile)
- Outputs: `data/pop_density.csv`

**Note**: Requires `2025_Gaz_counties_national.txt` and `co-est2025-pop.csv` in `raw_data/` directory.

### Step 5: Merge Datasets
```bash
jupyter notebook notebooks/4-merge.ipynb
```
- Joins life expectancy, Census, and density data on FIPS codes
- Inner join results in 3,062 counties with complete data
- Outputs: `data/merged_df.csv`

### Step 6: Single-Variable Regressions
```bash
jupyter notebook notebooks/5-single-variable-regressions.ipynb
```
- Bivariate relationships between each predictor and life expectancy
- Identifies correlations before multivariate modeling
- Generates scatterplots and simple regression coefficients

### Step 7: Multivariable Regression
```bash
jupyter notebook notebooks/6-multivariable-regression.ipynb
```
- **Main analysis**: Full 6-variable OLS model
- Compares nested models (socioeconomic-only vs. full)
- Generates coefficient table and model diagnostics
- Key output: Native American coefficient = -0.101 (p < 0.001)

### Step 8: Visualizations
```bash
jupyter notebook notebooks/7-native-american-gap.ipynb
```
- Creates publication-quality figures:
  1. Scatter plot: Residuals vs. Native American % (counties >20% in red)
  2. Bar chart: Top 10 counties with largest shortfall
- Interactive Altair visualizations for exploration

---

## Output Files

### Data Files
- `data/merged_df.csv`: Final analysis dataset (3,062 counties, 15 variables)

### Figures
- `outputs/figures/native_american_gap_scatter.png`: Main scatter plot showing counties below prediction line
- `outputs/figures/top_10_shortfall.png`: Counties with largest life expectancy shortfalls
- `outputs/figures/model_comparison.png`: Bar chart comparing R² across nested models

### Tables
- `outputs/tables/full_model_coefficients.csv`: Regression results with standard errors and p-values
- `outputs/tables/model_fit_statistics.csv`: R², adjusted R², AIC for model comparison

---

## Key Results

### Model Performance
- **R² = 0.650**: The six-variable model explains 65% of variance in county life expectancy
- **F(6, 3055) = 945.8, p < 0.001**: Model is highly significant overall

### Coefficient Estimates

| Variable | Coefficient | Std Error | p-value | Interpretation |
|----------|------------|-----------|---------|----------------|
| Median HH income (per $1,000) | +0.0001 | 0.00001 | < 0.001 | Higher income → longer life |
| % Bachelor's degree+ | +0.146 | 0.006 | < 0.001 | More education → longer life |
| % Below poverty | -0.156 | 0.011 | < 0.001 | More poverty → shorter life |
| **% Native American** | **-0.101** | **0.006** | **< 0.001** | **More NA → shorter life** |
| Median age | +0.021 | 0.008 | 0.008 | Older counties → slightly longer life |
| Log₁₀ pop density | -1.285 | 0.062 | < 0.001 | Denser counties → shorter life |

### Practical Interpretation
A county that is 50% Native American is predicted to have life expectancy **5.0 years shorter** than an otherwise identical county (same income, education, poverty, age, density) with 0% Native American population.

This gap persists after controlling for socioeconomic factors, pointing to structural factors beyond measured disadvantage.

---

## Methodology

### Sample
- **N = 3,062 counties** (97.4% of U.S. counties)
- 52 counties (1.7%) have Native American population share >20%
- 8 counties excluded due to missing life expectancy data
- 82 counties excluded due to missing Census data

### Model Specification
```
Life Expectancy = β₀ + β₁(Income) + β₂(Education) + β₃(Poverty) 
                + β₄(Native American %) + β₅(Age) + β₆(Log Density) + ε
```

**Estimation method**: Ordinary Least Squares (OLS)  
**Software**: statsmodels 0.14.0 (Python 3.9)

### Model Diagnostics
✓ Residuals approximately normal  
✓ No systematic pattern in residual plot  
✓ Variance inflation factors (VIF) < 4 for all predictors  
✓ Cook's distance < 0.5 for all observations (no influential outliers)

### Limitations
1. **Ecological inference**: County-level analysis cannot directly infer individual-level relationships
2. **Unmeasured confounding**: Healthcare access, discrimination, historical trauma not directly measured
3. **Cross-sectional design**: Cannot establish causation
4. **Temporal misalignment**: Life expectancy (2020-2022) includes COVID-19 period
5. **Geographic clustering**: High-NA counties concentrated in specific regions

See `methodology.pdf` for full documentation.

---

## Reproducing the Analysis

### Quick Start (Full Pipeline)
```bash
# 1. Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Add Census API key to .env
echo "CENSUS_API_KEY=your_key_here" > .env

# 3. Download external files (manual step)
# - Download County Health Rankings CSV → save as raw_data/chr_2024.csv
# - Download Census Gazetteer → save as raw_data/2025_Gaz_counties_national.txt
# - Download Population Estimates → save as raw_data/co-est2025-pop.csv

# 4. Run pipeline
jupyter notebook notebooks/1-download-chr-data.ipynb
jupyter notebook notebooks/2-explore-distributions.ipynb
jupyter notebook notebooks/3-download-census-data.ipynb
python scripts/build_pop_density.py
jupyter notebook notebooks/4-merge.ipynb
jupyter notebook notebooks/5-single-variable-regressions.ipynb
jupyter notebook notebooks/6-multivariable-regression.ipynb
jupyter notebook notebooks/7-native-american-gap.ipynb
```

### Expected Runtime
- Total pipeline: ~15-20 minutes on a standard laptop
- Census API download: ~2-3 minutes (rate limited)
- Model estimation: <1 minute

---

## Validating Results

### Sanity Checks

1. **Sample size check**:
```python
import pandas as pd
df = pd.read_csv('data/merged_df.csv')
assert len(df) == 3062, "Expected 3,062 counties"
```

2. **Coefficient sign check**:
```python
# Income should be positive (more $ → longer life)
# Poverty should be negative (more poverty → shorter life)
# Native American should be negative (residual gap)
```

3. **R² check**:
```python
# Should be ~0.65, indicating good model fit
```

### Common Issues

**Issue**: Census API returns 403 Forbidden  
**Solution**: Check that API key is in `.env` file and is valid

**Issue**: Merge results in wrong number of counties  
**Solution**: Ensure FIPS codes are zero-padded to 5 digits (e.g., "01001" not "1001")

**Issue**: Population density has extreme outliers  
**Solution**: This is expected. Log transformation in model handles skewness.

---


### Related Research

This analysis builds on the foundational work by:

**Arias et al. (2021)** corrected the 34% misclassification error in AIAN death certificates, establishing accurate baseline life expectancy figures.

**This analysis** extends that work by examining whether the documented gap persists after controlling for socioeconomic factors at the county level.

---

## License

Data: All source data are publicly available from U.S. government sources (see Data Sources section).

Code: [Choose appropriate license - MIT recommended for open science]

---

## Contact

**Questions about the analysis?**  
Dagmar Rothschild 
der2161@columbia.edu
MS in Data Journalism program, Columbia Journalism School

**Questions about data sources?**  
- County Health Rankings: https://www.countyhealthrankings.org/contact
- Census Bureau: https://www.census.gov/about/contact-us.html

---

## FAQ

**Q: Why 3,062 counties instead of 3,143?**  
A: After inner join on complete data, 8 counties lacked life expectancy estimates (very small population) and 82 lacked Census data (timing mismatches, e.g., county dissolutions).

**Q: Why log-transform population density but not other variables?**  
A: Population density is extremely right-skewed (range: 0.1 to 70,000+ per sq mi). Log transformation normalizes the distribution. Other variables are reasonably symmetric.

**Q: Why county-level instead of individual-level data?**  
A: Individual-level life expectancy data are not publicly available. County-level analysis allows us to identify structural patterns while being transparent about ecological inference limitations.

**Q: Does this prove that racism causes the gap?**  
A: The regression quantifies the gap after controlling for measured socioeconomic factors, but cannot establish specific causal mechanisms. The article combines statistical findings with qualitative evidence (interviews, case studies) to point toward plausible explanations.

**Q: What about Alaska Native villages?**  
A: Alaska's geography is unique. Many Native villages are census-designated places, not counties. This analysis aggregates to county-level, which may mask some variation in Alaska.

**Q: Can I use this methodology for other racial/ethnic groups?**  
A: Yes, with appropriate modifications. The framework (control for SES, examine residual gaps) is generalizable. Be mindful of group-specific measurement issues and historical context.

---

**Last updated**: [Date]  
**Repository**: [GitHub URL]  
**DOI**: [If archived on Zenodo/OSF]
