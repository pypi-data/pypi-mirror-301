"""
Type annotations for ec2 service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ec2.service_resource import EC2ServiceResource
    import types_aiobotocore_ec2.service_resource as ec2_resources

    session = get_session()
    async with session.resource("ec2") as resource:
        resource: EC2ServiceResource

        my_classic_address: ec2_resources.ClassicAddress = resource.ClassicAddress(...)
        my_dhcp_options: ec2_resources.DhcpOptions = resource.DhcpOptions(...)
        my_image: ec2_resources.Image = resource.Image(...)
        my_instance: ec2_resources.Instance = resource.Instance(...)
        my_internet_gateway: ec2_resources.InternetGateway = resource.InternetGateway(...)
        my_key_pair: ec2_resources.KeyPair = resource.KeyPair(...)
        my_key_pair_info: ec2_resources.KeyPairInfo = resource.KeyPairInfo(...)
        my_network_acl: ec2_resources.NetworkAcl = resource.NetworkAcl(...)
        my_network_interface: ec2_resources.NetworkInterface = resource.NetworkInterface(...)
        my_network_interface_association: ec2_resources.NetworkInterfaceAssociation = resource.NetworkInterfaceAssociation(...)
        my_placement_group: ec2_resources.PlacementGroup = resource.PlacementGroup(...)
        my_route: ec2_resources.Route = resource.Route(...)
        my_route_table: ec2_resources.RouteTable = resource.RouteTable(...)
        my_route_table_association: ec2_resources.RouteTableAssociation = resource.RouteTableAssociation(...)
        my_security_group: ec2_resources.SecurityGroup = resource.SecurityGroup(...)
        my_snapshot: ec2_resources.Snapshot = resource.Snapshot(...)
        my_subnet: ec2_resources.Subnet = resource.Subnet(...)
        my_tag: ec2_resources.Tag = resource.Tag(...)
        my_volume: ec2_resources.Volume = resource.Volume(...)
        my_vpc: ec2_resources.Vpc = resource.Vpc(...)
        my_vpc_peering_connection: ec2_resources.VpcPeeringConnection = resource.VpcPeeringConnection(...)
        my_vpc_address: ec2_resources.VpcAddress = resource.VpcAddress(...)
```
"""

import sys
from datetime import datetime
from typing import AsyncIterator, Awaitable, List, NoReturn, Sequence

from .client import EC2Client
from .literals import (
    ArchitectureValuesType,
    BootModeValuesType,
    DeviceTypeType,
    DomainTypeType,
    HypervisorTypeType,
    ImageStateType,
    ImageTypeValuesType,
    InstanceBootModeValuesType,
    InstanceLifecycleTypeType,
    InstanceTypeType,
    KeyTypeType,
    NetworkInterfaceStatusType,
    NetworkInterfaceTypeType,
    PlacementGroupStateType,
    PlacementStrategyType,
    ResourceTypeType,
    RouteOriginType,
    RouteStateType,
    SnapshotStateType,
    SpreadLevelType,
    SSETypeType,
    StorageTierType,
    SubnetStateType,
    TenancyType,
    VirtualizationTypeType,
    VolumeStateType,
    VolumeTypeType,
    VpcStateType,
)
from .type_defs import (
    AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef,
    AcceptVpcPeeringConnectionResultTypeDef,
    AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef,
    AssignPrivateIpAddressesResultTypeDef,
    AssociateAddressRequestClassicAddressAssociateTypeDef,
    AssociateAddressRequestVpcAddressAssociateTypeDef,
    AssociateAddressResultTypeDef,
    AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef,
    AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef,
    AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef,
    AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef,
    AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef,
    AttachClassicLinkVpcResultTypeDef,
    AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef,
    AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef,
    AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef,
    AttachNetworkInterfaceResultTypeDef,
    AttachVolumeRequestInstanceAttachVolumeTypeDef,
    AttachVolumeRequestVolumeAttachToInstanceTypeDef,
    AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef,
    AuthorizeSecurityGroupEgressResultTypeDef,
    AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef,
    AuthorizeSecurityGroupIngressResultTypeDef,
    BlockDeviceMappingTypeDef,
    CapacityReservationSpecificationResponseTypeDef,
    ConnectionTrackingConfigurationTypeDef,
    CopySnapshotRequestSnapshotCopyTypeDef,
    CopySnapshotResultTypeDef,
    CpuOptionsTypeDef,
    CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef,
    CreateImageRequestInstanceCreateImageTypeDef,
    CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef,
    CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef,
    CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef,
    CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef,
    CreateNetworkAclRequestVpcCreateNetworkAclTypeDef,
    CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef,
    CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef,
    CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef,
    CreateRouteRequestRouteTableCreateRouteTypeDef,
    CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef,
    CreateRouteTableRequestVpcCreateRouteTableTypeDef,
    CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef,
    CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef,
    CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef,
    CreateSnapshotRequestVolumeCreateSnapshotTypeDef,
    CreateSubnetRequestServiceResourceCreateSubnetTypeDef,
    CreateSubnetRequestVpcCreateSubnetTypeDef,
    CreateTagsRequestServiceResourceCreateTagsTypeDef,
    CreateVolumeRequestServiceResourceCreateVolumeTypeDef,
    CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef,
    CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef,
    CreateVpcRequestServiceResourceCreateVpcTypeDef,
    DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef,
    DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef,
    DeleteKeyPairRequestKeyPairDeleteTypeDef,
    DeleteKeyPairRequestKeyPairInfoDeleteTypeDef,
    DeleteKeyPairResultTypeDef,
    DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef,
    DeleteNetworkAclRequestNetworkAclDeleteTypeDef,
    DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef,
    DeletePlacementGroupRequestPlacementGroupDeleteTypeDef,
    DeleteRouteRequestRouteDeleteTypeDef,
    DeleteRouteTableRequestRouteTableDeleteTypeDef,
    DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef,
    DeleteSnapshotRequestSnapshotDeleteTypeDef,
    DeleteSubnetRequestSubnetDeleteTypeDef,
    DeleteTagsRequestTagDeleteTypeDef,
    DeleteVolumeRequestVolumeDeleteTypeDef,
    DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef,
    DeleteVpcPeeringConnectionResultTypeDef,
    DeleteVpcRequestVpcDeleteTypeDef,
    DeregisterImageRequestImageDeregisterTypeDef,
    DescribeImageAttributeRequestImageDescribeAttributeTypeDef,
    DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef,
    DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef,
    DescribeNetworkInterfaceAttributeResultTypeDef,
    DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef,
    DescribeSnapshotAttributeResultTypeDef,
    DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef,
    DescribeVolumeAttributeResultTypeDef,
    DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef,
    DescribeVolumeStatusResultTypeDef,
    DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef,
    DescribeVpcAttributeResultTypeDef,
    DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef,
    DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef,
    DetachClassicLinkVpcResultTypeDef,
    DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef,
    DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef,
    DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef,
    DetachVolumeRequestInstanceDetachVolumeTypeDef,
    DetachVolumeRequestVolumeDetachFromInstanceTypeDef,
    DhcpConfigurationTypeDef,
    DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef,
    DisableVpcClassicLinkResultTypeDef,
    DisassociateAddressRequestClassicAddressDisassociateTypeDef,
    DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef,
    DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef,
    DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef,
    ElasticGpuAssociationTypeDef,
    ElasticInferenceAcceleratorAssociationTypeDef,
    EnableVolumeIORequestVolumeEnableIoTypeDef,
    EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef,
    EnableVpcClassicLinkResultTypeDef,
    EnclaveOptionsTypeDef,
    FilterTypeDef,
    GetConsoleOutputRequestInstanceConsoleOutputTypeDef,
    GetConsoleOutputResultTypeDef,
    GetPasswordDataRequestInstancePasswordDataTypeDef,
    GetPasswordDataResultTypeDef,
    GroupIdentifierTypeDef,
    HibernationOptionsTypeDef,
    IamInstanceProfileTypeDef,
    ImageAttributeTypeDef,
    ImportKeyPairRequestServiceResourceImportKeyPairTypeDef,
    InstanceAttributeTypeDef,
    InstanceBlockDeviceMappingTypeDef,
    InstanceCreateTagsRequestTypeDef,
    InstanceDeleteTagsRequestTypeDef,
    InstanceMaintenanceOptionsTypeDef,
    InstanceMetadataOptionsResponseTypeDef,
    InstanceNetworkInterfaceTypeDef,
    InstanceStateTypeDef,
    InternetGatewayAttachmentTypeDef,
    IpPermissionOutputTypeDef,
    Ipv4PrefixSpecificationTypeDef,
    Ipv6PrefixSpecificationTypeDef,
    LicenseConfigurationTypeDef,
    ModifyImageAttributeRequestImageModifyAttributeTypeDef,
    ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef,
    ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef,
    ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef,
    ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef,
    ModifyVpcAttributeRequestVpcModifyAttributeTypeDef,
    MonitoringTypeDef,
    MonitorInstancesRequestInstanceMonitorTypeDef,
    MonitorInstancesResultTypeDef,
    NetworkAclAssociationTypeDef,
    NetworkAclEntryTypeDef,
    NetworkInterfaceAssociationTypeDef,
    NetworkInterfaceAttachmentTypeDef,
    NetworkInterfaceIpv6AddressTypeDef,
    NetworkInterfacePrivateIpAddressTypeDef,
    PlacementTypeDef,
    PrivateDnsNameOptionsOnLaunchTypeDef,
    PrivateDnsNameOptionsResponseTypeDef,
    ProductCodeTypeDef,
    PropagatingVgwTypeDef,
    RebootInstancesRequestInstanceRebootTypeDef,
    RegisterImageRequestServiceResourceRegisterImageTypeDef,
    RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef,
    RejectVpcPeeringConnectionResultTypeDef,
    ReleaseAddressRequestClassicAddressReleaseTypeDef,
    ReleaseAddressRequestVpcAddressReleaseTypeDef,
    ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef,
    ReplaceNetworkAclAssociationResultTypeDef,
    ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef,
    ReplaceRouteRequestRouteReplaceTypeDef,
    ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef,
    ReportInstanceStatusRequestInstanceReportStatusTypeDef,
    ResetImageAttributeRequestImageResetAttributeTypeDef,
    ResetInstanceAttributeRequestInstanceResetAttributeTypeDef,
    ResetInstanceAttributeRequestInstanceResetKernelTypeDef,
    ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef,
    ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef,
    ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef,
    ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef,
    RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef,
    RevokeSecurityGroupEgressResultTypeDef,
    RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef,
    RevokeSecurityGroupIngressResultTypeDef,
    RouteTableAssociationStateTypeDef,
    RouteTableAssociationTypeDef,
    RouteTypeDef,
    RunInstancesRequestServiceResourceCreateInstancesTypeDef,
    RunInstancesRequestSubnetCreateInstancesTypeDef,
    StartInstancesRequestInstanceStartTypeDef,
    StartInstancesResultTypeDef,
    StateReasonTypeDef,
    StopInstancesRequestInstanceStopTypeDef,
    StopInstancesResultTypeDef,
    SubnetIpv6CidrBlockAssociationTypeDef,
    TagTypeDef,
    TerminateInstancesRequestInstanceTerminateTypeDef,
    TerminateInstancesResultTypeDef,
    UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef,
    UnmonitorInstancesRequestInstanceUnmonitorTypeDef,
    UnmonitorInstancesResultTypeDef,
    VolumeAttachmentResponseTypeDef,
    VolumeAttachmentTypeDef,
    VpcCidrBlockAssociationTypeDef,
    VpcCreateTagsRequestTypeDef,
    VpcIpv6CidrBlockAssociationTypeDef,
    VpcPeeringConnectionStateReasonTypeDef,
    VpcPeeringConnectionVpcInfoTypeDef,
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
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = (
    "EC2ServiceResource",
    "ClassicAddress",
    "DhcpOptions",
    "Image",
    "Instance",
    "InternetGateway",
    "KeyPair",
    "KeyPairInfo",
    "NetworkAcl",
    "NetworkInterface",
    "NetworkInterfaceAssociation",
    "PlacementGroup",
    "Route",
    "RouteTable",
    "RouteTableAssociation",
    "SecurityGroup",
    "Snapshot",
    "Subnet",
    "Tag",
    "Volume",
    "Vpc",
    "VpcPeeringConnection",
    "VpcAddress",
    "ServiceResourceClassicAddressesCollection",
    "ServiceResourceDhcpOptionsSetsCollection",
    "ServiceResourceImagesCollection",
    "ServiceResourceInstancesCollection",
    "ServiceResourceInternetGatewaysCollection",
    "ServiceResourceKeyPairsCollection",
    "ServiceResourceNetworkAclsCollection",
    "ServiceResourceNetworkInterfacesCollection",
    "ServiceResourcePlacementGroupsCollection",
    "ServiceResourceRouteTablesCollection",
    "ServiceResourceSecurityGroupsCollection",
    "ServiceResourceSnapshotsCollection",
    "ServiceResourceSubnetsCollection",
    "ServiceResourceVolumesCollection",
    "ServiceResourceVpcAddressesCollection",
    "ServiceResourceVpcPeeringConnectionsCollection",
    "ServiceResourceVpcsCollection",
    "InstanceVolumesCollection",
    "InstanceVpcAddressesCollection",
    "PlacementGroupInstancesCollection",
    "SubnetInstancesCollection",
    "SubnetNetworkInterfacesCollection",
    "VolumeSnapshotsCollection",
    "VpcAcceptedVpcPeeringConnectionsCollection",
    "VpcInstancesCollection",
    "VpcInternetGatewaysCollection",
    "VpcNetworkAclsCollection",
    "VpcNetworkInterfacesCollection",
    "VpcRequestedVpcPeeringConnectionsCollection",
    "VpcRouteTablesCollection",
    "VpcSecurityGroupsCollection",
    "VpcSubnetsCollection",
)


class ServiceResourceClassicAddressesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
    """

    def all(self) -> "ServiceResourceClassicAddressesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> "ServiceResourceClassicAddressesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def limit(self, count: int) -> "ServiceResourceClassicAddressesCollection":
        """
        Return at most this many ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceClassicAddressesCollection":
        """
        Fetch at most this many ClassicAddresss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def pages(self) -> AsyncIterator[List["ClassicAddress"]]:
        """
        A generator which yields pages of ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """

    def __aiter__(self) -> AsyncIterator["ClassicAddress"]:
        """
        A generator which yields ClassicAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.classic_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceclassicaddressescollection)
        """


class ServiceResourceDhcpOptionsSetsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
    """

    def all(self) -> "ServiceResourceDhcpOptionsSetsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        DhcpOptionsIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceDhcpOptionsSetsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def limit(self, count: int) -> "ServiceResourceDhcpOptionsSetsCollection":
        """
        Return at most this many DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceDhcpOptionsSetsCollection":
        """
        Fetch at most this many DhcpOptionss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def pages(self) -> AsyncIterator[List["DhcpOptions"]]:
        """
        A generator which yields pages of DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """

    def __aiter__(self) -> AsyncIterator["DhcpOptions"]:
        """
        A generator which yields DhcpOptionss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.dhcp_options_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcedhcpoptionssetscollection)
        """


class ServiceResourceImagesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
    """

    def all(self) -> "ServiceResourceImagesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        ExecutableUsers: Sequence[str] = ...,
        ImageIds: Sequence[str] = ...,
        Owners: Sequence[str] = ...,
        IncludeDeprecated: bool = ...,
        IncludeDisabled: bool = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceImagesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def limit(self, count: int) -> "ServiceResourceImagesCollection":
        """
        Return at most this many Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceImagesCollection":
        """
        Fetch at most this many Images per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def pages(self) -> AsyncIterator[List["Image"]]:
        """
        A generator which yields pages of Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """

    def __aiter__(self) -> AsyncIterator["Image"]:
        """
        A generator which yields Images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceimagescollection)
        """


class ServiceResourceInstancesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
    """

    def all(self) -> "ServiceResourceInstancesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "ServiceResourceInstancesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def limit(self, count: int) -> "ServiceResourceInstancesCollection":
        """
        Return at most this many Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceInstancesCollection":
        """
        Fetch at most this many Instances per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def pages(self) -> AsyncIterator[List["Instance"]]:
        """
        A generator which yields pages of Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """

    def __aiter__(self) -> AsyncIterator["Instance"]:
        """
        A generator which yields Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinstancescollection)
        """


class ServiceResourceInternetGatewaysCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
    """

    def all(self) -> "ServiceResourceInternetGatewaysCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        InternetGatewayIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceInternetGatewaysCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def limit(self, count: int) -> "ServiceResourceInternetGatewaysCollection":
        """
        Return at most this many InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceInternetGatewaysCollection":
        """
        Fetch at most this many InternetGateways per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def pages(self) -> AsyncIterator[List["InternetGateway"]]:
        """
        A generator which yields pages of InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """

    def __aiter__(self) -> AsyncIterator["InternetGateway"]:
        """
        A generator which yields InternetGateways.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.internet_gateways)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceinternetgatewayscollection)
        """


class ServiceResourceKeyPairsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
    """

    def all(self) -> "ServiceResourceKeyPairsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        KeyNames: Sequence[str] = ...,
        KeyPairIds: Sequence[str] = ...,
        IncludePublicKey: bool = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceKeyPairsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def limit(self, count: int) -> "ServiceResourceKeyPairsCollection":
        """
        Return at most this many KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceKeyPairsCollection":
        """
        Fetch at most this many KeyPairInfos per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def pages(self) -> AsyncIterator[List["KeyPairInfo"]]:
        """
        A generator which yields pages of KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """

    def __aiter__(self) -> AsyncIterator["KeyPairInfo"]:
        """
        A generator which yields KeyPairInfos.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.key_pairs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcekeypairscollection)
        """


class ServiceResourceNetworkAclsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
    """

    def all(self) -> "ServiceResourceNetworkAclsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkAclIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceNetworkAclsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def limit(self, count: int) -> "ServiceResourceNetworkAclsCollection":
        """
        Return at most this many NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceNetworkAclsCollection":
        """
        Fetch at most this many NetworkAcls per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def pages(self) -> AsyncIterator[List["NetworkAcl"]]:
        """
        A generator which yields pages of NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """

    def __aiter__(self) -> AsyncIterator["NetworkAcl"]:
        """
        A generator which yields NetworkAcls.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_acls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkaclscollection)
        """


class ServiceResourceNetworkInterfacesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
    """

    def all(self) -> "ServiceResourceNetworkInterfacesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceNetworkInterfacesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def limit(self, count: int) -> "ServiceResourceNetworkInterfacesCollection":
        """
        Return at most this many NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceNetworkInterfacesCollection":
        """
        Fetch at most this many NetworkInterfaces per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def pages(self) -> AsyncIterator[List["NetworkInterface"]]:
        """
        A generator which yields pages of NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """

    def __aiter__(self) -> AsyncIterator["NetworkInterface"]:
        """
        A generator which yields NetworkInterfaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.network_interfaces)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcenetworkinterfacescollection)
        """


class ServiceResourcePlacementGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
    """

    def all(self) -> "ServiceResourcePlacementGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        GroupIds: Sequence[str] = ...,
        DryRun: bool = ...,
        GroupNames: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourcePlacementGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def limit(self, count: int) -> "ServiceResourcePlacementGroupsCollection":
        """
        Return at most this many PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def page_size(self, count: int) -> "ServiceResourcePlacementGroupsCollection":
        """
        Fetch at most this many PlacementGroups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def pages(self) -> AsyncIterator[List["PlacementGroup"]]:
        """
        A generator which yields pages of PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """

    def __aiter__(self) -> AsyncIterator["PlacementGroup"]:
        """
        A generator which yields PlacementGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.placement_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceplacementgroupscollection)
        """


class ServiceResourceRouteTablesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
    """

    def all(self) -> "ServiceResourceRouteTablesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        RouteTableIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceRouteTablesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def limit(self, count: int) -> "ServiceResourceRouteTablesCollection":
        """
        Return at most this many RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceRouteTablesCollection":
        """
        Fetch at most this many RouteTables per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def pages(self) -> AsyncIterator[List["RouteTable"]]:
        """
        A generator which yields pages of RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """

    def __aiter__(self) -> AsyncIterator["RouteTable"]:
        """
        A generator which yields RouteTables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.route_tables)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourceroutetablescollection)
        """


class ServiceResourceSecurityGroupsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
    """

    def all(self) -> "ServiceResourceSecurityGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        GroupIds: Sequence[str] = ...,
        GroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceSecurityGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSecurityGroupsCollection":
        """
        Return at most this many SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSecurityGroupsCollection":
        """
        Fetch at most this many SecurityGroups per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def pages(self) -> AsyncIterator[List["SecurityGroup"]]:
        """
        A generator which yields pages of SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """

    def __aiter__(self) -> AsyncIterator["SecurityGroup"]:
        """
        A generator which yields SecurityGroups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesecuritygroupscollection)
        """


class ServiceResourceSnapshotsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
    """

    def all(self) -> "ServiceResourceSnapshotsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        OwnerIds: Sequence[str] = ...,
        RestorableByUserIds: Sequence[str] = ...,
        SnapshotIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceSnapshotsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSnapshotsCollection":
        """
        Return at most this many Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSnapshotsCollection":
        """
        Fetch at most this many Snapshots per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def pages(self) -> AsyncIterator[List["Snapshot"]]:
        """
        A generator which yields pages of Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """

    def __aiter__(self) -> AsyncIterator["Snapshot"]:
        """
        A generator which yields Snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesnapshotscollection)
        """


class ServiceResourceSubnetsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
    """

    def all(self) -> "ServiceResourceSubnetsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SubnetIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> "ServiceResourceSubnetsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSubnetsCollection":
        """
        Return at most this many Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSubnetsCollection":
        """
        Fetch at most this many Subnets per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def pages(self) -> AsyncIterator[List["Subnet"]]:
        """
        A generator which yields pages of Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """

    def __aiter__(self) -> AsyncIterator["Subnet"]:
        """
        A generator which yields Subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcesubnetscollection)
        """


class ServiceResourceVolumesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
    """

    def all(self) -> "ServiceResourceVolumesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "ServiceResourceVolumesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def limit(self, count: int) -> "ServiceResourceVolumesCollection":
        """
        Return at most this many Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVolumesCollection":
        """
        Fetch at most this many Volumes per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def pages(self) -> AsyncIterator[List["Volume"]]:
        """
        A generator which yields pages of Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """

    def __aiter__(self) -> AsyncIterator["Volume"]:
        """
        A generator which yields Volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevolumescollection)
        """


class ServiceResourceVpcAddressesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
    """

    def all(self) -> "ServiceResourceVpcAddressesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def filter(  # type: ignore
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> "ServiceResourceVpcAddressesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def limit(self, count: int) -> "ServiceResourceVpcAddressesCollection":
        """
        Return at most this many VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVpcAddressesCollection":
        """
        Fetch at most this many VpcAddresss per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def pages(self) -> AsyncIterator[List["VpcAddress"]]:
        """
        A generator which yields pages of VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """

    def __aiter__(self) -> AsyncIterator["VpcAddress"]:
        """
        A generator which yields VpcAddresss.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcaddressescollection)
        """


class ServiceResourceVpcPeeringConnectionsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
    """

    def all(self) -> "ServiceResourceVpcPeeringConnectionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "ServiceResourceVpcPeeringConnectionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def limit(self, count: int) -> "ServiceResourceVpcPeeringConnectionsCollection":
        """
        Return at most this many VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVpcPeeringConnectionsCollection":
        """
        Fetch at most this many VpcPeeringConnections per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def pages(self) -> AsyncIterator[List["VpcPeeringConnection"]]:
        """
        A generator which yields pages of VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """

    def __aiter__(self) -> AsyncIterator["VpcPeeringConnection"]:
        """
        A generator which yields VpcPeeringConnections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpc_peering_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcpeeringconnectionscollection)
        """


class ServiceResourceVpcsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
    """

    def all(self) -> "ServiceResourceVpcsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def filter(  # type: ignore
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        VpcIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> "ServiceResourceVpcsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def limit(self, count: int) -> "ServiceResourceVpcsCollection":
        """
        Return at most this many Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceVpcsCollection":
        """
        Fetch at most this many Vpcs per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def pages(self) -> AsyncIterator[List["Vpc"]]:
        """
        A generator which yields pages of Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """

    def __aiter__(self) -> AsyncIterator["Vpc"]:
        """
        A generator which yields Vpcs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#serviceresourcevpcscollection)
        """


class InstanceVolumesCollection(AIOResourceCollection):
    def all(self) -> "InstanceVolumesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "InstanceVolumesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "InstanceVolumesCollection":
        """
        Return at most this many Volumes.
        """

    def page_size(self, count: int) -> "InstanceVolumesCollection":
        """
        Fetch at most this many Volumes per service request.
        """

    def pages(self) -> AsyncIterator[List["Volume"]]:
        """
        A generator which yields pages of Volumes.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Volumes.
        """

    def __aiter__(self) -> AsyncIterator["Volume"]:
        """
        A generator which yields Volumes.
        """


class InstanceVpcAddressesCollection(AIOResourceCollection):
    def all(self) -> "InstanceVpcAddressesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        PublicIps: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        AllocationIds: Sequence[str] = ...,
    ) -> "InstanceVpcAddressesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "InstanceVpcAddressesCollection":
        """
        Return at most this many VpcAddresss.
        """

    def page_size(self, count: int) -> "InstanceVpcAddressesCollection":
        """
        Fetch at most this many VpcAddresss per service request.
        """

    def pages(self) -> AsyncIterator[List["VpcAddress"]]:
        """
        A generator which yields pages of VpcAddresss.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcAddresss.
        """

    def __aiter__(self) -> AsyncIterator["VpcAddress"]:
        """
        A generator which yields VpcAddresss.
        """


class PlacementGroupInstancesCollection(AIOResourceCollection):
    def all(self) -> "PlacementGroupInstancesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "PlacementGroupInstancesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    def limit(self, count: int) -> "PlacementGroupInstancesCollection":
        """
        Return at most this many Instances.
        """

    def page_size(self, count: int) -> "PlacementGroupInstancesCollection":
        """
        Fetch at most this many Instances per service request.
        """

    def pages(self) -> AsyncIterator[List["Instance"]]:
        """
        A generator which yields pages of Instances.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.
        """

    def __aiter__(self) -> AsyncIterator["Instance"]:
        """
        A generator which yields Instances.
        """


class SubnetInstancesCollection(AIOResourceCollection):
    def all(self) -> "SubnetInstancesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "SubnetInstancesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    def limit(self, count: int) -> "SubnetInstancesCollection":
        """
        Return at most this many Instances.
        """

    def page_size(self, count: int) -> "SubnetInstancesCollection":
        """
        Fetch at most this many Instances per service request.
        """

    def pages(self) -> AsyncIterator[List["Instance"]]:
        """
        A generator which yields pages of Instances.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.
        """

    def __aiter__(self) -> AsyncIterator["Instance"]:
        """
        A generator which yields Instances.
        """


class SubnetNetworkInterfacesCollection(AIOResourceCollection):
    def all(self) -> "SubnetNetworkInterfacesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "SubnetNetworkInterfacesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "SubnetNetworkInterfacesCollection":
        """
        Return at most this many NetworkInterfaces.
        """

    def page_size(self, count: int) -> "SubnetNetworkInterfacesCollection":
        """
        Fetch at most this many NetworkInterfaces per service request.
        """

    def pages(self) -> AsyncIterator[List["NetworkInterface"]]:
        """
        A generator which yields pages of NetworkInterfaces.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.
        """

    def __aiter__(self) -> AsyncIterator["NetworkInterface"]:
        """
        A generator which yields NetworkInterfaces.
        """


class VolumeSnapshotsCollection(AIOResourceCollection):
    def all(self) -> "VolumeSnapshotsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        OwnerIds: Sequence[str] = ...,
        RestorableByUserIds: Sequence[str] = ...,
        SnapshotIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VolumeSnapshotsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VolumeSnapshotsCollection":
        """
        Return at most this many Snapshots.
        """

    def page_size(self, count: int) -> "VolumeSnapshotsCollection":
        """
        Fetch at most this many Snapshots per service request.
        """

    def pages(self) -> AsyncIterator[List["Snapshot"]]:
        """
        A generator which yields pages of Snapshots.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Snapshots.
        """

    def __aiter__(self) -> AsyncIterator["Snapshot"]:
        """
        A generator which yields Snapshots.
        """


class VpcAcceptedVpcPeeringConnectionsCollection(AIOResourceCollection):
    def all(self) -> "VpcAcceptedVpcPeeringConnectionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcAcceptedVpcPeeringConnectionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcAcceptedVpcPeeringConnectionsCollection":
        """
        Return at most this many VpcPeeringConnections.
        """

    def page_size(self, count: int) -> "VpcAcceptedVpcPeeringConnectionsCollection":
        """
        Fetch at most this many VpcPeeringConnections per service request.
        """

    def pages(self) -> AsyncIterator[List["VpcPeeringConnection"]]:
        """
        A generator which yields pages of VpcPeeringConnections.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.
        """

    def __aiter__(self) -> AsyncIterator["VpcPeeringConnection"]:
        """
        A generator which yields VpcPeeringConnections.
        """


class VpcInstancesCollection(AIOResourceCollection):
    def all(self) -> "VpcInstancesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        InstanceIds: Sequence[str] = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> "VpcInstancesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    async def create_tags(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def monitor(self, *, DryRun: bool = ...) -> List[MonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def reboot(self, *, DryRun: bool = ...) -> None:
        """
        Batch method.
        """

    async def start(
        self, *, AdditionalInfo: str = ..., DryRun: bool = ...
    ) -> List[StartInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def stop(
        self, *, Hibernate: bool = ..., DryRun: bool = ..., Force: bool = ...
    ) -> List[StopInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def terminate(self, *, DryRun: bool = ...) -> List[TerminateInstancesResultTypeDef]:
        """
        Batch method.
        """

    async def unmonitor(self, *, DryRun: bool = ...) -> List[UnmonitorInstancesResultTypeDef]:
        """
        Batch method.
        """

    def limit(self, count: int) -> "VpcInstancesCollection":
        """
        Return at most this many Instances.
        """

    def page_size(self, count: int) -> "VpcInstancesCollection":
        """
        Fetch at most this many Instances per service request.
        """

    def pages(self) -> AsyncIterator[List["Instance"]]:
        """
        A generator which yields pages of Instances.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Instances.
        """

    def __aiter__(self) -> AsyncIterator["Instance"]:
        """
        A generator which yields Instances.
        """


class VpcInternetGatewaysCollection(AIOResourceCollection):
    def all(self) -> "VpcInternetGatewaysCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        InternetGatewayIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcInternetGatewaysCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcInternetGatewaysCollection":
        """
        Return at most this many InternetGateways.
        """

    def page_size(self, count: int) -> "VpcInternetGatewaysCollection":
        """
        Fetch at most this many InternetGateways per service request.
        """

    def pages(self) -> AsyncIterator[List["InternetGateway"]]:
        """
        A generator which yields pages of InternetGateways.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields InternetGateways.
        """

    def __aiter__(self) -> AsyncIterator["InternetGateway"]:
        """
        A generator which yields InternetGateways.
        """


class VpcNetworkAclsCollection(AIOResourceCollection):
    def all(self) -> "VpcNetworkAclsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkAclIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcNetworkAclsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcNetworkAclsCollection":
        """
        Return at most this many NetworkAcls.
        """

    def page_size(self, count: int) -> "VpcNetworkAclsCollection":
        """
        Fetch at most this many NetworkAcls per service request.
        """

    def pages(self) -> AsyncIterator[List["NetworkAcl"]]:
        """
        A generator which yields pages of NetworkAcls.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkAcls.
        """

    def __aiter__(self) -> AsyncIterator["NetworkAcl"]:
        """
        A generator which yields NetworkAcls.
        """


class VpcNetworkInterfacesCollection(AIOResourceCollection):
    def all(self) -> "VpcNetworkInterfacesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        NetworkInterfaceIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcNetworkInterfacesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcNetworkInterfacesCollection":
        """
        Return at most this many NetworkInterfaces.
        """

    def page_size(self, count: int) -> "VpcNetworkInterfacesCollection":
        """
        Fetch at most this many NetworkInterfaces per service request.
        """

    def pages(self) -> AsyncIterator[List["NetworkInterface"]]:
        """
        A generator which yields pages of NetworkInterfaces.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields NetworkInterfaces.
        """

    def __aiter__(self) -> AsyncIterator["NetworkInterface"]:
        """
        A generator which yields NetworkInterfaces.
        """


class VpcRequestedVpcPeeringConnectionsCollection(AIOResourceCollection):
    def all(self) -> "VpcRequestedVpcPeeringConnectionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        VpcPeeringConnectionIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcRequestedVpcPeeringConnectionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcRequestedVpcPeeringConnectionsCollection":
        """
        Return at most this many VpcPeeringConnections.
        """

    def page_size(self, count: int) -> "VpcRequestedVpcPeeringConnectionsCollection":
        """
        Fetch at most this many VpcPeeringConnections per service request.
        """

    def pages(self) -> AsyncIterator[List["VpcPeeringConnection"]]:
        """
        A generator which yields pages of VpcPeeringConnections.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields VpcPeeringConnections.
        """

    def __aiter__(self) -> AsyncIterator["VpcPeeringConnection"]:
        """
        A generator which yields VpcPeeringConnections.
        """


class VpcRouteTablesCollection(AIOResourceCollection):
    def all(self) -> "VpcRouteTablesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        RouteTableIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcRouteTablesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcRouteTablesCollection":
        """
        Return at most this many RouteTables.
        """

    def page_size(self, count: int) -> "VpcRouteTablesCollection":
        """
        Fetch at most this many RouteTables per service request.
        """

    def pages(self) -> AsyncIterator[List["RouteTable"]]:
        """
        A generator which yields pages of RouteTables.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields RouteTables.
        """

    def __aiter__(self) -> AsyncIterator["RouteTable"]:
        """
        A generator which yields RouteTables.
        """


class VpcSecurityGroupsCollection(AIOResourceCollection):
    def all(self) -> "VpcSecurityGroupsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        GroupIds: Sequence[str] = ...,
        GroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> "VpcSecurityGroupsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcSecurityGroupsCollection":
        """
        Return at most this many SecurityGroups.
        """

    def page_size(self, count: int) -> "VpcSecurityGroupsCollection":
        """
        Fetch at most this many SecurityGroups per service request.
        """

    def pages(self) -> AsyncIterator[List["SecurityGroup"]]:
        """
        A generator which yields pages of SecurityGroups.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields SecurityGroups.
        """

    def __aiter__(self) -> AsyncIterator["SecurityGroup"]:
        """
        A generator which yields SecurityGroups.
        """


class VpcSubnetsCollection(AIOResourceCollection):
    def all(self) -> "VpcSubnetsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self,
        *,
        Filters: Sequence[FilterTypeDef] = ...,
        SubnetIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
        DryRun: bool = ...,
    ) -> "VpcSubnetsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "VpcSubnetsCollection":
        """
        Return at most this many Subnets.
        """

    def page_size(self, count: int) -> "VpcSubnetsCollection":
        """
        Fetch at most this many Subnets per service request.
        """

    def pages(self) -> AsyncIterator[List["Subnet"]]:
        """
        A generator which yields pages of Subnets.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subnets.
        """

    def __aiter__(self) -> AsyncIterator["Subnet"]:
        """
        A generator which yields Subnets.
        """


class ClassicAddress(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.ClassicAddress)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddress)
    """

    allocation_id: Awaitable[str]
    association_id: Awaitable[str]
    domain: Awaitable[DomainTypeType]
    network_interface_id: Awaitable[str]
    network_interface_owner_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    public_ipv4_pool: Awaitable[str]
    network_border_group: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    customer_owned_ipv4_pool: Awaitable[str]
    carrier_ip: Awaitable[str]
    instance_id: Awaitable[str]
    public_ip: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def associate(
        self, **kwargs: Unpack[AssociateAddressRequestClassicAddressAssociateTypeDef]
    ) -> AssociateAddressResultTypeDef:
        """
        Associates an Elastic IP address, or carrier IP address (for instances that are
        in subnets in Wavelength Zones) with an instance or a network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.associate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressassociate-method)
        """

    async def disassociate(
        self, **kwargs: Unpack[DisassociateAddressRequestClassicAddressDisassociateTypeDef]
    ) -> None:
        """
        Disassociates an Elastic IP address from the instance or network interface it's
        associated
        with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.disassociate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressdisassociate-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_addresses` to update the attributes of the
        ClassicAddress
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressload-method)
        """

    async def release(
        self, **kwargs: Unpack[ReleaseAddressRequestClassicAddressReleaseTypeDef]
    ) -> None:
        """
        Releases the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.release)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressrelease-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_addresses` to update the attributes of the
        ClassicAddress
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ClassicAddress.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#classicaddressreload-method)
        """


