import streamlit as st 
import pandas as pd
import pydeck as pdk
from ai_module import generate_itenary
from map_utils import geocode_location, fetch_nearby_attractions
from pdf_generator import generate_pdf

#Title of the page
st.markdown(
            '''<h1 style = "text-align : center;">AI Travel Planner for Students</h1>''',
            unsafe_allow_html=True
        )
st.set_page_config(
    page_title="AI Travel Planner",
    layout="wide"
)
st.markdown('''<p style= "text-align : center; font-size: 18px; margin-left: 5%; margin-right : 5%;padding-bottom:20px;">Smart AI-powered trip planning for students — generate budget-friendly, 
            personalized day-wise itineraries with nearby attractions, maps, and travel recommendations.</p><br>
            ''',unsafe_allow_html=True)

def vaildate_input(destination, interest):
    if not (destination):
        st.error("Please enter a destination")
        st.stop()

    if not (interest):
        st.warning("Select at least one interest for better reccomendation")

left, center, right = st.columns([1,2,1])

with center : 
    with st.form("my_form"):
        destination = st.text_input("Destination")
        duration = st.number_input("Duration of trip (in days) ",min_value=1)
        budget = st.number_input("Total Budget (in INR)",min_value=1000)
        people = st.number_input("Number of People in Group",min_value=1)
        interests = st.multiselect("Select you interests ",
                                ["Adventure",
                                "Nature",
                                "Food",
                                "History",
                                "Nightlife",
                                "Shopping",
                                "Spiritual",
                                "Photography"])

        accomodation = st.selectbox("Accomodation Type",
                                    [
                                        "Hotel",
                                        "AirBnB",
                                        "Budget Hotel",
                                        "Luxury"
                                    ])
        
        submitted = st.form_submit_button("Generate Travel Plan",use_container_width=True)

if submitted:
    vaildate_input(destination, interests)

    #Geocoding locations
    lat, lon = geocode_location(destination)

    #Error handling
    if (lat is None):
        st.error("Cannot find the location! Please enter a valid location. ")
        st.stop()

    attractions, used_radius = fetch_nearby_attractions(lat, lon,interests)

    #adding attractions to travel details
    travel_details = {
        "destination" : destination,
        "duration" : duration,
        "budget" : budget,
        "people" : people,
        "interests" : interests,
        "accomodation" : accomodation,
        
        #Add additional details to make output better 
        "budget_per_day" : int(budget/duration),
        "budget_per_person" : int(budget/people),
        "nearby_attractions" : attractions
    }
    st.divider()
    st.markdown(
            '''<h2 style = "text-align : center;">Nearby Locations</h2>''',
            unsafe_allow_html=True
        )
    st.markdown("\n")
    left, right = st.columns([2, 1])
    with left:
        locations = pd.DataFrame(attractions)
        if not locations.empty:

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=locations,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 160]',
                get_radius=120,
                pickable=True,
            )

            view_state = pdk.ViewState(
                latitude=locations["lat"].mean(),
                longitude=locations["lon"].mean(),
                zoom=12,
            )

            tooltip = {
                "html": "<b>{name}</b>",
                "style": {"color": "white"}
            }

            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip
            )

            st.pydeck_chart(deck)

    with right:
        st.markdown("\n")
        st.subheader("List of nearby attractions")
        for place in attractions[:10]:
            st.write("  ->",place["name"])

    # Displaying Itenary
    st.divider()
    with st.spinner("Generating your travel plan ..."):
        itenary = generate_itenary(travel_details)

    st.markdown(
            '''<h2 style = "text-align : center;">Your Day wise Itenary</h2>''',
            unsafe_allow_html=True
        )
