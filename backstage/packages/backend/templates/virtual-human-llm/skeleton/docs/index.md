# Virtual Human LLM Service

## Overview
This service provides a lightweight API for LLM-powered virtual human interactions. It supports both local models and OpenAI-backed models.

## Architecture
The service exposes a controller API that routes requests to the configured model provider.

## Configuration
- OPEN_AI_KEY (optional): Set to enable OpenAI-backed requests.

## Running locally
- Create local env: `python -m venv venv`
- Activate local env: `\\venv\\Scripts\\Activate.ps1`
- Download dependencies: `pip install -r ./dependencies/local.txt`
- Run the controller: `python controller.py`

## Relational diagrams
See `docs/diagrams.md` for entity relationships.