_ClassicAddress = ClassicAddress


class DhcpOptions(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.DhcpOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptions)
    """

    owner_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    dhcp_options_id: Awaitable[str]
    dhcp_configurations: Awaitable[List[DhcpConfigurationTypeDef]]
    id: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def associate_with_vpc(
        self, **kwargs: Unpack[AssociateDhcpOptionsRequestDhcpOptionsAssociateWithVpcTypeDef]
    ) -> None:
        """
        Associates a set of DHCP options (that you've previously created) with the
        specified VPC, or associates no DHCP options with the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.associate_with_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsassociate_with_vpc-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteDhcpOptionsRequestDhcpOptionsDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_dhcp_options` to update the attributes of
        the DhcpOptions
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_dhcp_options` to update the attributes of
        the DhcpOptions
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionsreload-method)
        """


_DhcpOptions = DhcpOptions


class Image(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Image)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#image)
    """

    platform_details: Awaitable[str]
    usage_operation: Awaitable[str]
    block_device_mappings: Awaitable[List[BlockDeviceMappingTypeDef]]
    description: Awaitable[str]
    ena_support: Awaitable[bool]
    hypervisor: Awaitable[HypervisorTypeType]
    image_owner_alias: Awaitable[str]
    name: Awaitable[str]
    root_device_name: Awaitable[str]
    root_device_type: Awaitable[DeviceTypeType]
    sriov_net_support: Awaitable[str]
    state_reason: Awaitable[StateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    virtualization_type: Awaitable[VirtualizationTypeType]
    boot_mode: Awaitable[BootModeValuesType]
    tpm_support: Awaitable[Literal["v2.0"]]
    deprecation_time: Awaitable[str]
    imds_support: Awaitable[Literal["v2.0"]]
    source_instance_id: Awaitable[str]
    deregistration_protection: Awaitable[str]
    last_launched_time: Awaitable[str]
    image_id: Awaitable[str]
    image_location: Awaitable[str]
    state: Awaitable[ImageStateType]
    owner_id: Awaitable[str]
    creation_date: Awaitable[str]
    public: Awaitable[bool]
    product_codes: Awaitable[List[ProductCodeTypeDef]]
    architecture: Awaitable[ArchitectureValuesType]
    image_type: Awaitable[ImageTypeValuesType]
    kernel_id: Awaitable[str]
    ramdisk_id: Awaitable[str]
    platform: Awaitable[Literal["windows"]]
    id: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def deregister(
        self, **kwargs: Unpack[DeregisterImageRequestImageDeregisterTypeDef]
    ) -> None:
        """
        Deregisters the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.deregister)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagederegister-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeImageAttributeRequestImageDescribeAttributeTypeDef]
    ) -> ImageAttributeTypeDef:
        """
        Describes the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagedescribe_attribute-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imageget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_images` to update the attributes of the
        Image
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imageload-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyImageAttributeRequestImageModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagemodify_attribute-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_images` to update the attributes of the
        Image
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagereload-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetImageAttributeRequestImageResetAttributeTypeDef]
    ) -> None:
        """
        Resets an attribute of an AMI to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.reset_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagereset_attribute-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until this Image is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.wait_until_exists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagewait_until_exists-method)
        """


_Image = Image


class InternetGateway(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.InternetGateway)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgateway)
    """

    attachments: Awaitable[List[InternetGatewayAttachmentTypeDef]]
    internet_gateway_id: Awaitable[str]
    owner_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    id: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def attach_to_vpc(
        self, **kwargs: Unpack[AttachInternetGatewayRequestInternetGatewayAttachToVpcTypeDef]
    ) -> None:
        """
        Attaches an internet gateway or a virtual private gateway to a VPC, enabling
        connectivity between the internet and the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.attach_to_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayattach_to_vpc-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteInternetGatewayRequestInternetGatewayDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified internet gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaydelete-method)
        """

    async def detach_from_vpc(
        self, **kwargs: Unpack[DetachInternetGatewayRequestInternetGatewayDetachFromVpcTypeDef]
    ) -> None:
        """
        Detaches an internet gateway from a VPC, disabling connectivity between the
        internet and the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.detach_from_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaydetach_from_vpc-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_internet_gateways` to update the attributes
        of the InternetGateway
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_internet_gateways` to update the attributes
        of the InternetGateway
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewayreload-method)
        """


_InternetGateway = InternetGateway


class KeyPair(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.KeyPair)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypair)
    """

    key_pair_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    key_name: Awaitable[str]
    key_fingerprint: Awaitable[str]
    key_material: Awaitable[str]
    name: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(
        self, **kwargs: Unpack[DeleteKeyPairRequestKeyPairDeleteTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair, by removing the public key from Amazon EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPair.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPair.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairget_available_subresources-method)
        """


_KeyPair = KeyPair


class KeyPairInfo(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.KeyPairInfo)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfo)
    """

    key_pair_id: Awaitable[str]
    key_type: Awaitable[KeyTypeType]
    tags: Awaitable[List[TagTypeDef]]
    public_key: Awaitable[str]
    create_time: Awaitable[datetime]
    key_name: Awaitable[str]
    key_fingerprint: Awaitable[str]
    name: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(
        self, **kwargs: Unpack[DeleteKeyPairRequestKeyPairInfoDeleteTypeDef]
    ) -> DeleteKeyPairResultTypeDef:
        """
        Deletes the specified key pair, by removing the public key from Amazon EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPairInfo.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfodelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPairInfo.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfoget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_key_pairs` to update the attributes of the
        KeyPairInfo
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPairInfo.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinfoload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_key_pairs` to update the attributes of the
        KeyPairInfo
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.KeyPairInfo.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#keypairinforeload-method)
        """


_KeyPairInfo = KeyPairInfo


class NetworkAcl(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkAcl)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacl)
    """

    associations: Awaitable[List[NetworkAclAssociationTypeDef]]
    entries: Awaitable[List[NetworkAclEntryTypeDef]]
    is_default: Awaitable[bool]
    network_acl_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    owner_id: Awaitable[str]
    id: str
    vpc: "Vpc"
    meta: "EC2ResourceMeta"  # type: ignore

    async def create_entry(
        self, **kwargs: Unpack[CreateNetworkAclEntryRequestNetworkAclCreateEntryTypeDef]
    ) -> None:
        """
        Creates an entry (a rule) in a network ACL with the specified rule number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_entry-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteNetworkAclRequestNetworkAclDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacldelete-method)
        """

    async def delete_entry(
        self, **kwargs: Unpack[DeleteNetworkAclEntryRequestNetworkAclDeleteEntryTypeDef]
    ) -> None:
        """
        Deletes the specified ingress or egress entry (rule) from the specified network
        ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.delete_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkacldelete_entry-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_acls` to update the attributes of
        the NetworkAcl
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_acls` to update the attributes of
        the NetworkAcl
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreload-method)
        """

    async def replace_association(
        self,
        **kwargs: Unpack[ReplaceNetworkAclAssociationRequestNetworkAclReplaceAssociationTypeDef],
    ) -> ReplaceNetworkAclAssociationResultTypeDef:
        """
        Changes which network ACL a subnet is associated with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.replace_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreplace_association-method)
        """

    async def replace_entry(
        self, **kwargs: Unpack[ReplaceNetworkAclEntryRequestNetworkAclReplaceEntryTypeDef]
    ) -> None:
        """
        Replaces an entry (rule) in a network ACL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.replace_entry)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclreplace_entry-method)
        """


_NetworkAcl = NetworkAcl


class NetworkInterface(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkInterface)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterface)
    """

    association_attribute: Awaitable[NetworkInterfaceAssociationTypeDef]
    attachment: Awaitable[NetworkInterfaceAttachmentTypeDef]
    availability_zone: Awaitable[str]
    connection_tracking_configuration: Awaitable[ConnectionTrackingConfigurationTypeDef]
    description: Awaitable[str]
    groups: Awaitable[List[GroupIdentifierTypeDef]]
    interface_type: Awaitable[NetworkInterfaceTypeType]
    ipv6_addresses: Awaitable[List[NetworkInterfaceIpv6AddressTypeDef]]
    mac_address: Awaitable[str]
    network_interface_id: Awaitable[str]
    outpost_arn: Awaitable[str]
    owner_id: Awaitable[str]
    private_dns_name: Awaitable[str]
    private_ip_address: Awaitable[str]
    private_ip_addresses: Awaitable[List[NetworkInterfacePrivateIpAddressTypeDef]]
    ipv4_prefixes: Awaitable[List[Ipv4PrefixSpecificationTypeDef]]
    ipv6_prefixes: Awaitable[List[Ipv6PrefixSpecificationTypeDef]]
    requester_id: Awaitable[str]
    requester_managed: Awaitable[bool]
    source_dest_check: Awaitable[bool]
    status: Awaitable[NetworkInterfaceStatusType]
    subnet_id: Awaitable[str]
    tag_set: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    deny_all_igw_traffic: Awaitable[bool]
    ipv6_native: Awaitable[bool]
    ipv6_address: Awaitable[str]
    id: str
    association: "NetworkInterfaceAssociation"
    subnet: "Subnet"
    vpc: "Vpc"
    meta: "EC2ResourceMeta"  # type: ignore

    async def assign_private_ip_addresses(
        self,
        **kwargs: Unpack[
            AssignPrivateIpAddressesRequestNetworkInterfaceAssignPrivateIpAddressesTypeDef
        ],
    ) -> AssignPrivateIpAddressesResultTypeDef:
        """
        Assigns one or more secondary private IP addresses to the specified network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.assign_private_ip_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassign_private_ip_addresses-method)
        """

    async def attach(
        self, **kwargs: Unpack[AttachNetworkInterfaceRequestNetworkInterfaceAttachTypeDef]
    ) -> AttachNetworkInterfaceResultTypeDef:
        """
        Attaches a network interface to an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.attach)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceattach-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteNetworkInterfaceRequestNetworkInterfaceDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified network interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedelete-method)
        """

    async def describe_attribute(
        self,
        **kwargs: Unpack[
            DescribeNetworkInterfaceAttributeRequestNetworkInterfaceDescribeAttributeTypeDef
        ],
    ) -> DescribeNetworkInterfaceAttributeResultTypeDef:
        """
        Describes a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedescribe_attribute-method)
        """

    async def detach(
        self, **kwargs: Unpack[DetachNetworkInterfaceRequestNetworkInterfaceDetachTypeDef]
    ) -> None:
        """
        Detaches a network interface from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.detach)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacedetach-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_interfaces` to update the
        attributes of the NetworkInterface
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceload-method)
        """

    async def modify_attribute(
        self,
        **kwargs: Unpack[
            ModifyNetworkInterfaceAttributeRequestNetworkInterfaceModifyAttributeTypeDef
        ],
    ) -> None:
        """
        Modifies the specified network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacemodify_attribute-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_interfaces` to update the
        attributes of the NetworkInterface
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacereload-method)
        """

    async def reset_attribute(
        self,
        **kwargs: Unpack[
            ResetNetworkInterfaceAttributeRequestNetworkInterfaceResetAttributeTypeDef
        ],
    ) -> None:
        """
        Resets a network interface attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.reset_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacereset_attribute-method)
        """

    async def unassign_private_ip_addresses(
        self,
        **kwargs: Unpack[
            UnassignPrivateIpAddressesRequestNetworkInterfaceUnassignPrivateIpAddressesTypeDef
        ],
    ) -> None:
        """
        Unassigns one or more secondary private IP addresses, or IPv4 Prefix Delegation
        prefixes from a network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.unassign_private_ip_addresses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceunassign_private_ip_addresses-method)
        """


