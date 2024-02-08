package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type SentenceRequest struct {
	Sentence string `json:"sentence"`
}

type BERTEmbedding struct {
	Values []float32 `json:"values"`
}

func main() {
	router := gin.Default()

	router.POST("/bert-embedding", func(c *gin.Context) {
		var request SentenceRequest
		if err := c.ShouldBindJSON(&request); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// Call your BERT embedding function here
		embedding, err := createBERTEmbedding(request.Sentence)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, gin.H{"embedding": embedding})
	})

	router.Run(":8080")
}

func createBERTEmbedding(sentence string) (BERTEmbedding, error) {
	// Implement BERT embeddings retrieval using an appropriate package
	// The embedding should be of type BERTEmbedding

	// Placeholder code for demonstration purposes
	embedding := BERTEmbedding{
		Values: []float32{0.1, 0.2, 0.3},
	}

	return embedding, nil
}