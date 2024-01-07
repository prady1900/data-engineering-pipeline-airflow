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
![Python,Docker,SKlearn](https://skillicons.dev/icons?i=python,docker,sklearn)

### Tools Used
![Airflow]([https://upload.wikimedia.org/wikipedia/commons/d/de/AirflowLogo.png](https://dash.elest.io/templatesIcones/Airflow.png))

![ServiceNow]([https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/ServiceNow_logo.svg/2560px-ServiceNow_logo.svg.png](https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/b3/0e/18/b30e187a-48f1-f3cf-2a2d-6c69fe1b27e3/SNAppIcon-1x_U007emarketing-0-7-0-0-85-220-0.png/256x256bb.jpg)https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/b3/0e/18/b30e187a-48f1-f3cf-2a2d-6c69fe1b27e3/SNAppIcon-1x_U007emarketing-0-7-0-0-85-220-0.png/256x256bb.jpg)

