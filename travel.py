import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

# --------------------------------------------------
# 1. LOAD LANGFLOW CREDENTIALS
# --------------------------------------------------

load_dotenv()

API_URL = os.getenv("LANGFLOW_API_URL")
API_KEY = os.getenv("LANGFLOW_API_KEY")

# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Travel Planner Agent")
st.markdown(
    "Plan your next trip with the help of IBM Granite AI."
)

# --------------------------------------------------
# 3. CHECK CONFIGURATION
# --------------------------------------------------

if not API_URL or not API_KEY:
    st.error(
        "Langflow configuration is missing. "
        "Please check LANGFLOW_API_URL and LANGFLOW_API_KEY "
        "in your .env file."
    )
    st.stop()

# --------------------------------------------------
# 4. FUNCTION TO EXTRACT AI RESPONSE
# --------------------------------------------------

def extract_text(data):
    """Extract readable text from different Langflow response formats."""

    if isinstance(data, str):
        return data.strip()

    if isinstance(data, list):
        for item in data:
            result = extract_text(item)
            if result:
                return result

    if isinstance(data, dict):

        # Common Langflow response fields
        for key in (
            "text",
            "message",
            "output",
            "content",
            "result"
        ):
            value = data.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

        # Common nested Langflow response structures
        for key in (
            "outputs",
            "results",
            "data",
            "messages"
        ):
            value = data.get(key)

            if isinstance(value, (dict, list)):
                result = extract_text(value)
                if result:
                    return result

    return ""


# --------------------------------------------------
# 5. FUNCTION TO CALL LANGFLOW
# --------------------------------------------------

def generate_travel_plan(prompt):

    payload = {
        "input_type": "chat",
        "output_type": "chat",
        "input_value": prompt,
        "session_id": str(uuid.uuid4())
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=180
        )

        # Raise an error for HTTP failures
        response.raise_for_status()

        result = response.json()

        # Extract the generated itinerary
        answer = extract_text(result)

        if not answer:
            return None, (
                "Langflow responded, but no readable text "
                "was found in its response."
            ), result

        return answer, None, result

    except requests.exceptions.HTTPError:
        status = response.status_code

        if status == 401 or status == 403:
            message = (
                "Langflow rejected the API key. "
                "Check that your Langflow API key is correct "
                "and that the endpoint belongs to your flow."
            )
        else:
            message = (
                f"Langflow returned HTTP error {status}: "
                f"{response.text[:1500]}"
            )

        return None, message, None

    except requests.exceptions.ConnectionError:
        return None, (
            "Cannot connect to Langflow. Make sure "
            "Langflow Desktop is running and the API URL "
            "is correct."
        ), None

    except requests.exceptions.Timeout:
        return None, (
            "The request took too long. Please try again."
        ), None

    except requests.exceptions.RequestException as error:
        return None, f"Request error: {error}", None

    except ValueError:
        return None, (
            "Langflow did not return valid JSON. "
            "Check your flow API response."
        ), None


# --------------------------------------------------
# 6. TRAVEL PLANNING FORM
# --------------------------------------------------

st.divider()

st.subheader("🌍 Enter Your Travel Details")

col1, col2 = st.columns(2)

with col1:
    source = st.text_input(
        "Starting City",
        placeholder="Example: Nashik"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Example: Goa"
    )

    travel_dates = st.text_input(
        "Travel Dates",
        placeholder="Example: 10–13 December 2026"
    )

    travellers = st.number_input(
        "Number of Travellers",
        min_value=1,
        max_value=50,
        value=2,
        step=1
    )

with col2:
    budget = st.number_input(
        "Total Budget (₹)",
        min_value=1000,
        value=15000,
        step=1000
    )

    travel_style = st.multiselect(
        "Travel Preferences",
        [
            "Nature",
            "Adventure",
            "Beach",
            "Historical Places",
            "Shopping",
            "Relaxation",
            "Culture",
            "Wildlife"
        ],
        default=["Nature", "Adventure"]
    )

    accommodation = st.selectbox(
        "Accommodation Preference",
        [
            "Budget",
            "Comfort",
            "Luxury"
        ]
    )

food_preference = st.text_input(
    "Food Preferences",
    placeholder="Example: Local foods, vegetarian food"
)

extra_requirements = st.text_area(
    "Additional Requirements",
    placeholder=(
        "Mention anything else you want in your trip, "
        "such as transport preferences or places to visit."
    )
)

# --------------------------------------------------
# 7. GENERATE TRAVEL PLAN
# --------------------------------------------------

if st.button(
    "✈️ Generate My Travel Plan",
    use_container_width=True,
    type="primary"
):

    if not source.strip():
        st.error("Please enter your starting city.")

    elif not destination.strip():
        st.error("Please enter your destination.")

    elif not travel_dates.strip():
        st.error("Please enter your travel dates.")

    else:

        prompt = f"""
You are an intelligent AI Travel Planner Agent
powered by IBM Granite.

Create a complete, practical and easy-to-understand
travel itinerary using these details.

TRAVEL DETAILS

Starting City: {source}
Destination: {destination}
Travel Dates: {travel_dates}
Number of Travellers: {travellers}
Total Budget: ₹{budget}
Travel Preferences: {", ".join(travel_style) if travel_style else "General sightseeing"}
Accommodation Preference: {accommodation}
Food Preferences: {food_preference or "No specific preference"}
Additional Requirements: {extra_requirements or "None"}

YOUR TASK

1. Give a short introduction to the destination.

2. Create a detailed day-wise itinerary.
   Include morning, afternoon and evening activities.

3. Suggest attractions and activities matching
   the travel preferences.

4. Suggest suitable local food and restaurants or
   food areas where appropriate.

5. Suggest accommodation options or types matching
   the selected accommodation preference.

6. Explain possible transportation options.

7. Prepare an estimated budget for all travellers.

BUDGET BREAKDOWN

Show separate estimates for:
- Transportation
- Accommodation
- Food
- Sightseeing and activities
- Miscellaneous expenses

Calculate the total estimated cost by adding
all categories.

Calculate the remaining budget as:

Remaining Budget = Total Budget - Estimated Total Cost

Show whether the trip is within the given budget.

Check all arithmetic carefully. Do not invent
exact live prices or booking availability.

IMPORTANT RULES

- Clearly label costs as estimates.
- Do not claim that bookings have been made.
- Do not invent live weather or real-time prices.
- If information is uncertain, say so.
- Keep the plan realistic for the number of days.
- Use clear headings, tables and bullet points.
- Give the final answer in readable Markdown.

Now generate the complete travel plan.
"""

        with st.spinner(
            "🤖 IBM Granite is preparing your travel plan..."
        ):

            answer, error, raw_result = generate_travel_plan(prompt)

        if error:
            st.error("Unable to generate your travel plan.")
            st.warning(error)

            if raw_result is not None:
                with st.expander("View technical response"):
                    st.json(raw_result)

        else:
            st.success("Your travel plan has been generated!")

            st.session_state["travel_plan"] = answer

            st.markdown("---")
            st.subheader("🗺️ Your Personalized Travel Itinerary")

            st.markdown(answer)

            st.markdown("---")

            st.download_button(
                label="⬇️ Download Travel Plan",
                data=answer,
                file_name="my_travel_plan.md",
                mime="text/markdown",
                use_container_width=True
            )

# --------------------------------------------------
# 8. DISPLAY PREVIOUS RESULT
# --------------------------------------------------

if "travel_plan" in st.session_state:
    pass

# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built using IBM Granite, Langflow, Python and Streamlit."
)