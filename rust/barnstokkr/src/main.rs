use rust_bert::{RustBertError, pipelines::sentence_embeddings::{SentenceEmbeddingsBuilder, SentenceEmbeddingsModelType}};

pub fn create_bert_embeddings(texts: &[String]) -> Result<Vec<Vec<f32>>, RustBertError> {

    let model = SentenceEmbeddingsBuilder::remote(
        SentenceEmbeddingsModelType::AllMiniLmL12V2
    )
    .create_model()?;

    let embeddings = model.encode(texts)?;

    let ebd = embeddings
        .into_iter()
        .collect();

    Ok(ebd)
}



fn main() {
    // create embedding from text
    let text = "This is a test";
    let embeddings = create_bert_embeddings(&[text.to_string()]).unwrap();

    println!("{:?}", embeddings);
}
