from topics.configuration.mongo_db_connection import MongoDBClient


if __name__ == "__main__":
    mongo_db_client = MongoDBClient()
    print(mongo_db_client.database.list_collection_names())