"""
    DigiCloud Compute Instance Service.
"""
from rich.prompt import Confirm

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..utils import is_tty

class ListDatastore(Lister):
    """List datastore."""
    schema = schemas.DbaasDatastoreList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/dbaas/datastores')

        datastores = []
        for datastore in data:
            for version in datastore['versions']:
                datastores.append({
                    'name': datastore['name'],
                    'version': version['name'],
                })

        return datastores


class ListInstance(Lister):
    """List database instance."""
    schema = schemas.DbaasInstanceList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/dbaas/instances')
        return data


class CreateInstance(ShowOne):
    """Create database Instance."""
    schema = schemas.DbaasInstanceDetails()

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Database Instance name'
        )
        parser.add_argument(
            '--instance-type',
            required=True,
            metavar='<instance_type>',
            help='InstanceType name or ID'
        )
        parser.add_argument(
            '--volume-size',
            required=True,
            type=int,
            metavar='<volume_size>'
        )
        parser.add_argument(
            '--volume-type',
            required=False,
            metavar='<volume_type>',
            choices=['SSD', 'ULTRA_DISK'],
            type=lambda value: str(value).upper().replace("-", "_"),
            help=(
                'Optionally you can set the type of root volume, '
                'could be SSD or ULTRA_DISK case insensitive, the default is SSD'
            )
        )
        parser.add_argument(
            '--network',
            required=True,
            metavar='<network>',
            help='Network name or ID'
        )
        parser.add_argument(
            '--datastore-name',
            metavar='<datastore_name>',
            required=True,
            help='Datastore name',
        )
        parser.add_argument(
            '--datastore-version',
            metavar='<datastore_version>',
            required=True,
            help='Datastore version',
        )
        parser.add_argument(
            '--is-public',
            required=False,
            help='Whether the database service is exposed to the public',
            action = 'store_true'
        )
        parser.add_argument(
            '--allow-cidr',
            required=False,
            metavar='<allow_cidr>',
            help='A list of IPv4 that restrict access to the database service. 0.0.0.0/0 is used by default if this parameter is not provided.',
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'instance_type': parsed_args.instance_type,
            'network': parsed_args.network,
            'datastore_name': parsed_args.datastore_name,
            'datastore_version': parsed_args.datastore_version,
            'volume_type': parsed_args.volume_type,
            'volume_size': parsed_args.volume_size,
        }
        if parsed_args.is_public:
            payload['is_public'] = parsed_args.is_public
        if parsed_args.allow_cidr:
            payload['allow_cidr'] = parsed_args.allow_cidr

        data = self.app.session.post('/dbaas/instances', payload)
        return data


class ShowInstance(ShowOne):
    """Show database instance details."""
    schema = schemas.DbaasInstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ShowInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Database instance name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/dbaas/instances/%s' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class DeleteInstance(Command):
    """Delete a  database instance."""

    def get_parser(self, prog_name):
        parser = super(DeleteInstance, self).get_parser(prog_name)

        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        uri = '/dbaas/instances/%s' % parsed_args.instance
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            instance = self.app.session.get('/dbaas/instances/%s' % parsed_args.instance)
            user_response = Confirm.ask(
                "You're about to delete a database instance named "
                "[red bold]{}[/red bold]. "
                "Are you sure?".format(
                    instance['name'],
                ))
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete database instance' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False


class ListDatabase(Lister):
    """List database instance."""
    schema = schemas.DbaasDatabaseList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListDatabase, self).get_parser(prog_name)

        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/dbaas/instances/%s/databases' % (parsed_args.instance)
        data = self.app.session.get(uri)
        return data


class CreateDatabase(ShowOne):
    """Create dbass db."""
    schema = schemas.DbaasDatabaseDetails()

    def get_parser(self, prog_name):
        parser = super(CreateDatabase, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Database name'
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
        }

        uri = '/dbaas/instances/%s/databases' % (parsed_args.instance)
        data = self.app.session.post(uri, payload)
        return data


class DeleteDatabase(Command):
    """Delete dbass db."""

    def get_parser(self, prog_name):
        parser = super(DeleteDatabase, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Database Instance name'
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        uri = '/dbaas/instances/%s/databases/%s' % (parsed_args.instance, parsed_args.name)
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete a database, "
                "Are you sure?")
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete database' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False

class ListUser(Lister):
    """List database users."""
    schema = schemas.DbaasUserList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListUser, self).get_parser(prog_name)

        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/dbaas/instances/%s/users' % (parsed_args.instance)
        data = self.app.session.get(uri)
        return data


class CreateUser(ShowOne):
    """Create dbass user."""
    schema = schemas.DbaasUserDetails()

    def get_parser(self, prog_name):
        parser = super(CreateUser, self).get_parser(prog_name)
        parser.add_argument(
            '--instance',
            metavar='<instance>',
            help='instance name or id'
        )
        parser.add_argument(
            '--username',
            metavar='<username>',
            help='Database username'
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            help='Database password'
        )
        parser.add_argument(
            '--host',
            required=False,
            metavar='<host>',
            help='host'
        )
        parser.add_argument(
            '--databases',
            dest='databases',
            help='list of databases',
            required=False
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.username,
            'password': parsed_args.password,
        }
        if parsed_args.host:
            payload['host'] = parsed_args.host
        if parsed_args.databases:
            payload['databases'] =  parsed_args.databases.split(',')

        uri = '/dbaas/instances/%s/users' % (parsed_args.instance)
        data = self.app.session.post(uri, payload)
        return data


class DeleteUser(Command):
    """Delete dbass user."""

    def get_parser(self, prog_name):
        parser = super(DeleteUser, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Database username'
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        uri = '/dbaas/instances/%s/users/%s' % (parsed_args.instance, parsed_args.name)
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete a database user, "
                "Are you sure?")
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete database user' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False