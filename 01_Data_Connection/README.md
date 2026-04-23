# Phase 1 - Data Connection

## Goal
Connect to MongoDB, fetch accident records, convert to pandas DataFrame, and remove unnecessary fields (such as `_id`).

## Files
- `src/data/connect_mongodb.py`: Loads MongoDB config and creates connection.
- `src/data/fetch_data.py`: Fetches records and converts to DataFrame.
- `01_Data_Connection/run_phase1.py`: Runs Phase 1 flow and prints preview.

## Setup
1. Copy `.env.example` to `.env`
2. Fill your MongoDB URI, DB name, and collection name
3. Install dependencies:
   `pip install -r requirements.txt`

## Run
`python 01_Data_Connection/run_phase1.py`

## Expected Output
- Connection succeeds
- Data fetched from MongoDB
- DataFrame created with columns: `time`, `weather`, `road_type`, `severity`
- `_id` excluded
