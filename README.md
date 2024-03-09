# Barnstokkr
Service for creating embeddings from strings.

![logo](docs/logo.png)


## Setup

```sh
python -m venv env
pip install -r requirements.txt

# Run the server
make local
```

## Documentation

Once you are set up you can browse to [http://localhost:8000/docs](http://localhost:8080/docs) to see the documentation.


## Test

```sh
curl -X 'POST' \
          'http://127.0.0.1:8000/embeddings/' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{"text": "Your text here and its great"}'
```
