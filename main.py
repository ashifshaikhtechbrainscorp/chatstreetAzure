import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.INFO)
logging.info("🚀 App starting up")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/get_url_response")
def get_url_response(url: str, publisher_id: int = 3):
    llm_url = "https://chatstreetbrains.xyz/scrap"

    # Token (if needed later)
    token = "mysecuretoken21429"

    # Query parameters
    params = {
        "url": url,
        "publisher_id": publisher_id
    }

    print(f"[INFO] Received request for URL: {url}")
    print(f"[INFO] Forwarding request to LLM server: {llm_url} with params: {params}")

    try:
        response = requests.get(url=llm_url, params=params, verify=False)
        print(f"[DEBUG] LLM Response Code: {response.status_code}")

        if response.status_code == 200:
            print(f"[DEBUG] LLM Response JSON (truncated): {str(response.json())[:500]}")
            return response.json()
        else:
            print(f"[ERROR] LLM server returned status code: {response.status_code}")
            print(f"[ERROR] Response content: {response.text}")
            return {
                "status_code": response.status_code,
                "error": "Non-200 response from LLM server",
                "details": response.text
            }

    except requests.exceptions.Timeout:
        print(f"[EXCEPTION] Timeout while trying to reach LLM server at {llm_url}")
        return {"error": "Request to LLM server timed out"}

    except requests.exceptions.RequestException as e:
        print(f"[EXCEPTION] General error during request to LLM server: {e}")
        return {"error": "Request to LLM server failed", "details": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("[BOOT] Starting FastAPI server on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
