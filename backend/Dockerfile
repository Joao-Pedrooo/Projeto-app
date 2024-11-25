
# Usar a imagem base do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários para o backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expor a porta para o backend
EXPOSE 5000

# Comando para iniciar o backend
CMD ["python", "app.py"]
