import argparse

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError
from ..utils import t_or_f_or_n


class NodeGroupsCreateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ng_params = values.split(',')
        ng_dict = {
            'node_type': None,
            'node_count': None,
            'flavor_id': None
        }
        for param in ng_params:
            key, value = param.split('=')
            ng_dict[key] = value

        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(ng_dict)


class NodeGroupsResizeAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ng_params = values.split(',')
        ng_dict = {
            'id': None,
            'node_count': None,
        }
        for param in ng_params:
            key, value = param.split('=')
            ng_dict[key] = value

        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(ng_dict)


class NodeGroupsDeleteAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ng_params = values.split(',')
        ng_dict = {
            'id': None,
        }
        for param in ng_params:
            key, value = param.split('=')
            ng_dict[key] = value

        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(ng_dict)


class ListClusterCoes(Lister):
    """List Cluster Coes."""
    schema = schemas.CoeSchema(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/clusters/coes')

        return data


class ListClusterTemplate(Lister):
    """List Cluster Template."""
    schema = schemas.ClusterTemplateSchema(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/clusters/templates')

        return data


class ShowClusterTemplate(ShowOne):
    """Show Cluster Template details."""
    schema = schemas.ClusterTemplateSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowClusterTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template',
            metavar='<template>',
            help='Template name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/clusters/templates/%s' % parsed_args.template
        data = self.app.session.get(uri)

        return data


class DeleteClusterTemplate(Command):
    """Delete template."""

    def get_parser(self, prog_name):
        parser = super(DeleteClusterTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'template',
            metavar='<template>',
            help='Cluster Template name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/clusters/templates/%s' % parsed_args.template
        self.app.session.delete(uri)


class CreateClusterTemplate(ShowOne):
    """Create ClusterTemplate."""
    schema = schemas.ClusterTemplateSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(CreateClusterTemplate, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Cluster Template name'
        )
        parser.add_argument(
            '--coe',
            required=True,
            metavar='<Coe>',
            help='Set coe, could be kubernetes or docker',
        )
        parser.add_argument(
            '--coe-version',
            required=True,
            metavar='<CoeVersion>',
            help='Set coe version, could be get from coe list',
        )
        parser.add_argument(
            '--image-id',
            required=True,
            metavar='<ImageId>',
            help='Image ID for cluster',
        )
        parser.add_argument(
            '--ssh-key-id',
            required=True,
            metavar='<SshKeyId>',
            help='Set ssh key for cluster template',
        )
        parser.add_argument(
            '--dns-nameservers',
            metavar='<DnsNameServers>',
            action='append',
            dest='dns_name_servers',
            help="DNS server for cluster"
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'coe': parsed_args.coe,
            'coe_version': parsed_args.coe_version,
            'image_id': parsed_args.image_id,
            'ssh_key_id': parsed_args.ssh_key_id,
            'dns_nameservers': parsed_args.dns_name_servers,
        }

        data = self.app.session.post('/clusters/templates', payload)

        return data


class CreateCluster(ShowOne):
    """Create Cluster."""
    schema = schemas.ClusterSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(CreateCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='ClusterTemplate name'
        )
        parser.add_argument(
            '--cluster-template-id',
            required=True,
            metavar='<ClusterTemplateId>',
            help='Set cluster template id, could be get from cluster template list',
        )
        parser.add_argument(
            '--node-groups',
            action=NodeGroupsCreateAction,
            required=True,
            help='Node groups in the format '
                 'node_type=value,'
                 'node_count=value,'
                 'flavor_id=value',
        )
        parser.add_argument(
            '--cidr',
            required=True,
            metavar='<Cidr>',
            help='Set cidr for cluster',
        )
        parser.add_argument(
            '--service-domain',
            required=True,
            metavar='<ServiceDomain>',
            help='Set cidr for service domain',
        )
        parser.add_argument(
            '--service-cidr',
            metavar='<ServiceCidr>',
            action='append',
            dest='service_cidr',
            help="Set cidr for service cidr"
        )
        parser.add_argument(
            '--dns-nameservers',
            metavar='<DnsNameServers>',
            action='append',
            dest='dns_name_servers',
            help="DNS server for cluster"
        )
        parser.add_argument(
            '--ingress',
            metavar='<Ingress>',
            type=t_or_f_or_n,
            help="Ingress for cluster, true or false respectively. "
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'cluster_template_id': parsed_args.cluster_template_id,
            'node_groups': parsed_args.node_groups,
            'cidr': parsed_args.cidr,
            'service_domain': parsed_args.service_domain,
        }

        if parsed_args.service_cidr:
            payload['service_cidr'] = parsed_args.service_cidr

        if parsed_args.dns_name_servers:
            payload['dns_nameservers'] = parsed_args.dns_name_servers

        if parsed_args.ingress is not None:
            payload['ingress_enabled'] = parsed_args.ingress

        data = self.app.session.post('/clusters', payload)

        return data


class ListClusters(Lister):
    """List Cluster."""
    schema = schemas.ClusterSchema(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/clusters')

        return data


class ShowCluster(ShowOne):
    """Show Cluster details."""
    schema = schemas.ClusterSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowCluster, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            metavar='<identifier>',
            help='Cluster name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/clusters/%s' % parsed_args.identifier
        data = self.app.session.get(uri)

        return data


class AddAnotherNodeGroupCluster(ShowOne):
    """Add NodeGroup Cluster."""
    schema = schemas.ClusterSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(AddAnotherNodeGroupCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name_or_id',
            metavar='<name_or_id>',
            help='Cluster name or id'
        )
        parser.add_argument(
            '--node-groups',
            action=NodeGroupsCreateAction,
            required=True,
            help='Node groups in the format '
                 'node_type=value,'
                 'node_count=value,'
                 'flavor_id=value',
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'node_groups': parsed_args.node_groups,
        }

        data = self.app.session.post(f'/clusters/{parsed_args.name_or_id}/node-groups', payload)

        return data


class DeleteNodeGroupCluster(ShowOne):
    """Delete NodeGroup Cluster."""
    schema = schemas.ClusterSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(DeleteNodeGroupCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name_or_id',
            metavar='<name_or_id>',
            help='Cluster name or id'
        )
        parser.add_argument(
            '--node-groups',
            action=NodeGroupsDeleteAction,
            required=True,
            help='Node groups in the format '
                 'id=value'
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'node_groups': parsed_args.node_groups,
        }

        data = self.app.session.delete(f'/clusters/{parsed_args.name_or_id}/node-groups', payload)

        return data


class NodeGroupResizeCluster(ShowOne):
    """Resize Cluster."""
    schema = schemas.ClusterSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(NodeGroupResizeCluster, self).get_parser(prog_name)
        parser.add_argument(
            'name_or_id',
            metavar='<name_or_id>',
            help='Cluster name or id'
        )
        parser.add_argument(
            '--node-groups',
            action=NodeGroupsResizeAction,
            required=True,
            help='Node groups in the format '
                 'id=value,'
                 'node_count=value'
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'node_groups': parsed_args.node_groups,
        }

        data = self.app.session.patch(f'/clusters/{parsed_args.name_or_id}/node-groups', payload)

        return data


class ShowKubeConfigCluster(ShowOne):
    """Show Cluster KubeConfig."""
    schema = schemas.ClusterKubeConfigSchema(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowKubeConfigCluster, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            metavar='<identifier>',
            help='Cluster name or ID',
        )
        parser.add_argument(
            '--output',
            metavar='<output>',
            required=True,
            help='File path to save'
        )
        return parser

    def get_data(self, parsed_args):
        uri = f'/clusters/{parsed_args.identifier}/kube-config'
        data = self.app.session.get(uri)

        if data.get('value'):
            config = open(parsed_args.output, "w")
            config.write(data.get('value'))
            config.close()

        return data
