\# 📊 E-Commerce Sales Storytelling Dashboard



> An interactive data storytelling dashboard built with \*\*Python, Pandas, and Plotly Dash\*\* — transforming raw sales data into actionable business insights.



!\[Dashboard Preview](https://img.shields.io/badge/Status-Live-brightgreen)

!\[Python](https://img.shields.io/badge/Python-3.8+-blue)

!\[Plotly](https://img.shields.io/badge/Plotly-Dash-purple)

!\[Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)



\---



\## 🚀 Live Features



| Feature | Description |

|---|---|

| 💰 KPI Cards | Total Revenue, Orders, AOV, YoY Growth |

| 🎛️ Interactive Filters | Filter by Region, Category, and Year |

| 📈 Monthly Trend | Revenue trend across 2 years |

| 🏆 Category Analysis | Which category drives the most revenue |

| 🌍 Regional Breakdown | Donut chart of revenue by region |

| 📊 YoY Comparison | 2023 vs 2024 monthly bar chart |

| 🥇 Top Products | Top 10 products by revenue |

| 🔍 Discount Impact | Does discounting help or hurt revenue? |

| 📖 Narrative Section | Auto-generated data story \& insights |



\---



\## 🛠️ Tech Stack



\- \*\*Python 3.x\*\* — Core language

\- \*\*Pandas\*\* — Data cleaning \& feature engineering

\- \*\*Plotly\*\* — Interactive charts

\- \*\*Dash\*\* — Web dashboard framework



\---



\## 📁 Project Structure

```

ecommerce-sales-dashboard/

├── data/

│   ├── generate\_data.py      ← Generates 1500-row dataset

│   └── ecommerce\_sales.csv   ← Generated sales data

├── src/

│   ├── data\_loader.py        ← Data cleaning \& feature engineering

│   ├── kpis.py               ← KPI calculation functions

│   └── charts.py             ← All 6 Plotly chart functions

├── assets/

│   └── style.css             ← Dashboard styling

├── app.py                    ← Main Dash application

├── requirements.txt          ← Dependencies

└── README.md

```



\---



\## ⚡ Quick Start

```bash

\# 1. Clone the repo

git clone https://github.com/Ayushi-1205/ecommerce-sales-dashboard.git

cd ecommerce-sales-dashboard



\# 2. Create virtual environment

python -m venv venv

venv\\Scripts\\activate        # Windows

source venv/bin/activate     # Mac/Linux



\# 3. Install dependencies

pip install -r requirements.txt



\# 4. Generate the dataset

python data/generate\_data.py



\# 5. Run the dashboard

python app.py

```



Then open 👉 \*\*http://127.0.0.1:8050\*\*



\---



\## 📊 Key Business Insights



\- 📈 \*\*1.97% YoY Growth\*\* — Revenue grew from $555K (2023) to $566K (2024)

\- 🏆 \*\*Electronics\*\* dominates revenue — highest AOV category

\- 🌍 \*\*Regional gaps exist\*\* — opportunity to expand underperforming regions

\- 📅 \*\*Seasonality detected\*\* — peak months visible in trend chart

\- 🛒 \*\*AOV of $747\*\* — bundle strategies can push this higher



\---



\## 👩‍💻 Author



Built with ❤️ by \*\*Ayushi\*\* | \[GitHub](https://github.com/Ayushi-1205)

