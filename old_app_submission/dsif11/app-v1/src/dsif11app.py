

from fastapi import FastAPI

app = FastAPI() #creates an instance of the FastAPI application

@app.get("/")
def read_root(): # Decorator, defines a route for the root URL (/). Returns a JSON response with welcome message
    return {"message": "Welcome to the best ELVTR course ever"}

