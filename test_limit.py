import requests
import concurrent.futures

# Update this to your actual login URL
URL = "https://www.harada.global/sign-in/"
TOTAL_REQUESTS = 25

print(f"Starting concurrent rate limit test on {URL}...")

def fetch(i):
    try:
        response = requests.get(URL, timeout=5)
        return i, response.status_code
    except requests.exceptions.RequestException as e:
        return i, str(e)

# Send all 25 requests at the exact same time using threads
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    futures = [executor.submit(fetch, i) for i in range(1, TOTAL_REQUESTS + 1)]
    
    for future in concurrent.futures.as_completed(futures):
        i, status = future.result()
        if status == 200:
            print(f"Request {i}: ✅ Success (200)")
        elif status in (503, 429):
            print(f"Request {i}: 🛑 Blocked ({status}) - Rate limit working!")
        else:
            print(f"Request {i}: ❓ Unexpected Status ({status})")

print("\nTest complete.")
