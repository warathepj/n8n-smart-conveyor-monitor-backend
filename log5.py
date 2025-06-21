from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from datetime import datetime
from db import MongoDBManager
def print_last_5_data_points():
    try:
        db_manager = MongoDBManager()
        collection = db_manager.get_collection()

        # Fetch the last 5 data points
        last_5_data_points = list(collection.find().sort([("timestamp", -1)]).limit(5))

        # Print the data points
        for data_point in last_5_data_points:
            print(data_point)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'db_manager' in locals() and db_manager:
            db_manager.close_connection()

if __name__ == "__main__":
    print_last_5_data_points()