_NetworkInterface = NetworkInterface


class NetworkInterfaceAssociation(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkInterfaceAssociation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociation)
    """

    carrier_ip: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    ip_owner_id: Awaitable[str]
    public_dns_name: Awaitable[str]
    public_ip: Awaitable[str]
    id: str
    address: "VpcAddress"
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(
        self, **kwargs: Unpack[DisassociateAddressRequestNetworkInterfaceAssociationDeleteTypeDef]
    ) -> None:
        """
        Disassociates an Elastic IP address from the instance or network interface it's
        associated
        with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterfaceAssociation.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterfaceAssociation.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_interfaces` to update the
        attributes of the NetworkInterfaceAssociation
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterfaceAssociation.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_network_interfaces` to update the
        attributes of the NetworkInterfaceAssociation
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterfaceAssociation.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfaceassociationreload-method)
        """


_NetworkInterfaceAssociation = NetworkInterfaceAssociation


class PlacementGroup(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.PlacementGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroup)
    """

    group_name: Awaitable[str]
    state: Awaitable[PlacementGroupStateType]
    strategy: Awaitable[PlacementStrategyType]
    partition_count: Awaitable[int]
    group_id: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    group_arn: Awaitable[str]
    spread_level: Awaitable[SpreadLevelType]
    name: str
    instances: PlacementGroupInstancesCollection
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(
        self, **kwargs: Unpack[DeletePlacementGroupRequestPlacementGroupDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified placement group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.PlacementGroup.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.PlacementGroup.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_placement_groups` to update the attributes
        of the PlacementGroup
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.PlacementGroup.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_placement_groups` to update the attributes
        of the PlacementGroup
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.PlacementGroup.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#placementgroupreload-method)
        """


_PlacementGroup = PlacementGroup


class SecurityGroup(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.SecurityGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroup)
    """

    group_id: Awaitable[str]
    ip_permissions_egress: Awaitable[List[IpPermissionOutputTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    owner_id: Awaitable[str]
    group_name: Awaitable[str]
    description: Awaitable[str]
    ip_permissions: Awaitable[List[IpPermissionOutputTypeDef]]
    id: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def authorize_egress(
        self,
        **kwargs: Unpack[AuthorizeSecurityGroupEgressRequestSecurityGroupAuthorizeEgressTypeDef],
    ) -> AuthorizeSecurityGroupEgressResultTypeDef:
        """
        Adds the specified outbound (egress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.authorize_egress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupauthorize_egress-method)
        """

    async def authorize_ingress(
        self,
        **kwargs: Unpack[AuthorizeSecurityGroupIngressRequestSecurityGroupAuthorizeIngressTypeDef],
    ) -> AuthorizeSecurityGroupIngressResultTypeDef:
        """
        Adds the specified inbound (ingress) rules to a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.authorize_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupauthorize_ingress-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteSecurityGroupRequestSecurityGroupDeleteTypeDef]
    ) -> None:
        """
        Deletes a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_security_groups` to update the attributes
        of the SecurityGroup
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_security_groups` to update the attributes
        of the SecurityGroup
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupreload-method)
        """

    async def revoke_egress(
        self, **kwargs: Unpack[RevokeSecurityGroupEgressRequestSecurityGroupRevokeEgressTypeDef]
    ) -> RevokeSecurityGroupEgressResultTypeDef:
        """
        Removes the specified outbound (egress) rules from the specified security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.revoke_egress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygrouprevoke_egress-method)
        """

    async def revoke_ingress(
        self, **kwargs: Unpack[RevokeSecurityGroupIngressRequestSecurityGroupRevokeIngressTypeDef]
    ) -> RevokeSecurityGroupIngressResultTypeDef:
        """
        Removes the specified inbound (ingress) rules from a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.revoke_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygrouprevoke_ingress-method)
        """


_SecurityGroup = SecurityGroup


class Snapshot(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Snapshot)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshot)
    """

    owner_alias: Awaitable[str]
    outpost_arn: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    storage_tier: Awaitable[StorageTierType]
    restore_expiry_time: Awaitable[datetime]
    sse_type: Awaitable[SSETypeType]
    snapshot_id: Awaitable[str]
    volume_id: Awaitable[str]
    state: Awaitable[SnapshotStateType]
    state_message: Awaitable[str]
    start_time: Awaitable[datetime]
    progress: Awaitable[str]
    owner_id: Awaitable[str]
    description: Awaitable[str]
    volume_size: Awaitable[int]
    encrypted: Awaitable[bool]
    kms_key_id: Awaitable[str]
    data_encryption_key_id: Awaitable[str]
    id: str
    volume: "Volume"
    meta: "EC2ResourceMeta"  # type: ignore

    async def copy(
        self, **kwargs: Unpack[CopySnapshotRequestSnapshotCopyTypeDef]
    ) -> CopySnapshotResultTypeDef:
        """
        Copies a point-in-time snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcopy-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteSnapshotRequestSnapshotDeleteTypeDef]) -> None:
        """
        Deletes the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotdelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeSnapshotAttributeRequestSnapshotDescribeAttributeTypeDef]
    ) -> DescribeSnapshotAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotdescribe_attribute-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_snapshots` to update the attributes of the
        Snapshot
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotload-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifySnapshotAttributeRequestSnapshotModifyAttributeTypeDef]
    ) -> None:
        """
        Adds or removes permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotmodify_attribute-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_snapshots` to update the attributes of the
        Snapshot
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotreload-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetSnapshotAttributeRequestSnapshotResetAttributeTypeDef]
    ) -> None:
        """
        Resets permission settings for the specified snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.reset_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotreset_attribute-method)
        """

    async def wait_until_completed(self) -> None:
        """
        Waits until this Snapshot is completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.wait_until_completed)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotwait_until_completed-method)
        """


_Snapshot = Snapshot


class Tag(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Tag)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tag)
    """

    resource_type: Awaitable[ResourceTypeType]
    resource_id: str
    key: str
    value: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(self, **kwargs: Unpack[DeleteTagsRequestTagDeleteTypeDef]) -> None:
        """
        Deletes the specified set of tags from the specified set of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_tags` to update the attributes of the Tag
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_tags` to update the attributes of the Tag
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#tagreload-method)
        """


_Tag = Tag


class VpcPeeringConnection(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.VpcPeeringConnection)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnection)
    """

    accepter_vpc_info: Awaitable[VpcPeeringConnectionVpcInfoTypeDef]
    expiration_time: Awaitable[datetime]
    requester_vpc_info: Awaitable[VpcPeeringConnectionVpcInfoTypeDef]
    status: Awaitable[VpcPeeringConnectionStateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    vpc_peering_connection_id: Awaitable[str]
    id: str
    accepter_vpc: "Vpc"
    requester_vpc: "Vpc"
    meta: "EC2ResourceMeta"  # type: ignore

    async def accept(
        self, **kwargs: Unpack[AcceptVpcPeeringConnectionRequestVpcPeeringConnectionAcceptTypeDef]
    ) -> AcceptVpcPeeringConnectionResultTypeDef:
        """
        Accept a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.accept)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionaccept-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionRequestVpcPeeringConnectionDeleteTypeDef]
    ) -> DeleteVpcPeeringConnectionResultTypeDef:
        """
        Deletes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectiondelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_vpc_peering_connections` to update the
        attributes of the VpcPeeringConnection
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionload-method)
        """

    async def reject(
        self, **kwargs: Unpack[RejectVpcPeeringConnectionRequestVpcPeeringConnectionRejectTypeDef]
    ) -> RejectVpcPeeringConnectionResultTypeDef:
        """
        Rejects a VPC peering connection request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.reject)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionreject-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_vpc_peering_connections` to update the
        attributes of the VpcPeeringConnection
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionreload-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until this VpcPeeringConnection is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcPeeringConnection.wait_until_exists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcpeeringconnectionwait_until_exists-method)
        """


_VpcPeeringConnection = VpcPeeringConnection


class VpcAddress(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.VpcAddress)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddress)
    """

    association_id: Awaitable[str]
    domain: Awaitable[DomainTypeType]
    network_interface_id: Awaitable[str]
    network_interface_owner_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    public_ipv4_pool: Awaitable[str]
    network_border_group: Awaitable[str]
    customer_owned_ip: Awaitable[str]
    customer_owned_ipv4_pool: Awaitable[str]
    carrier_ip: Awaitable[str]
    instance_id: Awaitable[str]
    public_ip: Awaitable[str]
    allocation_id: str
    association: "NetworkInterfaceAssociation"
    meta: "EC2ResourceMeta"  # type: ignore

    async def associate(
        self, **kwargs: Unpack[AssociateAddressRequestVpcAddressAssociateTypeDef]
    ) -> AssociateAddressResultTypeDef:
        """
        Associates an Elastic IP address, or carrier IP address (for instances that are
        in subnets in Wavelength Zones) with an instance or a network
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcAddress.associate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressassociate-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcAddress.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_addresses` to update the attributes of the
        VpcAddress
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcAddress.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressload-method)
        """

    async def release(
        self, **kwargs: Unpack[ReleaseAddressRequestVpcAddressReleaseTypeDef]
    ) -> None:
        """
        Releases the specified Elastic IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcAddress.release)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressrelease-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_addresses` to update the attributes of the
        VpcAddress
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.VpcAddress.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcaddressreload-method)
        """


