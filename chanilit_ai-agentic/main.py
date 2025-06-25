import os
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request

load_dotenv()

def main():
    credentials = None
    try:
        # Try to load credentials from environment variables
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_json:
            credentials = service_account.Credentials.from_service_account_info(
                credentials_json
            )
        else:
            # If no credentials in env, use the API key method
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("Error: No API key found in environment variables")
                return
            
            print(f"API Key loaded: {'***' + api_key[-4:] if api_key else 'NOT FOUND'}")
            
            # Using the correct Gemini API endpoint
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            print(f"Making API request to: {url}")
            
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    "contents": [{
                        "parts": [{
                            "text": "how"
                        }]
                    }]
                }
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print("\nResponse:", result["candidates"][0]["content"][0]["parts"][0]["text"])
            else:
                print(f"\nError: {response.status_code}")
                try:
                    error_details = response.json()
                    print("Detailed error:", error_details)
                except:
                    print("Response body:", response.text)
            
    except Exception as e:
        import traceback
        print(f"\nError: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()