"""
Type annotations for iam service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam.service_resource import IAMServiceResource
    import types_aiobotocore_iam.service_resource as iam_resources

    session = get_session()
    async with session.resource("iam") as resource:
        resource: IAMServiceResource

        my_access_key: iam_resources.AccessKey = resource.AccessKey(...)
        my_access_key_pair: iam_resources.AccessKeyPair = resource.AccessKeyPair(...)
        my_account_password_policy: iam_resources.AccountPasswordPolicy = resource.AccountPasswordPolicy(...)
        my_account_summary: iam_resources.AccountSummary = resource.AccountSummary(...)
        my_assume_role_policy: iam_resources.AssumeRolePolicy = resource.AssumeRolePolicy(...)
        my_current_user: iam_resources.CurrentUser = resource.CurrentUser(...)
        my_group: iam_resources.Group = resource.Group(...)
        my_group_policy: iam_resources.GroupPolicy = resource.GroupPolicy(...)
        my_instance_profile: iam_resources.InstanceProfile = resource.InstanceProfile(...)
        my_login_profile: iam_resources.LoginProfile = resource.LoginProfile(...)
        my_mfa_device: iam_resources.MfaDevice = resource.MfaDevice(...)
        my_policy: iam_resources.Policy = resource.Policy(...)
        my_policy_version: iam_resources.PolicyVersion = resource.PolicyVersion(...)
        my_role: iam_resources.Role = resource.Role(...)
        my_role_policy: iam_resources.RolePolicy = resource.RolePolicy(...)
        my_saml_provider: iam_resources.SamlProvider = resource.SamlProvider(...)
        my_server_certificate: iam_resources.ServerCertificate = resource.ServerCertificate(...)
        my_signing_certificate: iam_resources.SigningCertificate = resource.SigningCertificate(...)
        my_user: iam_resources.User = resource.User(...)
        my_user_policy: iam_resources.UserPolicy = resource.UserPolicy(...)
        my_virtual_mfa_device: iam_resources.VirtualMfaDevice = resource.VirtualMfaDevice(...)
```
"""

import sys
from datetime import datetime
from typing import AsyncIterator, Awaitable, Dict, List, NoReturn, Sequence

from .client import IAMClient
from .literals import (
    AssignmentStatusTypeType,
    EntityTypeType,
    PolicyScopeTypeType,
    PolicyUsageTypeType,
    StatusTypeType,
    SummaryKeyTypeType,
)
from .type_defs import (
    AddRoleToInstanceProfileRequestInstanceProfileAddRoleTypeDef,
    AddUserToGroupRequestGroupAddUserTypeDef,
    AddUserToGroupRequestUserAddGroupTypeDef,
    AttachedPermissionsBoundaryTypeDef,
    AttachGroupPolicyRequestGroupAttachPolicyTypeDef,
    AttachGroupPolicyRequestPolicyAttachGroupTypeDef,
    AttachRolePolicyRequestPolicyAttachRoleTypeDef,
    AttachRolePolicyRequestRoleAttachPolicyTypeDef,
    AttachUserPolicyRequestPolicyAttachUserTypeDef,
    AttachUserPolicyRequestUserAttachPolicyTypeDef,
    ChangePasswordRequestServiceResourceChangePasswordTypeDef,
    CreateAccountAliasRequestServiceResourceCreateAccountAliasTypeDef,
    CreateGroupRequestGroupCreateTypeDef,
    CreateGroupRequestServiceResourceCreateGroupTypeDef,
    CreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef,
    CreateLoginProfileRequestLoginProfileCreateTypeDef,
    CreateLoginProfileRequestUserCreateLoginProfileTypeDef,
    CreatePolicyRequestServiceResourceCreatePolicyTypeDef,
    CreatePolicyVersionRequestPolicyCreateVersionTypeDef,
    CreateRoleRequestServiceResourceCreateRoleTypeDef,
    CreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef,
    CreateUserRequestServiceResourceCreateUserTypeDef,
    CreateUserRequestUserCreateTypeDef,
    CreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef,
    DetachGroupPolicyRequestGroupDetachPolicyTypeDef,
    DetachGroupPolicyRequestPolicyDetachGroupTypeDef,
    DetachRolePolicyRequestPolicyDetachRoleTypeDef,
    DetachRolePolicyRequestRoleDetachPolicyTypeDef,
    DetachUserPolicyRequestPolicyDetachUserTypeDef,
    DetachUserPolicyRequestUserDetachPolicyTypeDef,
    EnableMFADeviceRequestMfaDeviceAssociateTypeDef,
    EnableMFADeviceRequestUserEnableMfaTypeDef,
    PolicyDocumentTypeDef,
    PutGroupPolicyRequestGroupCreatePolicyTypeDef,
    PutGroupPolicyRequestGroupPolicyPutTypeDef,
    PutRolePolicyRequestRolePolicyPutTypeDef,
    PutUserPolicyRequestUserCreatePolicyTypeDef,
    PutUserPolicyRequestUserPolicyPutTypeDef,
    RemoveRoleFromInstanceProfileRequestInstanceProfileRemoveRoleTypeDef,
    RemoveUserFromGroupRequestGroupRemoveUserTypeDef,
    RemoveUserFromGroupRequestUserRemoveGroupTypeDef,
    ResyncMFADeviceRequestMfaDeviceResyncTypeDef,
    RoleLastUsedTypeDef,
    RoleTypeDef,
    ServerCertificateMetadataTypeDef,
    TagTypeDef,
    UpdateAccessKeyRequestAccessKeyActivateTypeDef,
    UpdateAccessKeyRequestAccessKeyDeactivateTypeDef,
    UpdateAccessKeyRequestAccessKeyPairActivateTypeDef,
    UpdateAccessKeyRequestAccessKeyPairDeactivateTypeDef,
    UpdateAccountPasswordPolicyRequestAccountPasswordPolicyUpdateTypeDef,
    UpdateAccountPasswordPolicyRequestServiceResourceCreateAccountPasswordPolicyTypeDef,
    UpdateAssumeRolePolicyRequestAssumeRolePolicyUpdateTypeDef,
    UpdateGroupRequestGroupUpdateTypeDef,
    UpdateLoginProfileRequestLoginProfileUpdateTypeDef,
    UpdateSAMLProviderRequestSamlProviderUpdateTypeDef,
    UpdateSAMLProviderResponseTypeDef,
    UpdateServerCertificateRequestServerCertificateUpdateTypeDef,
    UpdateSigningCertificateRequestSigningCertificateActivateTypeDef,
    UpdateSigningCertificateRequestSigningCertificateDeactivateTypeDef,
    UpdateUserRequestUserUpdateTypeDef,
    UploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef,
    UploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef,
    UserTypeDef,
)

try:
    from aioboto3.resources.base import AIOBoto3ServiceResource
except ImportError:
    from builtins import object as AIOBoto3ServiceResource
try:
    from aioboto3.resources.collection import AIOResourceCollection
except ImportError:
    from builtins import object as AIOResourceCollection
