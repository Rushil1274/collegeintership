#Use an official Python runtime as a parent image with Python 3.10
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]