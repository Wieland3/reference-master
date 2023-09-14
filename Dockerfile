FROM python:3.8
COPY requirements.txt /
RUN apt-get update && apt-get install -y libsndfile1
RUN pip3 install -r /requirements.txt
COPY reference_master reference_master
COPY webapp webapp
COPY songs songs
COPY settings.yaml settings.yaml
WORKDIR /webapp
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app:app"]

