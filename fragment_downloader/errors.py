

class InvalidUrlException(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FragmentDownloadException(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
