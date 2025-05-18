from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()

import os
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ.get("AIzaSyDfsDfODl8Yd02x4XIGFLNa6MFGjjNQgBM"))

template = """The following is a friendly conversation between a user and an AI assistant.
The chatbot is talkative and provides lots of specific details from its context.
If the chatbot does not know the answer to a question, it truthfully says it does not know.

{chat_history}
User: {input}
Chatbot:"""
prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)

llm_chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = llm_chain.run(input=user_input)
    print(f"Chatbot: {response}")