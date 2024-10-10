# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Callable, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['Mk8sArgs', 'Mk8s']

@pulumi.input_type
class Mk8sArgs:
    def __init__(__self__, *,
                 version: pulumi.Input[str],
                 add_ons: Optional[pulumi.Input['Mk8sAddOnsArgs']] = None,
                 aws_provider: Optional[pulumi.Input['Mk8sAwsProviderArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ephemeral_provider: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']] = None,
                 firewalls: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]] = None,
                 generic_provider: Optional[pulumi.Input['Mk8sGenericProviderArgs']] = None,
                 hetzner_provider: Optional[pulumi.Input['Mk8sHetznerProviderArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Mk8s resource.
        :param pulumi.Input[str] description: Description of the Mk8s.
        :param pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]] firewalls: Allow-list.
        :param pulumi.Input[str] name: Name of the Mk8s.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags.
        """
        Mk8sArgs._configure(
            lambda key, value: pulumi.set(__self__, key, value),
            version=version,
            add_ons=add_ons,
            aws_provider=aws_provider,
            description=description,
            ephemeral_provider=ephemeral_provider,
            firewalls=firewalls,
            generic_provider=generic_provider,
            hetzner_provider=hetzner_provider,
            name=name,
            tags=tags,
        )
    @staticmethod
    def _configure(
             _setter: Callable[[Any, Any], None],
             version: pulumi.Input[str],
             add_ons: Optional[pulumi.Input['Mk8sAddOnsArgs']] = None,
             aws_provider: Optional[pulumi.Input['Mk8sAwsProviderArgs']] = None,
             description: Optional[pulumi.Input[str]] = None,
             ephemeral_provider: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']] = None,
             firewalls: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]] = None,
             generic_provider: Optional[pulumi.Input['Mk8sGenericProviderArgs']] = None,
             hetzner_provider: Optional[pulumi.Input['Mk8sHetznerProviderArgs']] = None,
             name: Optional[pulumi.Input[str]] = None,
             tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
             opts: Optional[pulumi.ResourceOptions]=None,
             **kwargs):
        if 'addOns' in kwargs:
            add_ons = kwargs['addOns']
        if 'awsProvider' in kwargs:
            aws_provider = kwargs['awsProvider']
        if 'ephemeralProvider' in kwargs:
            ephemeral_provider = kwargs['ephemeralProvider']
        if 'genericProvider' in kwargs:
            generic_provider = kwargs['genericProvider']
        if 'hetznerProvider' in kwargs:
            hetzner_provider = kwargs['hetznerProvider']

        _setter("version", version)
        if add_ons is not None:
            _setter("add_ons", add_ons)
        if aws_provider is not None:
            _setter("aws_provider", aws_provider)
        if description is not None:
            _setter("description", description)
        if ephemeral_provider is not None:
            _setter("ephemeral_provider", ephemeral_provider)
        if firewalls is not None:
            _setter("firewalls", firewalls)
        if generic_provider is not None:
            _setter("generic_provider", generic_provider)
        if hetzner_provider is not None:
            _setter("hetzner_provider", hetzner_provider)
        if name is not None:
            _setter("name", name)
        if tags is not None:
            _setter("tags", tags)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)

    @property
    @pulumi.getter(name="addOns")
    def add_ons(self) -> Optional[pulumi.Input['Mk8sAddOnsArgs']]:
        return pulumi.get(self, "add_ons")

    @add_ons.setter
    def add_ons(self, value: Optional[pulumi.Input['Mk8sAddOnsArgs']]):
        pulumi.set(self, "add_ons", value)

    @property
    @pulumi.getter(name="awsProvider")
    def aws_provider(self) -> Optional[pulumi.Input['Mk8sAwsProviderArgs']]:
        return pulumi.get(self, "aws_provider")

    @aws_provider.setter
    def aws_provider(self, value: Optional[pulumi.Input['Mk8sAwsProviderArgs']]):
        pulumi.set(self, "aws_provider", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Mk8s.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ephemeralProvider")
    def ephemeral_provider(self) -> Optional[pulumi.Input['Mk8sEphemeralProviderArgs']]:
        return pulumi.get(self, "ephemeral_provider")

    @ephemeral_provider.setter
    def ephemeral_provider(self, value: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']]):
        pulumi.set(self, "ephemeral_provider", value)

    @property
    @pulumi.getter
    def firewalls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]]:
        """
        Allow-list.
        """
        return pulumi.get(self, "firewalls")

    @firewalls.setter
    def firewalls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]]):
        pulumi.set(self, "firewalls", value)

    @property
    @pulumi.getter(name="genericProvider")
    def generic_provider(self) -> Optional[pulumi.Input['Mk8sGenericProviderArgs']]:
        return pulumi.get(self, "generic_provider")

    @generic_provider.setter
    def generic_provider(self, value: Optional[pulumi.Input['Mk8sGenericProviderArgs']]):
        pulumi.set(self, "generic_provider", value)

    @property
    @pulumi.getter(name="hetznerProvider")
    def hetzner_provider(self) -> Optional[pulumi.Input['Mk8sHetznerProviderArgs']]:
        return pulumi.get(self, "hetzner_provider")

    @hetzner_provider.setter
    def hetzner_provider(self, value: Optional[pulumi.Input['Mk8sHetznerProviderArgs']]):
        pulumi.set(self, "hetzner_provider", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Mk8s.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _Mk8sState:
    def __init__(__self__, *,
                 add_ons: Optional[pulumi.Input['Mk8sAddOnsArgs']] = None,
                 alias: Optional[pulumi.Input[str]] = None,
                 aws_provider: Optional[pulumi.Input['Mk8sAwsProviderArgs']] = None,
                 cpln_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ephemeral_provider: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']] = None,
                 firewalls: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]] = None,
                 generic_provider: Optional[pulumi.Input['Mk8sGenericProviderArgs']] = None,
                 hetzner_provider: Optional[pulumi.Input['Mk8sHetznerProviderArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 self_link: Optional[pulumi.Input[str]] = None,
                 statuses: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sStatusArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Mk8s resources.
        :param pulumi.Input[str] alias: The alias name of the Mk8s.
        :param pulumi.Input[str] cpln_id: The ID, in GUID format, of the Mk8s.
        :param pulumi.Input[str] description: Description of the Mk8s.
        :param pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]] firewalls: Allow-list.
        :param pulumi.Input[str] name: Name of the Mk8s.
        :param pulumi.Input[str] self_link: Full link to this resource. Can be referenced by other resources.
        :param pulumi.Input[Sequence[pulumi.Input['Mk8sStatusArgs']]] statuses: Status of the mk8s.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags.
        """
        _Mk8sState._configure(
            lambda key, value: pulumi.set(__self__, key, value),
            add_ons=add_ons,
            alias=alias,
            aws_provider=aws_provider,
            cpln_id=cpln_id,
            description=description,
            ephemeral_provider=ephemeral_provider,
            firewalls=firewalls,
            generic_provider=generic_provider,
            hetzner_provider=hetzner_provider,
            name=name,
            self_link=self_link,
            statuses=statuses,
            tags=tags,
            version=version,
        )
    @staticmethod
    def _configure(
             _setter: Callable[[Any, Any], None],
             add_ons: Optional[pulumi.Input['Mk8sAddOnsArgs']] = None,
             alias: Optional[pulumi.Input[str]] = None,
             aws_provider: Optional[pulumi.Input['Mk8sAwsProviderArgs']] = None,
             cpln_id: Optional[pulumi.Input[str]] = None,
             description: Optional[pulumi.Input[str]] = None,
             ephemeral_provider: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']] = None,
             firewalls: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]] = None,
             generic_provider: Optional[pulumi.Input['Mk8sGenericProviderArgs']] = None,
             hetzner_provider: Optional[pulumi.Input['Mk8sHetznerProviderArgs']] = None,
             name: Optional[pulumi.Input[str]] = None,
             self_link: Optional[pulumi.Input[str]] = None,
             statuses: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sStatusArgs']]]] = None,
             tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
             version: Optional[pulumi.Input[str]] = None,
             opts: Optional[pulumi.ResourceOptions]=None,
             **kwargs):
        if 'addOns' in kwargs:
            add_ons = kwargs['addOns']
        if 'awsProvider' in kwargs:
            aws_provider = kwargs['awsProvider']
        if 'cplnId' in kwargs:
            cpln_id = kwargs['cplnId']
        if 'ephemeralProvider' in kwargs:
            ephemeral_provider = kwargs['ephemeralProvider']
        if 'genericProvider' in kwargs:
            generic_provider = kwargs['genericProvider']
        if 'hetznerProvider' in kwargs:
            hetzner_provider = kwargs['hetznerProvider']
        if 'selfLink' in kwargs:
            self_link = kwargs['selfLink']

        if add_ons is not None:
            _setter("add_ons", add_ons)
        if alias is not None:
            _setter("alias", alias)
        if aws_provider is not None:
            _setter("aws_provider", aws_provider)
        if cpln_id is not None:
            _setter("cpln_id", cpln_id)
        if description is not None:
            _setter("description", description)
        if ephemeral_provider is not None:
            _setter("ephemeral_provider", ephemeral_provider)
        if firewalls is not None:
            _setter("firewalls", firewalls)
        if generic_provider is not None:
            _setter("generic_provider", generic_provider)
        if hetzner_provider is not None:
            _setter("hetzner_provider", hetzner_provider)
        if name is not None:
            _setter("name", name)
        if self_link is not None:
            _setter("self_link", self_link)
        if statuses is not None:
            _setter("statuses", statuses)
        if tags is not None:
            _setter("tags", tags)
        if version is not None:
            _setter("version", version)

    @property
    @pulumi.getter(name="addOns")
    def add_ons(self) -> Optional[pulumi.Input['Mk8sAddOnsArgs']]:
        return pulumi.get(self, "add_ons")

    @add_ons.setter
    def add_ons(self, value: Optional[pulumi.Input['Mk8sAddOnsArgs']]):
        pulumi.set(self, "add_ons", value)

    @property
    @pulumi.getter
    def alias(self) -> Optional[pulumi.Input[str]]:
        """
        The alias name of the Mk8s.
        """
        return pulumi.get(self, "alias")

    @alias.setter
    def alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alias", value)

    @property
    @pulumi.getter(name="awsProvider")
    def aws_provider(self) -> Optional[pulumi.Input['Mk8sAwsProviderArgs']]:
        return pulumi.get(self, "aws_provider")

    @aws_provider.setter
    def aws_provider(self, value: Optional[pulumi.Input['Mk8sAwsProviderArgs']]):
        pulumi.set(self, "aws_provider", value)

    @property
    @pulumi.getter(name="cplnId")
    def cpln_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID, in GUID format, of the Mk8s.
        """
        return pulumi.get(self, "cpln_id")

    @cpln_id.setter
    def cpln_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cpln_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Mk8s.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="ephemeralProvider")
    def ephemeral_provider(self) -> Optional[pulumi.Input['Mk8sEphemeralProviderArgs']]:
        return pulumi.get(self, "ephemeral_provider")

    @ephemeral_provider.setter
    def ephemeral_provider(self, value: Optional[pulumi.Input['Mk8sEphemeralProviderArgs']]):
        pulumi.set(self, "ephemeral_provider", value)

    @property
    @pulumi.getter
    def firewalls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]]:
        """
        Allow-list.
        """
        return pulumi.get(self, "firewalls")

    @firewalls.setter
    def firewalls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sFirewallArgs']]]]):
        pulumi.set(self, "firewalls", value)

    @property
    @pulumi.getter(name="genericProvider")
    def generic_provider(self) -> Optional[pulumi.Input['Mk8sGenericProviderArgs']]:
        return pulumi.get(self, "generic_provider")

    @generic_provider.setter
    def generic_provider(self, value: Optional[pulumi.Input['Mk8sGenericProviderArgs']]):
        pulumi.set(self, "generic_provider", value)

    @property
    @pulumi.getter(name="hetznerProvider")
    def hetzner_provider(self) -> Optional[pulumi.Input['Mk8sHetznerProviderArgs']]:
        return pulumi.get(self, "hetzner_provider")

    @hetzner_provider.setter
    def hetzner_provider(self, value: Optional[pulumi.Input['Mk8sHetznerProviderArgs']]):
        pulumi.set(self, "hetzner_provider", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Mk8s.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> Optional[pulumi.Input[str]]:
        """
        Full link to this resource. Can be referenced by other resources.
        """
        return pulumi.get(self, "self_link")

    @self_link.setter
    def self_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "self_link", value)

    @property
    @pulumi.getter
    def statuses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sStatusArgs']]]]:
        """
        Status of the mk8s.
        """
        return pulumi.get(self, "statuses")

    @statuses.setter
    def statuses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['Mk8sStatusArgs']]]]):
        pulumi.set(self, "statuses", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class Mk8s(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_ons: Optional[pulumi.Input[pulumi.InputType['Mk8sAddOnsArgs']]] = None,
                 aws_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sAwsProviderArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ephemeral_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sEphemeralProviderArgs']]] = None,
                 firewalls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sFirewallArgs']]]]] = None,
                 generic_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sGenericProviderArgs']]] = None,
                 hetzner_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sHetznerProviderArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Mk8s resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the Mk8s.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sFirewallArgs']]]] firewalls: Allow-list.
        :param pulumi.Input[str] name: Name of the Mk8s.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Mk8sArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Mk8s resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param Mk8sArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(Mk8sArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            kwargs = kwargs or {}
            def _setter(key, value):
                kwargs[key] = value
            Mk8sArgs._configure(_setter, **kwargs)
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 add_ons: Optional[pulumi.Input[pulumi.InputType['Mk8sAddOnsArgs']]] = None,
                 aws_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sAwsProviderArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 ephemeral_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sEphemeralProviderArgs']]] = None,
                 firewalls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sFirewallArgs']]]]] = None,
                 generic_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sGenericProviderArgs']]] = None,
                 hetzner_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sHetznerProviderArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = Mk8sArgs.__new__(Mk8sArgs)

            if add_ons is not None and not isinstance(add_ons, Mk8sAddOnsArgs):
                add_ons = add_ons or {}
                def _setter(key, value):
                    add_ons[key] = value
                Mk8sAddOnsArgs._configure(_setter, **add_ons)
            __props__.__dict__["add_ons"] = add_ons
            if aws_provider is not None and not isinstance(aws_provider, Mk8sAwsProviderArgs):
                aws_provider = aws_provider or {}
                def _setter(key, value):
                    aws_provider[key] = value
                Mk8sAwsProviderArgs._configure(_setter, **aws_provider)
            __props__.__dict__["aws_provider"] = aws_provider
            __props__.__dict__["description"] = description
            if ephemeral_provider is not None and not isinstance(ephemeral_provider, Mk8sEphemeralProviderArgs):
                ephemeral_provider = ephemeral_provider or {}
                def _setter(key, value):
                    ephemeral_provider[key] = value
                Mk8sEphemeralProviderArgs._configure(_setter, **ephemeral_provider)
            __props__.__dict__["ephemeral_provider"] = ephemeral_provider
            __props__.__dict__["firewalls"] = firewalls
            if generic_provider is not None and not isinstance(generic_provider, Mk8sGenericProviderArgs):
                generic_provider = generic_provider or {}
                def _setter(key, value):
                    generic_provider[key] = value
                Mk8sGenericProviderArgs._configure(_setter, **generic_provider)
            __props__.__dict__["generic_provider"] = generic_provider
            if hetzner_provider is not None and not isinstance(hetzner_provider, Mk8sHetznerProviderArgs):
                hetzner_provider = hetzner_provider or {}
                def _setter(key, value):
                    hetzner_provider[key] = value
                Mk8sHetznerProviderArgs._configure(_setter, **hetzner_provider)
            __props__.__dict__["hetzner_provider"] = hetzner_provider
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__.__dict__["version"] = version
            __props__.__dict__["alias"] = None
            __props__.__dict__["cpln_id"] = None
            __props__.__dict__["self_link"] = None
            __props__.__dict__["statuses"] = None
        super(Mk8s, __self__).__init__(
            'cpln:index/mk8s:Mk8s',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            add_ons: Optional[pulumi.Input[pulumi.InputType['Mk8sAddOnsArgs']]] = None,
            alias: Optional[pulumi.Input[str]] = None,
            aws_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sAwsProviderArgs']]] = None,
            cpln_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            ephemeral_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sEphemeralProviderArgs']]] = None,
            firewalls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sFirewallArgs']]]]] = None,
            generic_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sGenericProviderArgs']]] = None,
            hetzner_provider: Optional[pulumi.Input[pulumi.InputType['Mk8sHetznerProviderArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            self_link: Optional[pulumi.Input[str]] = None,
            statuses: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sStatusArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            version: Optional[pulumi.Input[str]] = None) -> 'Mk8s':
        """
        Get an existing Mk8s resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alias: The alias name of the Mk8s.
        :param pulumi.Input[str] cpln_id: The ID, in GUID format, of the Mk8s.
        :param pulumi.Input[str] description: Description of the Mk8s.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sFirewallArgs']]]] firewalls: Allow-list.
        :param pulumi.Input[str] name: Name of the Mk8s.
        :param pulumi.Input[str] self_link: Full link to this resource. Can be referenced by other resources.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['Mk8sStatusArgs']]]] statuses: Status of the mk8s.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _Mk8sState.__new__(_Mk8sState)

        __props__.__dict__["add_ons"] = add_ons
        __props__.__dict__["alias"] = alias
        __props__.__dict__["aws_provider"] = aws_provider
        __props__.__dict__["cpln_id"] = cpln_id
        __props__.__dict__["description"] = description
        __props__.__dict__["ephemeral_provider"] = ephemeral_provider
        __props__.__dict__["firewalls"] = firewalls
        __props__.__dict__["generic_provider"] = generic_provider
        __props__.__dict__["hetzner_provider"] = hetzner_provider
        __props__.__dict__["name"] = name
        __props__.__dict__["self_link"] = self_link
        __props__.__dict__["statuses"] = statuses
        __props__.__dict__["tags"] = tags
        __props__.__dict__["version"] = version
        return Mk8s(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addOns")
    def add_ons(self) -> pulumi.Output[Optional['outputs.Mk8sAddOns']]:
        return pulumi.get(self, "add_ons")

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        The alias name of the Mk8s.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="awsProvider")
    def aws_provider(self) -> pulumi.Output[Optional['outputs.Mk8sAwsProvider']]:
        return pulumi.get(self, "aws_provider")

    @property
    @pulumi.getter(name="cplnId")
    def cpln_id(self) -> pulumi.Output[str]:
        """
        The ID, in GUID format, of the Mk8s.
        """
        return pulumi.get(self, "cpln_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Mk8s.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="ephemeralProvider")
    def ephemeral_provider(self) -> pulumi.Output[Optional['outputs.Mk8sEphemeralProvider']]:
        return pulumi.get(self, "ephemeral_provider")

    @property
    @pulumi.getter
    def firewalls(self) -> pulumi.Output[Optional[Sequence['outputs.Mk8sFirewall']]]:
        """
        Allow-list.
        """
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter(name="genericProvider")
    def generic_provider(self) -> pulumi.Output[Optional['outputs.Mk8sGenericProvider']]:
        return pulumi.get(self, "generic_provider")

    @property
    @pulumi.getter(name="hetznerProvider")
    def hetzner_provider(self) -> pulumi.Output[Optional['outputs.Mk8sHetznerProvider']]:
        return pulumi.get(self, "hetzner_provider")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Mk8s.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> pulumi.Output[str]:
        """
        Full link to this resource. Can be referenced by other resources.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter
    def statuses(self) -> pulumi.Output[Sequence['outputs.Mk8sStatus']]:
        """
        Status of the mk8s.
        """
        return pulumi.get(self, "statuses")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "version")

