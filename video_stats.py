import requests, api_key, json

CHANNEL_HANDLE = "MrBeast"

# url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={api_key.api_key}"

content_id = "VLPLoSWVnSA9vG_s-XT40oPKF0iWFGw8pOp2%3Fsbp%3DKgtIUEpLeEFoTHc1SUAB"

url=f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={content_id}&key={api_key.api_key}'

response = requests.get(url)

print(response)

data = response.json()

print(json.dumps(data, indent=4))