[![Travis CI](https://travis-ci.org/PyBossa/pbs.svg?branch=master)](https://travis-ci.org/#!/PyBossa/pbs)
[![Code
Health](https://landscape.io/github/PyBossa/pbs/master/landscape.svg)](https://landscape.io/github/PyBossa/pbs/master)
[![Coverage Status](https://img.shields.io/coveralls/PyBossa/pbs.svg)](https://coveralls.io/r/PyBossa/pbs?branch=master) [![Downloads](https://img.shields.io/pypi/dm/pybossa-pbs.svg)](https://pypi.python.org/pypi/pybossa-pbs/) [![Version](https://img.shields.io/pypi/v/pybossa-pbs.svg)](https://pypi.python.org/pypi/pybossa-pbs/)



PBS - a PyBossa command line interface
======================================

**pbs** is a very simple command line interface to a PyBossa server. It allows
you to create projects, add tasks (from a CSV, JSON, PO or a PROPERTIES file) with a nice
progress bar, delete them and update the project templates 
(tutorial, task_presenter, and descriptions) all from the command line.

Requirements
============

[PyBossa server](http://pybossa.com) >= 0.2.3.

Installation
============

pbs is available in Pypi, so you can install the software with pip:

```bash
    pip install pybossa-pbs
```

If you have all the dependencies, the package will be installed and you will be
able to use it from the command line. The command is: **pbs**.

If you want to hack on the code, just install it but with the **--editable**
flag after cloning the repository:

```
    git clone https://github.com/PyBossa/pbs.git
    cd pbs
    virtualenv env
    source env/bin/activate
    pip install --editable .
```

This will install the pbs package, and you'll be able to modify it, patch it,
etc. If you improve it, please, let us know and share the code so we can
integrate it back ;-)

## Configuring pbs

pbs is very handy when you work with one or two PyBossa servers. The best way
to configure it is creating a simple config file in your home folder:

```bash
    cd ~
    vim .pybossa.cfg
```

The file should have the following structure:

```ini
[default]
server: http://theserver.com
apikey: yourkey
```

If you are working with more servers, add another section below it. For
example:

```ini
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

## Creating a project

Creating a project is very simple. All you have to do is create a file named
**project.json** with the following fields:

```json
{
    "name": "Flickr Person Finder",
    "short_name": "flickrperson",
    "description": "Image pattern recognition",
    "question": "Do you see a real human face in this photo?"
}
``` 

If you use the name **project.json** you will not have to pass the file name
via an argument, as it's the named used by default. Once you have the file
created, run the following command:

```bash
    pbs create_project
```

That command should create the project. If you want to see all the available
options, please check the **--help** command:

```bash
    pbs create_project --help
```

## Adding tasks to a project

Adding tasks is very simple. You can have your tasks in three formats:

 * JSON
 * CSV
 * PO (any po file that you want to translate)
 * PROPERTIES (any PROPERTIES file that you want to translate)

Therefore, adding tasks to your project is as simple as this command:

```bash
    pbs add_tasks --tasks-file tasks_file.json
```

If you want to see all the available
options, please check the **--help** command:

**NOTE**: By default PyBossa servers use a rate limit for avoiding abuse of the
API. For this reason, you can only do usually 300 requests per every 15
minutes. If you are going to add more than 300 tasks, pbs will detect it and
warn you, auto-enabling the throttling for you to respect the limits.

```bash
    pbs add_tasks --help
```

## Updating project templates

Now that you have added tasks, you can work in your templates. All you have to
do to add/update the templates to your project is running the following
command:

```bash
    pbs update_project
```

That command needs to have in the same folder where you are running it, the
following files:

 * template.html
 * long_description.md
 * tutorial.html

If you want to use another template, you can via arguments:

```bash
    pbs update_project --template /tmp/template.html
```

If you want to see all the available
options, please check the **--help** command:

```bash
    pbs update_project --help
```

### Auto-updating while developing a PyBossa project

At some point you will end up running lots of pbs update_project commands, as 
you will be using your own editor for fixing CSS, HTML or JavaScript. For these
scenarios, pbs comes with a handy feature: --watch. This argument will tell pbs
to run update_project automatically when template.html, tutorial.html or
long_description.md are modified in the file system. As simple as that.

You can run it like this:

```bash
    pbs update_project --watch
```

And the output will be similar to this:

![GIF of pbs in action](http://i.imgur.com/QoYC4oV.gif)

## Updating tasks redundancy from a project

If you need it, you can update the redundancy of a task using its ID or all the
tasks skipping the ID. For example, to update the redundancy of one task to 5:

```bash
    pbs update-task-redundancy --task-id 34234 --redundancy 5
```

To update all of them:

```bash
    pbs update-task-redundancy --redundancy 5
```

**Note**: without the --redundancy argument it will revert the redundancy to
the default value: 30.

This last command will confirm that you want to update all the tasks.

If you want to see all the available
options, please check the **--help** command:

```bash
    pbs update-task-redundancy --help
```


## Deleting tasks from a project

If you need it, you can delete all the tasks from your project, or only one
using its task.id. For deleting all the tasks, all you've to do is run the
following command:

```bash
    pbs delete_tasks
```

This command will confirm that you want to delete all the tasks and associated
task_runs. 

If you want to see all the available
options, please check the **--help** command:

```bash
    pbs delete_tasks --help
```

# Documentation

You have more documentation, with real examples at
[http://docs.pybossa.com](http://docs.pybossa.com).

Check the [tutorial](http://docs.pybossa.com/en/latest/user/tutorial.html) as
it uses **pbs**, and also its [pbs](http://docs.pybossa.com/en/latest/user/pbs.html) section
in the site.
