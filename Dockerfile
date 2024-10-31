FROM python:3.10-slim

# Copy the python scripts into the service
COPY main.py /main.py
COPY helpers.py /helpers.py

# Install required Python packages
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


# Run the main script
CMD ["python", "main.py"]