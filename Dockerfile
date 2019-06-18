FROM python:3.5
COPY . /app
WORKDIR /app
ENV MODE server
RUN pip install -r requirements.txt
ENTRYPOINT ["python","WhenToBuy.py"]