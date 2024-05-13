"""API Module for controlling a Capra Hircus"""
import os
import json
import logging
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from capra_control import ControlCapra


# pylint: disable=line-too-long
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

# Define SQLAlchemy models
Base = declarative_base()

load_dotenv()
BROKER_ADRRESS = "10.46.28.1"
BROKER_PORT = 1883
controller = ControlCapra(BROKER_ADRRESS, BROKER_PORT)


class Instruction(Base):
    """Creates Instruction table in the database"""
    __tablename__ = "instructions"
    id = Column(Integer, primary_key=True, index=True)
    angle = Column(Float, nullable=False)
    speed = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)


# Configure MySQL database
SQLALCHEMY_DATABASE_URL = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic models


class InstructionCreate(BaseModel):
    """Instruction model"""
    angle: float = 0
    speed: int
    distance: float


class InstructionResponse(InstructionCreate):
    """Instruction Response code"""
    id: int


# API endpoints


@app.post("/drive/", response_model=InstructionResponse)
async def create_instruction(instruction: InstructionCreate):
    """Creates a driving instruction and sends it to the robot"""
    db = SessionLocal()
    db_instruction = Instruction(**instruction.model_dump())
    print(db_instruction.speed)
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)
    controller.mq_set_mode(1)
    controller.remote_control(db_instruction.distance,
                              db_instruction.speed, db_instruction.angle)
    return db_instruction


@app.post("/stop/")
def stop_robot():
    """Send instruction to the robot to stop driving"""
    controller.mq_set_mode(5)
    return {"message": "Robot stopped"}


@app.get("/connect_to_robot")
def connect_to_robot():
    """Establishes a connection to the Capra Hircus"""
    try:
        controller.connect_to_robot()
        return {"message": "Successfully connected to the robot"}
    except Exception as e:
        # Log de foutmelding
        print(f"Error connecting to the robot: {e}")

        raise HTTPException(
            status_code=500, detail="Failed to connect to Capra Hircus") from e


@app.get("/instructions/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int):
    """Retrieves an instruction from the Database"""
    db = SessionLocal()
    instruction = db.query(Instruction).filter(
        Instruction.id == instruction_id).first()
    if instruction is None:
        raise HTTPException(status_code=404, detail="Instruction not found")
    return instruction


@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...)):
    """Endpoint to upload a JSON file"""
    try:
        # Validate if file-format is correct.
        if not file.filename.endswith(".json"):
            return JSONResponse(status_code=400, content={"message": "Uploaded file must be a JSON file"})

        # Lees de inhoud van het bestand
        contents = await file.read()

        data = json.loads(contents)

        return {"message": "JSON file uploaded and processed successfully"}
    except FileNotFoundError as e:
        return JSONResponse(status_code=500, content={"message": f"Error processing JSON file: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
