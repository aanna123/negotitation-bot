Clone the repository:

git clone https://github.com/your-username/negotiation-chatbot-api.git
cd negotiation-chatbot-api

Additional Notes:
Environment Variables: Ensure you have a .env file in the same directory as your chat.py file that contains your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key_here
Dependencies: Make sure you have the required packages installed. You can install them via pip:


pip install Flask python-dotenv requests streamlit
Running the Applications:

First, run the Flask API:

python chat.py
Then, run the Streamlit application:

streamlit run app.py
