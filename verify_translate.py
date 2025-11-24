import requests
import json

def test_translate(text):
    url = "http://localhost:8000/api/translate/do"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(f"Input: {text}")
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return result
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return None

print("--- Testing English to Chinese ---")
res1 = test_translate("I'm from Canada")

print("\n--- Testing Chinese to English ---")
res2 = test_translate("你好")

if res1 and "translated_text" in res1 and res2 and "translated_text" in res2:
    print("\nSUCCESS: Both translations worked.")
else:
    print("\nFAILURE: One or more translations failed.")
