# ML-Pipeline using ServiceNow and Apache Airflow

The pipeline includes extracting data from the data source, transforming the data, storing it into a database, and building an ML model from the data. The following technologies were used in this project: Docker, Apache Airflow, Scikit-learn, Pandas, and ServiceNow.

## Problem Statement

The goal of this project is to build an end-to-end data pipeline to train a machine learning model to predict the resolution time of an incident.

## Pre-requisites

Build the docker file for creating your custom airflow image with sk-learn

## Pipeline Stages

The pipeline is represented as a Directed Acyclic Graph (DAG) with three stages:

### 1. Extract Data from ServiceNow

In this stage, we extract our dataset, which is a list of incidents created in the ServiceNow table. Here we utilize the ServiceNow's Table API with Query for extracting only the latest incident data created on that particular day. We will use this raw data to transform and load it into our database of our choice.

### 2. Load Data in DB

This stage creates a table and loads the required data into the database, i.e., Postgres. Once the data is extracted from the 1st DAG, the database DAG gets triggered, and then we perform preprocessing, create a table if not already present in Postgres, and upload the data into the table. All the database operations are performed using `postgres_hook` provided by Airflow.

### 3. Training the ML Model

This stage creates our actual ML model for use. Here we utilize the Scikit-learn library to train our machine learning model. A simple preprocessing step like One-hot encoding is performed for the categories column of our incident data. Once the model is created, it is translated into a Pickle file for predicting the output.

## Way Forward

Use Spark Jobs to perform ML-modeling and preprocessing.


### Technologies Used
![Python,Docker,SKlearn](https://skillicons.dev/icons?i=python,docker)

### Tools Used

![Airflow](https://github.com/prady1900/machine-learning-pipeline/blob/main/Airflow.png)
![SERVICENOW.jpg](https://github.com/prady1900/machine-learning-pipeline/blob/main/SERVICENOW.jpg)
