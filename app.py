import streamlit as st
import sqlite3
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sarvam AI API configuration
SARVAM_API_KEY = os.getenv("9265dfae-35c2-41d1-b4c4-7f519587283d", "Bearer 9265dfae-35c2-41d1-b4c4-7f519587283d")
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"

def get_database_schema():
    """Get the database schema information"""
    conn = sqlite3.connect('sample_business.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_info = []
    for table in tables:
        table_name = table[0]
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info.append({
            'table': table_name,
            'columns': [{'name': col[1], 'type': col[2]} for col in columns]
        })
    
    conn.close()
    return schema_info

def clean_sql_query(query):
    """Clean up the SQL query by removing markdown formatting and extra whitespace"""
    # Remove markdown code block formatting
    query = query.replace('```sql', '').replace('```', '')
    # Remove extra whitespace and newlines
    query = ' '.join(query.split())
    return query.strip()

def generate_sql_query(natural_language_query, schema_info):
    """Generate SQL query using Sarvam AI"""
    
    # Create schema context
    schema_context = "Database Schema:\n"
    for table_info in schema_info:
        schema_context += f"\nTable: {table_info['table']}\n"
        schema_context += "Columns:\n"
        for col in table_info['columns']:
            schema_context += f"- {col['name']} ({col['type']})\n"
    
    # Prepare the prompt
    system_prompt = """You are a SQL expert. Given a database schema and a natural language question, 
    generate the corresponding SQL query. Only return the SQL query without any explanations or markdown formatting."""
    
    headers = {
        "Authorization": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{schema_context}\n\nQuestion: {natural_language_query}\n\nGenerate SQL query:"}
        ],
        "temperature": 0.1,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(SARVAM_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            sql_query = result["choices"][0]["message"]["content"].strip()
            return clean_sql_query(sql_query)
        else:
            st.error(f"Error from Sarvam AI API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error calling Sarvam AI API: {str(e)}")
        return None

def execute_sql_query(query):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect('sample_business.db')
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error executing SQL query: {str(e)}")
        return None

def main():
    st.title("📊 Text-to-SQL Query System")
    st.write("Ask questions about the business data in natural language!")
    
    # Get database schema
    schema_info = get_database_schema()
    
    # Display schema information in expander
    with st.expander("📚 Database Schema"):
        for table_info in schema_info:
            st.write(f"**Table: {table_info['table']}**")
            for col in table_info['columns']:
                st.write(f"- {col['name']} ({col['type']})")
    
    # User input
    user_query = st.text_area("Enter your question:", 
                             placeholder="Example: What are the top 5 products by sales?")
    
    if st.button("Generate SQL"):
        if user_query:
            with st.spinner("Generating SQL query..."):
                # Generate SQL query
                sql_query = generate_sql_query(user_query, schema_info)
                
                if sql_query:
                    # Display generated SQL
                    st.subheader("Generated SQL Query:")
                    st.code(sql_query, language="sql")
                    
                    # Execute query and display results
                    with st.spinner("Executing query..."):
                        results = execute_sql_query(sql_query)
                        if results is not None:
                            st.subheader("Query Results:")
                            st.dataframe(results)
        else:
            st.warning("Please enter a question!")

if __name__ == "__main__":
    main() 