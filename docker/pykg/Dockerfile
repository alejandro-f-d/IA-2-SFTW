FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python-scripts/ .

VOLUME ["/input", "/output", "/ontology"]

ENV INPUT_DIR="/input"
ENV OUTPUT_DIR="/output"
ENV ONTOLOGY_PATH="/ontology/citation_ontology.ttl"

CMD ["python", "main.py"]
