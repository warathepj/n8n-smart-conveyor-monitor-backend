import matplotlib.pyplot as plt
import pandas as pd
from db import MongoDBManager
from datetime import datetime
import os

def create_chart():
    """
    Fetches data from MongoDB and creates a line chart of currentRate over time.
    Saves the chart to a file named chart.png.
    """
    db_manager = MongoDBManager()
    try:
        collection = db_manager.get_collection()

        # Fetch data from MongoDB
        data = list(collection.find())
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        return

    # Convert data to Pandas DataFrame
    df = pd.DataFrame(data)

    # Convert timestamp to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set timestamp as index
    df.set_index('timestamp', inplace=True)

    # Create the chart
    plt.figure(figsize=(12, 6))  # Adjust figure size as needed
    plt.plot(df['currentRate'], label='Current Rate')

    # Customize the chart
    plt.title('Conveyor Current Rate Over Time')
    plt.xlabel('Time')
    plt.ylabel('Current Rate')
    plt.legend()
    plt.grid(True)

    # Save the chart to a file
    # Create the chart directory if it doesn't exist
    chart_dir = 'backend/chart'
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)

    plt.savefig('backend/chart/chart.png')
    # Create a file to indicate chart creation
    with open('backend/chart/chart_created.txt', 'w') as f:
        f.write(f"Chart created on {datetime.now()}")
    plt.close()  # Close the plot to free memory
    print("Chart created and saved to backend/chart/chart.png")

if __name__ == "__main__":
    create_chart()
