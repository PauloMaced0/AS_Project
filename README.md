# AS_Project TrotiNet
This project implements a service for scooter rental, similar to Uber. 
## Get Started
### Requirements
- Docker
- Docker-compose

### Installation
- Clone repository and cd into `TrotiNet_Webapp/`
- To run docker containers, run:

    ```bash
    docker compose up --build
    ```
    - Flask application will be available at http://localhost:5001
    - Prometheus metrics will be available at https://localhost:9090
        - Metrics:
            - Kafka service status 
            - scooter status and metrics

### Testing
After running docker containers, you can test the application by importing `TrotiNet_Webapp/TrotiNET.side` into Selenium IDE. There you will find all the scenarios of the user stories.