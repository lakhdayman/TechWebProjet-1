from pydantic import BaseModel

class UserSchema(BaseModel):
    firstname: str
    name: str
    id: int
    email: str
    password: str
    role: str

class DishSchema(BaseModel):
    dishid: int
    dishname: str
    dishtype: str
    price: int

class OrderSchema(BaseModel):
    orderid: int
    clientid: int
    dishes: str
    orderprice: int
    complete: bool
    status: str

class TableSchema(BaseModel):
    tableid: int
    clientid: int
    available: bool
    day: str
    time: str

class FeedbackSchema(BaseModel):
    feedbackid: int
    clientemail: str
    feedback: str