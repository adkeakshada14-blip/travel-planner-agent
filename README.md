✈️ AI Travel Planner Agent

An AI-powered Travel Planner Agent built using IBM Granite, Langflow, Python and Streamlit. It helps users generate personalized travel itineraries based on their destination, travel dates, budget, number of travellers and preferences.

🌍 Project Overview

Planning a trip involves choosing destinations, preparing itineraries, estimating expenses and finding suitable activities. This project uses an AI agent to simplify the travel-planning process and provide personalized travel suggestions.

🎯 Objectives

- Generate personalized travel itineraries.
- Suggest activities and attractions based on user preferences.
- Estimate travel expenses and provide a budget breakdown.
- Recommend food and accommodation options.
- Make travel planning easier and faster.

🛠️ Technologies Used

- IBM Granite – AI language model.
- Langflow – AI agent workflow and orchestration.
- Python – Application development.
- Streamlit – User interface.
- Requests – API communication.
- python-dotenv – Environment variable management.

✨ Features

- Enter starting city and destination.
- Select travel dates and number of travellers.
- Set a total travel budget.
- Choose travel preferences such as nature, adventure and sightseeing.
- Specify accommodation and food preferences.
- Generate a personalized day-wise itinerary.
- View estimated expenses and budget breakdown.
- Download the generated travel plan.

🏗️ Project Structure

travel-planner-agent/
│
├── travel.py
├── requirements.txt
├── .gitignore
├── .env                 # Keep private; do not upload
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd travel-planner-agent

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a ".env" file in the project folder:

LANGFLOW_API_URL=YOUR_LANGFLOW_API_ENDPOINT
LANGFLOW_API_KEY=YOUR_LANGFLOW_API_KEY

Use your own Langflow API endpoint and API key. Never publish your API key.

4. Start Langflow

Open IBM Langflow Desktop and make sure your Travel Planner flow is running and available.

5. Run the application

streamlit run travel.py

Open the local URL displayed in your terminal.

🔄 Project Workflow

1. User enters travel details in the Streamlit application.
2. Python collects the user's travel preferences.
3. The application sends the request to the Langflow API.
4. Langflow processes the request using the IBM Granite model.
5. The AI agent generates a personalized travel plan.
6. Streamlit displays the itinerary and estimated budget.

🔐 Security

- API credentials are stored in a local ".env" file.
- The ".env" file must not be uploaded to GitHub.
- Never share IBM Cloud or Langflow API keys publicly.

👩‍💻 Developed By

Akshada Adke

B.Tech – Artificial Intelligence and Data Science

Project: AI Travel Planner Agent

📌 Note

The current application uses a local Langflow endpoint. Langflow Desktop must be running for the application to communicate with the agent. Public deployment requires a reachable hosted Langflow endpoint and secure credential configuration.