try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "IAMServiceResource",
    "AccessKey",
    "AccessKeyPair",
    "AccountPasswordPolicy",
    "AccountSummary",
    "AssumeRolePolicy",
    "CurrentUser",
    "Group",
    "GroupPolicy",
    "InstanceProfile",
    "LoginProfile",
    "MfaDevice",
    "Policy",
    "PolicyVersion",
    "Role",
    "RolePolicy",
    "SamlProvider",
    "ServerCertificate",
    "SigningCertificate",
    "User",
    "UserPolicy",
    "VirtualMfaDevice",
    "ServiceResourceGroupsCollection",
    "ServiceResourceInstanceProfilesCollection",
    "ServiceResourcePoliciesCollection",
    "ServiceResourceRolesCollection",
    "ServiceResourceSamlProvidersCollection",
    "ServiceResourceServerCertificatesCollection",
    "ServiceResourceUsersCollection",
    "ServiceResourceVirtualMfaDevicesCollection",
    "CurrentUserAccessKeysCollection",
    "CurrentUserMfaDevicesCollection",
    "CurrentUserSigningCertificatesCollection",
    "GroupAttachedPoliciesCollection",
    "GroupPoliciesCollection",
    "GroupUsersCollection",
    "PolicyAttachedGroupsCollection",
    "PolicyAttachedRolesCollection",
    "PolicyAttachedUsersCollection",
    "PolicyVersionsCollection",
    "RoleAttachedPoliciesCollection",
    "RoleInstanceProfilesCollection",
    "RolePoliciesCollection",
    "UserAccessKeysCollection",
    "UserAttachedPoliciesCollection",
    "UserGroupsCollection",
    "UserMfaDevicesCollection",
    "UserPoliciesCollection",
    "UserSigningCertificatesCollection",
)


class ServiceResourceGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
    """

    def all(self) -> "ServiceResourceGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "ServiceResourceGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def limit(self, count: int) -> "ServiceResourceGroupsCollection":
        """
        Return at most this many Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceGroupsCollection":
        """
        Fetch at most this many Groups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def pages(self) -> AsyncIterator[List["Group"]]:
        """
        A generator which yields pages of Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """

    def __aiter__(self) -> AsyncIterator["Group"]:
        """
        A generator which yields Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcegroupscollection)
        """


class ServiceResourceInstanceProfilesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
    """

    def all(self) -> "ServiceResourceInstanceProfilesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "ServiceResourceInstanceProfilesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def limit(self, count: int) -> "ServiceResourceInstanceProfilesCollection":
        """
        Return at most this many InstanceProfiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceInstanceProfilesCollection":
        """
        Fetch at most this many InstanceProfiles per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def pages(self) -> AsyncIterator[List["InstanceProfile"]]:
        """
        A generator which yields pages of InstanceProfiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InstanceProfiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """

    def __aiter__(self) -> AsyncIterator["InstanceProfile"]:
        """
        A generator which yields InstanceProfiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceinstanceprofilescollection)
        """


class ServiceResourcePoliciesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
    """

    def all(self) -> "ServiceResourcePoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        Scope: PolicyScopeTypeType = ...,
        OnlyAttached: bool = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> "ServiceResourcePoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def limit(self, count: int) -> "ServiceResourcePoliciesCollection":
        """
        Return at most this many Policys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def page_size(self, count: int) -> "ServiceResourcePoliciesCollection":
        """
        Fetch at most this many Policys per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def pages(self) -> AsyncIterator[List["Policy"]]:
        """
        A generator which yields pages of Policys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Policys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """

    def __aiter__(self) -> AsyncIterator["Policy"]:
        """
        A generator which yields Policys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcepoliciescollection)
        """


class ServiceResourceRolesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
    """

    def all(self) -> "ServiceResourceRolesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "ServiceResourceRolesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def limit(self, count: int) -> "ServiceResourceRolesCollection":
        """
        Return at most this many Roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceRolesCollection":
        """
        Fetch at most this many Roles per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def pages(self) -> AsyncIterator[List["Role"]]:
        """
        A generator which yields pages of Roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """

    def __aiter__(self) -> AsyncIterator["Role"]:
        """
        A generator which yields Roles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcerolescollection)
        """


class ServiceResourceSamlProvidersCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
    """

    def all(self) -> "ServiceResourceSamlProvidersCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def filter(  # type: ignore
        self,
    ) -> "ServiceResourceSamlProvidersCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSamlProvidersCollection":
        """
        Return at most this many SamlProviders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSamlProvidersCollection":
        """
        Fetch at most this many SamlProviders per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def pages(self) -> AsyncIterator[List["SamlProvider"]]:
        """
        A generator which yields pages of SamlProviders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SamlProviders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """

    def __aiter__(self) -> AsyncIterator["SamlProvider"]:
        """
        A generator which yields SamlProviders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.saml_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcesamlproviderscollection)
        """


class ServiceResourceServerCertificatesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
    """

    def all(self) -> "ServiceResourceServerCertificatesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "ServiceResourceServerCertificatesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def limit(self, count: int) -> "ServiceResourceServerCertificatesCollection":
        """
        Return at most this many ServerCertificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceServerCertificatesCollection":
        """
        Fetch at most this many ServerCertificates per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def pages(self) -> AsyncIterator[List["ServerCertificate"]]:
        """
        A generator which yields pages of ServerCertificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields ServerCertificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """

    def __aiter__(self) -> AsyncIterator["ServerCertificate"]:
        """
        A generator which yields ServerCertificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.server_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceservercertificatescollection)
        """


class ServiceResourceUsersCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
    """

    def all(self) -> "ServiceResourceUsersCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "ServiceResourceUsersCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def limit(self, count: int) -> "ServiceResourceUsersCollection":
        """
        Return at most this many Users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceUsersCollection":
        """
        Fetch at most this many Users per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def pages(self) -> AsyncIterator[List["User"]]:
        """
        A generator which yields pages of Users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """

    def __aiter__(self) -> AsyncIterator["User"]:
        """
        A generator which yields Users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourceuserscollection)
        """


class ServiceResourceVirtualMfaDevicesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
    """

    def all(self) -> "ServiceResourceVirtualMfaDevicesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        AssignmentStatus: AssignmentStatusTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> "ServiceResourceVirtualMfaDevicesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def limit(self, count: int) -> "ServiceResourceVirtualMfaDevicesCollection":
        """
        Return at most this many VirtualMfaDevices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVirtualMfaDevicesCollection":
        """
        Fetch at most this many VirtualMfaDevices per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def pages(self) -> AsyncIterator[List["VirtualMfaDevice"]]:
        """
        A generator which yields pages of VirtualMfaDevices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VirtualMfaDevices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """

    def __aiter__(self) -> AsyncIterator["VirtualMfaDevice"]:
        """
        A generator which yields VirtualMfaDevices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.virtual_mfa_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#serviceresourcevirtualmfadevicescollection)
        """


class CurrentUserAccessKeysCollection(AIOResourceCollection):
    def all(self) -> "CurrentUserAccessKeysCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "CurrentUserAccessKeysCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "CurrentUserAccessKeysCollection":
        """
        Return at most this many AccessKeys.
        """

    def page_size(self, count: int) -> "CurrentUserAccessKeysCollection":
        """
        Fetch at most this many AccessKeys per service request.
        """

    def pages(self) -> AsyncIterator[List["AccessKey"]]:
        """
        A generator which yields pages of AccessKeys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields AccessKeys.
        """

    def __aiter__(self) -> AsyncIterator["AccessKey"]:
        """
        A generator which yields AccessKeys.
        """


