---
title: "Scenario: Molecule"
date: "2023-03-23"
slug: "scenario-molecule"
categories: ["technical"]
aliases: ["/wps/2023/03/23/scenario-molecule/", "/wps/2026/10/23/scenario-molecule/"]
wp_id: 2487
---

A scenario in Molecule is a configuration that defines how a role should be tested. It consists of a set of instructions and parameters that determine how a role is provisioned, converged, and verified. The purpose of scenarios is to allow for flexibility in testing a role by allowing multiple testing configurations to be defined and executed. You can have as many scenarios as you like and Molecule will run one after the other.

{{< lead >}}
Scenarios are the starting point for a lot of powerful functionality that Molecule offers.
— molecule
{{< /lead >}}

In a molecule role directory you can add a new scenario with the following command

```text
molecule init scenario check_python_installed -d docker
```

It should initialize a directory with following files

```text
> tree molecule/check_python_installed 
molecule/check_python_installed
├── converge.yml
├── molecule.yml
└── verify.yml

1 directory, 3 files
```

The default layout that get created with the molecule role looks like below

```text
└── role1
    ├── README.md
    ├── defaults
    │   └── main.yml
    ├── files
    ├── handlers
    │   └── main.yml
    ├── meta
    │   └── main.yml
    ├── molecule
    │   └── default
    │       ├── INSTALL.rst
    │       ├── converge.yml
    │       ├── create.yml
    │       ├── destroy.yml
    │       ├── molecule.yml
    │       └── verify.yml
    ├── tasks
    │   └── main.yml
    ├── templates
    ├── tests
    │   ├── inventory
    │   └── test.yml
    └── vars
        └── main.yml
```

This is the layout for the scenario.

From the official documentation the description of the files in `./default` is as under

- `INSTALL.rst` contains instructions on what additional software or setup steps you will need to take in order to allow Molecule to successfully interface with the driver.
- `molecule.yml` is the central configuration entrypoint for Molecule. With this file, you can configure **each tool** that Molecule will employ when testing your role.
- `converge.yml` is the playbook file that contains the call for your role. Molecule will invoke this playbook with `ansible-playbook` and run it against an instance created by the driver.
- `verify.yml` is the Ansible file used for testing as Ansible is the default [verifier](https://molecule.readthedocs.io/configuration/#verifier). This allows you to write specific tests against the state of the container after your role has finis

### Molecule.YML

`molecule.yml` is a configuration file for Molecule, a testing framework for Ansible roles. The `molecule.yml` file defines the test scenarios for a role, including the provisioning of test instances, the configuration of test instances, and the execution of test playbooks against the test instances.

The basic structure of a `molecule.yml` file contains the following sections:

1. `dependency`: Used to define the required dependencies for the role
2. `driver`: Used to configure the driver for the provisioning of the test instances
3. `platforms`: Used to define the target systems for the role
4. `provisioner`: Used to configure the provisioning process for the test instances
5. `scenario`: Used to define the individual test scenarios for the role

Each scenario can have its own set of playbooks, tests, and environments. The playbooks are executed against the test instances to test the role. The tests are used to verify that the role has been correctly implemented and configured.
