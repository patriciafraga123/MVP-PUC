# Define os schemas de resposta para mensagens de erro da API.

from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    message: str