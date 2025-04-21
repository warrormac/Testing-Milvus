from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import numpy as np

# -------------------------
# STEP 1: Connect to Milvus
# -------------------------
connections.connect(alias="default", host="127.0.0.1", port="19530")
print("✅ Connected to Milvus")

# -------------------------
# STEP 2: Define Collection
# -------------------------
collection_name = "FastS3Data"

# Drop if it already exists
if utility.has_collection(collection_name):
    Collection(collection_name).drop()
    print("🔁 Dropped existing collection.")

# Define schema (example: using 1536-dim embedding vectors)
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536)
]
schema = CollectionSchema(fields, description="Test multimodal embedding collection")

# Create collection
collection = Collection(name=collection_name, schema=schema)
print(f"📁 Collection '{collection_name}' created")

# -------------------------
# STEP 3: Insert Data
# -------------------------
vectors = np.random.rand(3, 1536).astype(np.float32)  # Simulating 3 embedded files
ids = [1, 2, 3]
data = [ids, vectors]

collection.insert(data)
print("✅ Inserted 3 vectors")

# STEP 3.5: Create Index (Required before load + search)
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128}
}
collection.create_index(field_name="embedding", index_params=index_params)
print("🧠 Index created on 'embedding'")


# -------------------------
# STEP 4: Search (Find)
# -------------------------
collection.load()
query_vector = [vectors[0]]  # Search using first vector
results = collection.search(query_vector, "embedding", param={"metric_type": "L2", "params": {"nprobe": 10}}, limit=3)

print("🔍 Search results (top 3):")
for hit in results[0]:
    print(f"  - ID: {hit.id}, Distance: {hit.distance:.4f}")

# -------------------------
# STEP 5: Simulate Update (delete + insert new vector)
# -------------------------
collection.delete(f"id in [2]")
print("🗑️ Deleted vector with ID 2")

new_vector = np.random.rand(1, 1536).astype(np.float32)
collection.insert([[2], new_vector])
print("🔄 Re-inserted ID 2 with new vector (update simulation)")

# -------------------------
# STEP 6: Delete All
# -------------------------
collection.delete("id in [1, 2, 3]")
print("❌ Deleted all test vectors")

# -------------------------
# STEP 7: Drop Collection
# -------------------------
collection.drop()
print("🧹 Cleaned up: Collection dropped")

