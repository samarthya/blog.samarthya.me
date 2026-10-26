---
title: "Ansible: Templates"
date: "2023-02-08T12:00:00Z"
slug: "ansible-templates"
description: "Templates in Ansible are a type of file that contain configuration information or scripts written in a Jinja2 templating language."
categories: ["technical"]
tags: ["ansible", "jinga2", "templates"]
aliases: ["/wps/2023/02/08/ansible-templates/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

*[image unavailable: an-template.png]*

Templates in `Ansible` are a type of file that contain configuration information or scripts written in a `Jinja2` templating language.

> Templates in `Ansible` are used to configure and manage a set of files with similar or identical content.
>
> Ansible

Templates are used to define the structure and content of a file that will be deployed to a remote host. They are commonly used for configuration files, scripts, and service definitions. Using templates can help automate repetitive tasks, reduce human error, and ensure consistency and accuracy in the configuration of systems. For example, you can use a template to create an Apache configuration file with specific settings that can be changed depending on the environment.

Here’s an example of how you can use templates in a role:

```text
- name: Copy apache configuration file
  template:
    src: templates/httpd.conf.j2
    dest: /etc/httpd/conf/httpd.conf
    owner: root
    group: root
    mode: 0644
```

In this example, we use the `template` module to copy a file from the `templates` directory in the role to the `/etc/httpd/conf/` directory on the remote host. The source file is named `httpd.conf.j2`, which is a Jinja2 template file. The `dest` parameter specifies the destination file name, and the `owner`, `group`, and `mode` parameters set the file permissions.

{{< lead >}}
Jinja2 is a popular templating language that is used by many web frameworks and other software platforms. It is used in Ansible to generate dynamic content within playbooks and templates.
— ANSIBLE
{{< /lead >}}

## When to use templates?

Some examples of when to use templates in Ansible include:

- When you need to generate configuration files based on system-specific [variables]({{< relref "/posts/ansible-variables" >}}), such as hostnames, IP addresses, or operating system versions.
- When you need to apply the same configuration to multiple systems, and you want to keep the configuration in a single place, rather than copying and pasting it multiple times.
- When you need to generate scripts or files with a specific format or structure, and you want to ensure that the format or structure remains consistent and correct.

Overall, using templates can simplify the management and configuration of your systems, and Jinja2 provides a powerful and flexible way to define and use templates in Ansible.

## Jinja

Jinja2 is a fast and versatile templating language for Python applications. It is widely used in the Ansible community for generating dynamic content in playbooks. Jinja2 provides a simple syntax for defining variables, loops, and conditional statements, making it easy to create templates that can be used to generate configuration files, scripts, and other text-based content.

One of the key benefits of using Jinja2 is that it allows you to separate the logic of your playbooks from the content that is generated. For example, you can create a template that defines the structure of a configuration file, and then use variables to fill in the specific values that are relevant to each target host. This makes it easy to reuse templates across multiple playbooks, and to maintain consistency in the content that is generated.

Jinja2 also provides a wide range of built-in functions that can be used to manipulate data, perform calculations, and conditionally render content. For example, you can use the “filter” function to format numbers or strings, the “map” function to perform transformations on lists and dictionaries, and the “select” function to select elements from a list based on a condition.

In addition, Jinja2 provides a number of advanced features, such as custom filters and tests, macros, and support for custom tags and blocks. These features allow you to extend the language in ways that are specific to your use case, making it possible to create complex and highly customized templates.

Overall, Jinja2 is a powerful and flexible templating language that is well-suited to the needs of the Ansible community. Whether you are generating simple configuration files or complex scripts, Jinja2 makes it easy to create and maintain templates that can be used to automate your infrastructure.
