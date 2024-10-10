# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['WlanPortalImageArgs', 'WlanPortalImage']

@pulumi.input_type
class WlanPortalImageArgs:
    def __init__(__self__, *,
                 file: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 wlan_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a WlanPortalImage resource.
        :param pulumi.Input[str] file: path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        :param pulumi.Input[str] wlan_id: Org WLAN ID
        """
        pulumi.set(__self__, "file", file)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "wlan_id", wlan_id)

    @property
    @pulumi.getter
    def file(self) -> pulumi.Input[str]:
        """
        path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @file.setter
    def file(self, value: pulumi.Input[str]):
        pulumi.set(self, "file", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="wlanId")
    def wlan_id(self) -> pulumi.Input[str]:
        """
        Org WLAN ID
        """
        return pulumi.get(self, "wlan_id")

    @wlan_id.setter
    def wlan_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "wlan_id", value)


@pulumi.input_type
class _WlanPortalImageState:
    def __init__(__self__, *,
                 file: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 wlan_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering WlanPortalImage resources.
        :param pulumi.Input[str] file: path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        :param pulumi.Input[str] wlan_id: Org WLAN ID
        """
        if file is not None:
            pulumi.set(__self__, "file", file)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if wlan_id is not None:
            pulumi.set(__self__, "wlan_id", wlan_id)

    @property
    @pulumi.getter
    def file(self) -> Optional[pulumi.Input[str]]:
        """
        path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @file.setter
    def file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="wlanId")
    def wlan_id(self) -> Optional[pulumi.Input[str]]:
        """
        Org WLAN ID
        """
        return pulumi.get(self, "wlan_id")

    @wlan_id.setter
    def wlan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "wlan_id", value)


class WlanPortalImage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 file: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 wlan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource is used to upload a WLAN Captive Web Portal background image.
        The WLAN object contains all the required configuration to broadcast an SSID (Authentication, VLAN, ...)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file: path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        :param pulumi.Input[str] wlan_id: Org WLAN ID
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WlanPortalImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource is used to upload a WLAN Captive Web Portal background image.
        The WLAN object contains all the required configuration to broadcast an SSID (Authentication, VLAN, ...)

        :param str resource_name: The name of the resource.
        :param WlanPortalImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WlanPortalImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 file: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 wlan_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WlanPortalImageArgs.__new__(WlanPortalImageArgs)

            if file is None and not opts.urn:
                raise TypeError("Missing required property 'file'")
            __props__.__dict__["file"] = file
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if wlan_id is None and not opts.urn:
                raise TypeError("Missing required property 'wlan_id'")
            __props__.__dict__["wlan_id"] = wlan_id
        super(WlanPortalImage, __self__).__init__(
            'junipermist:org/wlanPortalImage:WlanPortalImage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            file: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            wlan_id: Optional[pulumi.Input[str]] = None) -> 'WlanPortalImage':
        """
        Get an existing WlanPortalImage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file: path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        :param pulumi.Input[str] wlan_id: Org WLAN ID
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WlanPortalImageState.__new__(_WlanPortalImageState)

        __props__.__dict__["file"] = file
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["wlan_id"] = wlan_id
        return WlanPortalImage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def file(self) -> pulumi.Output[str]:
        """
        path to the background image file. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="wlanId")
    def wlan_id(self) -> pulumi.Output[str]:
        """
        Org WLAN ID
        """
        return pulumi.get(self, "wlan_id")

