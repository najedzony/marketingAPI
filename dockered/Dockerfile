FROM python:3.9-slim-buster

#WORKDIR /python-docker

COPY ./dockered/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


ENV FLASK_ENV=dev
ENV SECRET_KEY="dev"
ENV JWR_SECRET_KEY='JWR_SECRET_KEY'

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000