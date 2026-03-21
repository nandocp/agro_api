#! /bin/sh

# Verifica se podman/docker está instalado
if command -v podman &> /dev/null; then
    CMD="podman"
    echo -e "${GREEN}🐳 Using Podman${NC}"
elif command -v docker &> /dev/null; then
    CMD="docker"
    echo -e "${GREEN}🐳 Using Docker${NC}"
else
    echo -e "${RED}❌ Neither docker nor podman found${NC}"
    exit 1
fi

if ! $CMD image inspect localhost/agro_api-toolbox >/dev/null 2>&1; then
    echo "❌ ERROR: Image agro_api-toolbox not found!" >&2
    echo "⚠️ Execute: bin/build" >&2
    exit 1
else
    echo -e "${GREEN}✅ Image localhost/agro_api-toolbox found${NC}"
fi

$CMD network create agro_api_network 2>/dev/null || true

echo '🐳 Initializing agro-api db'
$CMD run -d \
    --name agro_api-db \
    -p 5432:5432 \
    -dit \
    -e POSTGRES_HOST_AUTH_METHOD=trust \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -v agro_api_db:/var/lib/postgresql \
    --replace \
    docker.io/postgis/postgis:18-3.6-alpine "$@" > /dev/null 2>&1

# if $CMD image inspect agro_api-ollama >/dev/null 2>&1; then
#     echo '🐳 Initializing agro-api Ollama server'
#     $CMD run -d \
#         --name agro_api-ollama \
#         --network agro_api_network \
#         -p 11434:11434 \
#         -v agro_api_ollama:/home/ubuntu/.ollama \
#         --user 1000:1000 \
#         --userns=keep-id \
#         --device nvidia.com/gpu=all \
#         --security-opt label=disable \
#         --replace \
#         localhost/agro_api-ollama:latest

#     echo "🚀 Initializing agro-api Open WebUI"
#     $CMD run -d \
#         --name agro_api-openwebui \
#         --network agro_api_network \
#         -p 3000:8080 \
#         -v agro_api_openwebui:/app/backend/data \
#         -e OLLAMA_BASE_URL=http://agro_api-ollama:11434 \
#         -e USER_AGENT=agro_api \
#         -e WEBUI_AUTH=False \
#         --replace \
#         ghcr.io/open-webui/open-webui:main-slim
# else
#     echo "⚠️ WARN: Image localhost/agro_api-ollama not found!" >&2
# fi

echo '📦 Initializing agro-api toolbox'
toolbox create --image localhost/agro_api-toolbox:latest agro_api-toolbox > /dev/null 2>&1
toolbox enter agro_api-toolbox

$(pwd)/scripts/toolbox/stop.sh
