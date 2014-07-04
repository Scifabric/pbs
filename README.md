[![Travis CI](https://travis-ci.org/PyBossa/pbs.png?branch=master)](https://travis-ci.org/#!/PyBossa/pbs)  [![Coverage Status](https://img.shields.io/coveralls/PyBossa/pbs.svg)](https://coveralls.io/r/PyBossa/pbs?branch=master) [![Downloads](https://pypip.in/download/pybossa-pbs/badge.png)](https://pypi.python.org/pypi/pybossa-pbs/) 
[![License](https://pypip.in/license/pybossa-pbs/badge.png)](https://pypi.python.org/pypi/pybossa-pbs/)



PBS - a PyBossa command line interface
======================================

**pbs** is a very simple command line interface to a PyBossa server. It allows
you to create projects, add tasks (from a CSV or JSON file), delete tasks and
update the project templates (tutorial, task_presenter, and descriptions).

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

Adding tasks is very simple. You can have your tasks in two formats:

 * JSON
 * CSV

Therefore, adding tasks to your project is as simple as this command:

```bash
    pbs add_tasks --tasks-file tasks_file.json --tasks-type=json
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

## Deleting tasks from a project

If you need it, you can delete all the tasks from your project, or only one
using its task.id. For deleting all the tasks, all you've to do is run the
following command:

```pbs
    pbs delete_tasks
```

This command will confirm that you want to delete all the tasks and associated
task_runs. 

If you want to see all the available
options, please check the **--help** command:

```bash
    pbs delete_tasks --help
```