class CurrentUserMfaDevicesCollection(AIOResourceCollection):
    def all(self) -> "CurrentUserMfaDevicesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "CurrentUserMfaDevicesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "CurrentUserMfaDevicesCollection":
        """
        Return at most this many MfaDevices.
        """

    def page_size(self, count: int) -> "CurrentUserMfaDevicesCollection":
        """
        Fetch at most this many MfaDevices per service request.
        """

    def pages(self) -> AsyncIterator[List["MfaDevice"]]:
        """
        A generator which yields pages of MfaDevices.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields MfaDevices.
        """

    def __aiter__(self) -> AsyncIterator["MfaDevice"]:
        """
        A generator which yields MfaDevices.
        """


class CurrentUserSigningCertificatesCollection(AIOResourceCollection):
    def all(self) -> "CurrentUserSigningCertificatesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "CurrentUserSigningCertificatesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "CurrentUserSigningCertificatesCollection":
        """
        Return at most this many SigningCertificates.
        """

    def page_size(self, count: int) -> "CurrentUserSigningCertificatesCollection":
        """
        Fetch at most this many SigningCertificates per service request.
        """

    def pages(self) -> AsyncIterator[List["SigningCertificate"]]:
        """
        A generator which yields pages of SigningCertificates.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SigningCertificates.
        """

    def __aiter__(self) -> AsyncIterator["SigningCertificate"]:
        """
        A generator which yields SigningCertificates.
        """


class GroupAttachedPoliciesCollection(AIOResourceCollection):
    def all(self) -> "GroupAttachedPoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "GroupAttachedPoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "GroupAttachedPoliciesCollection":
        """
        Return at most this many Policys.
        """

    def page_size(self, count: int) -> "GroupAttachedPoliciesCollection":
        """
        Fetch at most this many Policys per service request.
        """

    def pages(self) -> AsyncIterator[List["Policy"]]:
        """
        A generator which yields pages of Policys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Policys.
        """

    def __aiter__(self) -> AsyncIterator["Policy"]:
        """
        A generator which yields Policys.
        """


class GroupPoliciesCollection(AIOResourceCollection):
    def all(self) -> "GroupPoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "GroupPoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "GroupPoliciesCollection":
        """
        Return at most this many GroupPolicys.
        """

    def page_size(self, count: int) -> "GroupPoliciesCollection":
        """
        Fetch at most this many GroupPolicys per service request.
        """

    def pages(self) -> AsyncIterator[List["GroupPolicy"]]:
        """
        A generator which yields pages of GroupPolicys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields GroupPolicys.
        """

    def __aiter__(self) -> AsyncIterator["GroupPolicy"]:
        """
        A generator which yields GroupPolicys.
        """


class GroupUsersCollection(AIOResourceCollection):
    def all(self) -> "GroupUsersCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "GroupUsersCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "GroupUsersCollection":
        """
        Return at most this many Users.
        """

    def page_size(self, count: int) -> "GroupUsersCollection":
        """
        Fetch at most this many Users per service request.
        """

    def pages(self) -> AsyncIterator[List["User"]]:
        """
        A generator which yields pages of Users.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Users.
        """

    def __aiter__(self) -> AsyncIterator["User"]:
        """
        A generator which yields Users.
        """


class PolicyAttachedGroupsCollection(AIOResourceCollection):
    def all(self) -> "PolicyAttachedGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        EntityFilter: EntityTypeType = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> "PolicyAttachedGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PolicyAttachedGroupsCollection":
        """
        Return at most this many Groups.
        """

    def page_size(self, count: int) -> "PolicyAttachedGroupsCollection":
        """
        Fetch at most this many Groups per service request.
        """

    def pages(self) -> AsyncIterator[List["Group"]]:
        """
        A generator which yields pages of Groups.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Groups.
        """

    def __aiter__(self) -> AsyncIterator["Group"]:
        """
        A generator which yields Groups.
        """


class PolicyAttachedRolesCollection(AIOResourceCollection):
    def all(self) -> "PolicyAttachedRolesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        EntityFilter: EntityTypeType = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> "PolicyAttachedRolesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PolicyAttachedRolesCollection":
        """
        Return at most this many Roles.
        """

    def page_size(self, count: int) -> "PolicyAttachedRolesCollection":
        """
        Fetch at most this many Roles per service request.
        """

    def pages(self) -> AsyncIterator[List["Role"]]:
        """
        A generator which yields pages of Roles.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Roles.
        """

    def __aiter__(self) -> AsyncIterator["Role"]:
        """
        A generator which yields Roles.
        """


class PolicyAttachedUsersCollection(AIOResourceCollection):
    def all(self) -> "PolicyAttachedUsersCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        EntityFilter: EntityTypeType = ...,
        PathPrefix: str = ...,
        PolicyUsageFilter: PolicyUsageTypeType = ...,
        Marker: str = ...,
        MaxItems: int = ...,
    ) -> "PolicyAttachedUsersCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PolicyAttachedUsersCollection":
        """
        Return at most this many Users.
        """

    def page_size(self, count: int) -> "PolicyAttachedUsersCollection":
        """
        Fetch at most this many Users per service request.
        """

    def pages(self) -> AsyncIterator[List["User"]]:
        """
        A generator which yields pages of Users.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Users.
        """

    def __aiter__(self) -> AsyncIterator["User"]:
        """
        A generator which yields Users.
        """


class PolicyVersionsCollection(AIOResourceCollection):
    def all(self) -> "PolicyVersionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "PolicyVersionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PolicyVersionsCollection":
        """
        Return at most this many PolicyVersions.
        """

    def page_size(self, count: int) -> "PolicyVersionsCollection":
        """
        Fetch at most this many PolicyVersions per service request.
        """

    def pages(self) -> AsyncIterator[List["PolicyVersion"]]:
        """
        A generator which yields pages of PolicyVersions.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields PolicyVersions.
        """

    def __aiter__(self) -> AsyncIterator["PolicyVersion"]:
        """
        A generator which yields PolicyVersions.
        """


class RoleAttachedPoliciesCollection(AIOResourceCollection):
    def all(self) -> "RoleAttachedPoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "RoleAttachedPoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "RoleAttachedPoliciesCollection":
        """
        Return at most this many Policys.
        """

    def page_size(self, count: int) -> "RoleAttachedPoliciesCollection":
        """
        Fetch at most this many Policys per service request.
        """

    def pages(self) -> AsyncIterator[List["Policy"]]:
        """
        A generator which yields pages of Policys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Policys.
        """

    def __aiter__(self) -> AsyncIterator["Policy"]:
        """
        A generator which yields Policys.
        """


class RoleInstanceProfilesCollection(AIOResourceCollection):
    def all(self) -> "RoleInstanceProfilesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "RoleInstanceProfilesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "RoleInstanceProfilesCollection":
        """
        Return at most this many InstanceProfiles.
        """

    def page_size(self, count: int) -> "RoleInstanceProfilesCollection":
        """
        Fetch at most this many InstanceProfiles per service request.
        """

    def pages(self) -> AsyncIterator[List["InstanceProfile"]]:
        """
        A generator which yields pages of InstanceProfiles.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InstanceProfiles.
        """

    def __aiter__(self) -> AsyncIterator["InstanceProfile"]:
        """
        A generator which yields InstanceProfiles.
        """


