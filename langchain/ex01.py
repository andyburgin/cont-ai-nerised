# based on example code from https://python.langchain.com/docs/integrations/llms/llamacpp/

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

# Callback support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path="/models/llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0,
    max_tokens=2000,
    top_p=1,
    callback_manager=callback_manager,
    verbose=False,
)

question = """
What is the fastest land animal?
"""

llm.invoke(question)
