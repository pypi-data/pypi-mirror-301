import grpc
from .__internal__.AuthTokenValidation_pb2_grpc import AuthTokenValidatorStub
from .__internal__.AuthTokenValidation_pb2 import Token, TokenStatus


class Client:
    """Client class for interacting with the gRPC authentication server.

    Attributes:
        hostname (str): The hostname of the gRPC server eg: localhost
        port (str): The port number of the gRPC server eg: 50051
    """

    def __init__(self, hostname: str, port: int):
        self.channel = grpc.insecure_channel(f"{hostname}:{port}")
        self.stub = AuthTokenValidatorStub(self.channel)

    def validate_auth_token(self, token: Token) -> TokenStatus:
        """
        Validates the provided authentication token by communicating with the gRPC server.
        Args:
            token (str): The authentication token to be validated.
        Returns:
            bool: True if the token is valid, False otherwise.
        """

        token_payload = token
        is_token_valid = self.stub.ValidateToken(token_payload)
        return is_token_valid


# if __name__ == "__main__":
#     token_string = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImppeFNaX1puRHdWVXNnMTA1TzZMUyJ9.eyJpc3MiOiJodHRwczovL2Vhcmx5LXJpc2VyMTguZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY2ZThmNjI2YmViMGQ1YjEzNDdjN2I0OCIsImF1ZCI6Imh0dHBzOi8vbG9jYWxob3N0IiwiaWF0IjoxNzI3NDk1NDc1LCJleHAiOjE3Mjc1ODE4NzUsImd0eSI6InBhc3N3b3JkIiwiYXpwIjoibzVFZDVGM1BEVFQ2MWtuNUpuTVhkZlRuZHp5andUa0sifQ.Co-X8-0PpV4-ZC3NN4npTqpGXUG0g2oFBhnS4FtU5oAy6o0ixyNs1iv4AdNDfBXkkef-8BebqiXmapstp9-fXKCAUIHX7kh_jCg9ySUysZ-7ORcKyk45OWRqY1rr-5TAhpvs4HH-tYixsxZn-DPyrVx3omNe7Q-tXk-AsCWcWg58myNWFTpFmfnYm9wfIhD3enTtZ5BMPOpf6rve-gxEzDDFlAk2SFD6VgZEK7Wndezf2GLO9eKijBxblfQPjGSxq79vK_E1_w3u9EQAISe2rt_tAvoyRRoNGE3DizPJMNV55XVHXB6NQwSv0qWxEn_oVMifzv5z_G_pDDPFUWertg"
#     token = Token(token=token_string)
#     is_token_valid = stub.ValidateToken(token)
#     print(is_token_valid)
