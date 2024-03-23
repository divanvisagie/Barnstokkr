curl -X 'POST' \
	  'http://127.0.0.1:11434/api/embeddings' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{"model": "all-minilm", "prompt": "Your text here and its great"}'