_VpcAddress = VpcAddress


class Instance(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Instance)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instance)
    """

    architecture: Awaitable[ArchitectureValuesType]
    block_device_mappings: Awaitable[List[InstanceBlockDeviceMappingTypeDef]]
    client_token: Awaitable[str]
    ebs_optimized: Awaitable[bool]
    ena_support: Awaitable[bool]
    hypervisor: Awaitable[HypervisorTypeType]
    iam_instance_profile: Awaitable[IamInstanceProfileTypeDef]
    instance_lifecycle: Awaitable[InstanceLifecycleTypeType]
    elastic_gpu_associations: Awaitable[List[ElasticGpuAssociationTypeDef]]
    elastic_inference_accelerator_associations: Awaitable[
        List[ElasticInferenceAcceleratorAssociationTypeDef]
    ]
    network_interfaces_attribute: Awaitable[List[InstanceNetworkInterfaceTypeDef]]
    outpost_arn: Awaitable[str]
    root_device_name: Awaitable[str]
    root_device_type: Awaitable[DeviceTypeType]
    security_groups: Awaitable[List[GroupIdentifierTypeDef]]
    source_dest_check: Awaitable[bool]
    spot_instance_request_id: Awaitable[str]
    sriov_net_support: Awaitable[str]
    state_reason: Awaitable[StateReasonTypeDef]
    tags: Awaitable[List[TagTypeDef]]
    virtualization_type: Awaitable[VirtualizationTypeType]
    cpu_options: Awaitable[CpuOptionsTypeDef]
    capacity_reservation_id: Awaitable[str]
    capacity_reservation_specification: Awaitable[CapacityReservationSpecificationResponseTypeDef]
    hibernation_options: Awaitable[HibernationOptionsTypeDef]
    licenses: Awaitable[List[LicenseConfigurationTypeDef]]
    metadata_options: Awaitable[InstanceMetadataOptionsResponseTypeDef]
    enclave_options: Awaitable[EnclaveOptionsTypeDef]
    boot_mode: Awaitable[BootModeValuesType]
    platform_details: Awaitable[str]
    usage_operation: Awaitable[str]
    usage_operation_update_time: Awaitable[datetime]
    private_dns_name_options: Awaitable[PrivateDnsNameOptionsResponseTypeDef]
    ipv6_address: Awaitable[str]
    tpm_support: Awaitable[str]
    maintenance_options: Awaitable[InstanceMaintenanceOptionsTypeDef]
    current_instance_boot_mode: Awaitable[InstanceBootModeValuesType]
    instance_id: Awaitable[str]
    image_id: Awaitable[str]
    state: Awaitable[InstanceStateTypeDef]
    private_dns_name: Awaitable[str]
    public_dns_name: Awaitable[str]
    state_transition_reason: Awaitable[str]
    key_name: Awaitable[str]
    ami_launch_index: Awaitable[int]
    product_codes: Awaitable[List[ProductCodeTypeDef]]
    instance_type: Awaitable[InstanceTypeType]
    launch_time: Awaitable[datetime]
    placement: Awaitable[PlacementTypeDef]
    kernel_id: Awaitable[str]
    ramdisk_id: Awaitable[str]
    platform: Awaitable[Literal["windows"]]
    monitoring: Awaitable[MonitoringTypeDef]
    subnet_id: Awaitable[str]
    vpc_id: Awaitable[str]
    private_ip_address: Awaitable[str]
    public_ip_address: Awaitable[str]
    id: str
    classic_address: "ClassicAddress"
    image: "Image"
    key_pair: "KeyPairInfo"
    network_interfaces: List["NetworkInterface"]
    placement_group: "PlacementGroup"
    subnet: "Subnet"
    vpc: "Vpc"
    volumes: InstanceVolumesCollection
    vpc_addresses: InstanceVpcAddressesCollection
    meta: "EC2ResourceMeta"  # type: ignore

    async def attach_classic_link_vpc(
        self, **kwargs: Unpack[AttachClassicLinkVpcRequestInstanceAttachClassicLinkVpcTypeDef]
    ) -> AttachClassicLinkVpcResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.attach_classic_link_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceattach_classic_link_vpc-method)
        """

    async def attach_volume(
        self, **kwargs: Unpack[AttachVolumeRequestInstanceAttachVolumeTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Attaches an EBS volume to a running or stopped instance and exposes it to the
        instance with the specified device
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.attach_volume)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceattach_volume-method)
        """

    async def console_output(
        self, **kwargs: Unpack[GetConsoleOutputRequestInstanceConsoleOutputTypeDef]
    ) -> GetConsoleOutputResultTypeDef:
        """
        Gets the console output for the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.console_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceconsole_output-method)
        """

    async def create_image(
        self, **kwargs: Unpack[CreateImageRequestInstanceCreateImageTypeDef]
    ) -> "_Image":
        """
        Creates an Amazon EBS-backed AMI from an Amazon EBS-backed instance that is
        either running or
        stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.create_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancecreate_image-method)
        """

    async def create_tags(self, **kwargs: Unpack[InstanceCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancecreate_tags-method)
        """

    async def delete_tags(self, **kwargs: Unpack[InstanceDeleteTagsRequestTypeDef]) -> None:
        """
        Deletes the specified set of tags from the specified set of resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedelete_tags-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeInstanceAttributeRequestInstanceDescribeAttributeTypeDef]
    ) -> InstanceAttributeTypeDef:
        """
        Describes the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedescribe_attribute-method)
        """

    async def detach_classic_link_vpc(
        self, **kwargs: Unpack[DetachClassicLinkVpcRequestInstanceDetachClassicLinkVpcTypeDef]
    ) -> DetachClassicLinkVpcResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.detach_classic_link_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedetach_classic_link_vpc-method)
        """

    async def detach_volume(
        self, **kwargs: Unpack[DetachVolumeRequestInstanceDetachVolumeTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Detaches an EBS volume from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.detach_volume)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancedetach_volume-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_instances` to update the attributes of the
        Instance
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceload-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyInstanceAttributeRequestInstanceModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancemodify_attribute-method)
        """

    async def monitor(
        self, **kwargs: Unpack[MonitorInstancesRequestInstanceMonitorTypeDef]
    ) -> MonitorInstancesResultTypeDef:
        """
        Enables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancemonitor-method)
        """

    async def password_data(
        self, **kwargs: Unpack[GetPasswordDataRequestInstancePasswordDataTypeDef]
    ) -> GetPasswordDataResultTypeDef:
        """
        Retrieves the encrypted administrator password for a running Windows instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.password_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancepassword_data-method)
        """

    async def reboot(self, **kwargs: Unpack[RebootInstancesRequestInstanceRebootTypeDef]) -> None:
        """
        Requests a reboot of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reboot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereboot-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_instances` to update the attributes of the
        Instance
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereload-method)
        """

    async def report_status(
        self, **kwargs: Unpack[ReportInstanceStatusRequestInstanceReportStatusTypeDef]
    ) -> None:
        """
        Submits feedback about the status of an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.report_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereport_status-method)
        """

    async def reset_attribute(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetAttributeTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reset_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_attribute-method)
        """

    async def reset_kernel(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetKernelTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reset_kernel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_kernel-method)
        """

    async def reset_ramdisk(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetRamdiskTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reset_ramdisk)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_ramdisk-method)
        """

    async def reset_source_dest_check(
        self, **kwargs: Unpack[ResetInstanceAttributeRequestInstanceResetSourceDestCheckTypeDef]
    ) -> None:
        """
        Resets an attribute of an instance to its default value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reset_source_dest_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancereset_source_dest_check-method)
        """

    async def start(
        self, **kwargs: Unpack[StartInstancesRequestInstanceStartTypeDef]
    ) -> StartInstancesResultTypeDef:
        """
        Starts an Amazon EBS-backed instance that you've previously stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.start)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancestart-method)
        """

    async def stop(
        self, **kwargs: Unpack[StopInstancesRequestInstanceStopTypeDef]
    ) -> StopInstancesResultTypeDef:
        """
        Stops an Amazon EBS-backed instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.stop)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancestop-method)
        """

    async def terminate(
        self, **kwargs: Unpack[TerminateInstancesRequestInstanceTerminateTypeDef]
    ) -> TerminateInstancesResultTypeDef:
        """
        Shuts down the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.terminate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceterminate-method)
        """

    async def unmonitor(
        self, **kwargs: Unpack[UnmonitorInstancesRequestInstanceUnmonitorTypeDef]
    ) -> UnmonitorInstancesResultTypeDef:
        """
        Disables detailed monitoring for a running instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.unmonitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instanceunmonitor-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until this Instance is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_exists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_exists-method)
        """

    async def wait_until_running(self) -> None:
        """
        Waits until this Instance is running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_running)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_running-method)
        """

    async def wait_until_stopped(self) -> None:
        """
        Waits until this Instance is stopped.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_stopped)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_stopped-method)
        """

    async def wait_until_terminated(self) -> None:
        """
        Waits until this Instance is terminated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_terminated)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#instancewait_until_terminated-method)
        """


_Instance = Instance


class Route(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Route)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#route)
    """

    destination_ipv6_cidr_block: Awaitable[str]
    destination_prefix_list_id: Awaitable[str]
    egress_only_internet_gateway_id: Awaitable[str]
    gateway_id: Awaitable[str]
    instance_id: Awaitable[str]
    instance_owner_id: Awaitable[str]
    nat_gateway_id: Awaitable[str]
    transit_gateway_id: Awaitable[str]
    local_gateway_id: Awaitable[str]
    carrier_gateway_id: Awaitable[str]
    network_interface_id: Awaitable[str]
    origin: Awaitable[RouteOriginType]
    state: Awaitable[RouteStateType]
    vpc_peering_connection_id: Awaitable[str]
    core_network_arn: Awaitable[str]
    route_table_id: str
    destination_cidr_block: str
    meta: "EC2ResourceMeta"  # type: ignore

    async def RouteTable(self) -> "_RouteTable":
        """
        Creates a RouteTable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Route.RouteTable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routeroutetable-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteRouteRequestRouteDeleteTypeDef]) -> None:
        """
        Deletes the specified route from the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Route.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routedelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Route.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routeget_available_subresources-method)
        """

    async def replace(self, **kwargs: Unpack[ReplaceRouteRequestRouteReplaceTypeDef]) -> None:
        """
        Replaces an existing route within a route table in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Route.replace)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routereplace-method)
        """


_Route = Route


