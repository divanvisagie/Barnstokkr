# Barnstokkr
Service for creating embeddings from strings.

![logo](docs/logo.png)
# Test

```sh
curl -X POST -H "Content-Type: application/json" -d '{"content":"Your Test String"}' http://localhost:8080/embeddings
{"embedding":[0.1,0.2,0.3]}%
```
