from pydantic import BaseModel, Field, IPvAnyAddress


class RouterHost(BaseModel):
    alias: str
    address: IPvAnyAddress
    description: str | None = None


class RouterCommand(BaseModel):
    host: str
    command: str = Field(..., description="Raw RouterOS command to execute")
    dry_run: bool = Field(default=True)
