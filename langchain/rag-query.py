from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# setup retrieval from vector db
embeddings = HuggingFaceEmbeddings(model_name="/models/embeddings/bge-base-en-v1.5/")
vectorstore = Chroma(persist_directory="chroma", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# Callback support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Use the LlamaCpp llm 
llm = LlamaCpp(
    model_path="/models/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0,
    max_tokens=2000,
    top_p=1,
    callback_manager=callback_manager,
    verbose=False,
)

# create prompt
sys_prompt = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible using the context text provided. Your answers should only answer the question once and not have any text after the answer is done.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

instruction = """CONTEXT:/n/n {context}/n

Question: {question}"""

# prompt as defined on the huggingface model card for llama2-7b-chat.Q4_K_M.gguf 
prompt = "[INST]" + "<<SYS>>\n" + sys_prompt + "\n<</SYS>>\n\n" + instruction +"[/INST]"

custom_rag_prompt = PromptTemplate.from_template(template=prompt)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

question = "What did President Zelenskyy say in his speech to the European Parliament ?"
response = rag_chain.invoke(question)
