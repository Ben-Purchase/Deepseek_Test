from flask import Flask, request, jsonify
import subprocess
import re
from speech_interpreter import interpret_speech

app = Flask(__name__)

def generate_response(prompt):
    """
    Generate a response by calling the Deepseek model through Ollama.
    Make sure that Ollama is installed and Deepseek is set up locally.
    """
    # System prompt to set the context for the AI

    # Open prompt.txt in read mode
    with open('prompt.txt', 'r') as file:
        # Read all lines into a list (each line is an element)
        sys_prompt = file.readlines()

    # Strip newline characters from each line
        sys_prompt = [line.strip() for line in prompt]
        
    system_prompt = (
        # DeepSeek R1 Prompt  

        '**Instruction**:  '
        '- Listen to the customers order.  '
        '- Identify the closest matching menu items from the given list.  '
        '- Respond ONLY with: **"You want [selected items]."** ' 
        '- Do not add any extra text, explanations, or greetings.  '
        '- The items must match items from the menu exactly'
        ''
        '**Menu Items**:  '
        '1. Pasta:  '
        '- Spaghetti Carbonara  '
        '- Penne alla Vodka  '
        '- Lobster Ravioli  '
        '2. Pizza:  '
        '- Margherita  '
        '- Pepperoni Pizza  '
        '- Truffle Mushroom Pizza  '
        '3. Sandwiches:  '
        '- Classic Club Sandwich  '
        '- Italian Sub  '
        '- Grilled Chicken Panini  '
        '4. Curry:  '
        '- Chicken Tikka Masala  '
        '- Vegetable Korma  '
        '- Lamb Rogan Josh  '
        '5. Fish:  '
        '- Grilled Salmon  '
        '- Fish and Chips  '
        '- Seared Tuna Steak  '
        ''
        '**Example**:  '
        'Customer: "Can I get a chicken sandwich?"  '
        'AI: **"You want Grilled Chicken Panini."**  '
        ''
        'Customer: "Id like some salmon and spaghetti."  '
        'AI: **"You want Grilled Salmon, Spaghetti Carbonara."**  '
        ''
        '**Model Settings**:  '
        '- Temperature: 0.3 (for accurate selection) '
        ''
        '**Order**:'
        'Customer: '
    )
    
    # Combine the system prompt with the user's message
    full_prompt = f"{system_prompt}\n\nCustomer: {prompt}\nWaiter:"

    # Construct the command to call Deepseek via Ollama
    command = ["ollama", "run", "deepseek-r1:1.5b", full_prompt] # Uncomment to run the 1.5b params version of deepseek
    #command = ["ollama", "run", "deepseek-r1:7b", full_prompt] # Uncomment to run the 7b params version of deepseek
    #command = ["ollama", "run", "deepseek-r1:14b", full_prompt] # Uncomment to run the 14b params version of deepseek

    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # The response is expected in stdout
        response = result.stdout.strip()

        # Remove content inside <think></think> tags
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
    except subprocess.CalledProcessError as e:
        response = f"Error generating response: {e}"

    return response

@app.route("/chat", methods=["POST"])
def chat():
    """
    API endpoint to receive a user message and return a chatbot response.
    """
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

@app.route("/get_speech", methods=["GET"])
def get_speech():
    speech_message = interpret_speech()
    return jsonify({"message": speech_message})

# Optionally, serve the frontend from the Flask app
@app.route("/")
def home():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)