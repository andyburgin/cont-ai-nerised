from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import  TextLoader

loader = TextLoader("state_of_the_union.txt")
documents = loader.load()

chunk_size = 500
chunk_overlap = 50
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
texts = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="/models/embeddings/bge-base-en-v1.5/")

db = Chroma.from_documents(texts, embedding=embeddings, persist_directory="chroma")
db.persist()
db = None
