from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Example texts
reference_answer = "Mount Kilimanjaro is located in Tanzania."
generated_answer = "Kilimanjaro is a mountain in Tanzania."

# Generate embeddings for both the reference and generated text
reference_embedding = model.encode(reference_answer)
generated_embedding = model.encode(generated_answer)

# Calculate cosine similarity between embeddings
similarity_score = cosine_similarity([reference_embedding], [generated_embedding])

# Define a threshold for similarity (e.g., 0.85 for strong conceptual similarity)
threshold = 0.85

if similarity_score >= threshold:
    print("Core idea matches! \n")
    print(similarity_score)
else:
    print("Core idea does not match.")
