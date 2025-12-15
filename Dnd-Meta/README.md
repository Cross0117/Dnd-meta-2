# D&D Meta Analysis

# Project Overview
This project is part of my Mid-Course Milestone Capstone for Code:You  
The goal is to demonstrate the full data analysis process — from loading raw data to cleaning, exploring, and visualizing it.

The dataset (`dnd_classes_races_starter.csv`) contains information about Dungeons & Dragons races, classes, subclasses, and related features. I use Python, pandas, and matplotlib to explore the data, clean it, and create meaningful visualizations.

---

# Repository Contents
- analysis.py → Main analysis script (load, clean, explore, and visualize data)
- Data/dnd_classes_races_starter.csv → Starter dataset
- Data/race_class_matrix.csv → Generated Race × Class pivot table
- Data/class_counts.png → Bar chart of class distribution
- Data/race_pie.png → Pie chart of race distribution
- Data/race_class_heatmap.png → Heatmap of Race × Class matrix
- Data/sessions_log.csv → Empty sessions log template (created by script)
- requirements.txt → List of Python dependencies
- README.md → Project documentation

---

# Setup Instructions
1. Clone this repository.  
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate # Mac/Linux
pip install -r requirements.txt
python analysis.py

---

# Data Cleaning
The raw dataset required some light cleaning and restructuring:
- Normalized **Race**, **Class**, and **Subclass** names to Title Case.  
- Converted `"Hit Die"` values (e.g., `d8`) into numeric values for easier comparison.  
- Mapped **Tier (Power Level)** into numbers (`Low=1, Mid=2, High=3`).  
- Mapped **Popularity** into numbers (`Low=1, Medium=2, High=3`).  
- Dropped exact duplicate rows if found.  

---

# Exploratory Data Analysis (EDA)
I used pandas methods like `.head()`, `.info()`, `.describe()`, and `.value_counts()` to understand the structure of the dataset and identify cleaning targets.

---

# Visualizations
# Class Distribution
![Class Distribution](Data/class_counts.png)

# Race Distribution
![Race Distribution](Data/race_pie.png)

# Race × Class Heatmap
![Race-Class Heatmap](Data/race_class_heatmap.png)

---

# Insights
- Certain classes (e.g., **Wizard** and **Fighter**) appear more frequently than others.  
- Some races show stronger alignment with specific classes (e.g., **Elves → Wizard**).  
- Popularity scores suggest that players favor **high-tier, high-popularity** builds.  
- The Race × Class matrix highlights imbalances — some combinations are rare or missing.  