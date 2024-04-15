from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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
sys_prompt = """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
"""
instruction = """Plese answer the following question:
{question}
"""

# prompt as defined on the huggingface model card for llama2-7b-chat.Q4_K_M.gguf 
prompt = "[INST]" + "<<SYS>>\n" + sys_prompt + "\n<</SYS>>\n\n" + instruction +"[/INST]"

custom_rag_prompt = PromptTemplate.from_template(template=prompt)

# define the chain 
rag_chain = (
    {"question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

#question
question = "What did President Zelenskyy say in his speech to the European Parliament ?"

# call chain
response = rag_chain.invoke(question)
