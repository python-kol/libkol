from functools import wraps

from ..Error import NotLoggedInError


def logged_in(func):
    @wraps(func)
    def _decorator(self, *args, **kwargs):
        session = self.session if hasattr(self, "session") else self
        if session.is_connected is False:
            raise NotLoggedInError
        return func(self, *args, **kwargs)

    return _decorator
