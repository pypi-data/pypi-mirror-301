import grpc
from concurrent import futures
from abc import ABC, abstractmethod
from logging import getLogger
from .__internal__.AuthTokenValidation_pb2_grpc import (
    AuthTokenValidatorServicer,
    add_AuthTokenValidatorServicer_to_server,
)
from .__internal__.AuthTokenValidation_pb2 import TokenStatus, Token

logger = getLogger()


class ServerABC(AuthTokenValidatorServicer, ABC):
    """Abstract base class for the gRPC server. Upon defining a concrete class, implement ValidateToken with the validation logic."""

    def __init__(self, port: int):
        super().__init__()
        self.port = port

    @abstractmethod
    def ValidateToken(self, request: Token, context) -> TokenStatus:
        """
        Validates the provided token using the authentication service's functions.

        Args:
                request (Token): The token to be validated.
                context: The context in which the token is being validated.
                See https://grpc.io/docs/languages/python/basics/ for more information.

        Returns:
                TokenStatus: is_valid = True if the token is valid, False otherwise.
        """
        pass

    def serve(self) -> None:
        """Launches the gRPC server and listens for incoming requests."""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_AuthTokenValidatorServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()
        logger.info("gRPC server running on port %s", self.port)
        server.wait_for_termination()
        logger.info("Turning off gRPC server...")
