class ResumeProcessingError(Exception):
    pass


class InvalidFileTypeError(ResumeProcessingError):
    pass


class InvalidPdfError(ResumeProcessingError):
    pass


class UnreadableContentError(ResumeProcessingError):
    pass


class ResumeParsingError(ResumeProcessingError):
    pass


class ResumeSchemaError(ResumeProcessingError):
    pass


class LlmProcessingError(ResumeProcessingError):
    pass


class StorageFailureError(ResumeProcessingError):
    pass
