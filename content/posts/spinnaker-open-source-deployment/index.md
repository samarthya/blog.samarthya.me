---
title: "Spinnaker: Open Source Deployment"
date: "2022-02-05T12:00:00Z"
slug: "spinnaker-open-source-deployment"
description: "I have written a series of blogs to capture how you can deploy spinnaker on a Kubernetes cluster & manage a helm chart deployment via pipeline."
categories: ["kubernetes", "technical"]
tags: ["docker", "spinnaker"]
aliases: ["/wps/2022/02/05/spinnaker-open-source-deployment/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

I have written a series of blogs to capture how you can deploy spinnaker on a `Kubernetes` cluster & manage a helm chart deployment via pipeline.

> The only way to enable more frequent changes is to invest in supporting people with better tooling, practices, and culture
>
> From the Book `Spinnaker`

![](big-picture.png)

Now once you have the docker/image or the helm chart published we can define automated deployment if you have a spinnaker.

{{< lead >}}
Learn more about Spinnaker [here](https://spinnaker.io/docs/concepts/).
— Official documentation
{{< /lead >}}

## What is spinnaker?

Spinnaker is an open-source, multi-cloud continuous delivery platform that helps you release software changes with high velocity and confidence. It acts as a single pane of glass from which to manage your global deployments across multiple clouds.

{{< lead >}}
Read more about installing Spinnaker [here]({{< relref "/posts/spinnaker" >}}).
— Step 1
{{< /lead >}}

In Spinnaker world – *pipeline* is the key deployment management construct in Spinnaker. You can start a pipeline manually, or you can configure it to be automatically triggered by an event, such as a Jenkins job completing, a new Docker image appearing in your registry, a CRON schedule, or a stage in another pipeline.

{{< alert "circle-info" >}}
You can download the [ebook](https://spinnaker.io/docs/concepts/ebook/ContinuousDeliveryWithSpinnaker.pdf) from here (Free of Cost)
{{< /alert >}}

{{< lead >}}
Pipeline in action *(not published: its screenshots were lost)*
— Step 2
{{< /lead >}}

{{< lead >}}
[Docker Provider configuration]({{< relref "/posts/spinnaker-docker-registry" >}}) (Docker – registry)
— Step 3
{{< /lead >}}

{{< lead >}}
[Helm registry]({{< relref "/posts/spinnaker-artifact-helm" >}})
— Step 4
{{< /lead >}}

## Help

- It will be handy to read more about HALYARD ([official documentation](https://spinnaker.io/docs/reference/halyard/))
