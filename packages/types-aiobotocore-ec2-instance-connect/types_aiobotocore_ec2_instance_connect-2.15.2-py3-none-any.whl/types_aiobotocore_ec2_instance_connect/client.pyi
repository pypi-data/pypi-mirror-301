"""
Type annotations for ec2-instance-connect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ec2_instance_connect.client import EC2InstanceConnectClient

    session = get_session()
    async with session.create_client("ec2-instance-connect") as client:
        client: EC2InstanceConnectClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    SendSerialConsoleSSHPublicKeyRequestRequestTypeDef,
    SendSerialConsoleSSHPublicKeyResponseTypeDef,
    SendSSHPublicKeyRequestRequestTypeDef,
    SendSSHPublicKeyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("EC2InstanceConnectClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AuthException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    EC2InstanceNotFoundException: Type[BotocoreClientError]
    EC2InstanceStateInvalidException: Type[BotocoreClientError]
    EC2InstanceTypeInvalidException: Type[BotocoreClientError]
    EC2InstanceUnavailableException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    SerialConsoleAccessDisabledException: Type[BotocoreClientError]
    SerialConsoleSessionLimitExceededException: Type[BotocoreClientError]
    SerialConsoleSessionUnavailableException: Type[BotocoreClientError]
    SerialConsoleSessionUnsupportedException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class EC2InstanceConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EC2InstanceConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#close)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#generate_presigned_url)
        """

    async def send_serial_console_ssh_public_key(
        self, **kwargs: Unpack[SendSerialConsoleSSHPublicKeyRequestRequestTypeDef]
    ) -> SendSerialConsoleSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.send_serial_console_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#send_serial_console_ssh_public_key)
        """

    async def send_ssh_public_key(
        self, **kwargs: Unpack[SendSSHPublicKeyRequestRequestTypeDef]
    ) -> SendSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance for use by the specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client.send_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#send_ssh_public_key)
        """

    async def __aenter__(self) -> "EC2InstanceConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
        """
