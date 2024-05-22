"""Instruction Response model"""
from models.instruction_create import InstructionCreate


class InstructionResponse(InstructionCreate):
    """Instruction Response code"""
    id: int
