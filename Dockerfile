# Usar a imagem base oficial do Python 3.10 slim
FROM python:3.10-slim

# Baixar e instalar a última versão estável do Google Chrome
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -f -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm google-chrome-stable_current_amd64.deb

# Definição do diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

# Atualizar pip e instalar as dependências do projeto Python, incluindo chromedriver_autoinstaller
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install chromedriver_autoinstaller

# Exposição da porta utilizada pelo aplicativo
EXPOSE 7000

# Comando para executar a aplicação
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7000", "app:app", "--log-level", "info"]
