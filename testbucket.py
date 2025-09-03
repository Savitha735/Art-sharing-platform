# from supabase import create_client
# import os

# # Put your credentials directly here just for the test
# SUPABASE_URL = "https://spbvkonufmfmkvwiklsa.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNwYnZrb251Zm1mbWt2d2lrbHNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ4MjIxNjUsImV4cCI6MjA3MDM5ODE2NX0.N1Ima-y2JDu04MOqb8VokyPshOQNQwEZ9xiWQpi7PCE"

# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# # List all buckets in this project
# buckets = supabase.storage.list_buckets()
# print("Available buckets:", buckets)
# from google.cloud import vision
# import os

# print("Using key file:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

# client = vision.ImageAnnotatorClient()
# print("Client initialized successfully ✅")
import os
from dotenv import load_dotenv
# from google.cloud import vision

# # 👇 Put your JSON key path here
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\js200\Documents\ASP\vision-art-key.json"

# client = vision.ImageAnnotatorClient()
# print("✅ Vision client initialized successfully")
load_dotenv()
print(os.getenv("DEEPAI_KEY"))