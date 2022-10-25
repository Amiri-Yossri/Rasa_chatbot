FROM python:3.8-slim
RUN python -m pip install rasa==3.1
WORKDIR /app
COPY . .
RUN rasa train nlu
#set the user to run, don't run as root 
USER 1001
#set the entrypoint for interactive shells 
ENTRYPOINT ["rasa"]
#command to run when container called to run
CMD ["run", "--enable-api", "--port", "8080"]
