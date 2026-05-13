"""
Custom exceptions for AI COS engine.
"""


class EngineException(Exception):
    """
    Base engine exception.
    """

    pass


class PipelineException(EngineException):
    """
    Pipeline execution error.
    """

    pass


class GenerationException(EngineException):
    """
    AI generation error.
    """

    pass


class VerificationException(EngineException):
    """
    Verification failed.
    """

    pass


class PublishingException(EngineException):
    """
    Publishing failed.
    """

    pass