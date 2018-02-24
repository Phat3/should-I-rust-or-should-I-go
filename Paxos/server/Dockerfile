FROM python:2
# This is gonna be our root dirtevctory for the client
WORKDIR /usr/src/app
# Instalkl dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# copy the root of the application
COPY ./src ./
COPY ./config.csv ./config.csv
# run the app
CMD [ "python", "./main.py" ]