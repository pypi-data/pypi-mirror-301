"""
Type annotations for ecr-public service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecr_public.client import ECRPublicClient

    session = get_session()
    async with session.create_client("ecr-public") as client:
        client: ECRPublicClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    DescribeImagesPaginator,
    DescribeImageTagsPaginator,
    DescribeRegistriesPaginator,
    DescribeRepositoriesPaginator,
)
from .type_defs import (
    BatchCheckLayerAvailabilityRequestRequestTypeDef,
    BatchCheckLayerAvailabilityResponseTypeDef,
    BatchDeleteImageRequestRequestTypeDef,
    BatchDeleteImageResponseTypeDef,
    CompleteLayerUploadRequestRequestTypeDef,
    CompleteLayerUploadResponseTypeDef,
    CreateRepositoryRequestRequestTypeDef,
    CreateRepositoryResponseTypeDef,
    DeleteRepositoryPolicyRequestRequestTypeDef,
    DeleteRepositoryPolicyResponseTypeDef,
    DeleteRepositoryRequestRequestTypeDef,
    DeleteRepositoryResponseTypeDef,
    DescribeImagesRequestRequestTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeImageTagsRequestRequestTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesRequestRequestTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesRequestRequestTypeDef,
    DescribeRepositoriesResponseTypeDef,
    GetAuthorizationTokenResponseTypeDef,
    GetRegistryCatalogDataResponseTypeDef,
    GetRepositoryCatalogDataRequestRequestTypeDef,
    GetRepositoryCatalogDataResponseTypeDef,
    GetRepositoryPolicyRequestRequestTypeDef,
    GetRepositoryPolicyResponseTypeDef,
    InitiateLayerUploadRequestRequestTypeDef,
    InitiateLayerUploadResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutImageRequestRequestTypeDef,
    PutImageResponseTypeDef,
    PutRegistryCatalogDataRequestRequestTypeDef,
    PutRegistryCatalogDataResponseTypeDef,
    PutRepositoryCatalogDataRequestRequestTypeDef,
    PutRepositoryCatalogDataResponseTypeDef,
    SetRepositoryPolicyRequestRequestTypeDef,
    SetRepositoryPolicyResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UploadLayerPartRequestRequestTypeDef,
    UploadLayerPartResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ECRPublicClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    EmptyUploadException: Type[BotocoreClientError]
    ImageAlreadyExistsException: Type[BotocoreClientError]
    ImageDigestDoesNotMatchException: Type[BotocoreClientError]
    ImageNotFoundException: Type[BotocoreClientError]
    ImageTagAlreadyExistsException: Type[BotocoreClientError]
    InvalidLayerException: Type[BotocoreClientError]
    InvalidLayerPartException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidTagParameterException: Type[BotocoreClientError]
    LayerAlreadyExistsException: Type[BotocoreClientError]
    LayerPartTooSmallException: Type[BotocoreClientError]
    LayersNotFoundException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ReferencedImagesNotFoundException: Type[BotocoreClientError]
    RegistryNotFoundException: Type[BotocoreClientError]
    RepositoryAlreadyExistsException: Type[BotocoreClientError]
    RepositoryCatalogDataNotFoundException: Type[BotocoreClientError]
    RepositoryNotEmptyException: Type[BotocoreClientError]
    RepositoryNotFoundException: Type[BotocoreClientError]
    RepositoryPolicyNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnsupportedCommandException: Type[BotocoreClientError]
    UploadNotFoundException: Type[BotocoreClientError]


class ECRPublicClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECRPublicClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#exceptions)
        """

    async def batch_check_layer_availability(
        self, **kwargs: Unpack[BatchCheckLayerAvailabilityRequestRequestTypeDef]
    ) -> BatchCheckLayerAvailabilityResponseTypeDef:
        """
        Checks the availability of one or more image layers that are within a
        repository in a public
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.batch_check_layer_availability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#batch_check_layer_availability)
        """

    async def batch_delete_image(
        self, **kwargs: Unpack[BatchDeleteImageRequestRequestTypeDef]
    ) -> BatchDeleteImageResponseTypeDef:
        """
        Deletes a list of specified images that are within a repository in a public
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.batch_delete_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#batch_delete_image)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#close)
        """

    async def complete_layer_upload(
        self, **kwargs: Unpack[CompleteLayerUploadRequestRequestTypeDef]
    ) -> CompleteLayerUploadResponseTypeDef:
        """
        Informs Amazon ECR that the image layer upload is complete for a specified
        public registry, repository name, and upload
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.complete_layer_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#complete_layer_upload)
        """

    async def create_repository(
        self, **kwargs: Unpack[CreateRepositoryRequestRequestTypeDef]
    ) -> CreateRepositoryResponseTypeDef:
        """
        Creates a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.create_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#create_repository)
        """

    async def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryRequestRequestTypeDef]
    ) -> DeleteRepositoryResponseTypeDef:
        """
        Deletes a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.delete_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#delete_repository)
        """

    async def delete_repository_policy(
        self, **kwargs: Unpack[DeleteRepositoryPolicyRequestRequestTypeDef]
    ) -> DeleteRepositoryPolicyResponseTypeDef:
        """
        Deletes the repository policy that's associated with the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.delete_repository_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#delete_repository_policy)
        """

    async def describe_image_tags(
        self, **kwargs: Unpack[DescribeImageTagsRequestRequestTypeDef]
    ) -> DescribeImageTagsResponseTypeDef:
        """
        Returns the image tag details for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_image_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#describe_image_tags)
        """

    async def describe_images(
        self, **kwargs: Unpack[DescribeImagesRequestRequestTypeDef]
    ) -> DescribeImagesResponseTypeDef:
        """
        Returns metadata that's related to the images in a repository in a public
        registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#describe_images)
        """

    async def describe_registries(
        self, **kwargs: Unpack[DescribeRegistriesRequestRequestTypeDef]
    ) -> DescribeRegistriesResponseTypeDef:
        """
        Returns details for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_registries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#describe_registries)
        """

    async def describe_repositories(
        self, **kwargs: Unpack[DescribeRepositoriesRequestRequestTypeDef]
    ) -> DescribeRepositoriesResponseTypeDef:
        """
        Describes repositories that are in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.describe_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#describe_repositories)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#generate_presigned_url)
        """

    async def get_authorization_token(self) -> GetAuthorizationTokenResponseTypeDef:
        """
        Retrieves an authorization token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_authorization_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_authorization_token)
        """

    async def get_registry_catalog_data(self) -> GetRegistryCatalogDataResponseTypeDef:
        """
        Retrieves catalog metadata for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_registry_catalog_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_registry_catalog_data)
        """

    async def get_repository_catalog_data(
        self, **kwargs: Unpack[GetRepositoryCatalogDataRequestRequestTypeDef]
    ) -> GetRepositoryCatalogDataResponseTypeDef:
        """
        Retrieve catalog metadata for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_repository_catalog_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_repository_catalog_data)
        """

    async def get_repository_policy(
        self, **kwargs: Unpack[GetRepositoryPolicyRequestRequestTypeDef]
    ) -> GetRepositoryPolicyResponseTypeDef:
        """
        Retrieves the repository policy for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_repository_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_repository_policy)
        """

    async def initiate_layer_upload(
        self, **kwargs: Unpack[InitiateLayerUploadRequestRequestTypeDef]
    ) -> InitiateLayerUploadResponseTypeDef:
        """
        Notifies Amazon ECR that you intend to upload an image layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.initiate_layer_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#initiate_layer_upload)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECR Public resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#list_tags_for_resource)
        """

    async def put_image(
        self, **kwargs: Unpack[PutImageRequestRequestTypeDef]
    ) -> PutImageResponseTypeDef:
        """
        Creates or updates the image manifest and tags that are associated with an
        image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#put_image)
        """

    async def put_registry_catalog_data(
        self, **kwargs: Unpack[PutRegistryCatalogDataRequestRequestTypeDef]
    ) -> PutRegistryCatalogDataResponseTypeDef:
        """
        Create or update the catalog data for a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_registry_catalog_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#put_registry_catalog_data)
        """

    async def put_repository_catalog_data(
        self, **kwargs: Unpack[PutRepositoryCatalogDataRequestRequestTypeDef]
    ) -> PutRepositoryCatalogDataResponseTypeDef:
        """
        Creates or updates the catalog data for a repository in a public registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.put_repository_catalog_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#put_repository_catalog_data)
        """

    async def set_repository_policy(
        self, **kwargs: Unpack[SetRepositoryPolicyRequestRequestTypeDef]
    ) -> SetRepositoryPolicyResponseTypeDef:
        """
        Applies a repository policy to the specified public repository to control
        access
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.set_repository_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#set_repository_policy)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#untag_resource)
        """

    async def upload_layer_part(
        self, **kwargs: Unpack[UploadLayerPartRequestRequestTypeDef]
    ) -> UploadLayerPartResponseTypeDef:
        """
        Uploads an image layer part to Amazon ECR.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.upload_layer_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#upload_layer_part)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_image_tags"]
    ) -> DescribeImageTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_images"]) -> DescribeImagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_registries"]
    ) -> DescribeRegistriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_repositories"]
    ) -> DescribeRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/#get_paginator)
        """

    async def __aenter__(self) -> "ECRPublicClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public.html#ECRPublic.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/client/)
        """