class RolePoliciesCollection(AIOResourceCollection):
    def all(self) -> "RolePoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "RolePoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "RolePoliciesCollection":
        """
        Return at most this many RolePolicys.
        """

    def page_size(self, count: int) -> "RolePoliciesCollection":
        """
        Fetch at most this many RolePolicys per service request.
        """

    def pages(self) -> AsyncIterator[List["RolePolicy"]]:
        """
        A generator which yields pages of RolePolicys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields RolePolicys.
        """

    def __aiter__(self) -> AsyncIterator["RolePolicy"]:
        """
        A generator which yields RolePolicys.
        """


class UserAccessKeysCollection(AIOResourceCollection):
    def all(self) -> "UserAccessKeysCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "UserAccessKeysCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserAccessKeysCollection":
        """
        Return at most this many AccessKeys.
        """

    def page_size(self, count: int) -> "UserAccessKeysCollection":
        """
        Fetch at most this many AccessKeys per service request.
        """

    def pages(self) -> AsyncIterator[List["AccessKey"]]:
        """
        A generator which yields pages of AccessKeys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields AccessKeys.
        """

    def __aiter__(self) -> AsyncIterator["AccessKey"]:
        """
        A generator which yields AccessKeys.
        """


class UserAttachedPoliciesCollection(AIOResourceCollection):
    def all(self) -> "UserAttachedPoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, PathPrefix: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "UserAttachedPoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserAttachedPoliciesCollection":
        """
        Return at most this many Policys.
        """

    def page_size(self, count: int) -> "UserAttachedPoliciesCollection":
        """
        Fetch at most this many Policys per service request.
        """

    def pages(self) -> AsyncIterator[List["Policy"]]:
        """
        A generator which yields pages of Policys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Policys.
        """

    def __aiter__(self) -> AsyncIterator["Policy"]:
        """
        A generator which yields Policys.
        """


class UserGroupsCollection(AIOResourceCollection):
    def all(self) -> "UserGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "UserGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserGroupsCollection":
        """
        Return at most this many Groups.
        """

    def page_size(self, count: int) -> "UserGroupsCollection":
        """
        Fetch at most this many Groups per service request.
        """

    def pages(self) -> AsyncIterator[List["Group"]]:
        """
        A generator which yields pages of Groups.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Groups.
        """

    def __aiter__(self) -> AsyncIterator["Group"]:
        """
        A generator which yields Groups.
        """


class UserMfaDevicesCollection(AIOResourceCollection):
    def all(self) -> "UserMfaDevicesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "UserMfaDevicesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserMfaDevicesCollection":
        """
        Return at most this many MfaDevices.
        """

    def page_size(self, count: int) -> "UserMfaDevicesCollection":
        """
        Fetch at most this many MfaDevices per service request.
        """

    def pages(self) -> AsyncIterator[List["MfaDevice"]]:
        """
        A generator which yields pages of MfaDevices.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields MfaDevices.
        """

    def __aiter__(self) -> AsyncIterator["MfaDevice"]:
        """
        A generator which yields MfaDevices.
        """


class UserPoliciesCollection(AIOResourceCollection):
    def all(self) -> "UserPoliciesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, Marker: str = ..., MaxItems: int = ...
    ) -> "UserPoliciesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserPoliciesCollection":
        """
        Return at most this many UserPolicys.
        """

    def page_size(self, count: int) -> "UserPoliciesCollection":
        """
        Fetch at most this many UserPolicys per service request.
        """

    def pages(self) -> AsyncIterator[List["UserPolicy"]]:
        """
        A generator which yields pages of UserPolicys.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields UserPolicys.
        """

    def __aiter__(self) -> AsyncIterator["UserPolicy"]:
        """
        A generator which yields UserPolicys.
        """


class UserSigningCertificatesCollection(AIOResourceCollection):
    def all(self) -> "UserSigningCertificatesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, UserName: str = ..., Marker: str = ..., MaxItems: int = ...
    ) -> "UserSigningCertificatesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "UserSigningCertificatesCollection":
        """
        Return at most this many SigningCertificates.
        """

    def page_size(self, count: int) -> "UserSigningCertificatesCollection":
        """
        Fetch at most this many SigningCertificates per service request.
        """

    def pages(self) -> AsyncIterator[List["SigningCertificate"]]:
        """
        A generator which yields pages of SigningCertificates.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SigningCertificates.
        """

    def __aiter__(self) -> AsyncIterator["SigningCertificate"]:
        """
        A generator which yields SigningCertificates.
        """


