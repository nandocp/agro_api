#!/bin/sh
# docker-entrypoint.sh

set -e

# Verifica se é um comando do Poetry
if [[ "$1" == "poetry" ]]; then
    shift
    exec poetry "$@"
fi

# Se não for um comando específico, instala dependências e executa o comando
if [ -f pyproject.toml ] && [ ! -d ".venv" ] || [ ! -f ".venv/bin/activate" ]; then
    echo "Instalando dependências do Poetry..."
    poetry config virtualenvs.create false
    poetry install --no-interaction --no-ansi

    # Cria arquivo de ativação simbólico para o venv
    if [ ! -f ".venv/bin/activate" ]; then
        mkdir -p .venv/bin
        ln -sf /usr/local/bin/true .venv/bin/activate
    fi
fi

# Executa o comando passado
exec "$@"
