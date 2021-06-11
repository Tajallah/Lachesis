FROM python:3.9
WORKDIR /metatron0
COPY requirements.txt requirements.txt
COPY .env .env
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "wiki.py"]
