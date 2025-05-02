from pydantic import BaseModel, Field
from typing import Annotated

class Currency(BaseModel):
    cur_code: Annotated[str, Field(max_length=3, min_length=3,)]