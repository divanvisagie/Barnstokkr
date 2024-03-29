# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /usr/src/app

RUN pip install fastapi uvicorn transformers torch accelerate
# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
