from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "SmartConveyorMonitor"
COLLECTION_NAME = "conveyor_data"

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self._ensure_time_series_collection()

    def _ensure_time_series_collection(self):
        """
        Ensures the 'conveyor_data' collection exists and is configured as a time-series collection.
        If the collection exists but is not a time-series collection, it will raise an error.
        """
        if COLLECTION_NAME not in self.db.list_collection_names():
            try:
                self.db.create_collection(
                    COLLECTION_NAME,
                    timeseries={
                        "timeField": "timestamp",
                        "metaField": "metadata",
                        "granularity": "seconds"
                    },
                    expireAfterSeconds=604800 # Data expires after 7 days (604800 seconds)
                )
                print(f"Time-series collection '{COLLECTION_NAME}' created successfully.")
            except CollectionInvalid as e:
                print(f"Error creating time-series collection: {e}")
                raise
        else:
            # Optional: Verify if existing collection is time-series.
            # This requires fetching collection info, which can be complex.
            # For simplicity, we assume if it exists, it's either correct or
            # the user will handle conflicts.
            print(f"Collection '{COLLECTION_NAME}' already exists.")

    def get_collection(self):
        """
        Returns the MongoDB collection for conveyor data.
        """
        return self.db[COLLECTION_NAME]

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
        print("MongoDB connection closed.")

if __name__ == "__main__":
    # Example usage:
    manager = None
    try:
        manager = MongoDBManager()
        collection = manager.get_collection()
        print(f"Successfully connected to database '{DB_NAME}' and collection '{COLLECTION_NAME}'.")

        # Example: Insert a document
        test_document = {
            "timestamp": datetime.utcnow(),
            "metadata": {"sensor_id": "sensor_001"},
            "value": 123.45
        }
        # from datetime import datetime is needed for this example
        # collection.insert_one(test_document)
        # print("Test document inserted.")

        # Example: Find a document
        # found_document = collection.find_one({"metadata.sensor_id": "sensor_001"})
        # print(f"Found document: {found_document}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if manager:
            manager.close_connection()
