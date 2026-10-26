---
title: "Jenkins: K8S"
date: "2022-02-02T12:00:00Z"
slug: "jenkins-k8s"
description: "Deploying Jenkins on K8S cluster is as simple as"
categories: ["kubernetes", "technical"]
tags: ["jenkins", "kubernetes"]
aliases: ["/wps/2022/02/02/jenkins-k8s/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

Deploying Jenkins on K8S cluster is as simple as

## Add Repo

```text
helm repo add jenkins https://charts.jenkins.io
helm repo update
```

Deploy instance

```text
helm upgrade --install myjenkins jenkins/jenkins -n jenkins --create-namespace
```

On my local machine the output is as under

```text
Release "myjenkins" does not exist. Installing it now.
NAME: myjenkins
LAST DEPLOYED: Wed Feb  2 10:20:57 2022
NAMESPACE: jenkins
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:
  kubectl exec --namespace jenkins -it svc/myjenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
2. Get the Jenkins URL to visit by running these commands in the same shell:
  echo http://127.0.0.1:8080
  kubectl --namespace jenkins port-forward svc/myjenkins 8080:8080

3. Login with the password from step 1 and the username: admin
4. Configure security realm and authorization strategy
5. Use Jenkins Configuration as Code by specifying configScripts in your values.yaml file, see documentation: http:///configuration-as-code and examples: https://github.com/jenkinsci/configuration-as-code-plugin/tree/master/demos

For more information on running Jenkins on Kubernetes, visit:
https://cloud.google.com/solutions/jenkins-on-container-engine

For more information about Jenkins Configuration as Code, visit:
https://jenkins.io/projects/jcasc/

NOTE: Consider using a custom image with pre-installed plugins
```

I will deploy it over ingress to be used over the web

*[image unavailable: Screenshot-2022-02-02-at-4.19.38-PM-1024x420.png]*

The password for the admin can be extracted

```text
kubectl exec --namespace jenkins -it svc/myjenkins -c jenkins -- /bin/cat /run/secrets/chart-admin-password && echo
```
