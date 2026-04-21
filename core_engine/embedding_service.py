from sentence_transformers import SentenceTransformer
import torch

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Use GPU if available for faster embedding generation
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"DEBUG: Initializing EmbeddingService with model '{model_name}' on device: {self.device}")
        
        # Load the model once
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, text: str):
        """
        Generates a vector embedding for the given text.
        """
        return self.model.encode(text)
    
    def get_model(self):
        """
        Returns the underlying model for advanced use-cases (like similarity calculations).
        """
        return self.model

# Singleton instance for the entire application
embedding_service = EmbeddingService()
