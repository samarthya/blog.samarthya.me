---
title: "K8S: Deployment"
date: "2020-12-22T12:45:09Z"
slug: "k8s-deployment"
categories: ["technical"]
tags: ["deployment", "k8s", "revisit", "service"]
aliases: ["/wps/2020/12/22/k8s-deployment/"]
wp_id: 1186
---

Time to re-test how to create deployments. It has been sometime, I created some deployments so just checking on how much I remember.

The quick way to always get started is to check the `HELP`.

![](screenshot-2020-05-02-at-3.49.39-pm-edited.png)

## `k create --help`

```text
Create a resource from a file or from stdin. 

JSON and YAML formats are accepted.

Examples:
  # Create a pod using the data in pod.json.
  kubectl create -f ./pod.json
  
  # Create a pod based on the JSON passed into stdin.
  cat pod.json | kubectl create -f -
  
  # Edit the data in docker-registry.yaml in JSON then create the resource using the edited data.
  kubectl create -f docker-registry.yaml --edit -o json

Available Commands:
  clusterrole         Create a ClusterRole.
  clusterrolebinding  Create a ClusterRoleBinding for a particular ClusterRole
  configmap           Create a configmap from a local file, directory or literal value
  deployment          Create a deployment with the specified name.
  job                 Create a job with the specified name.
  namespace           Create a namespace with the specified name
  poddisruptionbudget Create a pod disruption budget with the specified name.
  priorityclass       Create a priorityclass with the specified name.
  quota               Create a quota with the specified name.
  role                Create a role with single rule.
  rolebinding         Create a RoleBinding for a particular Role or ClusterRole
  secret              Create a secret using specified subcommand
  service             Create a service using specified subcommand.
  serviceaccount      Create a service account with the specified name

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --dry-run=false: If true, only print the object that would be sent, without sending it.
      --edit=false: Edit the API resource before creating
  -f, --filename=[]: Filename, directory, or URL to files to use to create the resource
  -o, --output='': Output format. One of:
json|yaml|name|template|go-template|go-template-file|templatefile|jsonpath|jsonpath-file.
      --raw='': Raw URI to POST to the server.  Uses the transport specified by the kubeconfig file.
      --record=false: Record current kubectl command in the resource annotation. If set to false, do not record the
command. If set to true, record the command. If not set, default to updating the existing annotation value only if one
already exists.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
      --save-config=false: If true, the configuration of current object will be saved in its annotation. Otherwise, the
annotation will be unchanged. This flag is useful when you want to perform kubectl apply on this object in the future.
  -l, --selector='': Selector (label query) to filter on, supports '=', '==', and '!='.(e.g. -l key1=value1,key2=value2)
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --validate=true: If true, use a schema to validate the input before sending it
      --windows-line-endings=false: Only relevant if --edit=true. Defaults to the line ending native to your platform.

Usage:
  kubectl create -f FILENAME [options]

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
```

```text
k create deployment <my-deployment> --image=<Image-Name> --dry-run=true --allow-missing-template-keys=true -o=yaml
```

The output has been set to YAML to see what it will output and I can use that to create my own deployment.yaml

```text
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: store-deployment
  name: store-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: store-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: store-deployment
    spec:
      containers:
      - image: <Image-Name>:1.0.0
        name: store-products
        resources: {}
status: {}
```

Once deployment is done Time to create a service

```text
k create service clusterip store-products --tcp=80:80 -o=json
```

```text
{
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "creationTimestamp": "2020-12-22T12:36:19Z",
        "labels": {
            "app": "store-products"
        },
        "name": "store-products",
        "namespace": "default",
        "resourceVersion": "7436",
        "selfLink": "/api/v1/namespaces/default/services/store-products",
        "uid": "4adac30d-4452-11eb-b86b-1276d3e8b6fb"
    },
    "spec": {
        "clusterIP": "10.97.209.47",
        "ports": [
            {
                "name": "80-80",
                "port": 80,
                "protocol": "TCP",
                "targetPort": 80
            }
        ],
        "selector": {
            "app": "store-products"
        },
        "sessionAffinity": "None",
        "type": "ClusterIP"
    },
    "status": {
        "loadBalancer": {}
    }
}
```

```text
k exec busybox -- curl -s store-products
```

```text
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: 2020-12-22T12:36:19Z
  labels:
    app: store-products
  name: store-products
  namespace: default
  resourceVersion: "7436"
  selfLink: /api/v1/namespaces/default/services/store-products
  uid: 4adac30d-4452-11eb-b86b-1276d3e8b6fb
spec:
  clusterIP: 10.97.209.47
  ports:
  - name: 80-80
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: store-products
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
~
```

## Namespace

It is always a good practice to create components under a specific namespace to avoid name collisions

```text
k create ns my-shop --dry-run 
namespace/my-shop created (dry run)
```

```text
k create ns my-shop
namespace/my-shop created
```

```text
k get ns
NAME          STATUS   AGE
default       Active   152m
kube-public   Active   152m
kube-system   Active   152m
my-shop       Active   2s
```
