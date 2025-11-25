import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from routers.tools_travel import call_gemini_api
    print("Successfully imported call_gemini_api")
except Exception as e:
    print(f"Failed to import: {e}")
    sys.exit(1)

async def test_gemini():
    print("Testing call_gemini_api...")
    question = "Plan a 1-day trip to Kyoto"
    
    try:
        result = await call_gemini_api(question)
        print("\nResult:")
        print(result)
        
        if result.get("source") == "Google Gemini":
            print("\nSUCCESS: Used Google Gemini!")
            print("Answer length:", len(result.get("answer", "")))
        else:
            print(f"\nWARNING: Source is {result.get('source')}")
            
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
