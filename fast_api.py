import uvicorn
from fastapi import FastAPI
from flight_agent import FlightAgent

app = FastAPI()


@app.post("/ask")
async def ask_ayka(query: str):
    """
    Endpoint to interact with the AI flight assistant (AYKA).
    Send a message like "I want to book a flight" and get a response.
    """
    try:
        # Format the message in the structure agent expects
        agent = FlightAgent()
        response = agent.get_response(query)
        return {"response": str(response)}
    except Exception as e:
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app,  port=8000)