---
title: "Gradle"
date: "2022-07-19"
slug: "gradle"
categories: ["technical"]
aliases: ["/wps/2022/07/19/gradle/", "/wps/2026/10/23/gradle/"]
wp_id: 2294
---

- Open source build automation tool
- FLEXIBLE and builds any type of software
- Run on JVM and must have a JDK installed to use it.
- Gradle models its buils as DAGs pf tasks.
- Build is graph of tasks
- Tasks consists of
  - Actions
  - Inputs
  - Outputs
- [Lifecycle Tasks](https://docs.gradle.org/current/userguide/base_plugin.html#sec:base_tasks)
  - Clean
  - Check
  - Assemble
  - Build
  - Build Configuration
  - Clean Task
- Gradle evaluates and executes build scripts in [three phases](https://docs.gradle.org/current/userguide/build_lifecycle.html#build_lifecycle)
  - Initialization
  - Configuration
  - Execution
