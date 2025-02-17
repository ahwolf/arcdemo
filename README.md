# ARC demo

[![check.yml](https://github.com/ahwolf/arcdemo/actions/workflows/check.yml/badge.svg)](https://github.com/ahwolf/arcdemo/actions/workflows/check.yml)
[![publish.yml](https://github.com/ahwolf/arcdemo/actions/workflows/publish.yml/badge.svg)](https://github.com/ahwolf/arcdemo/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://ahwolf.github.io/arcdemo/)
[![License](https://img.shields.io/github/license/ahwolf/arcdemo)](https://github.com/ahwolf/arcdemo/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/ahwolf/arcdemo)](https://github.com/ahwolf/arcdemo/releases)

Workflow for call logs.


ARC Demo is an MLOps pipeline designed for an end-to-end machine learning case study. This repository provides a structured scaffolding to develop a complete ML pipeline, covering data ingestion, preparation, training, evaluation, deployment, and monitoring.

Currently, the project includes data ingestion and data preparation steps, with future expansions planned for:
	•	Model Training & Evaluation
	•	Monitoring & Retraining Automation
	•	Model Deployment

# Completed Steps

1. Data Ingestion
	•	Reads raw data from CSV files (or other sources like APIs, databases, cloud storage).
	•	Saves the data for preprocessing.

2. Data Preparation
	•	Truncates historical data to keep only the last n hours.
	•	Geohashes location data (latitude, longitude) for spatial analysis.
	•	Aggregates data into fixed time intervals (TIME_GAP in seconds).
