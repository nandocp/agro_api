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

echo -e "${BLUE}🔨 Building development box${NC}"
$CMD build -t localhost/agro_api-toolbox:latest -f scripts/toolbox/Containerfile.dev


echo -e "${BLUE}🔨 Building database${NC}"
$CMD volume create --ignore agro_api_db > /dev/null 2>&1

echo -e "${BLUE}🔨 Building ollama${NC}"
$(pwd)/scripts/container/ollama/build.sh --model qwen3:4b

# if [[ "$@" == "--build-ollama"]] && [["$@" != "--no-build-ollama" ]]
# then
#     echo -e "${BLUE}🔨 Building ollama${NC}"
# fi
