#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEX_FILE="${1:-template.tex}"
BASENAME="${TEX_FILE%.tex}"

if [[ ! -f "$ROOT_DIR/$TEX_FILE" ]]; then
  echo "Error: no existe $TEX_FILE en $ROOT_DIR" >&2
  exit 1
fi

run_local() {
  local engine="$1"
  echo "Compilando con $engine (local)..."
  "$engine" -interaction=nonstopmode -halt-on-error "$TEX_FILE"
  "$engine" -interaction=nonstopmode -halt-on-error "$TEX_FILE"
}

run_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "Error: no hay compilador LaTeX local ni Docker disponible." >&2
    exit 2
  fi

  local image="blang/latex:ctanfull"
  echo "Compilando con Docker image $image ..."
  docker run --rm -v "$ROOT_DIR":/workdir -w /workdir "$image" \
    bash -lc "pdflatex -interaction=nonstopmode -halt-on-error '$TEX_FILE' && pdflatex -interaction=nonstopmode -halt-on-error '$TEX_FILE'"
}

cd "$ROOT_DIR"

if command -v pdflatex >/dev/null 2>&1; then
  run_local pdflatex
elif command -v xelatex >/dev/null 2>&1; then
  run_local xelatex
elif command -v lualatex >/dev/null 2>&1; then
  run_local lualatex
else
  run_docker
fi

if [[ -f "$BASENAME.pdf" ]]; then
  echo "PDF generado: $ROOT_DIR/$BASENAME.pdf"
else
  echo "No se encontró el PDF esperado ($BASENAME.pdf)." >&2
  exit 3
fi
