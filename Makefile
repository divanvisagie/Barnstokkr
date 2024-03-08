
main:
	docker-compose down
	docker-compose up --build

clean:
	docker-compose down

run:
	docker-compose up	

test:
	curl -X 'POST' \
	  'http://127.0.0.1:8000/embeddings/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{"text": "Your text here and its great"}'