class RouteTableAssociation(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.RouteTableAssociation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociation)
    """

    main: Awaitable[bool]
    route_table_association_id: Awaitable[str]
    route_table_id: Awaitable[str]
    subnet_id: Awaitable[str]
    gateway_id: Awaitable[str]
    association_state: Awaitable[RouteTableAssociationStateTypeDef]
    id: str
    route_table: "RouteTable"
    subnet: "Subnet"
    meta: "EC2ResourceMeta"  # type: ignore

    async def delete(
        self, **kwargs: Unpack[DisassociateRouteTableRequestRouteTableAssociationDeleteTypeDef]
    ) -> None:
        """
        Disassociates a subnet or gateway from a route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTableAssociation.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTableAssociation.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationget_available_subresources-method)
        """

    async def replace_subnet(
        self,
        **kwargs: Unpack[
            ReplaceRouteTableAssociationRequestRouteTableAssociationReplaceSubnetTypeDef
        ],
    ) -> "_RouteTableAssociation":
        """
        Changes the route table associated with a given subnet, internet gateway, or
        virtual private gateway in a
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTableAssociation.replace_subnet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociationreplace_subnet-method)
        """


_RouteTableAssociation = RouteTableAssociation


class Volume(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Volume)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volume)
    """

    outpost_arn: Awaitable[str]
    iops: Awaitable[int]
    tags: Awaitable[List[TagTypeDef]]
    volume_type: Awaitable[VolumeTypeType]
    fast_restored: Awaitable[bool]
    multi_attach_enabled: Awaitable[bool]
    throughput: Awaitable[int]
    sse_type: Awaitable[SSETypeType]
    volume_id: Awaitable[str]
    size: Awaitable[int]
    snapshot_id: Awaitable[str]
    availability_zone: Awaitable[str]
    state: Awaitable[VolumeStateType]
    create_time: Awaitable[datetime]
    attachments: Awaitable[List[VolumeAttachmentTypeDef]]
    encrypted: Awaitable[bool]
    kms_key_id: Awaitable[str]
    id: str
    snapshots: VolumeSnapshotsCollection
    meta: "EC2ResourceMeta"  # type: ignore

    async def attach_to_instance(
        self, **kwargs: Unpack[AttachVolumeRequestVolumeAttachToInstanceTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Attaches an EBS volume to a running or stopped instance and exposes it to the
        instance with the specified device
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.attach_to_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeattach_to_instance-method)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestVolumeCreateSnapshotTypeDef]
    ) -> "_Snapshot":
        """
        Creates a snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_snapshot-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteVolumeRequestVolumeDeleteTypeDef]) -> None:
        """
        Deletes the specified EBS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeVolumeAttributeRequestVolumeDescribeAttributeTypeDef]
    ) -> DescribeVolumeAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedescribe_attribute-method)
        """

    async def describe_status(
        self, **kwargs: Unpack[DescribeVolumeStatusRequestVolumeDescribeStatusTypeDef]
    ) -> DescribeVolumeStatusResultTypeDef:
        """
        Describes the status of the specified volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.describe_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedescribe_status-method)
        """

    async def detach_from_instance(
        self, **kwargs: Unpack[DetachVolumeRequestVolumeDetachFromInstanceTypeDef]
    ) -> VolumeAttachmentResponseTypeDef:
        """
        Detaches an EBS volume from an instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.detach_from_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumedetach_from_instance-method)
        """

    async def enable_io(self, **kwargs: Unpack[EnableVolumeIORequestVolumeEnableIoTypeDef]) -> None:
        """
        Enables I/O operations for a volume that had I/O operations disabled because
        the data on the volume was potentially
        inconsistent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.enable_io)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeenable_io-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_volumes` to update the attributes of the
        Volume
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumeload-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyVolumeAttributeRequestVolumeModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies a volume attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumemodify_attribute-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_volumes` to update the attributes of the
        Volume
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumereload-method)
        """


_Volume = Volume


class RouteTable(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.RouteTable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetable)
    """

    associations_attribute: Awaitable[List[RouteTableAssociationTypeDef]]
    propagating_vgws: Awaitable[List[PropagatingVgwTypeDef]]
    route_table_id: Awaitable[str]
    routes_attribute: Awaitable[List[RouteTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    owner_id: Awaitable[str]
    id: str
    associations: List["RouteTableAssociation"]
    routes: List["Route"]
    vpc: "Vpc"
    meta: "EC2ResourceMeta"  # type: ignore

    async def associate_with_subnet(
        self, **kwargs: Unpack[AssociateRouteTableRequestRouteTableAssociateWithSubnetTypeDef]
    ) -> "_RouteTableAssociation":
        """
        Associates a subnet in your VPC or an internet gateway or virtual private
        gateway attached to your VPC with a route table in your
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.associate_with_subnet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableassociate_with_subnet-method)
        """

    async def create_route(
        self, **kwargs: Unpack[CreateRouteRequestRouteTableCreateRouteTypeDef]
    ) -> "_Route":
        """
        Creates a route in a route table within a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_route-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(
        self, **kwargs: Unpack[DeleteRouteTableRequestRouteTableDeleteTypeDef]
    ) -> None:
        """
        Deletes the specified route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetabledelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_route_tables` to update the attributes of
        the RouteTable
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetableload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_route_tables` to update the attributes of
        the RouteTable
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablereload-method)
        """


_RouteTable = RouteTable


class Subnet(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Subnet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnet)
    """

    availability_zone_id: Awaitable[str]
    enable_lni_at_device_index: Awaitable[int]
    map_customer_owned_ip_on_launch: Awaitable[bool]
    customer_owned_ipv4_pool: Awaitable[str]
    owner_id: Awaitable[str]
    assign_ipv6_address_on_creation: Awaitable[bool]
    ipv6_cidr_block_association_set: Awaitable[List[SubnetIpv6CidrBlockAssociationTypeDef]]
    tags: Awaitable[List[TagTypeDef]]
    subnet_arn: Awaitable[str]
    outpost_arn: Awaitable[str]
    enable_dns64: Awaitable[bool]
    ipv6_native: Awaitable[bool]
    private_dns_name_options_on_launch: Awaitable[PrivateDnsNameOptionsOnLaunchTypeDef]
    subnet_id: Awaitable[str]
    state: Awaitable[SubnetStateType]
    vpc_id: Awaitable[str]
    cidr_block: Awaitable[str]
    available_ip_address_count: Awaitable[int]
    availability_zone: Awaitable[str]
    default_for_az: Awaitable[bool]
    map_public_ip_on_launch: Awaitable[bool]
    id: str
    vpc: "Vpc"
    instances: SubnetInstancesCollection
    network_interfaces: SubnetNetworkInterfacesCollection
    meta: "EC2ResourceMeta"  # type: ignore

    async def create_instances(
        self, **kwargs: Unpack[RunInstancesRequestSubnetCreateInstancesTypeDef]
    ) -> List["_Instance"]:
        """
        Launches the specified number of instances using an AMI for which you have
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_instances-method)
        """

    async def create_network_interface(
        self, **kwargs: Unpack[CreateNetworkInterfaceRequestSubnetCreateNetworkInterfaceTypeDef]
    ) -> "_NetworkInterface":
        """
        Creates a network interface in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_network_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_network_interface-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteSubnetRequestSubnetDeleteTypeDef]) -> None:
        """
        Deletes the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_subnets` to update the attributes of the
        Subnet
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_subnets` to update the attributes of the
        Subnet
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetreload-method)
        """


_Subnet = Subnet


class Vpc(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Vpc)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpc)
    """

    owner_id: Awaitable[str]
    instance_tenancy: Awaitable[TenancyType]
    ipv6_cidr_block_association_set: Awaitable[List[VpcIpv6CidrBlockAssociationTypeDef]]
    cidr_block_association_set: Awaitable[List[VpcCidrBlockAssociationTypeDef]]
    is_default: Awaitable[bool]
    tags: Awaitable[List[TagTypeDef]]
    vpc_id: Awaitable[str]
    state: Awaitable[VpcStateType]
    cidr_block: Awaitable[str]
    dhcp_options_id: Awaitable[str]
    id: str
    dhcp_options: "DhcpOptions"
    accepted_vpc_peering_connections: VpcAcceptedVpcPeeringConnectionsCollection
    instances: VpcInstancesCollection
    internet_gateways: VpcInternetGatewaysCollection
    network_acls: VpcNetworkAclsCollection
    network_interfaces: VpcNetworkInterfacesCollection
    requested_vpc_peering_connections: VpcRequestedVpcPeeringConnectionsCollection
    route_tables: VpcRouteTablesCollection
    security_groups: VpcSecurityGroupsCollection
    subnets: VpcSubnetsCollection
    meta: "EC2ResourceMeta"  # type: ignore

    async def associate_dhcp_options(
        self, **kwargs: Unpack[AssociateDhcpOptionsRequestVpcAssociateDhcpOptionsTypeDef]
    ) -> None:
        """
        Associates a set of DHCP options (that you've previously created) with the
        specified VPC, or associates no DHCP options with the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.associate_dhcp_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcassociate_dhcp_options-method)
        """

    async def attach_classic_link_instance(
        self, **kwargs: Unpack[AttachClassicLinkVpcRequestVpcAttachClassicLinkInstanceTypeDef]
    ) -> AttachClassicLinkVpcResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.attach_classic_link_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcattach_classic_link_instance-method)
        """

    async def attach_internet_gateway(
        self, **kwargs: Unpack[AttachInternetGatewayRequestVpcAttachInternetGatewayTypeDef]
    ) -> None:
        """
        Attaches an internet gateway or a virtual private gateway to a VPC, enabling
        connectivity between the internet and the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.attach_internet_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcattach_internet_gateway-method)
        """

    async def create_network_acl(
        self, **kwargs: Unpack[CreateNetworkAclRequestVpcCreateNetworkAclTypeDef]
    ) -> "_NetworkAcl":
        """
        Creates a network ACL in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_network_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_network_acl-method)
        """

    async def create_route_table(
        self, **kwargs: Unpack[CreateRouteTableRequestVpcCreateRouteTableTypeDef]
    ) -> "_RouteTable":
        """
        Creates a route table for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_route_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_route_table-method)
        """

    async def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestVpcCreateSecurityGroupTypeDef]
    ) -> "_SecurityGroup":
        """
        Creates a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_security_group-method)
        """

    async def create_subnet(
        self, **kwargs: Unpack[CreateSubnetRequestVpcCreateSubnetTypeDef]
    ) -> "_Subnet":
        """
        Creates a subnet in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_subnet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_subnet-method)
        """

    async def create_tags(self, **kwargs: Unpack[VpcCreateTagsRequestTypeDef]) -> None:
        """
        Adds or overwrites only the specified tags for the specified Amazon EC2
        resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.DhcpOptions.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#dhcpoptionscreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Image.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#imagecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.InternetGateway.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#internetgatewaycreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkAcl.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkaclcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.NetworkInterface.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#networkinterfacecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.RouteTable.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#routetablecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#securitygroupcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Snapshot.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#snapshotcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Subnet.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#subnetcreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Volume.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#volumecreate_tags-method)

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpccreate_tags-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteVpcRequestVpcDeleteTypeDef]) -> None:
        """
        Deletes the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdelete-method)
        """

    async def describe_attribute(
        self, **kwargs: Unpack[DescribeVpcAttributeRequestVpcDescribeAttributeTypeDef]
    ) -> DescribeVpcAttributeResultTypeDef:
        """
        Describes the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.describe_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdescribe_attribute-method)
        """

    async def detach_classic_link_instance(
        self, **kwargs: Unpack[DetachClassicLinkVpcRequestVpcDetachClassicLinkInstanceTypeDef]
    ) -> DetachClassicLinkVpcResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.detach_classic_link_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdetach_classic_link_instance-method)
        """

    async def detach_internet_gateway(
        self, **kwargs: Unpack[DetachInternetGatewayRequestVpcDetachInternetGatewayTypeDef]
    ) -> None:
        """
        Detaches an internet gateway from a VPC, disabling connectivity between the
        internet and the
        VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.detach_internet_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdetach_internet_gateway-method)
        """

    async def disable_classic_link(
        self, **kwargs: Unpack[DisableVpcClassicLinkRequestVpcDisableClassicLinkTypeDef]
    ) -> DisableVpcClassicLinkResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.disable_classic_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcdisable_classic_link-method)
        """

    async def enable_classic_link(
        self, **kwargs: Unpack[EnableVpcClassicLinkRequestVpcEnableClassicLinkTypeDef]
    ) -> EnableVpcClassicLinkResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.enable_classic_link)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcenable_classic_link-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_vpcs` to update the attributes of the Vpc
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcload-method)
        """

    async def modify_attribute(
        self, **kwargs: Unpack[ModifyVpcAttributeRequestVpcModifyAttributeTypeDef]
    ) -> None:
        """
        Modifies the specified attribute of the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.modify_attribute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcmodify_attribute-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`EC2.Client.describe_vpcs` to update the attributes of the Vpc
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcreload-method)
        """

    async def request_vpc_peering_connection(
        self,
        **kwargs: Unpack[CreateVpcPeeringConnectionRequestVpcRequestVpcPeeringConnectionTypeDef],
    ) -> "_VpcPeeringConnection":
        """
        Requests a VPC peering connection between two VPCs: a requester VPC that you
        own and an accepter VPC with which to create the
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.request_vpc_peering_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcrequest_vpc_peering_connection-method)
        """

    async def wait_until_available(self) -> None:
        """
        Waits until this Vpc is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.wait_until_available)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcwait_until_available-method)
        """

    async def wait_until_exists(self) -> None:
        """
        Waits until this Vpc is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.wait_until_exists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#vpcwait_until_exists-method)
        """


_Vpc = Vpc


class EC2ResourceMeta(ResourceMeta):
    client: EC2Client


class EC2ServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/)
    """

    meta: "EC2ResourceMeta"  # type: ignore
    classic_addresses: ServiceResourceClassicAddressesCollection
    dhcp_options_sets: ServiceResourceDhcpOptionsSetsCollection
    images: ServiceResourceImagesCollection
    instances: ServiceResourceInstancesCollection
    internet_gateways: ServiceResourceInternetGatewaysCollection
    key_pairs: ServiceResourceKeyPairsCollection
    network_acls: ServiceResourceNetworkAclsCollection
    network_interfaces: ServiceResourceNetworkInterfacesCollection
    placement_groups: ServiceResourcePlacementGroupsCollection
    route_tables: ServiceResourceRouteTablesCollection
    security_groups: ServiceResourceSecurityGroupsCollection
    snapshots: ServiceResourceSnapshotsCollection
    subnets: ServiceResourceSubnetsCollection
    volumes: ServiceResourceVolumesCollection
    vpc_addresses: ServiceResourceVpcAddressesCollection
    vpc_peering_connections: ServiceResourceVpcPeeringConnectionsCollection
    vpcs: ServiceResourceVpcsCollection

    async def ClassicAddress(self, public_ip: str) -> "_ClassicAddress":
        """
        Creates a ClassicAddress resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.ClassicAddress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceclassicaddress-method)
        """

    async def DhcpOptions(self, id: str) -> "_DhcpOptions":
        """
        Creates a DhcpOptions resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.DhcpOptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcedhcpoptions-method)
        """

    async def Image(self, id: str) -> "_Image":
        """
        Creates a Image resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceimage-method)
        """

    async def Instance(self, id: str) -> "_Instance":
        """
        Creates a Instance resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceinstance-method)
        """

    async def InternetGateway(self, id: str) -> "_InternetGateway":
        """
        Creates a InternetGateway resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.InternetGateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceinternetgateway-method)
        """

    async def KeyPair(self, name: str) -> "_KeyPair":
        """
        Creates a KeyPairInfo resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.KeyPair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcekeypair-method)
        """

    async def NetworkAcl(self, id: str) -> "_NetworkAcl":
        """
        Creates a NetworkAcl resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkAcl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkacl-method)
        """

    async def NetworkInterface(self, id: str) -> "_NetworkInterface":
        """
        Creates a NetworkInterface resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkInterface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkinterface-method)
        """

    async def NetworkInterfaceAssociation(self, id: str) -> "_NetworkInterfaceAssociation":
        """
        Creates a NetworkInterfaceAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.NetworkInterfaceAssociation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcenetworkinterfaceassociation-method)
        """

    async def PlacementGroup(self, name: str) -> "_PlacementGroup":
        """
        Creates a PlacementGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.PlacementGroup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceplacementgroup-method)
        """

    async def Route(self, route_table_id: str, destination_cidr_block: str) -> "_Route":
        """
        Creates a Route resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroute-method)
        """

    async def RouteTable(self, id: str) -> "_RouteTable":
        """
        Creates a RouteTable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.RouteTable)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroutetable-method)
        """

    async def RouteTableAssociation(self, id: str) -> "_RouteTableAssociation":
        """
        Creates a RouteTableAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.RouteTableAssociation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceroutetableassociation-method)
        """

    async def SecurityGroup(self, id: str) -> "_SecurityGroup":
        """
        Creates a SecurityGroup resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.SecurityGroup)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesecuritygroup-method)
        """

    async def Snapshot(self, id: str) -> "_Snapshot":
        """
        Creates a Snapshot resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesnapshot-method)
        """

    async def Subnet(self, id: str) -> "_Subnet":
        """
        Creates a Subnet resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Subnet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcesubnet-method)
        """

    async def Tag(self, resource_id: str, key: str, value: str) -> "_Tag":
        """
        Creates a Tag resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Tag)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcetag-method)
        """

    async def Volume(self, id: str) -> "_Volume":
        """
        Creates a Volume resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Volume)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevolume-method)
        """

    async def Vpc(self, id: str) -> "_Vpc":
        """
        Creates a Vpc resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.Vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpc-method)
        """

    async def VpcAddress(self, allocation_id: str) -> "_VpcAddress":
        """
        Creates a VpcAddress resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.VpcAddress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpcaddress-method)
        """

    async def VpcPeeringConnection(self, id: str) -> "_VpcPeeringConnection":
        """
        Creates a VpcPeeringConnection resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.VpcPeeringConnection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcevpcpeeringconnection-method)
        """

    async def create_dhcp_options(
        self, **kwargs: Unpack[CreateDhcpOptionsRequestServiceResourceCreateDhcpOptionsTypeDef]
    ) -> "_DhcpOptions":
        """
        Creates a custom set of DHCP options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_dhcp_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_dhcp_options-method)
        """

    async def create_instances(
        self, **kwargs: Unpack[RunInstancesRequestServiceResourceCreateInstancesTypeDef]
    ) -> List["_Instance"]:
        """
        Launches the specified number of instances using an AMI for which you have
        permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_instances-method)
        """

    async def create_internet_gateway(
        self,
        **kwargs: Unpack[CreateInternetGatewayRequestServiceResourceCreateInternetGatewayTypeDef],
    ) -> "_InternetGateway":
        """
        Creates an internet gateway for use with a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_internet_gateway)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_internet_gateway-method)
        """

    async def create_key_pair(
        self, **kwargs: Unpack[CreateKeyPairRequestServiceResourceCreateKeyPairTypeDef]
    ) -> "_KeyPair":
        """
        Creates an ED25519 or 2048-bit RSA key pair with the specified name and in the
        specified PEM or PPK
        format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_key_pair-method)
        """

    async def create_network_acl(
        self, **kwargs: Unpack[CreateNetworkAclRequestServiceResourceCreateNetworkAclTypeDef]
    ) -> "_NetworkAcl":
        """
        Creates a network ACL in a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_network_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_network_acl-method)
        """

    async def create_network_interface(
        self,
        **kwargs: Unpack[CreateNetworkInterfaceRequestServiceResourceCreateNetworkInterfaceTypeDef],
    ) -> "_NetworkInterface":
        """
        Creates a network interface in the specified subnet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_network_interface)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_network_interface-method)
        """

    async def create_placement_group(
        self,
        **kwargs: Unpack[CreatePlacementGroupRequestServiceResourceCreatePlacementGroupTypeDef],
    ) -> "_PlacementGroup":
        """
        Creates a placement group in which to launch instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_placement_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_placement_group-method)
        """

    async def create_route_table(
        self, **kwargs: Unpack[CreateRouteTableRequestServiceResourceCreateRouteTableTypeDef]
    ) -> "_RouteTable":
        """
        Creates a route table for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_route_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_route_table-method)
        """

    async def create_security_group(
        self, **kwargs: Unpack[CreateSecurityGroupRequestServiceResourceCreateSecurityGroupTypeDef]
    ) -> "_SecurityGroup":
        """
        Creates a security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_security_group-method)
        """

    async def create_snapshot(
        self, **kwargs: Unpack[CreateSnapshotRequestServiceResourceCreateSnapshotTypeDef]
    ) -> "_Snapshot":
        """
        Creates a snapshot of an EBS volume and stores it in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_snapshot-method)
        """

    async def create_subnet(
        self, **kwargs: Unpack[CreateSubnetRequestServiceResourceCreateSubnetTypeDef]
    ) -> "_Subnet":
        """
        Creates a subnet in the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_subnet)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_subnet-method)
        """

    async def create_tags(
        self, **kwargs: Unpack[CreateTagsRequestServiceResourceCreateTagsTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_tags-method)
        """

    async def create_volume(
        self, **kwargs: Unpack[CreateVolumeRequestServiceResourceCreateVolumeTypeDef]
    ) -> "_Volume":
        """
        Creates an EBS volume that can be attached to an instance in the same
        Availability
        Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_volume)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_volume-method)
        """

    async def create_vpc(
        self, **kwargs: Unpack[CreateVpcRequestServiceResourceCreateVpcTypeDef]
    ) -> "_Vpc":
        """
        Creates a VPC with the specified CIDR blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_vpc-method)
        """

    async def create_vpc_peering_connection(
        self,
        **kwargs: Unpack[
            CreateVpcPeeringConnectionRequestServiceResourceCreateVpcPeeringConnectionTypeDef
        ],
    ) -> "_VpcPeeringConnection":
        """
        Requests a VPC peering connection between two VPCs: a requester VPC that you
        own and an accepter VPC with which to create the
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_vpc_peering_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcecreate_vpc_peering_connection-method)
        """

    async def disassociate_route_table(
        self,
        **kwargs: Unpack[DisassociateRouteTableRequestServiceResourceDisassociateRouteTableTypeDef],
    ) -> None:
        """
        Disassociates a subnet or gateway from a route table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.disassociate_route_table)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourcedisassociate_route_table-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceget_available_subresources-method)
        """

    async def import_key_pair(
        self, **kwargs: Unpack[ImportKeyPairRequestServiceResourceImportKeyPairTypeDef]
    ) -> "_KeyPairInfo":
        """
        Imports the public key from an RSA or ED25519 key pair that you created with a
        third-party
        tool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.import_key_pair)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceimport_key_pair-method)
        """

    async def register_image(
        self, **kwargs: Unpack[RegisterImageRequestServiceResourceRegisterImageTypeDef]
    ) -> "_Image":
        """
        Registers an AMI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.register_image)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2/service_resource/#ec2serviceresourceregister_image-method)
        """
