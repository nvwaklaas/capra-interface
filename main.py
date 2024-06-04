"""API Module for controlling a Capra Hircus"""
import json
import logging
from typing import List
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from capra_control import ControlCapra
from models.instruction_create import InstructionCreate
from models.instruction_response import InstructionResponse


# pylint: disable=line-too-long

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define SQLAlchemy models
Base = declarative_base()

BROKER_ADRRESS = "10.46.28.1"
BROKER_PORT = 1883
controller = ControlCapra(BROKER_ADRRESS, BROKER_PORT)

API_META_DESCRIPTION = """
This API is used for interfacing with a Capra Hircus robot using Python and MQTT.
You can use this API to send driving instructions to control the robot.
"""

# Define instruction table


class Instruction(Base):
    """Creates Instruction table in the database"""
    __tablename__ = "instructions"
    id = Column(Integer, primary_key=True, index=True)
    angle = Column(Float, nullable=False)
    speed = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)


# Configure MySQL database
SQLALCHEMY_DATABASE_URL = "sqlite:///./capra_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="Capra API",
    description=API_META_DESCRIPTION,
    summary="API for interfacing with a Capra Hircus robot.",
    version="0.1.0"
)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoints


@app.post("/drive/", response_model=InstructionResponse)
async def create_instruction(instruction: InstructionCreate):
    """Creates a driving instruction and sends it to the robot"""
    logger.info("Received instruction: %s", instruction)
    db = SessionLocal()
    db_instruction = Instruction(**instruction.model_dump())
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)

    # Instruct robot to drive
    controller.mq_set_mode(1)

    try:
        controller.remote_control(db_instruction.distance,
                                  db_instruction.speed, db_instruction.angle)
        logger.info("Instruction sent to robot: %s", db_instruction)
    except ValueError as exc:
        logger.error("Error sending instruction to robot: %s", exc)
        raise HTTPException(
            status_code=422, detail="Invalid parameters for driving instruction") from exc

    return db_instruction


@app.post("/stop/")
def stop_robot():
    """Send instruction to the robot to stop driving"""
    logger.info("Stopping robot")
    controller.mq_set_mode(5)
    return {"message": "Robot stopped"}


@app.get("/connect_to_robot")
def connect_to_robot():
    """Establishes a connection to the Capra Hircus"""
    try:
        logger.info("Connecting to the robot")
        controller.connect_to_robot()
        logger.info("Successfully connected to the robot")
        return {"message": "Successfully connected to the robot"}
    except Exception as e:
        logger.error("Error connecting to the robot: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to connect to Capra Hircus, are you connected to its wifi?") from e


@app.get("/instructions/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int):
    """Retrieves an instruction from the Database"""
    logger.info("Fetching instruction with ID: %d", instruction_id)
    db = SessionLocal()
    instruction = db.query(Instruction).filter(
        Instruction.id == instruction_id).first()
    if instruction is None:
        logger.warning("Instruction not found: %d", instruction_id)
        raise HTTPException(status_code=404, detail="Instruction not found")
    logger.info("Instruction retrieved: %s", instruction)
    return instruction


@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...)):
    """Endpoint to upload a JSON file"""
    try:
        logger.info("Uploading JSON file: %s", file.filename)
        if not file.filename.endswith(".json"):
            logger.warning(
                "Uploaded file is not a JSON file: %s", file.filename)
            return JSONResponse(status_code=400, content={"message": "Uploaded file must be a JSON file"})

        contents = await file.read()
        data = json.loads(contents)
        logger.info("JSON file uploaded and processed successfully")
        return {"message": "JSON file uploaded and processed successfully"}
    except FileNotFoundError as e:
        logger.error("Error processing JSON file: %s", e)
        return JSONResponse(status_code=500, content={"message": f"Error processing JSON file: {str(e)}"})


@app.get("/instructions", response_model=List[InstructionResponse])
def get_all_instructions():
    """Retrieves all instructions from the Database"""
    db = SessionLocal()
    instructions = db.query(Instruction).all()
    return instructions


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
