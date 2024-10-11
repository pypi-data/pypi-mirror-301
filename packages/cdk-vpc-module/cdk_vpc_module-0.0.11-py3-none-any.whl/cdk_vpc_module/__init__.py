r'''
# cdk-vpc-module

cdk-vpc-module construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable aws vpc  and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## :sparkles: Features

* :white_check_mark: Option to configure custom IPv4 CIDR(10.10.0.0/24)
* :white_check_mark: VPC Peering with  route table entry
* :white_check_mark: Configurable NACL as per subnet group
* :white_check_mark: NATGateway as per availabilityZones

Using cdk a vpc can be deployed using the following sample code snippet:

```python
import { Network } from "@smallcase/cdk-vpc-module/lib/constructs/network";
import { aws_ec2 as ec2, App, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class VPCStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps = {}) {
    const s3EndpointIamPermission = new iam.PolicyStatement({
      actions: ["s3:*"],
      resources: ['arn:aws:s3:::*'],
      principals: [new iam.AnyPrincipal()],
    })
    const monitoringEndpointIamPermission = new iam.PolicyStatement({
      actions: ["*"],
      resources: ['*'],
      principals: [new iam.AnyPrincipal()],
    })
    super(scope, id, props);
    new Network(this, 'NETWORK', {
      vpc: {
        cidr: '10.10.0.0/16',
        subnetConfiguration: [],
      },
      peeringConfigs: {
        "TEST-PEERING": { // this key will be used as your peering id, which you will have to mention below when you configure a route table for your subnets
          peeringVpcId: "vpc-0000",
          tags: {
            "Name": "TEST-PEERING to CREATED-VPC",
            "Description": "Connect"
          }
        }
      },
      subnets: [
        {
          subnetGroupName: 'NATGateway',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.0.0/28', '10.10.0.16/28', '10.10.0.32/28'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
        },
        {
          subnetGroupName: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.2.0/24', '10.10.3.0/24', '10.10.4.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
            'kubernetes.io/role/elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.5.0/24', '10.10.6.0/24', '10.10.7.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },

          ],
          routes: [
            {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
              routerType: ec2.RouterType.VPC_PEERING_CONNECTION,
              destinationCidrBlock: "<destinationCidrBlock>",
              //<Your VPC PeeringConfig KEY, in this example TEST-PEERING will be your ID>
              existingVpcPeeringRouteKey: "TEST-PEERING"
            }
          ],
          tags: {
            'kubernetes.io/role/internal-elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Database',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.14.0/27', '10.10.14.32/27', '10.10.14.64/27'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
          },
        },
      ],
      vpcEndpoints: [
        {
          name: "s3-gw",
          service: ec2.GatewayVpcEndpointAwsService.S3,
          subnetGroupNames: ["Private","Database"],
          externalSubnets: [
            {
              id: "subnet-<id>",
              availabilityZone: "ap-south-1a",
              routeTableId: "rtb-<id>"
            },
            {
              id: "subnet-<id>",
              availabilityZone: "ap-south-1b",
              routeTableId: "rtb-<id>"
            }
          ],
          iamPolicyStatements: [s3EndpointIamPermission]
        },
        {
          name: "da-stag-monitoring-vpe",
          service: ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_MONITORING,
          subnetGroupNames: ["ManageServicePrivate"],
          iamPolicyStatements: [monitoringEndpointIamPermission],
          securityGroupRules: [
            {
              peer: ec2.Peer.ipv4("10.10.0.0/16"),
              port:  ec2.Port.tcp(443),
              description: "From Test VPC"
            }
          ],
        },
      ]
    });
  }
}
const envDef = {
  account: '<AWS-ID>',
  region: '<AWS-REGION>',
};

const app = new App();

new VPCStack(app, 'TEST', {
  env: envDef,
  terminationProtection: true,
  tags: {
});
app.synth();
```

Please refer [here](/API.md) to check how to use individual resource constructs.

## :clapper: Quick Start

The quick start shows you how to create an **AWS-VPC** using this module.

### Prerequisites

* A working [`aws`](https://aws.amazon.com/cli/) CLI installation with access to an account and administrator privileges
* You'll need a recent [NodeJS](https://nodejs.org) installation

To get going you'll need a CDK project. For details please refer to the [detailed guide for CDK](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html).

Create an empty directory on your system.

```bash
mkdir aws-quick-start-vpc && cd aws-quick-start-vpc
```

Bootstrap your CDK project, we will use TypeScript, but you can switch to any other supported language.

```bash
npx cdk init sample-vpc  --language typescript
npx cdk bootstrap
```

Install using NPM:

```
npm install @smallcase/cdk-vpc-module
```

Using yarn

```
yarn add @smallcase/cdk-vpc-module
```

Check the changed which are to be deployed

```bash
~ -> npx cdk diff
```

Deploy using

```bash
~ -> npx cdk deploy
```

Features
Multiple VPC Endpoints: Define and manage multiple VPC Endpoints in one configuration.
Flexible Subnet Selection: Attach VPC Endpoints to multiple subnet groups or external subnets.
Custom Security Groups: Configure security groups for Interface VPC Endpoints.
IAM Policies: Attach custom IAM policies to control access to the VPC Endpoints.
Tagging: Apply custom tags to each VPC Endpoint.

Defining VPC Endpoints Configuration
You can define multiple VPC Endpoints in the vpcEndpoints: [] configuration array. Each VPC Endpoint can be customized with different subnet groups, IAM policies, security group rules, and tags.

```
vpcEndpoints: [
  {
    name: "test-s3-gw",
    service: ec2.GatewayVpcEndpointAwsService.S3,
    subnetGroupNames: ["ManageServicePrivate", "ToolPrivate", "Database"],  // Subnet groups for the endpoint
    externalSubnets: [
      {
        id: "subnet-<id>",
        availabilityZone: "ap-south-1a",
        routeTableId: "rtb-<id>",
      },
      {
        id: "subnet-<id>",
        availabilityZone: "ap-south-1b",
        routeTableId: "rtb-<id>",
      }
    ],
    iamPolicyStatements: [s3EndpointIamPermission],  // Custom IAM policy for the endpoint
  },
  {
    name: "DynamoDbGatewayEndpoint",
    service: ec2.GatewayVpcEndpointAwsService.DYNAMODB,
    subnetGroupNames: ["private-subnet"],
    additionalTags: {
      Environment: "Staging",
    },
  },
],
```

In this example:

The S3 Gateway Endpoint is created in three subnet groups: ManageServicePrivate, ToolPrivate, and Database.
External subnets are specified with their IDs, availability zones, and route table IDs for the S3 endpoint.
A custom IAM policy (s3EndpointIamPermission) is attached to control access to the S3 endpoint.
A DynamoDB Gateway Endpoint is created in the private-subnet with additional tags specifying the environment and ownership.

Configuration Options
Here’s a breakdown of the configuration options available:

1. name: A unique name for the VPC Endpoint.
2. service: The AWS service the VPC Endpoint connects to (e.g., S3, DynamoDB, Secrets Manager)
3. subnetGroupNames: The subnet group names where the VPC Endpoint will be deployed.
4. externalSubnets: Specify external subnets if you need to define subnets manually (each with an id, availabilityZone, and routeTableId).
5. iamPolicyStatements: (Optional) Attach IAM policy statements to control access to the endpoint.
6. additionalTags: (Optional) Add custom tags to the VPC Endpoint for easier identification and tracking.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.AddRouteOptions",
    jsii_struct_bases=[],
    name_mapping={
        "router_type": "routerType",
        "destination_cidr_block": "destinationCidrBlock",
        "destination_ipv6_cidr_block": "destinationIpv6CidrBlock",
        "enables_internet_connectivity": "enablesInternetConnectivity",
        "existing_vpc_peering_route_key": "existingVpcPeeringRouteKey",
        "router_id": "routerId",
    },
)
class AddRouteOptions:
    def __init__(
        self,
        *,
        router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
        destination_cidr_block: typing.Optional[builtins.str] = None,
        destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
        enables_internet_connectivity: typing.Optional[builtins.bool] = None,
        existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param router_type: What type of router to route this traffic to.
        :param destination_cidr_block: IPv4 range this route applies to. Default: '0.0.0.0/0'
        :param destination_ipv6_cidr_block: IPv6 range this route applies to. Default: - Uses IPv6
        :param enables_internet_connectivity: Whether this route will enable internet connectivity. If true, this route will be added before any AWS resources that depend on internet connectivity in the VPC will be created. Default: false
        :param existing_vpc_peering_route_key: 
        :param router_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6)
            check_type(argname="argument router_type", value=router_type, expected_type=type_hints["router_type"])
            check_type(argname="argument destination_cidr_block", value=destination_cidr_block, expected_type=type_hints["destination_cidr_block"])
            check_type(argname="argument destination_ipv6_cidr_block", value=destination_ipv6_cidr_block, expected_type=type_hints["destination_ipv6_cidr_block"])
            check_type(argname="argument enables_internet_connectivity", value=enables_internet_connectivity, expected_type=type_hints["enables_internet_connectivity"])
            check_type(argname="argument existing_vpc_peering_route_key", value=existing_vpc_peering_route_key, expected_type=type_hints["existing_vpc_peering_route_key"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "router_type": router_type,
        }
        if destination_cidr_block is not None:
            self._values["destination_cidr_block"] = destination_cidr_block
        if destination_ipv6_cidr_block is not None:
            self._values["destination_ipv6_cidr_block"] = destination_ipv6_cidr_block
        if enables_internet_connectivity is not None:
            self._values["enables_internet_connectivity"] = enables_internet_connectivity
        if existing_vpc_peering_route_key is not None:
            self._values["existing_vpc_peering_route_key"] = existing_vpc_peering_route_key
        if router_id is not None:
            self._values["router_id"] = router_id

    @builtins.property
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''What type of router to route this traffic to.'''
        result = self._values.get("router_type")
        assert result is not None, "Required property 'router_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, result)

    @builtins.property
    def destination_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv4 range this route applies to.

        :default: '0.0.0.0/0'
        '''
        result = self._values.get("destination_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv6 range this route applies to.

        :default: - Uses IPv6
        '''
        result = self._values.get("destination_ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enables_internet_connectivity(self) -> typing.Optional[builtins.bool]:
        '''Whether this route will enable internet connectivity.

        If true, this route will be added before any AWS resources that depend
        on internet connectivity in the VPC will be created.

        :default: false
        '''
        result = self._values.get("enables_internet_connectivity")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_vpc_peering_route_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_vpc_peering_route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.IExternalVPEndpointSubnets")
class IExternalVPEndpointSubnets(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> builtins.str:
        ...


class _IExternalVPEndpointSubnetsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.IExternalVPEndpointSubnets"

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTableId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IExternalVPEndpointSubnets).__jsii_proxy_class__ = lambda : _IExternalVPEndpointSubnetsProxy


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.ISubnetsProps")
class ISubnetsProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        ...

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        ...


class _ISubnetsPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.ISubnetsProps"

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, jsii.get(self, "subnetType"))

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "egressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "ingressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        return typing.cast(typing.Optional[typing.List[AddRouteOptions]], jsii.get(self, "routes"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useSubnetForNAT"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubnetsProps).__jsii_proxy_class__ = lambda : _ISubnetsPropsProxy


class Network(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-vpc-module.Network",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union["PeeringConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoints: typing.Optional[typing.Sequence[typing.Union["VpcEndpointConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        :param vpc_endpoints: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VPCProps(
            subnets=subnets,
            vpc=vpc,
            nat_eip_allocation_ids=nat_eip_allocation_ids,
            peering_configs=peering_configs,
            vpc_endpoints=vpc_endpoints,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createSubnet")
    def create_subnet(
        self,
        option: ISubnetsProps,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]:
        '''
        :param option: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        peering_connection_id = PeeringConnectionInternalType()

        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet], jsii.invoke(self, "createSubnet", [option, vpc, peering_connection_id]))

    @builtins.property
    @jsii.member(jsii_name="endpointOutputs")
    def endpoint_outputs(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint]], jsii.get(self, "endpointOutputs"))

    @builtins.property
    @jsii.member(jsii_name="natProvider")
    def nat_provider(self) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.get(self, "natProvider"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupOutputs")
    def security_group_outputs(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.SecurityGroup], jsii.get(self, "securityGroupOutputs"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="natSubnets")
    def nat_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "natSubnets"))

    @nat_subnets.setter
    def nat_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pbSubnets")
    def pb_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "pbSubnets"))

    @pb_subnets.setter
    def pb_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pbSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pvSubnets")
    def pv_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet], jsii.get(self, "pvSubnets"))

    @pv_subnets.setter
    def pv_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pvSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(
        self,
    ) -> typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]]:
        return typing.cast(typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(
        self,
        value: typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c92e4cdb3e7dca57b71939ecd52b3318b82f9250bdbeca196ba690ca35f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.NetworkACL",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "traffic": "traffic"},
)
class NetworkACL:
    def __init__(
        self,
        *,
        cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
        traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
    ) -> None:
        '''
        :param cidr: 
        :param traffic: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "traffic": traffic,
        }

    @builtins.property
    def cidr(self) -> _aws_cdk_aws_ec2_ceddda9d.AclCidr:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclCidr, result)

    @builtins.property
    def traffic(self) -> _aws_cdk_aws_ec2_ceddda9d.AclTraffic:
        result = self._values.get("traffic")
        assert result is not None, "Required property 'traffic' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclTraffic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkACL(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peering_vpc_id": "peeringVpcId",
        "tags": "tags",
        "peer_assume_role_arn": "peerAssumeRoleArn",
        "peer_owner_id": "peerOwnerId",
        "peer_region": "peerRegion",
    },
)
class PeeringConfig:
    def __init__(
        self,
        *,
        peering_vpc_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        peer_assume_role_arn: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peering_vpc_id: 
        :param tags: 
        :param peer_assume_role_arn: 
        :param peer_owner_id: 
        :param peer_region: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246)
            check_type(argname="argument peering_vpc_id", value=peering_vpc_id, expected_type=type_hints["peering_vpc_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument peer_assume_role_arn", value=peer_assume_role_arn, expected_type=type_hints["peer_assume_role_arn"])
            check_type(argname="argument peer_owner_id", value=peer_owner_id, expected_type=type_hints["peer_owner_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peering_vpc_id": peering_vpc_id,
            "tags": tags,
        }
        if peer_assume_role_arn is not None:
            self._values["peer_assume_role_arn"] = peer_assume_role_arn
        if peer_owner_id is not None:
            self._values["peer_owner_id"] = peer_owner_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region

    @builtins.property
    def peering_vpc_id(self) -> builtins.str:
        result = self._values.get("peering_vpc_id")
        assert result is not None, "Required property 'peering_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def peer_assume_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_owner_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConnectionInternalType",
    jsii_struct_bases=[],
    name_mapping={},
)
class PeeringConnectionInternalType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConnectionInternalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.SecurityGroupRule",
    jsii_struct_bases=[],
    name_mapping={"peer": "peer", "port": "port", "description": "description"},
)
class SecurityGroupRule:
    def __init__(
        self,
        *,
        peer: typing.Union[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, _aws_cdk_aws_ec2_ceddda9d.IPeer],
        port: _aws_cdk_aws_ec2_ceddda9d.Port,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peer: 
        :param port: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd68ce1d83764f7d07cea64483e8a41653ce9918274f406bd230a98a95864f8a)
            check_type(argname="argument peer", value=peer, expected_type=type_hints["peer"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer": peer,
            "port": port,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def peer(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, _aws_cdk_aws_ec2_ceddda9d.IPeer]:
        result = self._values.get("peer")
        assert result is not None, "Required property 'peer' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, _aws_cdk_aws_ec2_ceddda9d.IPeer], result)

    @builtins.property
    def port(self) -> _aws_cdk_aws_ec2_ceddda9d.Port:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Port, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VPCProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnets": "subnets",
        "vpc": "vpc",
        "nat_eip_allocation_ids": "natEipAllocationIds",
        "peering_configs": "peeringConfigs",
        "vpc_endpoints": "vpcEndpoints",
    },
)
class VPCProps:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoints: typing.Optional[typing.Sequence[typing.Union["VpcEndpointConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        :param vpc_endpoints: 
        '''
        if isinstance(vpc, dict):
            vpc = _aws_cdk_aws_ec2_ceddda9d.VpcProps(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument nat_eip_allocation_ids", value=nat_eip_allocation_ids, expected_type=type_hints["nat_eip_allocation_ids"])
            check_type(argname="argument peering_configs", value=peering_configs, expected_type=type_hints["peering_configs"])
            check_type(argname="argument vpc_endpoints", value=vpc_endpoints, expected_type=type_hints["vpc_endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
            "vpc": vpc,
        }
        if nat_eip_allocation_ids is not None:
            self._values["nat_eip_allocation_ids"] = nat_eip_allocation_ids
        if peering_configs is not None:
            self._values["peering_configs"] = peering_configs
        if vpc_endpoints is not None:
            self._values["vpc_endpoints"] = vpc_endpoints

    @builtins.property
    def subnets(self) -> typing.List[ISubnetsProps]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[ISubnetsProps], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.VpcProps:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpcProps, result)

    @builtins.property
    def nat_eip_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("nat_eip_allocation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peering_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PeeringConfig]]:
        result = self._values.get("peering_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PeeringConfig]], result)

    @builtins.property
    def vpc_endpoints(self) -> typing.Optional[typing.List["VpcEndpointConfig"]]:
        result = self._values.get("vpc_endpoints")
        return typing.cast(typing.Optional[typing.List["VpcEndpointConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPCProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VpcEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service": "service",
        "subnet_group_names": "subnetGroupNames",
        "additional_tags": "additionalTags",
        "external_subnets": "externalSubnets",
        "iam_policy_statements": "iamPolicyStatements",
        "security_group_rules": "securityGroupRules",
    },
)
class VpcEndpointConfig:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
        subnet_group_names: typing.Sequence[builtins.str],
        additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external_subnets: typing.Optional[typing.Sequence[IExternalVPEndpointSubnets]] = None,
        iam_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        security_group_rules: typing.Optional[typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param name: 
        :param service: 
        :param subnet_group_names: 
        :param additional_tags: 
        :param external_subnets: 
        :param iam_policy_statements: 
        :param security_group_rules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73b977d0ef95f1e08b08f9303890f3ab452756f6c151eea2ffe6c531ffe2ecc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument subnet_group_names", value=subnet_group_names, expected_type=type_hints["subnet_group_names"])
            check_type(argname="argument additional_tags", value=additional_tags, expected_type=type_hints["additional_tags"])
            check_type(argname="argument external_subnets", value=external_subnets, expected_type=type_hints["external_subnets"])
            check_type(argname="argument iam_policy_statements", value=iam_policy_statements, expected_type=type_hints["iam_policy_statements"])
            check_type(argname="argument security_group_rules", value=security_group_rules, expected_type=type_hints["security_group_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service": service,
            "subnet_group_names": subnet_group_names,
        }
        if additional_tags is not None:
            self._values["additional_tags"] = additional_tags
        if external_subnets is not None:
            self._values["external_subnets"] = external_subnets
        if iam_policy_statements is not None:
            self._values["iam_policy_statements"] = iam_policy_statements
        if security_group_rules is not None:
            self._values["security_group_rules"] = security_group_rules

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService]:
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService], result)

    @builtins.property
    def subnet_group_names(self) -> typing.List[builtins.str]:
        result = self._values.get("subnet_group_names")
        assert result is not None, "Required property 'subnet_group_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("additional_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def external_subnets(
        self,
    ) -> typing.Optional[typing.List[IExternalVPEndpointSubnets]]:
        result = self._values.get("external_subnets")
        return typing.cast(typing.Optional[typing.List[IExternalVPEndpointSubnets]], result)

    @builtins.property
    def iam_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        result = self._values.get("iam_policy_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def security_group_rules(self) -> typing.Optional[typing.List[SecurityGroupRule]]:
        result = self._values.get("security_group_rules")
        return typing.cast(typing.Optional[typing.List[SecurityGroupRule]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddRouteOptions",
    "IExternalVPEndpointSubnets",
    "ISubnetsProps",
    "Network",
    "NetworkACL",
    "PeeringConfig",
    "PeeringConnectionInternalType",
    "SecurityGroupRule",
    "VPCProps",
    "VpcEndpointConfig",
]

publication.publish()

def _typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6(
    *,
    router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
    destination_cidr_block: typing.Optional[builtins.str] = None,
    destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
    enables_internet_connectivity: typing.Optional[builtins.bool] = None,
    existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
    router_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoints: typing.Optional[typing.Sequence[typing.Union[VpcEndpointConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1(
    option: ISubnetsProps,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c92e4cdb3e7dca57b71939ecd52b3318b82f9250bdbeca196ba690ca35f52(
    value: typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f(
    *,
    cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
    traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246(
    *,
    peering_vpc_id: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    peer_assume_role_arn: typing.Optional[builtins.str] = None,
    peer_owner_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd68ce1d83764f7d07cea64483e8a41653ce9918274f406bd230a98a95864f8a(
    *,
    peer: typing.Union[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, _aws_cdk_aws_ec2_ceddda9d.IPeer],
    port: _aws_cdk_aws_ec2_ceddda9d.Port,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40(
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoints: typing.Optional[typing.Sequence[typing.Union[VpcEndpointConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73b977d0ef95f1e08b08f9303890f3ab452756f6c151eea2ffe6c531ffe2ecc(
    *,
    name: builtins.str,
    service: typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService],
    subnet_group_names: typing.Sequence[builtins.str],
    additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external_subnets: typing.Optional[typing.Sequence[IExternalVPEndpointSubnets]] = None,
    iam_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    security_group_rules: typing.Optional[typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
