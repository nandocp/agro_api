#! /bin/sh

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

echo 'Cleaning containers'
for container in db toolbox ollama openwebui
do
    name=agro_api-$container
    echo $name
    podman stop --filter name=$name > /dev/null 2>&1
    podman rm --filter name=$name > /dev/null 2>&1
done
