[![Travis CI](https://travis-ci.org/PyBossa/pbs.png?branch=master)](https://travis-ci.org/#!/PyBossa/pbs)  [![Coverage Status](https://coveralls.io/repos/PyBossa/pbs/badge.png)](https://coveralls.io/r/PyBossa/pbs?branch=master)


PBS - a PyBossa command line interface
======================================

**pbs** is a very simple command line interface to a PyBossa server. It allows
you to create projects, add tasks (from a CSV or JSON file), delete tasks and
update the project templates (tutorial, task_presenter, and descriptions).

Installation
============

TODO

## Configuring pbs

pbs is very handy when you work with one or two PyBossa servers. The best way
to configure it is creating a simple config file in your home folder:

```bash
    cd ~
    vim .pybossa.cfg
```

The file should have the following structure:

```
[default]
server: http://theserver.com
apikey: yourkey
```

If you are working with more servers, add another section below it. For
example:

```
[default]
server: http://theserver.com
apikey: yourkey

[crowdcrafting]
server: http://crowdcrafting.org
apikey: yourkeyincrowdcrafting
```

By default pbs will use the credentials of the section default, so you don't
have to type anything to use those values. However, if you want to do actions
in the other server all you have to do is the following:

```bash
    pbs --credentials crowdcrafting --help
```

That command will use the values of the crowdcrafting section.




