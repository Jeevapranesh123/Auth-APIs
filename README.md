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


