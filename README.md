# TicketRoute API

TicketRoute is a personal project for learning FastAPI and improving my backend engineering skills through a practical use case.

The project uses a pretrained transformer model to classify the intent of banking support messages. It covers API design, validation, testing, persistence, model integration and deployment.

The API will classify and store predictions. It will not answer messages or resolve support requests.

## MVP

- Classify English banking support messages
- Store predictions and confidence scores
- Retrieve previous predictions
- Record feedback and corrected intents
- Expose supported intents and model metadata

## Stack

- Python 3.12
- FastAPI
- Hugging Face Transformers
- PostgreSQL

## Development

Install the project dependencies:

```bash
uv sync
```

If you use direnv, load the local environment:

```bash
direnv allow
```

Install and run the project checks:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

The project is in its initial setup phase.
