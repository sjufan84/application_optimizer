""" This file is used to register the routes for the API.
Each route is registered to a router instance, and the router
instances are exported as a list for convenience. """
from fastapi import APIRouter
# Import the router files to register the routes
from app.routes.chat_routes import router as chat_routes

# Create instances of APIRouter for each router
router_chat = APIRouter()

# Register the routers to the corresponding instances
router_chat.include_router(chat_routes)

# Export the routers as a list for convenience
routers = [router_chat]
