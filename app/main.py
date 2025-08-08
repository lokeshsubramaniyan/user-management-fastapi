"""
Main application module for the User Management API.

This module initializes the FastAPI application, configures middleware,
and includes all the API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
from app.api import users
from app.api import credential

load_dotenv()

# Create FastAPI application instance
app = FastAPI(
    title="User Management API",
    description="A FastAPI application for user management with JWT authentication",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix='/api/users')
app.include_router(credential.router, prefix='/api/credential')
    
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
})

