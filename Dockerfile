#base image, Base OS Ubuntu and Python Runtime
FROM python:3.9-slim
#working directory
WORKDIR /app
#copy all the file and folder into working directory
COPY . /app

# UPDATE all the os packages
RUN apt-get update

#Installing wget
#wget is a package used to download files from the link
RUN apt install wget -y

#downloading the model from the storage
RUN wget "https://model-cd-classification.s3.eu-north-1.amazonaws.com/best_epoch_cnn.h5"

#install the packages for APP
#dependencies for opencv
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

#all the python libraries
RUN pip install --no-cache-dir -r requirements.txt

#open the port for running the app
EXPOSE 5000

#CMD starting the app #run the flaskapp
CMD ["python", "app.py"]
