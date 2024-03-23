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

Once you are set up you can browse to [http://localhost:8000/docs](http://localhost:8000/docs) to see the documentation.


## Test

```sh
curl -X 'POST' \
          'http://127.0.0.1:8000/embeddings/' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{"text": "Your text here and its great"}'
```

## Benchmarks

Model: `distilbert-base-uncased`

```sh
Time (mean ± σ):       6.4 ms ±   0.5 ms    [User: 2.4 ms, System: 3.6 ms]
Range (min … max):     5.6 ms …   9.5 ms    374 runs
```

Model: `avsolatorio/GIST-large-Embedding-v0`

```sh
Time (mean ± σ):       6.5 ms ±   0.4 ms    [User: 2.4 ms, System: 3.6 ms]
Range (min … max):     5.8 ms …   8.7 ms    375 runs
```

Models can be compared [here](https://huggingface.co/spaces/mteb/leaderboard)
