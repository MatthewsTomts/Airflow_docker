FROM apache/airflow:3.0.1

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

USER root

# Update package lists and install OpenJDK 17
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

USER airflow
