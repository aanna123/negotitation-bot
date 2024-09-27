from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

# Define products and their prices
PRODUCTS = {
    "Product A": 100,
    "Product B": 150,
    "Product C": 200,
}

# State variables
negotiation_count = 0
last_bot_offer = None
selected_product = None
repeated_offers_count = 0
chat_history = []

def extract_offer(user_input):
    """Extract the first numerical offer from user input."""
    match = re.search(r'\d+', user_input)
    return int(match.group(0)) if match else None

def handle_user_input(user_input):
    global negotiation_count, last_bot_offer, selected_product, repeated_offers_count

    user_input = user_input.lower()
    chat_history.append(("You", user_input))  # Append user input to chat history

    # Check if the user selected a product
    if selected_product is None:
        if user_input in [product.lower() for product in PRODUCTS.keys()]:
            selected_product = user_input.title()
            last_bot_offer = PRODUCTS[selected_product]
            bot_response = f"You selected {selected_product}. The starting price is ${last_bot_offer}. What is your offer?"
            chat_history.append(("Bot", bot_response))  # Append bot response to chat history
            return bot_response
        else:
            product_options = ", ".join(PRODUCTS.keys())
            bot_response = f"Please select a product from the following options: {product_options}."
            chat_history.append(("Bot", bot_response))
            return bot_response

    # Handling acceptance and rejection of offers
    if any(keyword in user_input for keyword in ["ok", "done", "accept", "deal"]):
        negotiation_count = 0
        bot_response = "Great! I’ll mark that as accepted. Let’s finalize the deal."
        chat_history.append(("Bot", bot_response))
        return bot_response

    if "no" in user_input or "reject" in user_input:
        negotiation_count = 0
        bot_response = "I understand. If you change your mind, I'm here to help!"
        chat_history.append(("Bot", bot_response))
        return bot_response

    user_offer = extract_offer(user_input)
    if user_offer is not None:
        return process_offer(user_offer)

    # Ask for the user's offer if none was provided
    bot_response = "I'm here to help! Could you please provide your offer?"
    chat_history.append(("Bot", bot_response))
    return bot_response

def process_offer(user_offer):
    global negotiation_count, last_bot_offer, repeated_offers_count

    negotiation_count += 1

    # Check if the offer is too low
    if user_offer < 50:
        bot_response = "Sorry, I can't go lower than $50."
        chat_history.append(("Bot", bot_response))
        return bot_response

    # Check for repeated offers
    if user_offer == last_bot_offer:
        repeated_offers_count += 1
        if repeated_offers_count >= 3:
            negotiation_count = 0
            bot_response = f"I see we keep agreeing on ${user_offer}. Let's finalize this deal!"
            chat_history.append(("Bot", bot_response))
            return bot_response
    else:
        repeated_offers_count = 0

    if user_offer == last_bot_offer:
        negotiation_count = 0
        bot_response = f"Great! I’ll accept your offer of ${user_offer}."
        chat_history.append(("Bot", bot_response))
        return bot_response

    if negotiation_count >= 5:
        bot_response = f". I'll go with ${last_bot_offer} as a final deal."
        chat_history.append(("Bot", bot_response))
        return bot_response

    # Calculate and present a counter offer
    counter_offer = int((last_bot_offer + user_offer) / 2)
    last_bot_offer = counter_offer

    bot_response = f"I can’t accept ${user_offer}. How about ${counter_offer}?"
    chat_history.append(("Bot", bot_response))
    return bot_response

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    
    # Debug: Print incoming user input
    print(f"User input: {user_input}")
    
    response = handle_user_input(user_input)

    # Debug: Print the current chat history
    print("Current chat history:", chat_history)

    # Return only the latest response and the last 5 messages from chat history
    recent_history = chat_history[-5:]  # Get the last 5 messages to send back
    return jsonify({'response': response, 'history': recent_history})

if __name__ == '__main__':
    app.run(debug=True)
