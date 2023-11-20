""" This module contains the FastAPI application. It's responsible for 
    creating the FastAPI application and including the routers."""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import routers
#from app.routes.chat_routes import router as chat_routes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routes.chat_routes import router as chat_routes # noqa: E402


DESCRIPTION = """
  @TODO - Add a description of the application here.
"""



app = FastAPI(
    title="PR Prophet",
    description=DESCRIPTION,
    version="1.0",
    summary='Backend for the PR Prophet implementation\
    of the "BeSpokeTek" project.',
    contact={
        "name": "Dave Thomas aka the ChickenMon",
        "url": "https://enoughwebapp.com",
        "email": "dave_thomas@enoughwebapp.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Allow CORS for your front end
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
routers = [chat_routes]
for router in routers:
    app.include_router(router)
