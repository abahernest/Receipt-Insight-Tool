FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN ls .

COPY . .

RUN pip install -r requirements.txt
