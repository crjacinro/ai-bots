# LLM Chat Backend

This project is a FastAPI Python application that simulates chat interfaces to ChatGPT.
It uses Beanie as the Object-Document Mapper (ODM) to interact with MongoDB. 
It is containerized using Docker for easy setup and deployment.

## Prerequisites

Before running the project, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9+](https://www.python.org/downloads/)

## Open API Key

This project depends on the OpenAI Client. This requires an OpenAI API key to interact with the large language model.
For security purposes, this key is not included in this repository and typically is set in pipeline as an environmental variable.

To run the server locally in Docker, provide a valid OpenAPI API key with enough credits in the `docker-compose.yml` environment variable.

`OPENAI_API_KEY=sk-<your key here>`

## Running using Docker Compose

Make sure Docker is running on your machine. To build and run the application with Docker, use the following command:

`docker compose up --build`

This command will:

- Build the FastAPI application image.
- Pull the official MongoDB image.
- Start the FastAPI app and MongoDB as containers.

It will watch the changes in the source directory and automatically rebuilds the app once changes are detected.

## Running Locally using venv

Though it is recommended to run the project using Docker, it can also be run using `venv` locally.

- `pip install virtualenv` - install virtualenv
- `virtualenv venv` - create a new venv environment
- `source venv/bin/activate` - activate the newly created venv
- `pip install -r requirements.txt` - install the dependencies

## Accessing MongoDB using Mongosh

It is helpful during development to access the MongoDB data locally. To do this, make sure you have installed [Mongosh](https://www.mongodb.com/docs/mongodb-shell/install/).
Typically, it is just a zip or tar file so add its path to the $PATH variable so that it can be invoked from any directory.

To connect to the database, use this command:

`mongosh mongodb://localhost:27017`

Make sure that the port number matches the value used in Docker.

Once connected, you can now query the database such as:

- `use <db_name>` - to use the specific database
- `show collections` - to show all models and documents
- `db.<collection_name>.find().pretty()` - to show all contents of a document

## CORS Setup

This backend app is enabled with CORS (Cross-Origin Resource Sharing). To consume the APIs in this app, make sure that the origin matches to 
all the origins listed in `main.py`. Most commonly, `http://localhost:3000` will be used for web applications such as React.

## Endpoints

This project comes with the following endpoints:

- `/conversations` - CRUD endpoints to store different chat interactions to an LLM.
- `/queries/{id}` - A POST endpoint that accepts user input prompt that is sent to an LLM and the LLM response is returned to the caller.
This endpoint requires an `id`. To initiate a conversation, call the `/conversations` API to acquire a conversation id.

For more information about the endpoints, refer to the `http://127.0.0.1:8000/redoc` for the generated OpenAPI documentation.