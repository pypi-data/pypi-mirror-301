# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ImageArgs', 'Image']

@pulumi.input_type
class ImageArgs:
    def __init__(__self__, *,
                 device_id: pulumi.Input[str],
                 file: pulumi.Input[str],
                 image_number: pulumi.Input[int],
                 site_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a Image resource.
        :param pulumi.Input[str] file: path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        pulumi.set(__self__, "device_id", device_id)
        pulumi.set(__self__, "file", file)
        pulumi.set(__self__, "image_number", image_number)
        pulumi.set(__self__, "site_id", site_id)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "device_id")

    @device_id.setter
    def device_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_id", value)

    @property
    @pulumi.getter
    def file(self) -> pulumi.Input[str]:
        """
        path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @file.setter
    def file(self, value: pulumi.Input[str]):
        pulumi.set(self, "file", value)

    @property
    @pulumi.getter(name="imageNumber")
    def image_number(self) -> pulumi.Input[int]:
        return pulumi.get(self, "image_number")

    @image_number.setter
    def image_number(self, value: pulumi.Input[int]):
        pulumi.set(self, "image_number", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "site_id", value)


@pulumi.input_type
class _ImageState:
    def __init__(__self__, *,
                 device_id: Optional[pulumi.Input[str]] = None,
                 file: Optional[pulumi.Input[str]] = None,
                 image_number: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Image resources.
        :param pulumi.Input[str] file: path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        if device_id is not None:
            pulumi.set(__self__, "device_id", device_id)
        if file is not None:
            pulumi.set(__self__, "file", file)
        if image_number is not None:
            pulumi.set(__self__, "image_number", image_number)
        if site_id is not None:
            pulumi.set(__self__, "site_id", site_id)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "device_id")

    @device_id.setter
    def device_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device_id", value)

    @property
    @pulumi.getter
    def file(self) -> Optional[pulumi.Input[str]]:
        """
        path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @file.setter
    def file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file", value)

    @property
    @pulumi.getter(name="imageNumber")
    def image_number(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "image_number")

    @image_number.setter
    def image_number(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "image_number", value)

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "site_id")

    @site_id.setter
    def site_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "site_id", value)


class Image(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_id: Optional[pulumi.Input[str]] = None,
                 file: Optional[pulumi.Input[str]] = None,
                 image_number: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource is used to upload a Device picture.
        This resource can be used to add a picture to a Wireless Access point, a Switch or a Gateway. A Maximum of 3 pictures can be uploaded.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        device_image_one = junipermist.device.Image("device_image_one",
            device_id=inventory["devices"][1]["id"],
            site_id=inventory["devices"][1]["siteId"],
            file="/Users/johndoe/Documents/image.jpg",
            image_number=1)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file: path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource is used to upload a Device picture.
        This resource can be used to add a picture to a Wireless Access point, a Switch or a Gateway. A Maximum of 3 pictures can be uploaded.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_juniper_mist as junipermist

        device_image_one = junipermist.device.Image("device_image_one",
            device_id=inventory["devices"][1]["id"],
            site_id=inventory["devices"][1]["siteId"],
            file="/Users/johndoe/Documents/image.jpg",
            image_number=1)
        ```

        :param str resource_name: The name of the resource.
        :param ImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_id: Optional[pulumi.Input[str]] = None,
                 file: Optional[pulumi.Input[str]] = None,
                 image_number: Optional[pulumi.Input[int]] = None,
                 site_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageArgs.__new__(ImageArgs)

            if device_id is None and not opts.urn:
                raise TypeError("Missing required property 'device_id'")
            __props__.__dict__["device_id"] = device_id
            if file is None and not opts.urn:
                raise TypeError("Missing required property 'file'")
            __props__.__dict__["file"] = file
            if image_number is None and not opts.urn:
                raise TypeError("Missing required property 'image_number'")
            __props__.__dict__["image_number"] = image_number
            if site_id is None and not opts.urn:
                raise TypeError("Missing required property 'site_id'")
            __props__.__dict__["site_id"] = site_id
        super(Image, __self__).__init__(
            'junipermist:device/image:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            device_id: Optional[pulumi.Input[str]] = None,
            file: Optional[pulumi.Input[str]] = None,
            image_number: Optional[pulumi.Input[int]] = None,
            site_id: Optional[pulumi.Input[str]] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] file: path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ImageState.__new__(_ImageState)

        __props__.__dict__["device_id"] = device_id
        __props__.__dict__["file"] = file
        __props__.__dict__["image_number"] = image_number
        __props__.__dict__["site_id"] = site_id
        return Image(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "device_id")

    @property
    @pulumi.getter
    def file(self) -> pulumi.Output[str]:
        """
        path to the device image file to upload. File must be a `jpeg`, `jpg` or `png` image`
        """
        return pulumi.get(self, "file")

    @property
    @pulumi.getter(name="imageNumber")
    def image_number(self) -> pulumi.Output[int]:
        return pulumi.get(self, "image_number")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "site_id")

