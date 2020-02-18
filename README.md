# User Service
This is a REST API to be used as an interface for the user
management.

## Installation
The app and the db run each on a Docker container, and talk to each
other through docker-compose. This means that the only requirements
are [Docker](https://docs.docker.com/install/)
and [docker-compose](https://docs.docker.com/compose/install/).
```bash
git clone https://gitlab.com/heruapp/user_service
cd user_service
# May need sudo depending on the OS
docker-compose up db
```
This will get the API running on http://localhost:8000

## Endpoints

This service is autodocumented by [Swagger](https://swagger.io/) using
the [OpenAPI standard specification](https://www.openapis.org/).

To see the available endpoints, point your browser to
<http://localhost:8000/api/v1/> while the service is running.
