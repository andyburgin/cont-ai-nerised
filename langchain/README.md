# Setup dev container

## Run python image - mounting models folder
```
docker run -v ~/Documents/models/:/models --name llmdev -ti python:3.11-bookworm bash
```
## Update image and install vim
```
apt-get update
apt-get install vim
```
## Install python libraries
```
pip install langchain-community langchain[llm] llama-cpp-python sentence-transformerschromadb
```

# Run the demos

* ex01.py - simple query of llama2 llm using lamma-cpp-python.
* ex02.py - parameterised prompt query for information unknow to model.
* Download the state of the union file from https://github.com/hwchase17/chat-your-data/blob/master/state_of_the_union.txt
* rag-ingest.py - will chunk the state_of_the_union.txt file and store in chroma db.
* rag-query.py - queries chroma db for chunks of documnet then uses the llama2 llm to answer the question for ex02.py using the retrieved text.