use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct BERTEmbedding {
    pub values: Vec<f32>,
}

fn create_bert_embeddings(texts: &[String]) -> Result<Vec<BERTEmbedding>, RustBertError> {
    let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL12V2)
        .create_model()?;

    let embeddings = model.encode(texts)?;

    let ebd = embeddings
        .into_iter()
        .map(|e| BERTEmbedding { values: e })
        .collect();

    Ok(ebd)
}

#[get("/ping")]
async fn ping() -> impl Responder {
    HttpResponse::Ok().body("pong")
}

// Define a struct for the request body
#[derive(Deserialize)]
struct EmbeddingRequest {
    content: String,
}

// Define a struct for the response body
#[derive(Serialize)]
struct EmbeddingResponse {
    embedding: Vec<f32>,
}

// Takes in a string and returns a float array
#[post("/embeddings")]
async fn embeddings(req_body: web::Json<EmbeddingRequest>) -> impl Responder {
    // Here you would convert 'content' into an embedding
    // For this example, we'll return a mock embedding
    let text_to_use = req_body.content.clone();
    let embeddings = create_bert_embeddings(&[text_to_use]).unwrap();
    
    //get first embedding from list
    let mock_embedding = embeddings[0].values.clone();

    HttpResponse::Ok().json(EmbeddingResponse {
        embedding: mock_embedding,
    })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(ping)
            .service(embeddings)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
