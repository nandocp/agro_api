#!/bin/bash
set -e

# Configurações vindas do build
MODEL_NAME="${MODEL_NAME:-deepseek-r1:7b}"
MODELS_DIR="${MODELS_DIR:-/home/ubuntu/.ollama}"

# Função de log com timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🚀 Initializing Ollama sever"
log "📦 Model configured: $MODEL_NAME"
log "📂 Models directory: $MODELS_DIR"
log "🏠 Home: $HOME"

# Inicia o servidor em background
log "⏳ Initializing server..."
ollama serve &
SERVER_PID=$!

# Aguarda o servidor ficar pronto
log "⏳ Waiting for server to initialize"
MAX_RETRIES=30
RETRY_COUNT=0

until ollama list > /dev/null 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        log "❌ Servidor não iniciou após $MAX_RETRIES tentativas"
        exit 1
    fi
    log "⏳ Tentativa $RETRY_COUNT/$MAX_RETRIES..."
    sleep 2
done

log "✅ Servidor pronto!"

# Verifica se o modelo já existe
if ! ollama list | grep -q "$MODEL_NAME"; then
    log "📥 Modelo $MODEL_NAME não encontrado. Baixando..."

    # Tenta baixar com retry
    DOWNLOAD_RETRIES=3
    for i in $(seq 1 $DOWNLOAD_RETRIES); do
        log "⏳ Tentativa $i/$DOWNLOAD_RETRIES..."
        if ollama pull "$MODEL_NAME"; then
            log "✅ Modelo baixado com sucesso!"
            break
        else
            if [ $i -eq $DOWNLOAD_RETRIES ]; then
                log "❌ Falha ao baixar modelo após $DOWNLOAD_RETRIES tentativas"
                exit 1
            fi
            log "⚠️  Falha na tentativa $i. Aguardando 5 segundos..."
            sleep 5
        fi
    done
else
    log "✅ Modelo $MODEL_NAME já está disponível"
fi

# Mostra informações do modelo
log "📊 Modelos disponíveis:"
ollama list

log "🚀 Servidor pronto para uso na porta 11434"
log "📝 Logs do servidor:"

# Mantém o servidor em foreground e captura saída
wait $SERVER_PID
