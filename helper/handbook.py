from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle



def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Example usage
pdf_path = "./Employee-Handbook.pdf"
pdf_text = extract_text_from_pdf(pdf_path)


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


chunks = chunk_text(pdf_text)



# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(chunks, show_progress_bar=True)


# Create a FAISS index
dimension = embeddings.shape[1]  # Embedding dimension
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(np.array(embeddings))

# Save the index
faiss.write_index(index, "handover_index.faiss")

def search_faiss(query, model, index, chunks, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = [{"chunk": chunks[i], "distance": distances[0][j]} 
               for j, i in enumerate(indices[0])]
    return results

# Example usage
query = "What are the main responsibilities in the handover?"
results = search_faiss(query, model, index, chunks)
for result in results:
    print(f"Chunk: {result['chunk']}\nDistance: {result['distance']}\n")



data = {"index": index, "chunks": chunks}
with open("faiss_data.pkl", "wb") as f:
    pickle.dump(data, f)
