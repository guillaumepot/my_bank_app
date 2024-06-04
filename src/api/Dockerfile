# Version : 0.2.0
# Current state : Dev
# Author : Guillaume Pot
# Contact : guillaumepot.pro@outlook.com

# API image
FROM python:3.10

# Define Workdir
WORKDIR /app

# Copy files
COPY ./requirements.txt /app
COPY ./api.py /app
COPY ./generate_secret_key.py /app
COPY ./generate_secret_key.sh /app


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./generate_secret_key.sh


# Port to expose
EXPOSE 8000

# Start uvicorn server
CMD uvicorn api:app --host $UVICORN_HOST --port $UVICORN_PORT

# Define the entrypoint
ENTRYPOINT ["./generate_secret_key.sh"]