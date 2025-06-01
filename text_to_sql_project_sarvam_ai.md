# 🧠 Text-to-SQL Query System for Business Analytics (Sarvam AI Powered)

## 📌 Objective
Build a tool that translates **natural language questions** into **SQL queries** against a relational database and returns results — powered by **Sarvam AI API**.

## 🎯 Purpose
Enable **non-technical analysts** to explore data and run SQL queries by simply typing questions in plain English.

## ✅ Deliverables Checklist

- [ ] Extract and document **database schema** metadata (tables, columns, types).
- [ ] Create and populate a **sample database** with **10 tables**, each with **≥ 50 rows**.
- [ ] Implement Text-to-SQL translation using **Sarvam AI API**.
- [ ] Evaluate translations using:
  - `Exact Match Accuracy`
  - `Execution Accuracy`
- [ ] Build a **Streamlit UI**:
  - User inputs question
  - Generated SQL is displayed
  - SQL query results are shown

## 🧰 Tools & Technologies

- **Sarvam AI API** – LLM backend for natural language to SQL
- **Streamlit** – UI for interaction
- **SQLite/PostgreSQL** – Sample relational database
- **Pandas/SQLAlchemy** – Data interaction



## 🧪 Evaluation Metrics

- **Exact Match Accuracy** – Check if generated SQL exactly matches ground truth.
- **Execution Accuracy** – Check if the output of generated SQL equals expected result.

## 📈 Success Criteria

- ≥ **85% execution accuracy** on held-out test questions
- Streamlit UI displays:
  - 📝 Natural language question
  - 🧾 Generated SQL
  - 📊 Result table
- Documented guide for adapting to new schemas

## 📚 Data Requirements

Use at least **10 tables**, each with **≥ 50 rows**.



## 🚀 Future Work

- Extend to support joins across multiple schemas
- Add feedback loop for correcting poor SQL outputs
- Enhance model prompts using schema-specific context

## 📄 License
This project is for educational and non-commercial use only.
