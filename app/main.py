from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Config
from app.auth.middleware import SessionMiddleware
from app.auth.routes import router as auth_router

app = FastAPI()
app.add_middleware(SessionMiddleware)
app.include_router(auth_router, prefix="/auth", tags=["auth"])



@app.on_event("startup")
async def connect_to_db():
    """
    Connect to the MongoDB database when the application starts.
    """
    mongodb_client = AsyncIOMotorClient(Config.MONGO_URI)
    app.state.mongodb_client = mongodb_client
    app.state.database = mongodb_client[Config.MONGO_DB_NAME]
    print("✅ Connected to MongoDB")


app.on_event("shutdown")
async def disconnect_from_db():
    """
    Disconnect from the MongoDB database when the application shuts down.
    """
    app.state.mongodb_client.close()
    print("❌ Disconnected from MongoDB")