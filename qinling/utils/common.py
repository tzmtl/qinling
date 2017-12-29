# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import functools
import sys
import warnings

from oslo_utils import uuidutils
import six

from qinling import version


def print_server_info(service):
    QINLING_TITLE = r"""
                                    /^L_      ,."\
               /~\       __       /~    \   ./    \
              /   _\   _/  \     /T~\|~\_\ / \_  /~|          _^
            / \ /W  \ / V^\/X  /~         T  . \/   \    ,v-./
     ,'`-. /~   ^     H  ,  . \/    ;   .   \      `. \-'   /
         M      ~     | . ;  /         ,  _   :  .    ~\_,-'
        /    ~    .    \    /   :                   '   \   ,/`
       I o. ^    oP     '98b         -      _  9.`       `\9b.
     8oO888.  oO888P  d888b9bo. .8o 888o.       8bo.  o     988o.
     88888888888888888888888888bo.98888888bo.    98888bo. .d888P
     88888888888888888888888888888888888888888888888888888888888
                         _          __   _
                 ___ _  (_)  ___   / /  (_)  ___   ___ _
                / _ `/ / /  / _ \ / /  / /  / _ \ / _ `/
                \_, / /_/  /_//_//_/  /_/  /_//_/ \_, /
                 /_/                             /___/

    Function as a Service in OpenStack, version: %s
    """ % version.version_string()

    print(QINLING_TITLE)
    print('Launching server components %s...' % service)


def get_properly_ordered_parameters():
    """Orders launch parameters in the right order.

    In oslo it's important the order of the launch parameters.
    if --config-file came after the command line parameters the command
    line parameters are ignored.
    So to make user command line parameters are never ignored this method
    moves --config-file to be always first.
    """
    args = sys.argv[1:]

    for arg in sys.argv[1:]:
        if arg == '--config-file' or arg.startswith('--config-file='):
            if "=" in arg:
                conf_file_value = arg.split("=", 1)[1]
            else:
                conf_file_value = args[args.index(arg) + 1]
                args.remove(conf_file_value)
            args.remove(arg)
            args.insert(0, "--config-file")
            args.insert(1, conf_file_value)

    return args


def convert_dict_to_string(d):
    temp_list = ['%s=%s' % (k, v) for k, v in d.items()]

    return ','.join(temp_list)


def datetime_to_str(dct, attr_name):
    """Convert datetime object in dict to string."""
    if (dct.get(attr_name) is not None and
            not isinstance(dct.get(attr_name), six.string_types)):
        dct[attr_name] = dct[attr_name].isoformat(' ')


def generate_unicode_uuid(dashed=True):
    return uuidutils.generate_uuid(dashed=dashed)


def disable_ssl_warnings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="A true SSLContext object is not available"
            )
            warnings.filterwarnings(
                "ignore",
                message="Unverified HTTPS request is being made"
            )
            return func(*args, **kwargs)

    return wrapper
