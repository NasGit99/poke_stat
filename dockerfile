FROM python:3.10.5
#creating directory
RUN mkdir /app
#installing requests
RUN pip install requests
#RUN pip install time 
# adding application to directory
#ADD pokemon_stat.py /app

WORKDIR /app
#type of technology/ how are we executing container
ENTRYPOINT [ "python" ]
#which file we want to run in the container
CMD ["pokemon_stat.py"]
#EXPOSE 5000
#docker build -t pokestat-docker . the ., is so it picks up this docker file within this directory
#docker run -ti pokestat-docker