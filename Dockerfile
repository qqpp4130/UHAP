FROM python:3.11.8-slim
WORKDIR /app
COPY . .
RUN /usr/local/bin/pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "/usr/local/bin/python", "-u", "init.py" ]
EXPOSE 8080/tcp