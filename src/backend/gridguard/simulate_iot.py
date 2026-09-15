import requests
import random
import time

URL = "http://127.0.0.1:8000/api/ingest/"

def generate_telemetry():
    assets = ["TR-101", "TR-102", "SUB-201", "TR-104"]
    print("--- Starting IoT Sensor Data Ingestion ---")
    
    for i in range(1, 6):
        asset_id = random.choice(assets)
        payload = {
            "asset_id": asset_id,
            "temperature": round(random.uniform(50.0, 95.0), 2),
            "vibration": round(random.uniform(0.5, 2.2), 2),
            "partial_discharge": round(random.uniform(10.0, 60.0), 2),
            "oil_quality": round(random.uniform(30.0, 90.0), 2),
            "wind_speed": round(random.uniform(10.0, 60.0), 2),
            "rainfall": round(random.uniform(0.0, 50.0), 2),
            "humidity": round(random.uniform(40.0, 90.0), 2)
        }
        
        try:
            response = requests.post(URL, json=payload)
            print(f"[{i}/5] Asset: {asset_id} | Risk Level: {response.json().get('risk_level')} | Status: {response.status_code}")
        except Exception as e:
            print("Error connecting to server:", e)
            
        time.sleep(1)

if __name__ == "__main__":
    generate_telemetry()