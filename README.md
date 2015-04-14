# About

This is a [SCons](http://www.scons.org) tool that helps working with
boost if the host os supports it.

# Installation

You will need to clone this Git repository and then possibly additionally
provide some links. SCons has a number of ways of adding new tools depending
on whether you want them available only for a single project, for all the
projects of an individual user, or for all projects on a given system. The
location to which the clone should be made depends on which of these
situations you want to support.

Whichever location you choose the command will be:

    $ git clone https://github.com/manuelnaranjo/scons-boost-config.git boost-config

The name of the target directory will become the name of the tool for your
situation. In this case _boost-config_ is the target directory name and hence
_boost-config_ will be the name of the tool.

# Usage

Currently there are a few methods provided by this tool, in any case you first
need to initialize the tool

    e = Environment(tools=['boost-config'])

Another alternative is

    e = Environment(...)
    ...
    e.Tool('boost-config')

Now you you will find two new methods in the Configure environment:
_BjamSupported_ and _BoostVersionCheck_.

## Configure methods

### BjamSupported

This method allows testing if bjam is supported in the current environment

    e = Environment(tools=['boost-config'])
    c = e.Configure()
    if c.BjamSupported():
        print 'bjam supported'
    ...
    c.Finish()

### BoostVersionCheck

This method checks if available boost headers matches at least the given version
number

    ...
    if c.BoostVersionCheck('1.53'):
        print 'boost-1.53 headers supported'
    if c.BoostVersionCheck():
        print 'boost-1.54+ headers supported'
    ...
