from pydantic import BaseModel, IPvAnyInterface, ValidationError


class IPAddressModel(BaseModel):
    address: IPvAnyInterface
