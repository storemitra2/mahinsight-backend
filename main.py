import logging
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config import CORS_ORIGINS, LOG_LEVEL
from database.database import engine, Base
from routes import sentiment, sales, heatmap, chatbot, auth
from services.data_service import generate_social_media_samples, generate_sales_data

logging.basicConfig(level=LOG_LEVEL.upper())
logger = logging.getLogger('mahinsight')

app = FastAPI(title='MAHInsight API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS!=['*'] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sentiment.router)
app.include_router(sales.router)
app.include_router(heatmap.router)
app.include_router(chatbot.router)
app.include_router(auth.router)


@app.on_event('startup')
def startup():
    # create tables
    Base.metadata.create_all(bind=engine)
    logger.info('Database tables ensured')

@app.websocket('/ws/live')
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Echo: {data}")
    except Exception:
        await ws.close()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