class AccessKeyPair(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccessKeyPair)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeypair)
    """

    access_key_id: Awaitable[str]
    status: Awaitable[StatusTypeType]
    secret_access_key: Awaitable[str]
    create_date: Awaitable[datetime]
    user_name: str
    id: str
    secret: str
    meta: "IAMResourceMeta"  # type: ignore

    async def activate(
        self, **kwargs: Unpack[UpdateAccessKeyRequestAccessKeyPairActivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKeyPair.activate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeypairactivate-method)
        """

    async def deactivate(
        self, **kwargs: Unpack[UpdateAccessKeyRequestAccessKeyPairDeactivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKeyPair.deactivate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeypairdeactivate-method)
        """

    async def delete(self) -> None:
        """
        Deletes the access key pair associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKeyPair.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeypairdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKeyPair.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeypairget_available_subresources-method)
        """


_AccessKeyPair = AccessKeyPair


class AccountPasswordPolicy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccountPasswordPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicy)
    """

    minimum_password_length: Awaitable[int]
    require_symbols: Awaitable[bool]
    require_numbers: Awaitable[bool]
    require_uppercase_characters: Awaitable[bool]
    require_lowercase_characters: Awaitable[bool]
    allow_users_to_change_password: Awaitable[bool]
    expire_passwords: Awaitable[bool]
    max_password_age: Awaitable[int]
    password_reuse_prevention: Awaitable[int]
    hard_expiry: Awaitable[bool]
    meta: "IAMResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes the password policy for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountPasswordPolicy.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicydelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountPasswordPolicy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicyget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_account_password_policy` to update the
        attributes of the AccountPasswordPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountPasswordPolicy.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicyload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_account_password_policy` to update the
        attributes of the AccountPasswordPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountPasswordPolicy.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicyreload-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateAccountPasswordPolicyRequestAccountPasswordPolicyUpdateTypeDef]
    ) -> None:
        """
        Updates the password policy settings for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountPasswordPolicy.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountpasswordpolicyupdate-method)
        """


_AccountPasswordPolicy = AccountPasswordPolicy


class AccountSummary(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccountSummary)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountsummary)
    """

    summary_map: Awaitable[Dict[SummaryKeyTypeType, int]]
    meta: "IAMResourceMeta"  # type: ignore

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountSummary.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountsummaryget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_account_summary` to update the attributes of the
        AccountSummary
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountSummary.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountsummaryload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_account_summary` to update the attributes of the
        AccountSummary
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccountSummary.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accountsummaryreload-method)
        """


_AccountSummary = AccountSummary


class CurrentUser(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.CurrentUser)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#currentuser)
    """

    path: Awaitable[str]
    user_name: Awaitable[str]
    user_id: Awaitable[str]
    arn: Awaitable[str]
    create_date: Awaitable[datetime]
    password_last_used: Awaitable[datetime]
    permissions_boundary: Awaitable[AttachedPermissionsBoundaryTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    user: "User"
    access_keys: CurrentUserAccessKeysCollection
    mfa_devices: CurrentUserMfaDevicesCollection
    signing_certificates: CurrentUserSigningCertificatesCollection
    meta: "IAMResourceMeta"  # type: ignore

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.CurrentUser.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#currentuserget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user` to update the attributes of the
        CurrentUser
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.CurrentUser.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#currentuserload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user` to update the attributes of the
        CurrentUser
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.CurrentUser.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#currentuserreload-method)
        """


_CurrentUser = CurrentUser


class InstanceProfile(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.InstanceProfile)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofile)
    """

    path: Awaitable[str]
    instance_profile_name: Awaitable[str]
    instance_profile_id: Awaitable[str]
    arn: Awaitable[str]
    create_date: Awaitable[datetime]
    roles_attribute: Awaitable[List[RoleTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    name: str
    roles: List["Role"]
    meta: "IAMResourceMeta"  # type: ignore

    async def add_role(
        self, **kwargs: Unpack[AddRoleToInstanceProfileRequestInstanceProfileAddRoleTypeDef]
    ) -> None:
        """
        Adds the specified IAM role to the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.add_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofileadd_role-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofiledelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofileget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_instance_profile` to update the attributes of
        the InstanceProfile
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofileload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_instance_profile` to update the attributes of
        the InstanceProfile
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofilereload-method)
        """

    async def remove_role(
        self, **kwargs: Unpack[RemoveRoleFromInstanceProfileRequestInstanceProfileRemoveRoleTypeDef]
    ) -> None:
        """
        Removes the specified IAM role from the specified Amazon EC2 instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.InstanceProfile.remove_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#instanceprofileremove_role-method)
        """


_InstanceProfile = InstanceProfile


class PolicyVersion(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.PolicyVersion)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversion)
    """

    document: Awaitable[PolicyDocumentTypeDef]
    is_default_version: Awaitable[bool]
    create_date: Awaitable[datetime]
    arn: str
    version_id: str
    meta: "IAMResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes the specified version from the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.PolicyVersion.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversiondelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.PolicyVersion.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversionget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_policy_version` to update the attributes of the
        PolicyVersion
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.PolicyVersion.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversionload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_policy_version` to update the attributes of the
        PolicyVersion
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.PolicyVersion.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversionreload-method)
        """

    async def set_as_default(self) -> None:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative)
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.PolicyVersion.set_as_default)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyversionset_as_default-method)
        """


_PolicyVersion = PolicyVersion


class SamlProvider(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.SamlProvider)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlprovider)
    """

    saml_metadata_document: Awaitable[str]
    create_date: Awaitable[datetime]
    valid_until: Awaitable[datetime]
    tags: Awaitable[List[TagTypeDef]]
    arn: str
    meta: "IAMResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes a SAML provider resource in IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SamlProvider.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlproviderdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SamlProvider.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlproviderget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_saml_provider` to update the attributes of the
        SamlProvider
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SamlProvider.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlproviderload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_saml_provider` to update the attributes of the
        SamlProvider
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SamlProvider.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlproviderreload-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateSAMLProviderRequestSamlProviderUpdateTypeDef]
    ) -> UpdateSAMLProviderResponseTypeDef:
        """
        Updates the metadata document for an existing SAML provider resource object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SamlProvider.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#samlproviderupdate-method)
        """


_SamlProvider = SamlProvider


class VirtualMfaDevice(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.VirtualMfaDevice)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#virtualmfadevice)
    """

    base32_string_seed: Awaitable[bytes]
    qr_code_png: Awaitable[bytes]
    user_attribute: Awaitable[UserTypeDef]
    enable_date: Awaitable[datetime]
    tags: Awaitable[List[TagTypeDef]]
    serial_number: str
    user: "User"
    meta: "IAMResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes a virtual MFA device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.VirtualMfaDevice.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#virtualmfadevicedelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.VirtualMfaDevice.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#virtualmfadeviceget_available_subresources-method)
        """


_VirtualMfaDevice = VirtualMfaDevice


class AccessKey(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccessKey)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskey)
    """

    access_key_id: Awaitable[str]
    status: Awaitable[StatusTypeType]
    create_date: Awaitable[datetime]
    user_name: str
    id: str
    meta: "IAMResourceMeta"  # type: ignore

    async def User(self) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKey.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeyuser-method)
        """

    async def activate(
        self, **kwargs: Unpack[UpdateAccessKeyRequestAccessKeyActivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKey.activate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeyactivate-method)
        """

    async def deactivate(
        self, **kwargs: Unpack[UpdateAccessKeyRequestAccessKeyDeactivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified access key from Active to Inactive, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKey.deactivate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeydeactivate-method)
        """

    async def delete(self) -> None:
        """
        Deletes the access key pair associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKey.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeydelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AccessKey.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#accesskeyget_available_subresources-method)
        """


_AccessKey = AccessKey


class AssumeRolePolicy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AssumeRolePolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#assumerolepolicy)
    """

    role_name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def Role(self) -> "_Role":
        """
        Creates a Role resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AssumeRolePolicy.Role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#assumerolepolicyrole-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AssumeRolePolicy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#assumerolepolicyget_available_subresources-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateAssumeRolePolicyRequestAssumeRolePolicyUpdateTypeDef]
    ) -> None:
        """
        Updates the policy that grants an IAM entity permission to assume a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.AssumeRolePolicy.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#assumerolepolicyupdate-method)
        """


_AssumeRolePolicy = AssumeRolePolicy


class GroupPolicy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.GroupPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicy)
    """

    policy_name: Awaitable[str]
    policy_document: Awaitable[PolicyDocumentTypeDef]
    group_name: str
    name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def Group(self) -> "_Group":
        """
        Creates a Group resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.Group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicygroup-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicydelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicyget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_group_policy` to update the attributes of the
        GroupPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicyload-method)
        """

    async def put(self, **kwargs: Unpack[PutGroupPolicyRequestGroupPolicyPutTypeDef]) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.put)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicyput-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_group_policy` to update the attributes of the
        GroupPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.GroupPolicy.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicyreload-method)
        """


_GroupPolicy = GroupPolicy


class MfaDevice(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.MfaDevice)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadevice)
    """

    enable_date: Awaitable[datetime]
    user_name: str
    serial_number: str
    meta: "IAMResourceMeta"  # type: ignore

    async def User(self) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.MfaDevice.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadeviceuser-method)
        """

    async def associate(
        self, **kwargs: Unpack[EnableMFADeviceRequestMfaDeviceAssociateTypeDef]
    ) -> None:
        """
        Enables the specified MFA device and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.MfaDevice.associate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadeviceassociate-method)
        """

    async def disassociate(self) -> None:
        """
        Deactivates the specified MFA device and removes it from association with the
        user name for which it was originally
        enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.MfaDevice.disassociate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadevicedisassociate-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.MfaDevice.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadeviceget_available_subresources-method)
        """

    async def resync(self, **kwargs: Unpack[ResyncMFADeviceRequestMfaDeviceResyncTypeDef]) -> None:
        """
        Synchronizes the specified MFA device with its IAM resource object on the
        Amazon Web Services
        servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.MfaDevice.resync)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#mfadeviceresync-method)
        """


