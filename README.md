# Weather App on Kubernetes (Cloud Computing Course Project)

This project runs a weather web application on a local Kubernetes cluster (Minikube) using Docker containers.

## Credits
Based on the open-source project "What's the Weather?" by crcsmnky:
https://github.com/crcsmnky/weatherinfo (Apache License 2.0)

## Changes made
- Changed the base image of the services from `python:2.7-slim` to `python:3.9-slim`.
- Removed Locust load-testing libraries from `requirements.txt` (not needed by the frontend/backends).
- Built the Docker images locally instead of using Google Cloud Build, and loaded them into Minikube with `minikube image load`.
- Set `imagePullPolicy: IfNotPresent` so Kubernetes uses the local images.

## Cloud concepts demonstrated
- Containers (Docker)
- Container orchestration (Kubernetes Deployments and Services)
- Microservices (frontend and backend services)
- Secrets management (OpenWeatherMap API key stored as a Kubernetes Secret, not in the code)

## How to run
1. Start Docker Desktop and run: `minikube start --driver=docker`
2. Build the three images and load them into Minikube.
3. Create the secret: `kubectl create secret generic openweathermap --from-literal=apikey=YOUR_API_KEY`
4. Deploy: `kubectl apply -f manifests/weather-deployment.yaml`
5. Run: `kubectl port-forward deployment/weather-frontend 5000:5000` and open http://localhost:5000

Author: {Cloud`s Project Team:George,Yasmeen, Mena,Rana,Yara]
