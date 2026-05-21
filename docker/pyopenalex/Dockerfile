FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python-scripts/ .

# Volúmenes esperados desde el pipeline anterior (pyextract/pygrobid)
VOLUME ["/input", "/output"]

# Variables de entorno
# OPENALEX_EMAIL  → tu e-mail para el polite pool (recomendado, no obligatorio)
# OPENALEX_BASE_URL → por defecto https://api.openalex.org
ENV OPENALEX_EMAIL=""
ENV OPENALEX_BASE_URL="https://api.openalex.org"
ENV INPUT_DIR="/input"
ENV OUTPUT_DIR="/output"

CMD ["python", "main.py"]
