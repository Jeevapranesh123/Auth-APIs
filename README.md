## Authentication and Authorization APIs

This is a FastAPI project that implements authentication and authorization APIs.

## Installation

1. Clone the repository

```bash
git clone <repo-url>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following environment variables

```bash
PROJECT_NAME=<project-name>
MONGO_PROD_DATABASE=<production-database-name>
MONGODB_URL=<mongodb-url>
```

```Note: Please have a mongodb instance running on your local machine or provide a mongodb url to connect to a remote instance.
    If you have docker installed, run the following command to start a mongodb instance on your local machine.
```

```bash
docker run -d -p 27017:27017 mongo
``` 

This will start a mongodb instance on port 27017. You can then use `mongodb://localhost:27017` as the mongodb url in the `.env` file.

```Note: This command doesn't preserve data. So if you want to preserve data, please use a volume to mount the data directory to the container.```


4. Run the application

For windows

```bash
uvicorn app.main:app --reload
```

For linux

```bash
./ini.sh
```
or 
```bash
sh ini.sh
```
or 
```bash
uvicorn app.main:app --reload
```

## Usage

1. Open the swagger documentation at `http://localhost:8000/docs` to view the available endpoints and interact with them.


