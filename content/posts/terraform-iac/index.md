---
title: "Terraform (IaC)"
date: "2024-03-27T12:00:00Z"
slug: "terraform-iac"
description: "IaC stands for Infrastructure as Code."
categories: ["technical"]
tags: ["terraform"]
aliases: ["/wps/2024/03/27/terraform-iac/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](iac1.jpg)

IaC stands for **Infrastructure as Code**. It’s a concept where you define and manage your infrastructure using code files instead of manually provisioning resources through a web interface or command-line tools. This approach offers several benefits like:

- **Repeatability:** You can easily recreate your infrastructure from scratch or in different environments by simply running the code again.
- **Version control:** You can track changes to your infrastructure configuration over time, similar to how you would with software code.
- **Consistency:** IaC ensures all your infrastructure deployments follow the same specifications, reducing errors.

### What is Terraform?

**Terraform** is a popular open-source tool that implements the IaC concept. It allows you to define your infrastructure resources (like servers, virtual networks, databases) in human-readable configuration files written in `HashiCorp` Configuration Language (HCL). Terraform then provisions and manages those resources on various cloud platforms and on-premises infrastructure.

In simpler terms, IaC is the overall philosophy, and Terraform is a specific tool that lets you put IaC into practice.
