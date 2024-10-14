from typing import Generic, TypeVar

T = TypeVar('T')
TChatCompletion = TypeVar('TChatCompletion')


class _GeneralError(Exception, Generic[TChatCompletion]):
    def __init__(self, message: str, completion: TChatCompletion, *args):
        self.completion = completion
        super().__init__(message, *args)

class ExtractorValidationError(_GeneralError[T]):
    pass

class ExtractorError(_GeneralError[T]): 
    pass