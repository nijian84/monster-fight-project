FROM python:3.12

WORKDIR /monster-fight-project

# Copy the current directory contents into the container at /monster-fight-project
COPY . /monster-fight-project

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["python3", "main.py"]