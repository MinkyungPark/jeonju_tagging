import pymongo

print(pymongo.__version__)

conn = pymongo.MongoClient(
    host="192.168.0.6",
    port=29019,
    username="amy",
    password="zhd!!@4557",
)
str_database_name = "test_db"
db = conn.get_database(str_database_name)

str_collection_name = "test_table"
db.drop_collection(str_collection_name)
collection = db.get_collection(str_collection_name)

collection.insert_one({"name": "amy", "age": 29})
collection.insert_one({"name": "29", "age": 3})

results = collection.find({"age": {"$gte": 20}})
for result in results:
    print(result)