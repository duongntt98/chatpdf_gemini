from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS

GOOGLE_API_KEY = "GOOGLE_API_KEY" #get your GOOGLE_API_KEY in https://aistudio.google.com/app/apikey

loader = PyPDFLoader("./mycv.pdf")
pages = loader.load_and_split()

#embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.from_documents(pages, embeddings)

#-----
def gemini_with_langchain_model(query_input):
    docs = db.similarity_search(query_input)

    content = "\n".join([x.page_content for x in docs])
    qa_prompt = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.----------------"
    # text = "Use the following pieces of context to answer the user's question. If you don't know the answer, just say that incording by gemini i think"
    # qa_prompt = text + gemini_model(query_input)
    
    input_text = qa_prompt+"\nContext:"+content+"\nUser question:\n"+ query_input
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(input_text)
    return result.content


# # not use langchain
import google.generativeai as genai


genai.configure(api_key= GOOGLE_API_KEY )

def gemini_model(query_input):

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        query_input,
        generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=None,
        temperature=1.0))
    return response.text


print("----------------------\n")
print("Chatbot: Hi! welcome to Duong chatbot! Please input your question. If you want end session, please input 'exit'!\n")
print("User: ")
user_input = input()

while user_input != "exit":
    result = gemini_with_langchain_model(user_input) #replace model here!!
    print("- Chatbot: \n", result)
    print("- User: ")
    user_input = input()