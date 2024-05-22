"""API Module for controlling a Capra Hircus"""
import json
import logging
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, Float, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
from capra_control import ControlCapra
from models.instruction_create import InstructionCreate
from models.instruction_response import InstructionResponse
from tables.instructions_table import Instruction


# pylint: disable=line-too-long
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

# Define SQLAlchemy models
Base = declarative_base()

BROKER_ADRRESS = "10.46.28.1"
BROKER_PORT = 1883
controller = ControlCapra(BROKER_ADRRESS, BROKER_PORT)


# Configure MySQL database
SQLALCHEMY_DATABASE_URL = "sqlite:///./capra_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata = MetaData()

# Create tables
instructions_table = Table(
    'instructions',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('angle', Float, nullable=False),
    Column('speed', Integer, nullable=False),
    Column('distance', Float, nullable=False)

)

# Map tables
mapper(Instruction, instructions_table)

metadata.create_all(engine)

# Create DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI()

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

    # Store instruction
    db = SessionLocal()
    db_instruction = Instruction(**instruction.model_dump())
    print(db_instruction.speed)
    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)

    # Instruct robot to drive
    controller.mq_set_mode(1)
    controller.remote_control(db_instruction.distance,
                              db_instruction.speed, db_instruction.angle)
    return db_instruction


@app.post("/stop/")
def stop_robot():
    """Send instruction to the robot to stop driving"""

    # mode 5 = STOPPED
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

        # Read file contents
        contents = await file.read()

        data = json.loads(contents)

        return {"message": "JSON file uploaded and processed successfully"}
    except FileNotFoundError as e:
        return JSONResponse(status_code=500, content={"message": f"Error processing JSON file: {str(e)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
