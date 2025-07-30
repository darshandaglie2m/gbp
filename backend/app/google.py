import os
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/business.manage"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

credentials = None
if SERVICE_ACCOUNT_FILE and os.path.exists(SERVICE_ACCOUNT_FILE):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_gbp_details(location_id: str) -> dict:
    """Retrieve GBP location details using Google Business Information API."""
    if not credentials:
        raise RuntimeError("Google service account not configured")
    service = build("mybusinessbusinessinformation", "v1", credentials=credentials)
    name = f"locations/{location_id}"
    request = service.locations().get(name=name)
    return request.execute()


def fetch_reviews(location_id: str) -> list[dict]:
    """Retrieve GBP reviews using the My Business API."""
    if not credentials:
        raise RuntimeError("Google service account not configured")
    service = build("mybusiness", "v4", credentials=credentials)
    request = service.accounts().locations().reviews().list(parent=f"locations/{location_id}")
    response = request.execute()
    return response.get("reviews", [])

async def analyze_gbp(details: dict, reviews: list[str]) -> str:
    """Use OpenAI to generate improvement recommendations."""
    prompt = (
        "Given the following Google Business Profile details and reviews, "
        "provide recommendations to improve visibility and engagement.\n"
        f"Details: {details}\nReviews: {reviews}"
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
