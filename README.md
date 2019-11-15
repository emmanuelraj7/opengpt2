# OpenAI GPT-2 in Production 

This project enables you to deploy openAI's GPT-2 to production. Using python, flask, Apache server, Docker and Kubernetes.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a production system.

clone the repo.
```
git clone https://github.com/emmanuelraj7/opengpt2.git
```

### Prerequisites

What things you need to install the software and how to install them

```
pip3 install -r requirements.txt
```

and tensorflow-gpu to run in a GPU
```
pip3 install tensorflow-gpu==1.12.0
```

### Run Locally

After installing needed dependencies

```
Navigate to /flask_demo
```

Download model data: downloads models with 124, 355, 774 Million and 1.5 Billion parameters

```
python3 download_model.py 124M
python3 download_model.py 355M
python3 download_model.py 774M
python3 download_model.py 1558M
```

And run the development server
```
python3 flask_predict_api.py
```


server will run on http://0.0.0.0:5000/
access api documentation - http://0.0.0.0:5000/apidocs



## Deployment

1. Containerize the application using docker. Create a container,

```
docker build --tag openai-gpt2 .
```

2. Push the docker container image to docker hub/registry of your choice from where you can deploy to your target kubernetes cluster or needed deployment target.

docker push "container-id/tag"

To run it locally:


```
docker run -d -p 8000:8000 containerid
```

Bind port 8000 of the container to your local machine, as the Apache server in the container is running at port 8000.


## Built With

* [Python](http://www.https://www.python.org/) - Programming language used
* [Flask](http://flask.palletsprojects.com/) - The web framework used
* [Apache](https://httpd.apache.org/) - Server to host the web application
* [Docker](https://www.docker.com/) - Used for containerizing the application
* [Kubernetes](https://kubernetes.io/) - Container-orchestration system for deployments, scaling and managment



## Authors

* **Emmanuel Raj** - *Machine Learning Engineer, Tieto* - 


## License

This project has MIT license, check LICENSE file for more info and feel free to use it.

## Acknowledgments

* [OpenAI team](https://openai.com/) - For releasing the GPT-2 models and code. 
* Code for OpenAI's GPT-2 was taken from [OpenAI repo](https://github.com/openai/gpt-2) and using this I build Flask, Apache and Docker image for deployment. 