"""Instruction Pydantic Model"""
from pydantic import BaseModel, field_validator


class InstructionCreate(BaseModel):
    """Instruction model"""
    angle: float = 0
    speed: int
    distance: float

    @field_validator('angle')
    @classmethod
    def check_angle(cls, v):
        """Validate angle field"""
        if v < -0.8 or v > 1.5:
            raise ValueError("Angle must be between -0.8 and 1.5 radians")
        return v

    @field_validator('speed')
    @classmethod
    def check_speed(cls, v):
        """Validate speed field"""
        if v < -2 or v > 2:
            raise ValueError("Speed must be between -2 and 2 m/s")
        return v

    @field_validator('distance')
    @classmethod
    def check_distance(cls, v):
        """Validate distance field"""
        if v < 0.1 or v > 100:
            raise ValueError("Distance must be between 0.1 and 100 meter")
        return v
