from fastapi import FastAPI
import mysql.connector

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/db-check")
def check_db():
    try:
        conn = mysql.connector.connect(
            host="myapp-mysql",   # container name from docker-compose OR "localhost" if running manually
            user="myappuser",
            password="myapppass",
            database="myappdb"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        conn.close()
        return {"db_connection": f"Connected to {db_name}"}
    except Exception as e:
        return {"db_connection": f"Failed - {str(e)}"}
