"""Instruction Pydantic Model"""
from pydantic import BaseModel


class InstructionCreate(BaseModel):
    """Instruction model"""
    angle: float = 0
    speed: int
    distance: float
