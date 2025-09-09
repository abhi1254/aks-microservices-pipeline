from fastapi import FastAPI
import mysql.connector
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = FastAPI()

# Key Vault setup
KV_NAME = os.environ.get("KEY_VAULT_NAME", "deploymentkeyvault998")
KV_URI = f"https://{KV_NAME}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KV_URI, credential=credential)

# Fetch DB password from Key Vault
db_password = client.get_secret("dbpassword").value

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/db-check")
def check_db():
    try:
        conn = mysql.connector.connect(
            host="myapp-mysql",   
            user="myappuser",
            password=db_password,
            database="myappdb"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        conn.close()
        return {"db_connection": f"Connected to {db_name}"}
    except Exception as e:
        return {"db_connection": f"Failed - {str(e)}"}
