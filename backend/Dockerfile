# Usando uma imagem leve do Python
FROM python:3.9-slim

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiando o arquivo de dependências
COPY requirements.txt .

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante do código
COPY . .

# Expondo a porta 5000 para o Flask
EXPOSE 5000

# Comando para rodar o servidor Flask
CMD ["python", "app.py"]
