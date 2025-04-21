from pymilvus import connections, utility

# Conectar a Milvus
connections.connect(alias="default", host="127.0.0.1", port="19530")

# Verificar conexión
print("✅ Conexión a Milvus exitosa")

# Listar colecciones (debería estar vacío si no has creado nada aún)
collections = utility.list_collections()
print("Colecciones existentes:", collections)
