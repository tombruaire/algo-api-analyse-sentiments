FROM python:3.9-slim

WORKDIR /app

ARG PORT

ENV PORT=${PORT}
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_DEBUG=${FLASK_DEBUG}

COPY requirements.txt .

# Installer d'abord les bibliothèques lourdes
RUN pip install flask-cors
RUN pip install --upgrade pip
RUN pip install --no-cache-dir torch transformers

# Installer ensuite les bibliothèques rapides
RUN pip install --no-cache-dir flask python-dotenv mysql-connector-python scikit-learn pandas numpy matplotlib seaborn

COPY . .

EXPOSE ${PORT}

CMD ["python3", "app.py"]
