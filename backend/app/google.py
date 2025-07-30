import openai

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
