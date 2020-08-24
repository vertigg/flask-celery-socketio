# Flask-Celery-SocketIO-ReactJS

Example of web application based on Flask with Flask-SocketIO, Celery, RabbitMQ and React.JS on the frontend.

# Installation

Build frotend part using these commands:

On Linux

```
cd frontend
./build-local.sh
```

On Windows

```
cd frontend
npm run build
manually copy static folder contents to ../static and build folder contents to ../templates
```

After that:
```
docker-compose up
```
