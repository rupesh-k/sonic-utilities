import click
<<<<<<< ours
from show.main import *
=======
from show.main import get_bgp_summary_extended, ip, multi_instance_bgp_summary, run_command
from show.multi_npu import  multi_npu_platform, multi_npu_options

>>>>>>> theirs


###############################################################################
#
# 'show ip bgp' cli stanza
#
###############################################################################


@ip.group(cls=AliasedGroup, default_if_no_args=False)
def bgp():
    """Show IPv4 BGP (Border Gateway Protocol) information"""
    pass


# 'summary' subcommand ("show ip bgp summary")
@bgp.command()
@multi_npu_options
def summary(namespace, display):
    """Show summarized information of IPv4 BGP state"""
    if multi_npu_platform():
        multi_instance_bgp_summary(namespace, display, 'v4')
        return
    try:
        device_output = run_command('sudo vtysh -c "show ip bgp summary"', return_cmd=True)
        get_bgp_summary_extended(device_output)
    except:
        run_command('sudo vtysh -c "show ip bgp summary"')


# 'neighbors' subcommand ("show ip bgp neighbors")
@bgp.command()
@click.argument('ipaddress', required=False)
@click.argument('info_type', type=click.Choice(['routes', 'advertised-routes', 'received-routes']), required=False)
def neighbors(ipaddress, info_type):
    """Show IP (IPv4) BGP neighbors"""

    command = 'sudo vtysh -c "show ip bgp neighbor'

    if ipaddress is not None:
        command += ' {}'.format(ipaddress)

        # info_type is only valid if ipaddress is specified
        if info_type is not None:
            command += ' {}'.format(info_type)

    command += '"'

    run_command(command)
