# Model Trainer App

A Flask-based application for training machine learning models with authentication.

## Features

- Train models via `/train` endpoint
- Download trained models via `/download/<model_name>` endpoint
- Basic HTTP authentication to secure endpoints
- Uses Localtunnel to expose the Flask app publicly

## Installation

```bash
pip install model_trainer_app

npm install -g localtunnel

