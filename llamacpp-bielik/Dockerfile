FROM ghcr.io/ggml-org/llama.cpp:server
# Listen on all interfaces
ENV LLAMA_ARG_HOST=0.0.0.0
# Store model weight files in /models
ENV LLAMA_ARG_MODELS_DIR=/models
# Use custom jinja template
ENV LLAMA_ARG_CHAT_TEMPLATE=/models/template.jinja

# Provide model
ENV BIELIK_MODEL_NAME=speakleash/Bielik-11B-v2.6-Instruct-GGUF:q4_k_m
ENV LLAMA_ARG_HF_REPO=$BIELIK_MODEL_NAME

# Copy template
COPY template.jinja /models/template.jinja

EXPOSE 8080

# Start llama.cpp
ENTRYPOINT ["/app/llama-server"]
