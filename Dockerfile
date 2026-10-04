# Get the base image
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Create the virtual environment (venv)
RUN python -m venv .venv

# Switch the default shell from /bin/sh to /bin/bash
SHELL ["/bin/bash", "-c"]

# Activate the virtual environment
RUN source .venv/bin/activate

# Force Docker to use the virtual environment for everything automatically
ENV PATH="/app/.venv/bin:$PATH"

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Set the entry point for the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
