'''import os

print("Current Working Directory:", os.getcwd())
print("Files in this directory:", os.listdir())

db_path = "pharmacy.db"

if os.path.exists(db_path):
   os.remove(db_path)
   print("✅ pharmacy.db deleted successfully.")
else:
    print("❌ pharmacy.db does not exist.")'''
