FROM ubuntu

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

RUN apt-get update -y && apt-get install -y python3 python3-pip

# install dependencies
RUN pip3 install numpy pandas seaborn jupyter

# tell the port number the container should expose
EXPOSE 5000

# run the command
CMD ["sh", "-c", jupyter notebook --no-browser --port=5000 --ip='0.0.0.0' --allow-root"]