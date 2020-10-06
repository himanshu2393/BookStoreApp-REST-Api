# Use an official Python runtime as a parent image
FROM python:3.7

# Adding backend directory to make absolute filepaths consistent across services
WORKDIR /app/backend

# Install Python dependencies
COPY requirements.txt /app/backend
RUN pip install --upgrade pip -r requirements.txt

# Add the rest of the code
COPY . /app/backend

# Make port 8080 available for the app
EXPOSE 8080

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]