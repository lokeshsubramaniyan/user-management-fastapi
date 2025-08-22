"""
Main application module for the User Management API.

This module initializes the FastAPI application, configures middleware,
and includes all the API routers.
"""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import credential, users
from app.core.middleware import RateLimitMiddleware, TransactionIdMiddleware
from app.core.util import lifespan

load_dotenv()

app = FastAPI(
    title="User Management API",
    description="A FastAPI application for user management with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TransactionIdMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(users.router, prefix="/api/users")
app.include_router(credential.router, prefix="/api/credential")
