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

if "itenary" not in st.session_state:
    st.session_state.itenary = None

if "travel_details" not in st.session_state:
    st.session_state.travel_details = None

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

    st.markdown("\n")
    #Geocoding locations
    with st.spinner("Finding Nearby Locations") :
      lat, lon = geocode_location(destination)

      #Error handling
      if (lat is None):
          st.error("Cannot find the location! Please enter a valid location. ")
          st.stop()

      attractions, used_radius = fetch_nearby_attractions(lat, lon,interests)
    st.success(f"Found {len(attractions)} locations within {used_radius/1000} km")

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

    st.session_state.travel_details = travel_details

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
    with st.spinner("Generating your travel plan ..."):
        itenary = generate_itenary(travel_details)
        if itenary:
            st.session_state.itenary = itenary

if st.session_state.itenary : 
    st.markdown(
            '''<h2 style = "text-align : center;">Your Day wise Itenary</h2>''',
            unsafe_allow_html=True
        )

    left, center, right = st.columns([1,3,1])
    with center : 
        for day in st.session_state.itenary["days"]:
            with st.expander(f" Day {day['day']}"):
            #Convert all to markdown html
              for activity in day["activities"]:
                  st.markdown(
                  f'''<h4>{activity["time"]}</h4>''',
                  unsafe_allow_html=True
                  )
                  st.write(f"{activity["activity"]}")
                  st.write(f"Estimated Cost : INR {activity["estimated_cost"]}")
                  st.write(f"Food Recommendation : {activity["food_recommendation"]}")
                  st.write(f"Transport Suggestion : {activity["transport_suggestion"]}")

                  st.markdown("---")
              st.markdown(f'''<h4 style = "text-align : center">Daily Estimated total = INR {day["daily_estimated_total"]}</h4>''')
        
    with center:
      st.markdown("### Download Your Travel Plan")

      pdf_bytes = generate_pdf(st.session_state.itenary)

      st.download_button(
          label="📄 Download Travel Plan as PDF",
          data=pdf_bytes,
          file_name=f"{st.session_state.travel_details['destination']}_travel_plan.pdf",
          mime="application/pdf"
      )
      st.divider()
      #Display budget Card
      st.markdown('''<h3 style = "text-align = center">Budget Breakdown</h3>''',unsafe_allow_html=True)
      budget = st.session_state.itenary['budget_breakdown']
      st.write(f"Accommodation Expenditure : INR {budget['accommodation_total']}")
      st.write(f"Expense on Food  : INR {budget['food_total']}")
      st.write(f"Expense on Transport  : INR {budget['transport_total']}")
      st.write(f"Expense on Activities  : INR {budget['activities_total']}")
      st.write(f"Miscellaneous Expenditure  : INR {budget['miscellaneous']}")
      total_cost = budget['accommodation_total']+budget['food_total']+budget['transport_total']+budget['activities_total']+budget['miscellaneous']
      st.write(f"Total Expense : INR {total_cost}")

      st.markdown("\n")
      if total_cost < st.session_state.travel_details['budget']:
          st.write("All such fun within budget")
      else:
          st.write("A little overbudget but definitely worth it")
      