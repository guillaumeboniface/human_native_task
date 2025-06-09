# Getting started

This is an API service that exposes an endpoint allowing Human Native customers
to report violation of local laws by a data asset we provided.

## Installing dependencies
Create a virtual environment, we used python 3.12 for development and we make no guaranty of
compatibility with other versions
```
python -m venv venv
```
Activate the environment
```
source venv/bin/activate
```
Install the dependencies
```
pip install -r requirements.txt
```

## Running the test suite
```
pytest
```

## Running the service
```
python -m app.main
```

## Trying a request
```
curl -X POST "http://localhost:8000/violation" \
    -H "X-API-Key: api_key_1" \
    -H "Content-Type: application/json" \
    -d '{
          "dataset_id": "dataset_1",
          "item_id": "item_1",
          "jurisdictions": ["us", "eu"],
          "type": "privacy"
        }'
```

# Design choices

## Assumptions
Building this service, I assumed that:
- Customers already have a way to create and manage API keys. There's a persistent
layer that allows to check whether a key exists and to what user it belongs.
- The goal of the service is to allow for automated handling of those violations
downstream. For that reason, I did not include in the violation schema a
way to submit plain text explanation or catch-all type of violation. I assume that
for unforeseen violation, the customer will reach out to the team, at which point
we will decide whether to add the case they encountered to the API. We're starting
by supporting only "privacy" violation, but the service can easily be extended to
additional cases.
- We want to make reporting easy rather than put an unnecessary burden on the customer.
They are the ones paying us after all. For that reason and although I considered it,
the violation schema doesn't include a field to provide the details of where in the
asset the violation happened (as in the segment in an audio file for example)
- There's no need to allow for the management of those violations. Fetching, updating or
deleting violations were not covered.

## Violation request
The service expose a POST endpoint that takes in the body (see app/models/violation.py for the spec):
- dataset_id
- item_id (which corresponds to the "id" of the asset in the dataset)
- jurisdictions, which is a list of two letter codes marking against which set of rules
the violation is reported to be happening
- type, which is the type of violation (e.g privacy)

## Security
### Authentication
The calls are authenticated via an API key passed in the headers
### Rate limiting
I implemented a simple rate limiting logic to protect the service
from being overwhelmed by a single user.
## Scalability
Scalability wasn't the focus of the exercise, however the service could be scaled
with a few modifications:
- Scale horizontally by moving the authentication and rate limiting logic to an
API Gateway. Add a load balancer.
- Use redis for the rate limiting state, instead of doing it in memory
- Use a redis cache for the authentication logic to lighten the load on the DB.

# Next steps
To take this further I would:
- Integrate a persistence layer
- Add a Dockerfile for containerized deployment
- Add monitoring and logging using a 3rd party tool such as Datadog