_MfaDevice = MfaDevice


class Policy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Policy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policy)
    """

    policy_name: Awaitable[str]
    policy_id: Awaitable[str]
    path: Awaitable[str]
    default_version_id: Awaitable[str]
    attachment_count: Awaitable[int]
    permissions_boundary_usage_count: Awaitable[int]
    is_attachable: Awaitable[bool]
    description: Awaitable[str]
    create_date: Awaitable[datetime]
    update_date: Awaitable[datetime]
    tags: Awaitable[List[TagTypeDef]]
    arn: str
    default_version: "PolicyVersion"
    attached_groups: PolicyAttachedGroupsCollection
    attached_roles: PolicyAttachedRolesCollection
    attached_users: PolicyAttachedUsersCollection
    versions: PolicyVersionsCollection
    meta: "IAMResourceMeta"  # type: ignore

    async def attach_group(
        self, **kwargs: Unpack[AttachGroupPolicyRequestPolicyAttachGroupTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.attach_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyattach_group-method)
        """

    async def attach_role(
        self, **kwargs: Unpack[AttachRolePolicyRequestPolicyAttachRoleTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.attach_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyattach_role-method)
        """

    async def attach_user(
        self, **kwargs: Unpack[AttachUserPolicyRequestPolicyAttachUserTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.attach_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyattach_user-method)
        """

    async def create_version(
        self, **kwargs: Unpack[CreatePolicyVersionRequestPolicyCreateVersionTypeDef]
    ) -> "_PolicyVersion":
        """
        Creates a new version of the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.create_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policycreate_version-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified managed policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policydelete-method)
        """

    async def detach_group(
        self, **kwargs: Unpack[DetachGroupPolicyRequestPolicyDetachGroupTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.detach_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policydetach_group-method)
        """

    async def detach_role(
        self, **kwargs: Unpack[DetachRolePolicyRequestPolicyDetachRoleTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.detach_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policydetach_role-method)
        """

    async def detach_user(
        self, **kwargs: Unpack[DetachUserPolicyRequestPolicyDetachUserTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.detach_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policydetach_user-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_policy` to update the attributes of the Policy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_policy` to update the attributes of the Policy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Policy.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#policyreload-method)
        """


_Policy = Policy


class RolePolicy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.RolePolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicy)
    """

    policy_name: Awaitable[str]
    policy_document: Awaitable[PolicyDocumentTypeDef]
    role_name: str
    name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def Role(self) -> "_Role":
        """
        Creates a Role resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.Role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicyrole-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicydelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicyget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_role_policy` to update the attributes of the
        RolePolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicyload-method)
        """

    async def put(self, **kwargs: Unpack[PutRolePolicyRequestRolePolicyPutTypeDef]) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.put)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicyput-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_role_policy` to update the attributes of the
        RolePolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.RolePolicy.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicyreload-method)
        """


_RolePolicy = RolePolicy


class ServerCertificate(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.ServerCertificate)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificate)
    """

    server_certificate_metadata: Awaitable[ServerCertificateMetadataTypeDef]
    certificate_body: Awaitable[str]
    certificate_chain: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes the specified server certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServerCertificate.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificatedelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServerCertificate.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificateget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_server_certificate` to update the attributes of
        the ServerCertificate
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServerCertificate.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificateload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_server_certificate` to update the attributes of
        the ServerCertificate
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServerCertificate.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificatereload-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateServerCertificateRequestServerCertificateUpdateTypeDef]
    ) -> "_ServerCertificate":
        """
        Updates the name and/or the path of the specified server certificate stored in
        IAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServerCertificate.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#servercertificateupdate-method)
        """


_ServerCertificate = ServerCertificate


class SigningCertificate(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.SigningCertificate)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificate)
    """

    certificate_id: Awaitable[str]
    certificate_body: Awaitable[str]
    status: Awaitable[StatusTypeType]
    upload_date: Awaitable[datetime]
    user_name: str
    id: str
    meta: "IAMResourceMeta"  # type: ignore

    async def User(self) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SigningCertificate.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificateuser-method)
        """

    async def activate(
        self, **kwargs: Unpack[UpdateSigningCertificateRequestSigningCertificateActivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified user signing certificate from active to
        disabled, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SigningCertificate.activate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificateactivate-method)
        """

    async def deactivate(
        self, **kwargs: Unpack[UpdateSigningCertificateRequestSigningCertificateDeactivateTypeDef]
    ) -> None:
        """
        Changes the status of the specified user signing certificate from active to
        disabled, or vice
        versa.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SigningCertificate.deactivate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificatedeactivate-method)
        """

    async def delete(self) -> None:
        """
        Deletes a signing certificate associated with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SigningCertificate.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificatedelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.SigningCertificate.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#signingcertificateget_available_subresources-method)
        """


_SigningCertificate = SigningCertificate


class UserPolicy(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.UserPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicy)
    """

    policy_name: Awaitable[str]
    policy_document: Awaitable[PolicyDocumentTypeDef]
    user_name: str
    name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def User(self) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicyuser-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified inline policy that is embedded in the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicydelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicyget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user_policy` to update the attributes of the
        UserPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicyload-method)
        """

    async def put(self, **kwargs: Unpack[PutUserPolicyRequestUserPolicyPutTypeDef]) -> None:
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.put)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicyput-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user_policy` to update the attributes of the
        UserPolicy
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.UserPolicy.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicyreload-method)
        """


_UserPolicy = UserPolicy


class Group(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Group)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#group)
    """

    path: Awaitable[str]
    group_name: Awaitable[str]
    group_id: Awaitable[str]
    arn: Awaitable[str]
    create_date: Awaitable[datetime]
    name: str
    attached_policies: GroupAttachedPoliciesCollection
    policies: GroupPoliciesCollection
    users: GroupUsersCollection
    meta: "IAMResourceMeta"  # type: ignore

    async def Policy(self, name: str) -> "_GroupPolicy":
        """
        Creates a GroupPolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.Policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#grouppolicy-method)
        """

    async def add_user(self, **kwargs: Unpack[AddUserToGroupRequestGroupAddUserTypeDef]) -> None:
        """
        Adds the specified user to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.add_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupadd_user-method)
        """

    async def attach_policy(
        self, **kwargs: Unpack[AttachGroupPolicyRequestGroupAttachPolicyTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.attach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupattach_policy-method)
        """

    async def create(self, **kwargs: Unpack[CreateGroupRequestGroupCreateTypeDef]) -> "_Group":
        """
        Creates a new group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.create)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupcreate-method)
        """

    async def create_policy(
        self, **kwargs: Unpack[PutGroupPolicyRequestGroupCreatePolicyTypeDef]
    ) -> "_GroupPolicy":
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupcreate_policy-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupdelete-method)
        """

    async def detach_policy(
        self, **kwargs: Unpack[DetachGroupPolicyRequestGroupDetachPolicyTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.detach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupdetach_policy-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_group` to update the attributes of the Group
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_group` to update the attributes of the Group
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupreload-method)
        """

    async def remove_user(
        self, **kwargs: Unpack[RemoveUserFromGroupRequestGroupRemoveUserTypeDef]
    ) -> None:
        """
        Removes the specified user from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.remove_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupremove_user-method)
        """

    async def update(self, **kwargs: Unpack[UpdateGroupRequestGroupUpdateTypeDef]) -> "_Group":
        """
        Updates the name and/or the path of the specified IAM group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Group.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#groupupdate-method)
        """


