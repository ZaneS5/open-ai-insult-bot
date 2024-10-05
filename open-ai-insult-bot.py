import os
import openai
import pyttsx3
import dotenv
import argparse
import random

PERSONALITIES = {1: "You're Ronda Wrench, a rough and tuble female mechanic who is willing to say it how it is",
                 2: "You're Bob the Builder, a friendly and helpful construction worker who is always willing to lend a hand",
                 3: "You're Dr. Phil, a wise and insightful psychologist who is always ready to give advice",
                 4: "You're Sherlock Holmes, a brilliant detective who is always one step ahead of everyone else",
                 5: "You're Dora the Explorer, a curious and adventurous young girl who solves problems"}

def get_client():
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")
    print(f'API Key: {api_key}')
    # Initialize the client with your API key
    client = openai.Client(api_key=api_key)
    return client

def get_response(client, prompt, personality=PERSONALITIES[random.randint(1, len(PERSONALITIES))]):
    # Create a completion request
    print(f"Using personality: {personality}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can also use gpt-4
        messages=[
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def text_to_speech(statement):
    engine = pyttsx3.init()
    engine.setProperty('volume', 0.7)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(statement)
    engine.runAndWait()

def main(prompt, personality=None):
    client = get_client()
    response = get_response(client, prompt, personality) if personality else get_response(client, prompt)
    text_to_speech(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', action='store', type=str, required=True, help='prompt to give to chatbot')
    parser.add_argument('--personality', action='store', type=str, required=False, help='personality to give to chatbot')
    args = parser.parse_args()
    main(args.prompt, args.personality)