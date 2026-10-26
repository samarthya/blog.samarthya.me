---
title: "Async/Poll & Notify: Ansible Long running process"
date: "2023-03-24T12:00:00Z"
slug: "async-poll-notify-ansible-long-running-process"
description: "Recently during our discussion with a client a problem was raised how to show progress for a long running Ansible playbook task & this blog is just an outcome of the things I tried and delivered."
categories: ["ansible", "technical"]
tags: ["ansible", "async", "poll"]
aliases: ["/wps/2023/03/24/async-poll-notify-ansible-long-running-process/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

*[image unavailable: as-async.png]*

ASYNC & Poll

Recently during our discussion with a client a problem was raised how to show progress for a long running `Ansible` playbook task & this blog is just an outcome of the things I tried and delivered.

`Ansible` is a powerful automation tool that allows you to automate tasks across multiple hosts. However, some tasks can take a long time to complete, which can leave users wondering if the task is still running or if it has completed successfully. To provide feedback during long running tasks, Ansible provides several modules, including `async`, `poll`, and `notify`.

## `async` and `poll` Options in `Ansible`:

The `async` option allows you to run a task asynchronously, which means that it will run in the background and `Ansible` will not wait for it to complete before moving on to the next task. This can be useful for long running tasks, as it allows Ansible to continue running other tasks while the long running task is in progress.

The `poll` option specifies how often Ansible should check the status of the asynchronous task. By default, Ansible will check the status every 10 seconds. You can adjust this value to suit your needs.

Here’s an example playbook that uses the `async` and `poll` options to provide feedback during a long running task:

```text
- name: Long Running Task
  command: /path/to/long_running_task.sh
  async: 300
  poll: 60
  register: task_result

- name: Check Task Status
  async_status:
    jid: "{{ task_result.ansible_job_id }}"
  register: task_status
  until: task_status.finished

- name: Task Output
  debug:
    var: task_status.stdout_lines
```

In this example, the `command` module is used to run a long running task. The `async` option is set to 300, which means that the task will run asynchronously for up to 300 seconds (5 minutes). The `poll` option is set to 60, which means that Ansible will check the status of the task every 60 seconds.

The `register` keyword is used to capture the output of the `command` module in a variable called `task_result`.

After the task has been started, the `async_status` module is used to check the status of the task. The `jid` option is set to the `ansible_job_id` of the long running task. The `until` keyword is used to keep checking the status of the task until it has finished.

Finally, the `stdout_lines` of the task output are printed using the `debug` module.

With this playbook, users will be able to see the progress of the long running task and know when it has completed successfully.

## `notify` Module in `Ansible`:

The `notify` module in Ansible allows you to send a notification to a handler at the end of a task. This can be useful for providing real-time feedback during long running tasks.

Here’s an example playbook that uses the `notify` module to provide feedback during a long running task:

```text
- name: Long Running Task
  command: /path/to/long_running_task.sh
  async: 300
  poll: 60
  register: task_result
  notify: Update Status

- name: Wait for Task to Complete
  async_status:
    jid: "{{ task_result.ansible_job_id }}"
  register: task_status
  until: task_status.finished

- name: Task Output
  debug:
    var: task_status.stdout_lines

- name: Update Status
  debug:
    msg: "Task is still running"
  run_once: true
  when: task_result | changed
```

In this example, the `notify` module is used to call a task named `Update Status` for every poll. The `run_once` option is set to true, which means that the task will only be run once.

## Example

Let’s consider the following scenario: We have a web application running on a remote server. The application requires a database to function properly. We want to automate the process of creating a new database, configuring it, and starting the application. This process can take several minutes to complete. We want to provide feedback to the user about the status of the task during the process.

To solve this problem, we can use the `async`, `poll`, and `notify` modules in Ansible.

First, we create a playbook that contains the following tasks:

```text
- name: Create database
  command: create_database.sh
  async: 3600
  poll: 30
  register: db_task
  notify: Update Status

- name: Configure database
  command: configure_database.sh
  async: 3600
  poll: 30
  register: config_task
  notify: Update Status

- name: Start application
  command: start_application.sh
  async: 3600
  poll: 30
  register: app_task
  notify: Update Status

- name: Check database status
  command: check_database_status.sh
```

In this playbook, we have three tasks that create a database, configure it, and start the application. We have set the `async` option to 3600 seconds (1 hour), which means that the task will run asynchronously for up to 1 hour. We have set the `poll` option to 30 seconds, which means that Ansible will check the status of the task every 30 seconds.

We have also registered the output of each task in a variable (i.e., `db_task`, `config_task`, and `app_task`). This will allow us to check the status of each task later.

Finally, we have a task that checks the status of the database.

Next, we create a handler that will be called by the `notify` module:

```text
- name: Update Status
  debug:
    msg: "{{ ansible_job_id }}: {{ lookup('pipe', 'tail -1 /proc/' + ansible_job_id + '/stat') }}"
  run_once: true
  when: db_task | changed or config_task | changed or app_task | changed
```

This handler will print a message to the console every time one of the tasks changes status. The message will contain the Ansible job ID and the status of the task. We have set the `run_once` option to true, which means that the handler will only be run once even if there are multiple hosts.

Finally, we have used the `when` keyword to run the `Update Status` task only if one of the tasks has changed since the last poll. This means that the task will only be run if there is new progress to report.

### Explanation

When we run this playbook, Ansible will execute each task asynchronously. This means that Ansible will not wait for the task to complete before moving on to the next task.

The `poll` option specifies how often Ansible should check the status of the asynchronous task. In our example, Ansible will check the status every 30 seconds.

The `notify` module is used to call a handler named `Update Status` for every poll. The `when` keyword is used to run the `Update Status` task only if one

## Help

- Ansible [ASYNC](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_async.html)
