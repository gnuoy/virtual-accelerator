import charmhelpers.contrib.openstack.utils as ch_utils
import charmhelpers.fetch as  fetch

import charms_openstack.charm
import charms_openstack.adapters
import charms_openstack.ip as os_ip

def install():
    """Use the singleton from the VirtualAcceleratorCharm to install the packages on the
    unit
    """
    VirtualAcceleratorCharm.singleton.install()

def delete_default_virsh_nets():
    """Use the singleton from the VirtualAcceleratorCharm to delete default virsh net
    """
    VirtualAcceleratorCharm.singleton.delete_default_virsh_nets()

def install_credentials():
    """Use the singleton from the VirtualAcceleratorCharm to install creds"""
    VirtualAcceleratorCharm.singleton.install_credentials()

def install_license():
    """Use the singleton from the VirtualAcceleratorCharm to install license """
    VirtualAcceleratorCharm.singleton.install_license()

def generate_fast_path_env():
    """Use the singleton from the VirtualAcceleratorCharm to genertae generate_fast_path_env"""
    VirtualAcceleratorCharm.singleton.generate_fast_path_env()


class VirtualAcceleratorCharm(charms_openstack.charm.OpenStackCharm):

    # name of service to register into keystone
    service_name = 'vitrualaccelerator'

    # Internal name of charm - used for HA support + others
    name = 'vitrualaccelerator'

    # First release of openstack this charm supports
    release = 'mitaka'

    # Packages the service needs installed
    packages = ['libvirt-bin', 'python-libvirt', 'qemu', 'qemu-system-x86']

    # Init services the charm manages
    services = []

    # Standard interface adapters class to use.
    adapters_class = charms_openstack.adapters.OpenStackRelationAdapters

    # Ports that need exposing.
    default_service = ''

    # The restart map defines which services should be restarted when a given
    # file changes
    restart_map = {}

    def __init__(self, release=None, **kwargs):
        """Custom initialiser for class
        If no release is passed, then the charm determines the release from the
        ch_utils.os_release() function.
        """
        if release is None:
            release = 'mitaka'
        super(VirtualAcceleratorCharm, self).__init__(release=release, **kwargs)

    def install(self):
        """Customise the installation, configure the source and then call the
        parent install() method to install the packages
        """
 
        fetch.add_source('ppa:6wind/virt-mq-ppa')
        fetch.apt_install(self.packages, options=['--option=Dpkg::Options::=--force-confnew'])

    def delete_default_virsh_nets(self):
        """Delete the default virsh network"""
        pass

    def install_credentials(self):
        """Fetching and install the 6WIND repo package"""
        pass

    def install_license(self):
        """Fetching and install the license"""
        pass

    def generate_fast_path_env(self):
        """Generate fast-path.env"""
        # Note: Consider using a contextmanager here to get a sha of the config before and
        #       generation so that virtual-accelerator is only restarted when the file changes.
        pass
