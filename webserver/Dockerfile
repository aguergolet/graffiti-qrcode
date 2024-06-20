FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3.9 python3.9-dev python3-pip openscad
WORKDIR /app/tlgCode
COPY ./tlgCode/* ./
WORKDIR /app
COPY main.py .
COPY requirements.txt .
COPY template.scad .
RUN pip3 install -r requirements.txt
WORKDIR /app/templates
COPY ./templates/* ./
WORKDIR /app
EXPOSE 5000
CMD ["python3", "main.py"]