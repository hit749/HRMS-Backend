from pymongo import MongoClient

uri = f"mongodb+srv://{DB_HOST}}:admin@hrms.kt85gff.mongodb.net/hrms?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)

try:
    print(client.server_info())
    print("Connected successfully")
except Exception as e:
    print("Connection failed:", e)