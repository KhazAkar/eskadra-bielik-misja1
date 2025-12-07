FROM ghcr.io/ggml-org/llama.cpp:server-cuda
# Listen on all interfaces
ENV LLAMA_ARG_HOST=0.0.0.0
# Use custom jinja template
ENV LLAMA_ARG_CHAT_TEMPLATE_FILE=/models/template.jinja

# Provide model folder
ENV LLAMA_ARG_MODELS_DIR=/models

# Provide model
ENV BIELIK_MODEL_NAME=Bielik-11B-v2.6-Instruct.Q4_K_M.gguf
# Provide model name for endpoint
ENV LLAMA_ARG_MODEL=/models/$BIELIK_MODEL_NAME

# Use only one slot
ENV LLAMA_ARG_CTX_SIZE=8192
ENV LLAMA_ARG_NO_ENDPOINT_SLOTS=true
ENV LLAMA_ARG_MODELS_MAX=1

# Create models folder
RUN mkdir -p /models
# Copy template
COPY template.jinja /models/template.jinja

# Download model from Huggingface using curl
RUN curl -L https://huggingface.co/speakleash/Bielik-11B-v2.6-Instruct-GGUF/resolve/main/Bielik-11B-v2.6-Instruct.Q4_K_M.gguf?download=true -o /models/Bielik-11B-v2.6-Instruct.Q4_K_M.gguf

EXPOSE 8080

# Start llama.cpp
ENTRYPOINT ["/app/llama-server"]
