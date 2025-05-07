# Valeria AI - Alzheimer's Support Assistant

ValeriaAI is an AI-powered platform designed to help people with Alzheimer's manage their daily activities, slow down disease progression, and improve their quality of life.

## Features
- 🤖 Intelligent AI companion that adapts to user's cognitive stage
- 📅 Calendar management for appointments and reminders
- 🎯 Brain training activities and exercises
- 📋 Personalized care recommendations

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AlzAI.git
cd AlzAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Set up Google Calendar API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project and enable Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json` in the project root

5. Run the application:
```bash
streamlit run app.py
```

## Project Structure
```
AlzAI/
├── app.py                 # Main Streamlit application
├── .env                   # Environment variables
├── credentials.json       # Google Calendar API credentials
├── agents/               # AI agents and tools
└── pages/               # Streamlit pages
```

## Requirements
- Python 3.8+
- OpenAI API key
- Google Calendar API credentials
- Streamlit

## Notes
- The app requires both `.env` with OpenAI API key and `credentials.json` for Google Calendar integration
- First-time users will need to authenticate with Google Calendar
- Profile creation is required before using the chat features