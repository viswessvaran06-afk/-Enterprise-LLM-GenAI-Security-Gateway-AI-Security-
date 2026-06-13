import asyncio
import httpx
import time

BASE_URL = "http://127.0.0.1:8000"
API_KEY = "user123-key-abc"

async def send_request(client, prompt):
    response = await client.post(
        f"{BASE_URL}/api/v1/chat",
        headers={"X-API-Key": API_KEY},
        json={
            "model": "gpt-4",
            "prompt": prompt,
            "user_id": "user123",
            "department": "engineering"
        }
    )
    return response.status_code

async def stress_test():
    prompts = [
        "What is artificial intelligence?",
        "Explain machine learning",
        "What is deep learning?",
        "How does NLP work?",
        "What is computer vision?",
    ]

    async with httpx.AsyncClient(timeout=30) as client:
        start_time = time.time()
        
        tasks = [send_request(client, prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        print(f"\n--- Stress Test Results ---")
        print(f"Total requests: {len(results)}")
        print(f"Successful: {results.count(200)}")
        print(f"Failed: {len(results) - results.count(200)}")
        print(f"Total time: {end_time - start_time:.2f} seconds")
        print(f"Avg time per request: {(end_time - start_time) / len(results):.2f} seconds")

if __name__ == "__main__":
    asyncio.run(stress_test())