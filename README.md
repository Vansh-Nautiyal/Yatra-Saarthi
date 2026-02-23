# 🌍 Yatra Saarthi – AI Student Travel Planner

Yatra Saarthi is an AI-powered travel planning web application designed specifically for students.  
It generates personalized, budget-friendly itineraries using Large Language Models, real-time location data, and interactive maps.

🚀 Live Demo: https://yatra-saarthi-01.streamlit.app

---

## Features

-  AI-powered itinerary generation using Groq LLM
-  Real-time nearby attractions using OpenStreetMap (Overpass API)
-  Interactive map visualization with PyDeck
-  Automatic budget breakdown and cost estimation
-  Downloadable day-wise travel plan in PDF format
-  Secure API key management using Streamlit Secrets
-  Session-based usage limiting for demo control

---

##  How It Works

1. User enters:
   - Destination
   - Duration
   - Budget
   - Interests
   - Accommodation type

2. The system:
   - Geocodes the destination
   - Fetches nearby attractions using OpenStreetMap APIs
   - Sends structured prompt to Groq LLM
   - Receives JSON itinerary response
   - Displays formatted itinerary with budget breakdown
   - Generates downloadable PDF

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|----------|
| Streamlit | Web application framework |
| Groq API (LLM) | AI itinerary generation |
| OpenStreetMap + Overpass API | Nearby attractions data |
| PyDeck | Interactive maps |
| ReportLab | PDF generation |
| Pandas | Data handling |

Dependencies (from `requirements.txt`):
