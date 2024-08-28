from pymongo import MongoClient

try:
    client = MongoClient('mongodb+srv://hareshadmin:hareshkurade@cluster0.x70xv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    print("Connected successfully!")
    # Optionally list databases to test
    print(client.list_database_names())
except Exception as e:
    print(f"Connection failed: {e}")
