import charms.reactive as reactive
import charmhelpers.core.hookenv as hookenv

# This charm's library contains all of the handler code associated with
# virtual_accelerator
import charm.openstack.virtual_accelerator as virtual_accelerator


# use a synthetic state to ensure that it get it to be installed independent of
# the install hook.

@reactive.when_not('charm.installed')
def install_packages():
    virtual_accelerator.install()
    virtual_accelerator.delete_default_virsh_nets()
    virtual_accelerator.install_credentials()
    reactive.set_state('charm.installed')

@reactive.when('charm.installed')
def install_license():
    virtual_accelerator.install_license()
    virtual_accelerator.generate_fast_path_env()

@reactive.when('neutron-control.connected')
def check_connected(neutron_control):
    neutron_control.request_restart()

@reactive.when('neutron-plugin.connected')
def configure_neutron_plugin(neutron_plugin):
    neutron_plugin.configure_plugin(
        plugin='ovs',
        config={
            "nova-compute": {
                "/etc/nova/nova.conf": {
                    "sections": {
                        'DEFAULT': [
                            ('monkey_patch', 'true'),
                            ('monkey_patch_modules', 'nova.virt.libvirt.vif:openstack_6wind_extensions.liberty.nova.virt.libvirt.vif.decorator'),
                        ],
                    }
                }
            }
        })
