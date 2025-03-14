from google import genai
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()

def generate_idea(prompt):
    try:
        client = genai.Client(api_key="AIzaSyDfsDfODl8Yd02x4XIGFLNa6MFGjjNQgBM")
        # Make the API call with the new interface
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
        )
        # Return the generated idea
        return response.text
    
    
    except Exception as e:
        return f"Error occurred:"

# Example interaction with Gemini API
user_input = "Hello, how are you?"
gemini_response = generate_idea(user_input)
if gemini_response:
    print("Gemini response:", gemini_response)


# Example loop for ongoing conversation
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    gemini_reply = generate_idea(user_input)
    print("Gemini:", gemini_reply)
