import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/get_url_response")
def get_url_response(url: str):
    llm_url = "https://52.151.194.159:8001/scrap"

    # Token (replace with your actual token)
    token = "mysecuretoken21429"

    # Query parameters
    params = {"url": url}

    # Headers including the Authorization token
    # headers = {
    #     "Authorization": f"Bearer {token}"
    # }

    # Make the GET request
    response = requests.get(url=llm_url, params=params, verify=False)  # verify=False to ignore SSL warnings

    # Print the response
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port =8005)