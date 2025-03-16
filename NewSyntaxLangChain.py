import os

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"

# Step 1: Get API key securely
api_key = "AIzaSyDfsDfODl8Yd02x4XIGFLNa6MFGjjNQgBM"
os.environ["GOOGLE_API_KEY"] = api_key


# Ensure your VertexAI credentials are configured

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


from langchain_core.messages import HumanMessage

from langchain_core.messages import AIMessage

'''
response = model.invoke(
    [
        HumanMessage(content="Hi! I'm Bob"),
        AIMessage(content="Hello Bob! How can I assist you today?"),
        HumanMessage(content="What's my name?"),
    ]
)'
'

print(response)
'''


# LANG GRAPH WRAPPER


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You talk like a human being, but your primary purpose is helping with idea generation when asked"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model
def call_model(state: MessagesState):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke(
        {"messages": trimmed_messages}
    )
    response = model.invoke(prompt)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)



#END OF LANG GRAPH WRAPPER



'''
config = {"configurable": {"thread_id": "abc123"}}

query = "Hi! I'm Shravan."

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()  # output contains all messages in state

query = "What's my name?"

input_messages = [HumanMessage(query)]
output = app.invoke({"messages": input_messages}, config)
output["messages"][-1].pretty_print()
'''

from langchain_core.messages import SystemMessage, trim_messages

trimmer = trim_messages(
    max_tokens=120,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="You're a regular bot that acts like a human and talks like a human"),
]

def predict(something):
    config = {"configurable": {"thread_id": "abc567"}}
    query = something

    input_messages = messages + [HumanMessage(query)]
    output = app.invoke(
        {"messages": input_messages},
        config,
    )
    bot_response = output["messages"][-1]
    
    # Add both the human message and the bot's response to the history
    messages.append(HumanMessage(query))  # Add human message
    messages.append(bot_response)  # Add bot's response
    
    # Optionally print the bot's response
    bot_response.pretty_print()


# Function to handle category selection and generate custom responses
def get_custom_response():
    theName = input("🚀 Welcome to the Idea Generator! To begin, what is your name! ")
    nameMessage = f"My name is {theName}"
    messages.append(nameMessage)
    greeting = f"Hello {theName}!"
    print(greeting)
    
    choice = input("\nTell me what you need an idea for (or type 'exit' to quit): ")
    messages.append(choice)
    selected_prompt = f"Give me a well thought out idea from the following specifications: {choice}. If it doesn't seem like something thats specific enough, ask them for more information and keep the coversation going until you can sufficiently come up with a strong idea."

    while True:
        if choice.lower() == "exit":
            print("👋 Exiting. Have a great day!")
            break
        
        # Create the prompt dynamically from user input

        # Generate the response using the conversation chain (memory included)
        response = predict(selected_prompt)

        # Display the generated idea
        if(response != None):
            print(f"\n💡 Generated Idea:\n{response}")

        choice = input("\nPlease let me know how I can keep helping you(or type 'exit' to quit):")
        selected_prompt = choice

        # Optional: Show memory for debugging purposes (remove in production)
        # print("\n🧠 Memory Buffer:\n", memory.buffer)

# main
if __name__ == "__main__":
    get_custom_response()



