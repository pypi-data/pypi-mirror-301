# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = [
    "Completion",
    "Choice",
    "ChoiceLogProbs",
    "ChoiceLogProbsContent",
    "ChoiceLogProbsContentTopLogprob",
    "ChoiceLogProbsRefusal",
    "ChoiceLogProbsRefusalTopLogprob",
]


class ChoiceLogProbsContentTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None


class ChoiceLogProbsContent(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[ChoiceLogProbsContentTopLogprob]

    bytes: Optional[List[int]] = None


class ChoiceLogProbsRefusalTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None


class ChoiceLogProbsRefusal(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[ChoiceLogProbsRefusalTopLogprob]

    bytes: Optional[List[int]] = None


class ChoiceLogProbs(BaseModel):
    content: Optional[List[ChoiceLogProbsContent]] = None

    refusal: Optional[List[ChoiceLogProbsRefusal]] = None


class Choice(BaseModel):
    text: str
    """
    The generated text output from the model, which forms the main content of the
    response.
    """

    log_probs: Optional[ChoiceLogProbs] = None


class Completion(BaseModel):
    choices: List[Choice]
    """
    A list of choices generated by the model, each containing the text of the
    completion and associated metadata such as log probabilities.
    """

    model: Optional[str] = None
    """
    The identifier of the model that was used to generate the responses in the
    'choices' array.
    """
