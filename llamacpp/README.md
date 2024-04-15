# Creating llamacpp container

## Download LLM models
Download models from Huggingface e.g. Q4_K_M GGUF versions of:

* https://huggingface.co/TheBloke/stable-code-3b-GGUF
* https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

Store locally in ~/Documents/models

## Create container
```
docker run -v ~/Documents/models/:/models --name llmdemo -ti debian:12-slim
```
## Update the image and install build tools
```
apt-get update
apt-get install build-essential git
```
## Install llama.cpp
```
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```
## Replace models folder with mounted one
```
mv models/* /models/
rm -rf models/
ln -s /models/ models
```
## Store the image
```
exit
docker ps -a
docker commit llmdemo
docker images
```
Note the image id of the new image
```
docker tag <image id> llmdemo
docker images
```
Remove original container
```
docker rm llemdemo
```

# Run llama.cpp
```
docker run -v ~/Documents/models/:/models --rm --name llamacpp -ti llmdemo
cd llama.cpp
./main -m ./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf -n 256 --repeat_penalty 1.0 --color  -r "User:" -i  --prompt 'You are a helpful assistant' --in-prefix 'USER: ' --in-suffix 'ASSISTANT: '
```
Enjoy!
