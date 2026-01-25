# Git Setup Instructions

## Inicijalizacija Git Repozitorija

### 1. Inicijaliziraj Git
```bash
git init
```

### 2. Dodaj sve fajlove
```bash
git add .
```

### 3. Napravi prvi commit
```bash
git commit -m "Initial commit: Quahwa Analytics Dashboard"
```

### 4. Dodaj remote repository (GitHub/GitLab)
```bash
# Za GitHub:
git remote add origin https://github.com/your-username/quahwa-analytics.git

# Ili za privatni repo:
git remote add origin git@github.com:your-username/quahwa-analytics.git
```

### 5. Push na GitHub
```bash
git branch -M main
git push -u origin main
```

## Struktura Projekta

```
Quahwa/
├── .gitignore              # Git ignore file
├── LICENSE                 # MIT License
├── README.md              # Glavna dokumentacija
├── requirements.txt       # Python zavisnosti
├── example_usage.py       # Primjer korištenja
├── dashboard/             # Streamlit aplikacija
│   └── app.py
├── src/                   # Izvorni kod
│   ├── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── data_loader.py
│   └── analysis/
│       ├── __init__.py
│       ├── time_analysis.py
│       └── sales_analysis.py
└── data/                  # Folder za podatke (ignored)
```

## Važno

- Excel fajlovi (.xlsx, .xls) su ignorisani u `.gitignore`
- Nemoj push-ovati osjetljive podatke
- Virtual environment folderi (venv/, env/) su također ignorisani

## GitHub Repository Settings

Preporučene opcije:
- **Visibility**: Private (ako sadrži poslovne podatke)
- **Description**: "Analytics Dashboard for Sales Data Analysis - Streamlit & Plotly"
- **Topics**: `streamlit`, `analytics`, `dashboard`, `plotly`, `python`, `data-analysis`

## Collaborators

Dodaj kolaboratore preko GitHub Settings → Manage access
