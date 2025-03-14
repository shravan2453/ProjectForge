from google import genai

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

# Function to handle category selection and generate custom response
def get_custom_response():
    print("Welcome to the Idea Generator!")
    choice = input("Tell me what you need an idea for, and any specific help and I'll give it to you: ")


    # Get the prompt for the selected category
    selected_prompt = f"Give me an idea from the following specifications, which you will get from {choice}"

    response = generate_idea(selected_prompt)
    
    # Display the generated idea
    print(f"Generated Idea: {response}")

# Main function to run the program
if __name__ == "__main__":
    get_custom_response()

