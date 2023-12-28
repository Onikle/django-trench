from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from trench.exceptions import MFAValidationError


class DispatchResponse(Response):
    _FIELD_DETAILS = "details"


class SuccessfulDispatchResponse(DispatchResponse):
    def __init__(self, details: str, status: str = HTTP_200_OK, *args, **kwargs) -> None:
        super().__init__(data={self._FIELD_DETAILS: details}, status=status, *args, **kwargs)


class FailedDispatchResponse(DispatchResponse):
    def __init__(self, details: str, status: str = HTTP_422_UNPROCESSABLE_ENTITY, *args, **kwargs) -> None:
        super().__init__(data={self._FIELD_DETAILS: details}, status=status, *args, **kwargs)


class ErrorResponse(Response):
    def __init__(self, error: MFAValidationError, status: str = HTTP_400_BAD_REQUEST, *args, **kwargs) -> None:
        if isinstance(error.detail, list):
            detail = error.detail[0]
        else:
            detail = error.detail
        super().__init__(data={"code": getattr(detail, "code", "none"), "message": str(detail)}, status=status, *args, **kwargs)
