# Creator OS

A prototype Instagram growth-intelligence dashboard built with FastAPI, React/TypeScript, PostgreSQL, Redis, Celery, and scikit-learn.

## Implemented building blocks

- JWT registration/login and user-owned page/post routes.
- Page and post management with metrics.
- Seven-signal scoring, recommendations, and a Random Forest virality component.
- Dashboard charts and background-task definitions.
- Synthetic demo data for local exploration.

## Status and limits

This is **not a verified production-ready deployment**. Background Instagram sync currently generates random demo metrics; it does not connect to Instagram. Scores are prototype heuristics, not validated predictions of future growth. Setting INSTAGRAM_API_ENABLED does not implement an Instagram integration.

The checked-in Docker Compose frontend configuration conflicts with the frontend image, and the ORM model contains a reserved-name issue. See [known issues and testing](docs/TESTING_AND_LIMITATIONS.md) before following setup instructions.

## Documentation

- [Setup and environment](SETUP.md)
- [API reference](API.md)
- [Architecture and scoring](ARCHITECTURE.md)
- [Deployment considerations](DEPLOYMENT.md)
- [Project status](PROJECT_SUMMARY.md)
- [User workflow and data handling](docs/USER_GUIDE.md)
- [Testing and limitations](docs/TESTING_AND_LIMITATIONS.md)
- [Contributing](CONTRIBUTING.md)

The backend defines /health and /docs on port 8000. The Vite development configuration uses port 3000. These are local endpoints, not a hosted demo.

## Licensing

The original README stated MIT, but no LICENSE file is supplied in the repository. That historical declaration is preserved here; a complete license file and copyright attribution remain for the owner to establish. This documentation update does not choose new license terms.

## Verification scope

Documentation has been reviewed against source files, without deploying services or running a production/ML benchmark. No screenshot, successful deployment, or test-pass claim is fabricated.
