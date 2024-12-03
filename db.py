# database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://ramirezgrismaldo:IKNhwd6Nqpn7r4jU@cluster0.fpw8g.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.get_database("cluster0")
product_collection = database.get_collection("products_collection")

# Helpers


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "code": product["code"],
        "label": product["label"],
        "image": product["image"],
        "quantity": product["quantity"],
        "category": product["category"],
        "seller": product["seller"],
        "sender": product["sender"],
    }

# Verificar la conexión a la base de datos


async def check_connection():
    try:
        # Intentar listar las colecciones para verificar la conexión
        await database.list_collection_names()
        return "Conexión exitosa a la base de datos"
    except Exception as e:
        return f"Error al conectar a la base de datos: {e}"
