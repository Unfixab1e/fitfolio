FROM python:3.9-slim
WORKDIR /usr/src/app
COPY ./requirements ./requirements
RUN pip install --no-cache-dir -r ./requirements/development.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]