#     itenary = {
#   "trip_summary": {
#     "destination": "Manali",
#     "duration_days": 3,
#     "total_budget": 15000,
#     "budget_per_day": 5000,
#     "budget_per_person": 7500
#   },
#   "days": [
#     {
#       "day": 1,
#       "theme": "Local Sightseeing & Mall Road",
#       "activities": [
#         {
#           "time": "Morning",
#           "activity": "Visit Hadimba Temple and explore nearby cedar forest.",
#           "location": "Hadimba Temple",
#           "estimated_cost": 100,
#           "food_recommendation": "Breakfast at Cafe 1947",
#           "transport_suggestion": "Walk or take local auto (₹50-100)"
#         },
#         {
#           "time": "Afternoon",
#           "activity": "Explore Manu Temple and Old Manali streets.",
#           "location": "Old Manali",
#           "estimated_cost": 200,
#           "food_recommendation": "Lunch at Drifters Cafe",
#           "transport_suggestion": "Local cab (₹200)"
#         },
#         {
#           "time": "Evening",
#           "activity": "Shopping and leisure walk at Mall Road.",
#           "location": "Mall Road",
#           "estimated_cost": 500,
#           "food_recommendation": "Dinner at Johnson’s Cafe",
#           "transport_suggestion": "Walk"
#         }
#       ],
#       "daily_estimated_total": 800
#     },
#     {
#       "day": 2,
#       "theme": "Adventure & Snow Activities",
#       "activities": [
#         {
#           "time": "Morning",
#           "activity": "Visit Solang Valley for adventure sports like paragliding.",
#           "location": "Solang Valley",
#           "estimated_cost": 2500,
#           "food_recommendation": "Local food stalls",
#           "transport_suggestion": "Shared cab (₹500 round trip)"
#         },
#         {
#           "time": "Evening",
#           "activity": "Relax by Beas River and photography session.",
#           "location": "Beas River",
#           "estimated_cost": 100,
#           "food_recommendation": "Dinner near Mall Road",
#           "transport_suggestion": "Walk or local cab"
#         }
#       ],
#       "daily_estimated_total": 3100
#     },
#     {
#       "day": 3,
#       "theme": "Nature & Departure",
#       "activities": [
#         {
#           "time": "Morning",
#           "activity": "Visit Jogini Waterfall and short trek.",
#           "location": "Jogini Waterfall",
#           "estimated_cost": 200,
#           "food_recommendation": "Packed snacks",
#           "transport_suggestion": "Local cab (₹300)"
#         },
#         {
#           "time": "Afternoon",
#           "activity": "Last-minute shopping and departure.",
#           "location": "Mall Road",
#           "estimated_cost": 500,
#           "food_recommendation": "Lunch at local dhaba",
#           "transport_suggestion": "Auto to bus stand"
#         }
#       ],
#       "daily_estimated_total": 700
#     }
#   ],
#   "budget_breakdown": {
#     "accommodation_total": 6000,
#     "food_total": 3000,
#     "transport_total": 2000,
#     "activities_total": 3000,
#     "miscellaneous": 1000
#   },
#   "travel_tips": [
#     "Carry warm clothes even in summer.",
#     "Start early for Solang Valley to avoid crowd.",
#     "Keep some cash as small shops may not accept UPI."
#   ]
# }
    left, center, right = st.columns([1,3,1])
    with center : 
        for day in itenary["days"]:
            st.markdown(
                f'''<h3 style = "text-align : center;">Day {day["day"]}</h3>''',
                unsafe_allow_html=True
            )

            #Convert all to markdown html
            for activity in day["activities"]:
                st.markdown(
                f'''<h4>{activity["time"]}</h4>''',
                unsafe_allow_html=True
                )
                st.write(f"{activity["activity"]}")
                st.write(f"Estimated Cost : {activity["estimated_cost"]}")
                st.write(f"Food Recommendation : {activity["food_recommendation"]}")
                st.write(f"Transport Suggestion : {activity["transport_suggestion"]}")
                st.markdown("\n")
            st.markdown("\n")
        st.divider()

        st.markdown("### Download Your Travel Plan")

        pdf_bytes = generate_pdf(itenary)

        st.download_button(
            label="📄 Download Travel Plan as PDF",
            data=pdf_bytes,
            file_name=f"{travel_details['destination']}_travel_plan.pdf",
            mime="application/pdf"
        )