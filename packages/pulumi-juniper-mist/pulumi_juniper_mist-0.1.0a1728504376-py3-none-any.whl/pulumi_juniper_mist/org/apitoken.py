# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ApitokenArgs', 'Apitoken']

@pulumi.input_type
class ApitokenArgs:
    def __init__(__self__, *,
                 org_id: pulumi.Input[str],
                 privileges: pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]],
                 name: Optional[pulumi.Input[str]] = None,
                 src_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Apitoken resource.
        :param pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]] privileges: list of privileges the token has on the orgs/sites
        :param pulumi.Input[str] name: name of the token
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_ips: list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "privileges", privileges)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if src_ips is not None:
            pulumi.set(__self__, "src_ips", src_ips)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def privileges(self) -> pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]]:
        """
        list of privileges the token has on the orgs/sites
        """
        return pulumi.get(self, "privileges")

    @privileges.setter
    def privileges(self, value: pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]]):
        pulumi.set(self, "privileges", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the token
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="srcIps")
    def src_ips(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        return pulumi.get(self, "src_ips")

    @src_ips.setter
    def src_ips(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "src_ips", value)


@pulumi.input_type
class _ApitokenState:
    def __init__(__self__, *,
                 created_by: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]]] = None,
                 src_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Apitoken resources.
        :param pulumi.Input[str] created_by: email of the token creator / null if creator is deleted
        :param pulumi.Input[str] name: name of the token
        :param pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]] privileges: list of privileges the token has on the orgs/sites
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_ips: list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if privileges is not None:
            pulumi.set(__self__, "privileges", privileges)
        if src_ips is not None:
            pulumi.set(__self__, "src_ips", src_ips)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[pulumi.Input[str]]:
        """
        email of the token creator / null if creator is deleted
        """
        return pulumi.get(self, "created_by")

    @created_by.setter
    def created_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        name of the token
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def privileges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]]]:
        """
        list of privileges the token has on the orgs/sites
        """
        return pulumi.get(self, "privileges")

    @privileges.setter
    def privileges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApitokenPrivilegeArgs']]]]):
        pulumi.set(self, "privileges", value)

    @property
    @pulumi.getter(name="srcIps")
    def src_ips(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        return pulumi.get(self, "src_ips")

    @src_ips.setter
    def src_ips(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "src_ips", value)


class Apitoken(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ApitokenPrivilegeArgs', 'ApitokenPrivilegeArgsDict']]]]] = None,
                 src_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        This resource manages Org API Tokens.
        Org API token is a unique identifier used by an application to authenticate and access a service's API. These tokens are used to authenticate requests made to the API server and ensure secure access to the API. They are not bound to any specific user and provide access to the organization as a whole.
        Organization tokens support different privileges and can only be used for the specific organization they are generated for.
        Rate limiting is done on an individual token basis, so if one token reaches its rate limit, it does not impact other tokens.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: name of the token
        :param pulumi.Input[Sequence[pulumi.Input[Union['ApitokenPrivilegeArgs', 'ApitokenPrivilegeArgsDict']]]] privileges: list of privileges the token has on the orgs/sites
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_ips: list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApitokenArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource manages Org API Tokens.
        Org API token is a unique identifier used by an application to authenticate and access a service's API. These tokens are used to authenticate requests made to the API server and ensure secure access to the API. They are not bound to any specific user and provide access to the organization as a whole.
        Organization tokens support different privileges and can only be used for the specific organization they are generated for.
        Rate limiting is done on an individual token basis, so if one token reaches its rate limit, it does not impact other tokens.

        :param str resource_name: The name of the resource.
        :param ApitokenArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApitokenArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ApitokenPrivilegeArgs', 'ApitokenPrivilegeArgsDict']]]]] = None,
                 src_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApitokenArgs.__new__(ApitokenArgs)

            __props__.__dict__["name"] = name
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if privileges is None and not opts.urn:
                raise TypeError("Missing required property 'privileges'")
            __props__.__dict__["privileges"] = privileges
            __props__.__dict__["src_ips"] = src_ips
            __props__.__dict__["created_by"] = None
            __props__.__dict__["key"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["key"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Apitoken, __self__).__init__(
            'junipermist:org/apitoken:Apitoken',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_by: Optional[pulumi.Input[str]] = None,
            key: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            privileges: Optional[pulumi.Input[Sequence[pulumi.Input[Union['ApitokenPrivilegeArgs', 'ApitokenPrivilegeArgsDict']]]]] = None,
            src_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Apitoken':
        """
        Get an existing Apitoken resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_by: email of the token creator / null if creator is deleted
        :param pulumi.Input[str] name: name of the token
        :param pulumi.Input[Sequence[pulumi.Input[Union['ApitokenPrivilegeArgs', 'ApitokenPrivilegeArgsDict']]]] privileges: list of privileges the token has on the orgs/sites
        :param pulumi.Input[Sequence[pulumi.Input[str]]] src_ips: list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApitokenState.__new__(_ApitokenState)

        __props__.__dict__["created_by"] = created_by
        __props__.__dict__["key"] = key
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["privileges"] = privileges
        __props__.__dict__["src_ips"] = src_ips
        return Apitoken(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[str]:
        """
        email of the token creator / null if creator is deleted
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        name of the token
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def privileges(self) -> pulumi.Output[Sequence['outputs.ApitokenPrivilege']]:
        """
        list of privileges the token has on the orgs/sites
        """
        return pulumi.get(self, "privileges")

    @property
    @pulumi.getter(name="srcIps")
    def src_ips(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        list of allowed IP addresses from where the token can be used from. At most 10 IP addresses can be specified, cannot be changed once the API Token is created.
        """
        return pulumi.get(self, "src_ips")

