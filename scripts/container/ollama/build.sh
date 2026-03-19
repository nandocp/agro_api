#!/bin/sh

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações padrão
DEFAULT_MODEL="deepseek-r1:7b"
DEFAULT_TAG="ollama-server:latest"
DEFAULT_OLLAMA_MODELS="/home/ubuntu/.ollama"

# Função de ajuda
show_help() {
    cat << EOF
${BLUE}=== Ollama Build Script ===${NC}

Uso: $0 [OPÇÕES]

OPÇÕES:
    -m, --model MODEL       Specifies which model will be downloaded (default: $DEFAULT_MODEL)
    -t, --tag TAG           Image tag (padrão: $DEFAULT_TAG)
    -p, --path PATH         Models path (padrão: $DEFAULT_OLLAMA_MODELS)
    --no-cache              Build without cache
    --pull                  Always pull base image
    --help                  Shows help

    EXAMPLES:
    $0 -m deepseek-r1:7b
    $0 --model deepseek-r1:14b --tag meu-deepseek:latest
    $0 --no-cache --pull

EOF
}

MODEL="$DEFAULT_MODEL"
TAG="$DEFAULT_TAG"
OLLAMA_MODELS="$DEFAULT_OLLAMA_MODELS"
BUILD_ARGS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -p|--path)
            OLLAMA_MODELS="$2"
            shift 2
            ;;
        --no-cache)
            BUILD_ARGS+=("--no-cache")
            shift
            ;;
        --pull)
            BUILD_ARGS+=("--pull-always")
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown arg: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

echo -e "${BLUE}=== Ollama Build Script ===${NC}"
echo -e "${GREEN}📦 Settings:${NC}"
echo "   • Model: $MODEL"
echo "   • Image tag: $TAG"
echo "   • Model path: $OLLAMA_MODELS"
echo "   • Extra args: ${BUILD_ARGS[*]:-nenhum}"

# Verifica se podman/docker está instalado
if command -v podman &> /dev/null; then
    CMD="podman"
    echo -e "${GREEN}🐳 Usando Podman${NC}"
elif command -v docker &> /dev/null; then
    CMD="docker"
    echo -e "${GREEN}🐳 Usando Docker${NC}"
else
    echo -e "${RED}❌ Neither docker or podman found${NC}"
    exit 1
fi

# Verifica GPU NVIDIA
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${YELLOW}⚠️  NVIDIA GPU not detected. Container will run over CPU (slow).${NC}"
else
    echo -e "${GREEN}🎮 GPU NVIDIA detected:$(nvidia-smi --query-gpu=name --format=csv,noheader | head -n1)${NC}"
fi

# Build da imagem
echo -e "${BLUE}🔨 Building...${NC}"
echo -e "${YELLOW}Command: $CMD build \\"
echo "  --build-arg OLLAMA_MODEL=\"$MODEL\" \\"
echo "  --build-arg OLLAMA_MODELS_DIR=\"$OLLAMA_MODELS\" \\"
for arg in "${BUILD_ARGS[@]}"; do
    echo "  $arg \\"
done
echo "  -t $TAG .${NC}"

# Executa o build
$CMD build \
    --build-arg OLLAMA_MODEL="$MODEL" \
    --build-arg OLLAMA_MODELS_DIR="$OLLAMA_MODELS" \
    --format docker \
    "${BUILD_ARGS[@]}" \
    -t agro_api-ollama:latest \
    -f scripts/container/ollama/Containerfile
$CMD volume create --ignore agro_api_ollama > /dev/null 2>&1

# Verifica resultado
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build concluído com sucesso!${NC}"
else
    echo -e "${RED}❌ Falha no build${NC}"
    exit 1
fi
