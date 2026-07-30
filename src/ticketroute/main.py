from fastapi import FastAPI

from ticketroute.api.routes.health import router as health_router

app = FastAPI(
    title="TicketRoute API",
    description="Intent classification API for banking support messages",
    version="0.1.0",
)

app.include_router(health_router)
