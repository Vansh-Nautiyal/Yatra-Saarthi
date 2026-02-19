from google import genai
import streamlit as st
import json

def generate_itenary(travel_details):

    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

    prompt = f"""
    Create a {travel_details["duration"]} day itinerary for a group of {travel_details["people"]} people.
    Plan as a professional travel planner specializing in budget-friendly student trips.

    Destination: {travel_details["destination"]}
    Total budget: INR {travel_details["budget"]}
    Budget per day: INR {travel_details["budget_per_day"]}
    Budget per person: INR {travel_details["budget_per_person"]}
    Interested activities: {travel_details["interests"]}
    Accommodation: {travel_details["accomodation"]}

    IMPORTANT:
    - Return ONLY valid JSON
    - No markdown
    - No explanation text
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.3
        }
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        st.error("AI returned invalid JSON. Please try again.")
        return None
