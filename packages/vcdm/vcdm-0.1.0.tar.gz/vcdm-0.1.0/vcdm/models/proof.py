from typing import Dict, Any, List, Union
from pydantic import BaseModel, Field


class BaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class DataIntegrityProof(BaseModel):
    id: str = Field(None)
    type: Union[str, List[str]] = Field()
    cryptosuite: str = Field()
    verificationMethod: str = Field()
    created: str = Field(None)
    expires: str = Field(None)
    proofPurpose: str = Field()
    proofValue: str = Field()
