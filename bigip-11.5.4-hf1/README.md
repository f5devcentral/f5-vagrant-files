# BIGIP 11.5.4.1.0.286-HF1 Vagrant box

This Vagrantfile can be used to start a BIG-IP vagrant box for version
11.5.4 HF1.

## Requirements

This Vagrantfile requires that following be installed on the machine the
vagrant command is run on.

  * Virtualbox
  * Vagrant
  * A valid license for BIG-IP

## Usage

After creating a Vagrant box using the associated packer file found
[here](https://github.com/f5devcentral/f5-packer-templates/tree/master/bigip-11.5.4-hf1-x86_64-box),
take the created box 

  * BIGIP-11.5.4.1.0.286-HF1.box

and place it in this directory alongside the Vagrantfile.

Next, run the following command

  BIGIP_LICENSE=xxxx-xxxx-xxxx-xxxx-xxxxxxx vagrant up

and wait for it to finish. The resulting instance of BIG-IP will be
available via CLI and Web UI

## Connecting

To connect to the CLI, use either `vagrant ssh`, or open the VM in Virtualbox
by double clicking its entry in the list of VMs

To connect to the web UI, follow this link

  * https://localhost:10443/