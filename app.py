import streamlit as st 
import pandas as pd
import pydeck as pdk
from ai_module import generate_itenary
from map_utils import geocode_location, fetch_nearby_attractions

#Title of the page
st.markdown(
            '''<h1 style = "text-align : center;">AI Travel Planner for Students</h1>''',
            unsafe_allow_html=True
        )
st.set_page_config(
    page_title="AI Travel Planner",
    layout="wide"
)

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
        
        submitted = st.form_submit_button("Generate Travel Plan")

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