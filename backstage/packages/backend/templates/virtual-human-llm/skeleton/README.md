# LLM Communication Project

This project provides a robust framework for interacting with Large Language Models (LLMs). It supports:
- Local LLM deployment: Run and interact with the model on your local machine.
- OpenAI integration: Fetch responses from OpenAI models using your API key.
- Containerization & orchestration: Fully dockerizable and can be deployed to a Kubernetes cluster for scalable production use.

# Key Features

- Flexible LLM usage: Choose between local models or cloud-based OpenAI models.
- Easy deployment: Pre-configured for Docker and Kubernetes.
- Extensible architecture: Designed for integrating additional models or custom workflows.

# Getting Started
- Create local env: `python -m venv venv`
- Activate local env: `.\venv\Scripts\Activate.ps1`
- Download dependencies: `pip install -r ./dependencies/local.txt`
- Run the controller.py: `python controller.py`
