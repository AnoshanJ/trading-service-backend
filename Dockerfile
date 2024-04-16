# Development stage
FROM python:3.9-alpine AS development

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run tests (Assuming you have a test script named 'test_app.py')
CMD ["python", "test_app.py", "-v"]

# Production stage
FROM python:3.9-alpine AS production

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files for production
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user for running the application
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 50

# Set the environment variable to tell Flask to run in production
ENV FLASK_ENV=production

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
