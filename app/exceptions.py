# -*- coding: utf-8 -*-


class ExceptionBase(Exception):
    code = 400
    message = 'Exception'

    def __init__(self, message=None, code=None):
        if message:
            self.message = message

        if code:
            self.code = code

    def to_api_response(self):
        return {
            'detail': self.message,
            'code': self.code
        }


class BadRequestException(ExceptionBase):
    message = 'Bad request'
    code = 400


class UnauthenticatedException(ExceptionBase):
    message = 'User was not found or could not get user credentials'
    code = 401


class InvalidRequestParameter(ExceptionBase):
    message = 'Invalid request parameter'
    code = 400

    def __init__(self, *params):
        if params:
            self.message = self.message + "(s) named: " + ",".join(params)

        super().__init__(self.message, self.code)


class PermissionDeniedException(ExceptionBase):
    message = 'Permission denied'
    code = 403
