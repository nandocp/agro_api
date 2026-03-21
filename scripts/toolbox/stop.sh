#! /bin/sh

# Verifica se podman/docker está instalado
if command -v podman &> /dev/null; then
    CMD="podman"
elif command -v docker &> /dev/null; then
    CMD="docker"
else
    echo -e "${RED}❌ Neither docker or podman found${NC}"
    exit 1
fi

echo 'Cleaning containers'
for container in db toolbox
do
    name=agro_api-$container
    echo $name
    podman stop --filter name=$name > /dev/null 2>&1
    podman rm --filter name=$name > /dev/null 2>&1
done
