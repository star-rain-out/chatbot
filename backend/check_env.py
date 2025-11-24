import os
from dotenv import load_dotenv

def check_env():
    print("Checking environment variables...")
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print(f"✅ .env file found at: {env_path}")
    else:
        print(f"❌ .env file NOT found at: {env_path}")
        print("   Please make sure you have created a .env file in the backend directory.")
        return

    # Load environment variables
    load_dotenv(env_path)
    
    # List of keys to check
    keys_to_check = [
        "OPENAI_API_KEY",
        "BAIDU_API_KEY",
        "BAIDU_SECRET_KEY",
        "GOOGLE_VISION_API_KEY",
        "HF_API_TOKEN"
    ]
    
    print("\nStatus of API Keys:")
    all_present = True
    for key in keys_to_check:
        value = os.getenv(key)
        if value:
            masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "****"
            print(f"✅ {key}: Found ({masked_value})")
        else:
            print(f"❌ {key}: Missing")
            all_present = False
            
    if all_present:
        print("\n🎉 All required environment variables are set!")
    else:
        print("\n⚠️  Some environment variables are missing. Please check your .env file.")

    # Check for huggingface_hub library
    print("\nChecking dependencies:")
    try:
        import huggingface_hub
        print(f"✅ huggingface_hub library installed (version: {huggingface_hub.__version__})")
    except ImportError:
        print("❌ huggingface_hub library NOT installed")
        print("   Run: pip install huggingface_hub")

if __name__ == "__main__":
    check_env()
