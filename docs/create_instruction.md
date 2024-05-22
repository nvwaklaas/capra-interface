# Table of Contents

* [instruction\_create](#instruction_create)
  * [InstructionCreate](#instruction_create.InstructionCreate)
    * [check\_angle](#instruction_create.InstructionCreate.check_angle)
    * [check\_speed](#instruction_create.InstructionCreate.check_speed)
    * [check\_distance](#instruction_create.InstructionCreate.check_distance)

<a id="instruction_create"></a>

# instruction\_create

Instruction Pydantic Model

<a id="instruction_create.InstructionCreate"></a>

## InstructionCreate Objects

```python
class InstructionCreate(BaseModel)
```

Instruction model

<a id="instruction_create.InstructionCreate.check_angle"></a>

#### check\_angle

```python
@field_validator('angle')
@classmethod
def check_angle(cls, v)
```

Validate angle field

<a id="instruction_create.InstructionCreate.check_speed"></a>

#### check\_speed

```python
@field_validator('speed')
@classmethod
def check_speed(cls, v)
```

Validate speed field

<a id="instruction_create.InstructionCreate.check_distance"></a>

#### check\_distance

```python
@field_validator('distance')
@classmethod
def check_distance(cls, v)
```

Validate distance field

