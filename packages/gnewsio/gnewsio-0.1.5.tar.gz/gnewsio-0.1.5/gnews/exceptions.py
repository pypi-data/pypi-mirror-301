class APIClientError(Exception):
    pass


class UnauthorizedError(APIClientError):
    pass


class ForbiddenError(APIClientError):
    pass


class BadRequestError(APIClientError):
    pass
