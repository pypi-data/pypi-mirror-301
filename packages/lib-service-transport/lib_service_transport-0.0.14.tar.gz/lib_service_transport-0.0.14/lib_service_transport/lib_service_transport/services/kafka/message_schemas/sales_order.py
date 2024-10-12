from uuid import UUID

from pydantic import BaseModel


# TODO: удалить!
class OrderCreationMessage(BaseModel):
    order_id: UUID


class SalesOrderIncomingMessage(BaseModel):
    sales_order_nrec: str
    client_id: str


class SalesOrderOutgoingMessage(BaseModel):
    number: str
    first_name: str
    last_name: str
    address: str
    nrec: str
