from typing import Optional, Any, Union

from pydantic import BaseModel


class ServiceResponse(BaseModel):
    code: int
    data: Optional[dict] = None

    def __init__(self,
                 code: int,
                 data: Union[None, dict] = None,
                 **kw: Any):
        super().__init__(**kw)
        if data is None:
            self.data = {}
        self.code = code

    class Config:
        from_attributes = True
