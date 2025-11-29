from mistralai import Mistral
import os
from dotenv import load_dotenv


def llm_explanation(route_names, total_km, total_min, speed):
    load_dotenv()
    client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
    model_name = "mistral-medium-latest"
    prompt = f"""
    A routing optimizer produced the following trip:

    - Route order (excluding depot): {route_names}
    - Total distance: {total_km} km
    - Estimated time: {total_min} minutes
    - Average speed assumed: {speed} km/h

    Explain this result in clear, simple language as if speaking to a logistics manager.
    Highlight how the algorithm found the shortest/efficient path. Direclty start the explanation. Text must not contain '\\n'.
    """

    resp = client.chat.complete(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content.strip()


