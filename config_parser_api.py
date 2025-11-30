import configparser
import json
import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

DATABASE_NAME = "config_data.db"


def read_config_file(filename):
    """Reads INI config file and returns data as a dictionary."""
    config = configparser.ConfigParser()

    try:
        config.read(filename)

        if not config.sections():
            raise FileNotFoundError("Configuration file is empty or unreadable.")

        result = {}

        for section in config.sections():
            result[section] = dict(config.items(section))

        return result

    except FileNotFoundError:
        print("Error: Configuration file not found!")
        return None

    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None


def save_to_database(data):
    """Saves JSON data into SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                json_data TEXT
            )
        """)

        json_string = json.dumps(data, indent=4)

        cursor.execute("INSERT INTO config_data (json_data) VALUES (?)", (json_string,))
        conn.commit()

        conn.close()

    except Exception as e:
        print(f"Error saving data to database: {e}")


@app.get("/config")
def get_config():
    """Fetch configuration data from database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT json_data FROM config_data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        conn.close()

        if row:
            return JSONResponse(content=json.loads(row[0]))

        return {"message": "No configuration data found in database"}

    except Exception as e:
        return {"error": f"Failed to fetch data: {e}"}


# ----------- MAIN PROGRAM EXECUTION -----------

if __name__ == "__main__":
    filename = "config.ini"
    config_data = read_config_file(filename)

    if config_data:
        print("Configuration File Parser Results:\n")
        for section, values in config_data.items():
            print(f"{section}:")
            for key, value in values.items():
                print(f"- {key}: {value}")
            print()

        # Save JSON to DB
        save_to_database(config_data)
        print("Configuration data saved to database successfully!")

        print("\nRun API using:")
        print("uvicorn config_parser_api:app --reload")
