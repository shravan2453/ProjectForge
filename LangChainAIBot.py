from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema.messages import HumanMessage
import os
import getpass

#setup

# Step 1: Get API key securely
api_key = getpass.getpass('🔑 Enter your Google Gemini API Key: ')
os.environ["GOOGLE_API_KEY"] = api_key

# Initialize Gemini LLM (using LangChain)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# Add memory (remembers chat history)
memory = ConversationBufferMemory()

# Step 4: Set up a conversation chain (LLM + Memory)
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# Functions

# Function to handle category selection and generate custom responses
def get_custom_response():
    print("🚀 Welcome to the Idea Generator!")
    
    while True:
        choice = input("\nTell me what you need an idea for (or type 'exit' to quit): ")

        if choice.lower() == "exit":
            print("👋 Exiting. Have a great day!")
            break
        
        # Create the prompt dynamically from user input
        selected_prompt = f"Give me an idea from the following specifications: {choice}."

        # Generate the response using the conversation chain (memory included)
        response = conversation.predict(input=selected_prompt)

        # Display the generated idea
        print(f"\n💡 Generated Idea:\n{response}")

        # Optional: Show memory for debugging purposes (remove in production)
        # print("\n🧠 Memory Buffer:\n", memory.buffer)

# main
if __name__ == "__main__":
    get_custom_response()
