""" Run objects for the app """
import os
import sys
from pydantic import BaseModel, Field
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))


class CreateMessageRunRequest(BaseModel):
    """ Create Run Request Model """
    thread_id: str = Field(..., description="The thread id for the run to be added to.")
    assistant_id: str = Field(..., description="The assistant id for the run to be added to.")
    message_content: str = Field(..., description="The content of the message to be added to the thread.")

class CreateThreadRunRequest(BaseModel):
    """ Create Thread Run Request Model """
    assistant_id: str = Field(..., description="The assistant id for the run to be added to.")
    message_content: str = Field(..., description="The content of the message to be added to the thread.")   

class ListStepsRequest(BaseModel):
    """ List Steps Request Model """
    thread_id: str = Field(..., description="The thread id for the run to be added to.")
    run_id: str = Field(..., description="The run id for the run to be added to.")
    limit: int = Field(20, description="The number of steps to return.")
    order: str = Field("desc", description="The order to return the steps in. Must be one of ['asc', 'desc']")
