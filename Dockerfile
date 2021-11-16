FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt
ADD . /app
ADD wait-for-it.sh /app
RUN chmod +x /app/wait-for-it.sh
EXPOSE 8081 

# Install imagemagick with apt, since it's a dependency
RUN apt update
RUN apt install imagemagick -y