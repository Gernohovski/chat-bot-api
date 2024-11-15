from fastapi import FastAPI
from fastapi import HTTPException
import ollama
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/")
def read_root(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Envie uma mensagem válida.")
    try:
        response = ollama.chat(model="llama3.2", messages= [{
            "role": "user",
            "content": request.text
        }])
        
        llama_response = response.get('message', {}).get('content', '')
        return {"reply": llama_response}   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
