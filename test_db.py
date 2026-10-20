# from sqlalchemy import create_engine, text

# # Notice Nick%40123 instead of Nick@123
# db_uri = "postgresql+pg8000://postgres:Nick%40123@localhost:5432/Metricmind"

# engine = create_engine(db_uri)

# if __name__ == "__main__":
#     with engine.connect() as conn:
#         print("Testing connection to analytics.dim_customer...")
#         result = conn.execute(text("SELECT * FROM analytics.dim_customer LIMIT 5;"))
#         for row in result:
#             print(row)


from google import genai

client = genai.Client(GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE")

for m in client.models.list():
  print(m.name)