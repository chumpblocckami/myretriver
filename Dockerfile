FROM python:3.10-slim-bullseye
ENV LISTEN_PORT 8080
EXPOSE 8080
RUN apt-get update && apt-get install -y git
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
WORKDIR app/

COPY ./src ./src
COPY ./images ./images
COPY ./app.py ./app.py
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]