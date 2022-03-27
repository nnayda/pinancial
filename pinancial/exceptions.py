"""Classes for dealing with errors."""


class Error(Exception):
    """Base class for errors."""

    status: int = 500
    message: str = ""
    details: str = ""

    def __init__(self, details: str = "") -> None:
        """Constructor."""
        super().__init__()
        self.details = details

    def to_dict(self) -> dict:
        """Return the error as a dictionary."""
        return {
            "error": {
                "message": self.message,
                "details": self.details,
                "status": self.status,
            }
        }


class Error400(Error):
    """Bad Request
    The server could not understand the request due to invalid syntax.
    """

    status = 400
    message = "Bad Request"


class Error401(Error):
    """Unauthorized Request
    Although the HTTP standard specifies "unauthorized", semantically
    this response means "unauthenticated". That is, the client must
    authenticate itself to get the requested response.
    """

    status = 401
    message = "Unauthorized Request"


class Error403(Error):
    """Forbidden
    The client does not have access rights to the content; that is, it
    is unauthorized, so the server is refusing to give the requested resource.
    Unlike 401 Unauthorized, the client's identity is known to the server.
    """

    status = 403
    message = "Forbidden"


class Error404(Error):
    """Not Found
    The server can not find the requested resource. In the browser, this means
    the URL is not recognized. In an API, this can also mean that the endpoint
    is valid but the resource itself does not exist. Servers may also send this
    response instead of 403 Forbidden to hide the existence of a resource from
    an unauthorized client. This response code is probably the most well known
    due to its frequent occurrence on the web.
    """

    status = 404
    message = "Not Found"


class Error415(Error):
    """Unsupported Media Type
    The media format of the requested data is not supported by the server, so
    the server is rejecting the request.
    """

    status = 415
    message = "Unsupported Media Type"


class Error423(Error):
    """Locked
    The resource that is being accessed is locked.
    """

    status = 423
    message = "Locked"


class Error500(Error):
    """Internal Server Error
    The server has encountered a situation it does not know how to handle.
    """

    status = 500
    message = "Internal Server Error"


class Error501(Error):
    """Not Implemented
    The request method is not supported by the server and cannot be handled.
    The only methods that servers are required to support (and therefore that
    must not return this code) are GET and HEAD.
    """

    status = 501
    message = "Not Implemented"
