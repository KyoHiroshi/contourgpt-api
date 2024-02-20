FROM python:3.11.3
# RUN python -m pip install oracledb
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

CMD ["python", "app.py"]