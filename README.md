# f5-vagrant-file

Vagrantfiles that can be used to instantiate BIG-IP instances from Vagrant boxes

## About

These directories contain Vagrantfiles that you can use to create instances
of BIG-IP for purposes such as development of tools that integrate with BIG-IP.

The requirements to create these BIG-IP instances is a pre-created Vagrant box
that you have made from the ISOs available at F5's download site here

  * https://downloads.f5.com

Using the Packer templates available from this project's sister project found
here

  * https://github.com/f5devcentral/f5-packer-templates

If you are familiar with a BIG-IPs licensing restrictions and Vagrant, you
will say to yourself

    but BIG-IP wont accept my license when I 'vagrant up' a second time

And you will be right!

There are three options here

  * Get iWorkflow and buy a pool of licenses to activate against
  * Use a single license and call F5 support every time you need to 'vagrant up'
  * Request that F5 begin selling "recycleable" developer licenses
  
Those options are all probably less than ideal, but I don't make the rules.

## Support

I guarantee that you will find no help from F5 official support. I'm
putting this repository out there simply as a proof of concept.

If something doesn't work, you're free to raise Issues in Github here, but
I may not respond to them immediately, or at all.

## Instructions

Refer to the README.md files in each of the directories. While I have outlined
a fairly consistent set of steps in each Vagrantfile, you are free to add your
own customizations as needed.

Some things to note.

  * Virtualbox Guest Additions are not installed, nor available for BIG-IP. As
    a consequence of this, some more integrative features of Virtualbox are
    unavailable such as Shared Directories. I have deliberately turned this
    functionality off in the Vagrantfile.
  * Licensing is expected to be done has an environment variable provided at
    runtime. You're free to change this and embed your license key if you want.
    I left it off because in our own tolling we do not provide it so-as not to
    "accidentally" commit it to SCM.
  * The Vagrant box is expected to be on your filesystem in the Vagrantfile's
    directory. Of course, this is only a matter of implementation details. You
    can, of course, plop your Vagrant boxes on a local webserver or any other
    accessible destination that is supported by Vagrant and change the Vagrantfile's
    URL to use that. This is how we host boxes internally so that they are
    available to any developer who needs them.

## More releases

As new releases of BIG-IP happen (Hotfixes and major releases) I will update
the Vagrantfiles here. Do not expect a new template to land until after the
official F5 release.

If you have interest in a release that is not found in this repo, and is listed
as supported by F5 at our releases SOL5903 page here

  * https://support.f5.com/kb/en-us/solutions/public/5000/900/sol5903.html
  
Then open an issue on Github and I will address it.

## Required vagrant version

I always use the latest version, so use that. I boot these images on a Mac, but
we have build systems that do it on Linux as well. Frankly, it should work without
issue on any platform that vagrant is supported on.