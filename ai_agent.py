# import os
# from sqlalchemy import create_engine, text

# cube_secret = "20d4b545cafb72c24f349a11707ab585ded8ddb083e95d7fd26a6a5f2d1b9062426bd5d7922fa03d0917feece998d1bfb53173b9fc120b2c222090219e2f7a06"
# cube_uri = "postgresql+pg8000://postgres:Nick1234@localhost:15432/Metricmind"
# engine = create_engine(cube_uri)

# if __name__ == "__main__":
#     try:
#         with engine.connect() as conn:
#             print("Running simple connectivity query...")
#             # Using double quotes preserves case sensitivity for Cube views/tables
#             query = text('SELECT * FROM "FctSales" LIMIT 5;')
#             rows = conn.execute(query).fetchall()
            
#             print("\n--- Results ---")
#             for row in rows:
#                 print(row)
#     except Exception as e:
#         print(f"\nConnection or Query Error: {e}")  


import os
import time
from google import genai

from sqlalchemy import create_engine, text

# 1. Configuration & Connection Setup
# Replace with your actual Gemini API key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

cube_uri = "postgresql+pg8000://postgres:Nick1234@localhost:15432/Metricmind"
engine = create_engine(cube_uri)

# Initialize the official Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Semantic Context Prompt for Gemini
SYSTEM_PROMPT = """
You are an expert data analyst assistant for an e-commerce platform called MetricMind. 
Your task is to convert natural language user questions into valid SQL queries that will run against a Cube semantic layer PostgreSQL API (port 15432).

### Database Schema & Semantic Model Context:
You have access to a primary cube called `FctSales` which is joined with three dimension cubes (`DimCustomer`, `DimProduct`, `DimRegion`).

1. **Cube Name:** `FctSales`
   - **Measures (Aggregations):**
     - `totalRevenue` (Total sales revenue amount)
     - `totalProfit` (Total profit amount)
     - `avgProfitMargin` (Average profit margin percentage)
     - `count` (Total number of orders)
     - `returnRate` (Percentage of returned orders)
   - **Dimensions:**
     - `orderId` (Unique order identifier, primary key)
     - `customerId` (Customer foreign key)
     - `paymentMethod` (e.g., Credit Card, PayPal, Cash on Delivery)
     - `orderStatus` (e.g., Delivered, Returned, Processing)
     - `returned` (Boolean: true/false)
     - `dateId` (Timestamp/Date of the order)

2. **Linked Dimension Cubes:**
   - **`DimCustomer`**: 
     - `customerSegment` (Segment type)
     - `membershipStatus` (Status of membership)
     - `gender` (Customer gender)
   - **`DimProduct`**: 
     - `category` (Product category)
     - `subcategory` (Product subcategory)
     - `brand` (Product brand)
   - **`DimRegion`**: 
     - `country` (Country name)
     - `city` (City name)
     - `warehouseRegion` (Region of the warehouse)

### Instructions for SQL Generation:
- Output **ONLY** a valid SQL query enclosed in standard markdown block (e.g., ```sql ... ```). No extra conversational text or explanations.
- Query from the table/cube name `"FctSales"` using double quotes to preserve casing if necessary, or select standard columns mapped via Cube.
- Use standard SQL syntax compatible with PostgreSQL / Cube SQL API (e.g., `LIMIT`, `GROUP BY`, `ORDER BY`).
- IMPORTANT FOR CUBE SQL: When selecting measures (like totalRevenue) alongside dimensions (like orderId), do NOT use manual GROUP BY clauses unless necessary. Cube automatically handles aggregation. Simply select the fields and order by the measure descending with a LIMIT clause.
"""



def generate_sql_from_gemini(user_question: str) -> str:
    """Sends the user question and schema prompt to Gemini with an auto-retry backoff loop."""
    models_to_try = ['gemini-3.8-flash', 'gemini-3.7-flash', 'gemini-3.5-flash']
    max_retries = 2
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"{SYSTEM_PROMPT}\n\nUser Question: {user_question}",
            )
            raw_text = response.text.strip()
            if "```sql" in raw_text:
                raw_text = raw_text.split("```sql")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            return raw_text
        except Exception as e:
            print(f"Model {model_name} unavailable, trying next... (Error: {e})")
            time.sleep(1)
            
    raise Exception("All fallback models are currently unavailable due to high demand. Please try again shortly.")

def execute_query(sql_query: str):
    """Executes the generated SQL query against the Cube SQL API via SQLAlchemy."""
    print(f"\n[Generated SQL]:\n{sql_query}\n")
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            print("--- Query Results ---")
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Execution Error: {e}")

if __name__ == "__main__":
    # Test natural language question
    user_query = "Show me the top 5 orders with the highest total revenue"
    print(f"User Question: '{user_query}'")
    
    # Step 1: Get SQL from Gemini
    sql = generate_sql_from_gemini(user_query)
    
    # Step 2: Execute against Cube API
    execute_query(sql)
