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

__all__ = ['IdpprofileArgs', 'Idpprofile']

@pulumi.input_type
class IdpprofileArgs:
    def __init__(__self__, *,
                 base_profile: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 overwrites: Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]] = None):
        """
        The set of arguments for constructing a Idpprofile resource.
        :param pulumi.Input[str] base_profile: enum: `critical`, `standard`, `strict`
        """
        pulumi.set(__self__, "base_profile", base_profile)
        pulumi.set(__self__, "org_id", org_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if overwrites is not None:
            pulumi.set(__self__, "overwrites", overwrites)

    @property
    @pulumi.getter(name="baseProfile")
    def base_profile(self) -> pulumi.Input[str]:
        """
        enum: `critical`, `standard`, `strict`
        """
        return pulumi.get(self, "base_profile")

    @base_profile.setter
    def base_profile(self, value: pulumi.Input[str]):
        pulumi.set(self, "base_profile", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def overwrites(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]]:
        return pulumi.get(self, "overwrites")

    @overwrites.setter
    def overwrites(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]]):
        pulumi.set(self, "overwrites", value)


@pulumi.input_type
class _IdpprofileState:
    def __init__(__self__, *,
                 base_profile: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 overwrites: Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]] = None):
        """
        Input properties used for looking up and filtering Idpprofile resources.
        :param pulumi.Input[str] base_profile: enum: `critical`, `standard`, `strict`
        """
        if base_profile is not None:
            pulumi.set(__self__, "base_profile", base_profile)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if overwrites is not None:
            pulumi.set(__self__, "overwrites", overwrites)

    @property
    @pulumi.getter(name="baseProfile")
    def base_profile(self) -> Optional[pulumi.Input[str]]:
        """
        enum: `critical`, `standard`, `strict`
        """
        return pulumi.get(self, "base_profile")

    @base_profile.setter
    def base_profile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_profile", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
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
    def overwrites(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]]:
        return pulumi.get(self, "overwrites")

    @overwrites.setter
    def overwrites(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IdpprofileOverwriteArgs']]]]):
        pulumi.set(self, "overwrites", value)


class Idpprofile(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_profile: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 overwrites: Optional[pulumi.Input[Sequence[pulumi.Input[Union['IdpprofileOverwriteArgs', 'IdpprofileOverwriteArgsDict']]]]] = None,
                 __props__=None):
        """
        This resource manages WAN Assurance Idp Profiles.
        An IDP Profile is a configuration setting that defines the behavior and actions of an intrusion detection and prevention (IDP) system.It specifies how the idp system should detect and respond to potential security threats or attacks on a network.The profile includes rules and policies that determine which types of traffic or attacks should be monitored,what actions should be taken when a threat is detected, and any exceptions or exclusions for specific destinations or attack types.

        ## Import

        Using `pulumi import`, import `mist_org_idpprofile` with:

        IDP Profile can be imported by specifying the org_id and the idpprofile_id

        ```sh
        $ pulumi import junipermist:org/idpprofile:Idpprofile idpprofile_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] base_profile: enum: `critical`, `standard`, `strict`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IdpprofileArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource manages WAN Assurance Idp Profiles.
        An IDP Profile is a configuration setting that defines the behavior and actions of an intrusion detection and prevention (IDP) system.It specifies how the idp system should detect and respond to potential security threats or attacks on a network.The profile includes rules and policies that determine which types of traffic or attacks should be monitored,what actions should be taken when a threat is detected, and any exceptions or exclusions for specific destinations or attack types.

        ## Import

        Using `pulumi import`, import `mist_org_idpprofile` with:

        IDP Profile can be imported by specifying the org_id and the idpprofile_id

        ```sh
        $ pulumi import junipermist:org/idpprofile:Idpprofile idpprofile_one 17b46405-3a6d-4715-8bb4-6bb6d06f316a.d3c42998-9012-4859-9743-6b9bee475309
        ```

        :param str resource_name: The name of the resource.
        :param IdpprofileArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IdpprofileArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_profile: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 overwrites: Optional[pulumi.Input[Sequence[pulumi.Input[Union['IdpprofileOverwriteArgs', 'IdpprofileOverwriteArgsDict']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IdpprofileArgs.__new__(IdpprofileArgs)

            if base_profile is None and not opts.urn:
                raise TypeError("Missing required property 'base_profile'")
            __props__.__dict__["base_profile"] = base_profile
            __props__.__dict__["name"] = name
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            __props__.__dict__["overwrites"] = overwrites
        super(Idpprofile, __self__).__init__(
            'junipermist:org/idpprofile:Idpprofile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            base_profile: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            overwrites: Optional[pulumi.Input[Sequence[pulumi.Input[Union['IdpprofileOverwriteArgs', 'IdpprofileOverwriteArgsDict']]]]] = None) -> 'Idpprofile':
        """
        Get an existing Idpprofile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] base_profile: enum: `critical`, `standard`, `strict`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IdpprofileState.__new__(_IdpprofileState)

        __props__.__dict__["base_profile"] = base_profile
        __props__.__dict__["name"] = name
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["overwrites"] = overwrites
        return Idpprofile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="baseProfile")
    def base_profile(self) -> pulumi.Output[str]:
        """
        enum: `critical`, `standard`, `strict`
        """
        return pulumi.get(self, "base_profile")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter
    def overwrites(self) -> pulumi.Output[Optional[Sequence['outputs.IdpprofileOverwrite']]]:
        return pulumi.get(self, "overwrites")

