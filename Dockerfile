# Usar a imagem base oficial do Python 3.10 slim
FROM python:3.10-slim

# Definir variáveis de ambiente para evitar problemas de interação durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Baixar e instalar a última versão estável do Google Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -f -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm google-chrome-stable_current_amd64.deb

# Instalar o ChromeDriver manualmente
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

# Atualizar pip e instalar as dependências do projeto Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exposição da porta utilizada pelo aplicativo
EXPOSE 7000

# Comando para executar a aplicação
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7000", "app:app", "--log-level", "info"]
