from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

raw_teas = [{
      "id": 1,
      "name": "Ginger",
      "origin": "Home Made"
    },
    {
      "id": 2,
      "name": "Lemon",
      "origin": "Home Made"
    },
    {
      "id": 3,
      "name": "Honey Lemon",
      "origin": "Assam"
    },
    {
      "id": 4,
      "name": "Honey Ginger Lemon",
      "origin": "Ladakh"
    },
    {
      "id": 5,
      "name": "Masala Chain",
      "origin": "Assam"
    }]

# Define a Pydantic model for Tea
class Tea(BaseModel):
    id: int
    name: str
    origin: str

# Define a Pydantic response model for Tea
class TeaResponse(BaseModel):
    status_code: int
    data: List[Tea]
    message: Optional[str] = None

teas = [Tea(**tea) for tea in raw_teas]

# CRUD operations for Tea

# Root endpoint
@app.get("/")
def root():
    return ({"message": "Welcome to the Tea API!"})

# Get API Version
@app.get("/version")
def get_api_version():
    return ({"version": "2.0"})

# Get all teas
@app.get("/teas", response_model = TeaResponse)
def get_all_teas():
    return TeaResponse(status_code = 200, data = teas)

# Get a specific tea by ID
@app.get("/teas/{tea_id}", response_model = TeaResponse)
def get_tea(tea_id: int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            return TeaResponse(status_code = 200, data = [tea]);
    
    return TeaResponse(status_code = 404, data = [], message = "Tea not found")

# Create a new tea
@app.post("/teas", response_model = TeaResponse)
def create_tea(tea: Tea):
    try:
        if [existing_tea for existing_tea in teas if existing_tea.name == tea.name and existing_tea.origin == tea.origin]:
            return TeaResponse(status_code = 400, data = [], message = "Tea already exists")
        else:
            tea.id = len(teas) + 1
            teas.append(tea)
            return TeaResponse(status_code = 201, data = [tea], message = "Tea created successfully")
    except Exception as e:
        logging.error(f"Error creating tea: {e}")
        return TeaResponse(status_code = 500, data = [], message = "An error occurred while processing your request. Please try again later.")


# Update an existing tea
@app.put("/teas/{tea_id}", response_model = TeaResponse)
def update_tea(tea_id: int, updated_tea: Tea):
    try:
        existing_tea = next((tea for tea in teas if tea.id == tea_id), None)
        if existing_tea:
            existing_tea.name = updated_tea.name
            existing_tea.origin = updated_tea.origin
            return TeaResponse(status_code = 200, data = [existing_tea], message = "Tea updated successfully")
            
        # If the tea with the given ID does not exist, return a 404 response
        return TeaResponse(status_code = 404, data = [], message = "Tea not found")
        
    except Exception as e:
        logging.error(f"Error updating tea: {e}")
        return TeaResponse(status_code = 500, data = [], message = "An error occurred while processing your request. Please try again later.")


# Delete a tea
@app.delete("/teas/{tea_id}", response_model = TeaResponse)
def delete_tea(tea_id: int):
    try:
        existing_tea = next((tea for tea in teas if tea.id == tea_id), None)
        if existing_tea:
            teas.remove(existing_tea)
            return TeaResponse(status_code = 200, data = [], message = "Tea deleted successfully")
        
        # If the tea with the given ID does not exist, return a 404 response
        return TeaResponse(status_code = 404, data = [], message = "Tea not found")
    except Exception as e:
        logging.error(f"Error deleting tea: {e}")
        return TeaResponse(status_code = 500, data = [], message = "An error occurred while processing your request. Please try again later.")