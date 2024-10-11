FROM python:3.12.4-bullseye

ENV http_proxy=http://proxy.fpt.vn:80
ENV https_proxy=http://proxy.fpt.vn:80

WORKDIR /app    

RUN python3.12 -m pip install --upgrade pip
RUN pip3.12 install poetry 

RUN poetry install

COPY . /app
