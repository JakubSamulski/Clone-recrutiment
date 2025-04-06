# Clone recruitment task

## Backend
created with Django Rest Framework
### My assumptions
- I've created a simple mock as in the assigment so the robot is represented
by an python object instead of a database table (as the assigment stated this should be a simple mock)
- The state transitions were unclear in the pdf (more info in the robot.py near 109 line) so i assumed that the state machine looks like
  - offline -> idle
  - idle -> offline or running
  - running -> idle or offline or error
  - error -> idle or offline 

- also the command line config feels odd for a web app (at least in my opinion)
and the better way of doing it would be with env variables, as it would also play well
with ci pipeline

### how to run
It can be run locally or with docker (more in docker section)
- cd into the backend directory ```cd backend```
- create a virtual environment ```python3 -m venv venv```
- activate the virtual environment ```source venv/bin/activate```
- install the requirements ```pip install -r requirements.txt```
- run the server ```python manage.py run <host> <port> <log_level> <refresh_rate>```.
The defaults are localhost, 5478, INFO, 10

## frontend
created with React and vite
### how to run
- cd into the frontend directory ```cd frontend/my-robot-controller```
- install the requirements ```npm install```
- run the server ```npm run dev```
You can specify backend url in the .env file by filling .env.template


## Docker
Created simple docker config
It's not production ready, in production the backend should use uvicorn (or similar) and the frontend should be served with nginx(or similar)
### how to run
- you can specify backend config with ``` docker compose build --build-arg <arg>=<value>```
- set BACKEND_PORT env variable (depending on the os)
- to run the backend and frontend together ```docker compose up -d```

## extras
- added pylint config
- added black config
- added pre-commit config