_Group = Group


class LoginProfile(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.LoginProfile)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofile)
    """

    create_date: Awaitable[datetime]
    password_reset_required: Awaitable[bool]
    user_name: str
    meta: "IAMResourceMeta"  # type: ignore

    async def User(self) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofileuser-method)
        """

    async def create(
        self, **kwargs: Unpack[CreateLoginProfileRequestLoginProfileCreateTypeDef]
    ) -> "_LoginProfile":
        """
        Creates a password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.create)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofilecreate-method)
        """

    async def delete(self) -> None:
        """
        Deletes the password for the specified IAM user, For more information, see
        [Managing passwords for IAM
        users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_admin-change-user.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofiledelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofileget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_login_profile` to update the attributes of the
        LoginProfile
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofileload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_login_profile` to update the attributes of the
        LoginProfile
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofilereload-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateLoginProfileRequestLoginProfileUpdateTypeDef]
    ) -> None:
        """
        Changes the password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.LoginProfile.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#loginprofileupdate-method)
        """


_LoginProfile = LoginProfile


class Role(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Role)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#role)
    """

    path: Awaitable[str]
    role_name: Awaitable[str]
    role_id: Awaitable[str]
    arn: Awaitable[str]
    create_date: Awaitable[datetime]
    assume_role_policy_document: Awaitable[PolicyDocumentTypeDef]
    description: Awaitable[str]
    max_session_duration: Awaitable[int]
    permissions_boundary: Awaitable[AttachedPermissionsBoundaryTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    role_last_used: Awaitable[RoleLastUsedTypeDef]
    name: str
    attached_policies: RoleAttachedPoliciesCollection
    instance_profiles: RoleInstanceProfilesCollection
    policies: RolePoliciesCollection
    meta: "IAMResourceMeta"  # type: ignore

    async def AssumeRolePolicy(self) -> "_AssumeRolePolicy":
        """
        Creates a AssumeRolePolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.AssumeRolePolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roleassumerolepolicy-method)
        """

    async def Policy(self, name: str) -> "_RolePolicy":
        """
        Creates a RolePolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.Policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolepolicy-method)
        """

    async def attach_policy(
        self, **kwargs: Unpack[AttachRolePolicyRequestRoleAttachPolicyTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.attach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roleattach_policy-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roledelete-method)
        """

    async def detach_policy(
        self, **kwargs: Unpack[DetachRolePolicyRequestRoleDetachPolicyTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.detach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roledetach_policy-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roleget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_role` to update the attributes of the Role
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#roleload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_role` to update the attributes of the Role
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Role.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#rolereload-method)
        """


_Role = Role


class User(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.User)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#user)
    """

    path: Awaitable[str]
    user_name: Awaitable[str]
    user_id: Awaitable[str]
    arn: Awaitable[str]
    create_date: Awaitable[datetime]
    password_last_used: Awaitable[datetime]
    permissions_boundary: Awaitable[AttachedPermissionsBoundaryTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    name: str
    access_keys: UserAccessKeysCollection
    attached_policies: UserAttachedPoliciesCollection
    groups: UserGroupsCollection
    mfa_devices: UserMfaDevicesCollection
    policies: UserPoliciesCollection
    signing_certificates: UserSigningCertificatesCollection
    meta: "IAMResourceMeta"  # type: ignore

    async def AccessKey(self, id: str) -> "_AccessKey":
        """
        Creates a AccessKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.AccessKey)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#useraccesskey-method)
        """

    async def LoginProfile(self) -> "_LoginProfile":
        """
        Creates a LoginProfile resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.LoginProfile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userloginprofile-method)
        """

    async def MfaDevice(self, serial_number: str) -> "_MfaDevice":
        """
        Creates a MfaDevice resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.MfaDevice)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usermfadevice-method)
        """

    async def Policy(self, name: str) -> "_UserPolicy":
        """
        Creates a UserPolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.Policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userpolicy-method)
        """

    async def SigningCertificate(self, id: str) -> "_SigningCertificate":
        """
        Creates a SigningCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.SigningCertificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usersigningcertificate-method)
        """

    async def add_group(self, **kwargs: Unpack[AddUserToGroupRequestUserAddGroupTypeDef]) -> None:
        """
        Adds the specified user to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.add_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#useradd_group-method)
        """

    async def attach_policy(
        self, **kwargs: Unpack[AttachUserPolicyRequestUserAttachPolicyTypeDef]
    ) -> None:
        """
        Attaches the specified managed policy to the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.attach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userattach_policy-method)
        """

    async def create(self, **kwargs: Unpack[CreateUserRequestUserCreateTypeDef]) -> "_User":
        """
        Creates a new IAM user for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.create)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usercreate-method)
        """

    async def create_access_key_pair(self) -> "_AccessKeyPair":
        """
        Creates a new Amazon Web Services secret access key and corresponding Amazon
        Web Services access key ID for the specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.create_access_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usercreate_access_key_pair-method)
        """

    async def create_login_profile(
        self, **kwargs: Unpack[CreateLoginProfileRequestUserCreateLoginProfileTypeDef]
    ) -> "_LoginProfile":
        """
        Creates a password for the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.create_login_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usercreate_login_profile-method)
        """

    async def create_policy(
        self, **kwargs: Unpack[PutUserPolicyRequestUserCreatePolicyTypeDef]
    ) -> "_UserPolicy":
        """
        Adds or updates an inline policy document that is embedded in the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#usercreate_policy-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userdelete-method)
        """

    async def detach_policy(
        self, **kwargs: Unpack[DetachUserPolicyRequestUserDetachPolicyTypeDef]
    ) -> None:
        """
        Removes the specified managed policy from the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.detach_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userdetach_policy-method)
        """

    async def enable_mfa(
        self, **kwargs: Unpack[EnableMFADeviceRequestUserEnableMfaTypeDef]
    ) -> "_MfaDevice":
        """
        Enables the specified MFA device and associates it with the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.enable_mfa)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userenable_mfa-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user` to update the attributes of the User
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`IAM.Client.get_user` to update the attributes of the User
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userreload-method)
        """

    async def remove_group(
        self, **kwargs: Unpack[RemoveUserFromGroupRequestUserRemoveGroupTypeDef]
    ) -> None:
        """
        Removes the specified user from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.remove_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userremove_group-method)
        """

    async def update(self, **kwargs: Unpack[UpdateUserRequestUserUpdateTypeDef]) -> "_User":
        """
        Updates the name and/or the path of the specified IAM user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.User.update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#userupdate-method)
        """


_User = User


class IAMResourceMeta(ResourceMeta):
    client: IAMClient


class IAMServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/)
    """

    meta: "IAMResourceMeta"  # type: ignore
    groups: ServiceResourceGroupsCollection
    instance_profiles: ServiceResourceInstanceProfilesCollection
    policies: ServiceResourcePoliciesCollection
    roles: ServiceResourceRolesCollection
    saml_providers: ServiceResourceSamlProvidersCollection
    server_certificates: ServiceResourceServerCertificatesCollection
    users: ServiceResourceUsersCollection
    virtual_mfa_devices: ServiceResourceVirtualMfaDevicesCollection

    async def AccessKey(self, user_name: str, id: str) -> "_AccessKey":
        """
        Creates a AccessKey resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccessKey)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceaccesskey-method)
        """

    async def AccessKeyPair(self, user_name: str, id: str, secret: str) -> "_AccessKeyPair":
        """
        Creates a AccessKeyPair resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccessKeyPair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceaccesskeypair-method)
        """

    async def AccountPasswordPolicy(self) -> "_AccountPasswordPolicy":
        """
        Creates a AccountPasswordPolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccountPasswordPolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceaccountpasswordpolicy-method)
        """

    async def AccountSummary(self) -> "_AccountSummary":
        """
        Creates a AccountSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AccountSummary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceaccountsummary-method)
        """

    async def AssumeRolePolicy(self, role_name: str) -> "_AssumeRolePolicy":
        """
        Creates a AssumeRolePolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.AssumeRolePolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceassumerolepolicy-method)
        """

    async def CurrentUser(self) -> "_CurrentUser":
        """
        Creates a CurrentUser resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.CurrentUser)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecurrentuser-method)
        """

    async def Group(self, name: str) -> "_Group":
        """
        Creates a Group resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcegroup-method)
        """

    async def GroupPolicy(self, group_name: str, name: str) -> "_GroupPolicy":
        """
        Creates a GroupPolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.GroupPolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcegrouppolicy-method)
        """

    async def InstanceProfile(self, name: str) -> "_InstanceProfile":
        """
        Creates a InstanceProfile resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.InstanceProfile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceinstanceprofile-method)
        """

    async def LoginProfile(self, user_name: str) -> "_LoginProfile":
        """
        Creates a LoginProfile resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.LoginProfile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceloginprofile-method)
        """

    async def MfaDevice(self, user_name: str, serial_number: str) -> "_MfaDevice":
        """
        Creates a MfaDevice resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.MfaDevice)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcemfadevice-method)
        """

    async def Policy(self, arn: str) -> "_Policy":
        """
        Creates a Policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcepolicy-method)
        """

    async def PolicyVersion(self, arn: str, version_id: str) -> "_PolicyVersion":
        """
        Creates a PolicyVersion resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.PolicyVersion)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcepolicyversion-method)
        """

    async def Role(self, name: str) -> "_Role":
        """
        Creates a Role resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.Role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcerole-method)
        """

    async def RolePolicy(self, role_name: str, name: str) -> "_RolePolicy":
        """
        Creates a RolePolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.RolePolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcerolepolicy-method)
        """

    async def SamlProvider(self, arn: str) -> "_SamlProvider":
        """
        Creates a SamlProvider resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.SamlProvider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcesamlprovider-method)
        """

    async def ServerCertificate(self, name: str) -> "_ServerCertificate":
        """
        Creates a ServerCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.ServerCertificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceservercertificate-method)
        """

    async def SigningCertificate(self, user_name: str, id: str) -> "_SigningCertificate":
        """
        Creates a SigningCertificate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.SigningCertificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcesigningcertificate-method)
        """

    async def User(self, name: str) -> "_User":
        """
        Creates a User resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.User)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceuser-method)
        """

    async def UserPolicy(self, user_name: str, name: str) -> "_UserPolicy":
        """
        Creates a UserPolicy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.UserPolicy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceuserpolicy-method)
        """

    async def VirtualMfaDevice(self, serial_number: str) -> "_VirtualMfaDevice":
        """
        Creates a VirtualMfaDevice resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.VirtualMfaDevice)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcevirtualmfadevice-method)
        """

    async def change_password(
        self, **kwargs: Unpack[ChangePasswordRequestServiceResourceChangePasswordTypeDef]
    ) -> None:
        """
        Changes the password of the IAM user who is calling this operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.change_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcechange_password-method)
        """

    async def create_account_alias(
        self, **kwargs: Unpack[CreateAccountAliasRequestServiceResourceCreateAccountAliasTypeDef]
    ) -> None:
        """
        Creates an alias for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_account_alias)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_account_alias-method)
        """

    async def create_account_password_policy(
        self,
        **kwargs: Unpack[
            UpdateAccountPasswordPolicyRequestServiceResourceCreateAccountPasswordPolicyTypeDef
        ],
    ) -> "_AccountPasswordPolicy":
        """
        Updates the password policy settings for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_account_password_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_account_password_policy-method)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupRequestServiceResourceCreateGroupTypeDef]
    ) -> "_Group":
        """
        Creates a new group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_group-method)
        """

    async def create_instance_profile(
        self,
        **kwargs: Unpack[CreateInstanceProfileRequestServiceResourceCreateInstanceProfileTypeDef],
    ) -> "_InstanceProfile":
        """
        Creates a new instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_instance_profile-method)
        """

    async def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestServiceResourceCreatePolicyTypeDef]
    ) -> "_Policy":
        """
        Creates a new managed policy for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_policy-method)
        """

    async def create_role(
        self, **kwargs: Unpack[CreateRoleRequestServiceResourceCreateRoleTypeDef]
    ) -> "_Role":
        """
        Creates a new role for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_role-method)
        """

    async def create_saml_provider(
        self, **kwargs: Unpack[CreateSAMLProviderRequestServiceResourceCreateSamlProviderTypeDef]
    ) -> "_SamlProvider":
        """
        Creates an IAM resource that describes an identity provider (IdP) that supports
        SAML
        2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_saml_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_saml_provider-method)
        """

    async def create_server_certificate(
        self,
        **kwargs: Unpack[
            UploadServerCertificateRequestServiceResourceCreateServerCertificateTypeDef
        ],
    ) -> "_ServerCertificate":
        """
        Uploads a server certificate entity for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_server_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_server_certificate-method)
        """

    async def create_signing_certificate(
        self,
        **kwargs: Unpack[
            UploadSigningCertificateRequestServiceResourceCreateSigningCertificateTypeDef
        ],
    ) -> "_SigningCertificate":
        """
        Uploads an X.509 signing certificate and associates it with the specified IAM
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_signing_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_signing_certificate-method)
        """

    async def create_user(
        self, **kwargs: Unpack[CreateUserRequestServiceResourceCreateUserTypeDef]
    ) -> "_User":
        """
        Creates a new IAM user for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_user-method)
        """

    async def create_virtual_mfa_device(
        self,
        **kwargs: Unpack[CreateVirtualMFADeviceRequestServiceResourceCreateVirtualMfaDeviceTypeDef],
    ) -> "_VirtualMfaDevice":
        """
        Creates a new virtual MFA device for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.create_virtual_mfa_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourcecreate_virtual_mfa_device-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.ServiceResource.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/service_resource/#iamserviceresourceget_available_subresources-method)
        """
