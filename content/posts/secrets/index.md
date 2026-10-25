---
title: "Secrets"
date: "2021-04-12T09:35:03Z"
slug: "secrets"
categories: ["technical"]
tags: ["k8s", "secrets"]
aliases: ["/wps/2021/04/12/secrets/"]
wp_id: 1494
---

To manage sensitive information you create `secrets`

```text
k create secret --help
```

```text
Create a secret using specified subcommand.

Available Commands:
  docker-registry Create a secret for use with a Docker registry
  generic         Create a secret from a local file, directory or literal value
  tls             Create a TLS secret

Usage:
  kubectl create secret [flags] [options]

Use "kubectl <command> --help" for more information about a given command.
Use "kubectl options" for a list of global command-line options (applies to all commands).
```

`type` specifies the type of secret you are creating (options are as shown above). As I need to create only key value pairs for my dummy secret file I need to know a way of how to facilitate that, and the option `-h` helped me there

Further looking at the options for `generic`

```text
k create secret generic -h
```

```text
Create a secret based on a file, directory, or specified literal value.

 A single secret may package one or more key/value pairs.

 When creating a secret based on a file, the key will default to the basename of the file, and the value will default to
the file content. If the basename is an invalid key or you wish to chose your own, you may specify an alternate key.

 When creating a secret based on a directory, each file whose basename is a valid key in the directory will be packaged
into the secret. Any directory entries except regular files are ignored (e.g. subdirectories, symlinks, devices, pipes,
etc).

Examples:
  # Create a new secret named my-secret with keys for each file in folder bar
  kubectl create secret generic my-secret --from-file=path/to/bar
  
  # Create a new secret named my-secret with specified keys instead of names on disk
  kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa
--from-file=ssh-publickey=path/to/id_rsa.pub
  
  # Create a new secret named my-secret with key1=supersecret and key2=topsecret
  kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret
  
  # Create a new secret named my-secret using a combination of a file and a literal
  kubectl create secret generic my-secret --from-file=ssh-privatekey=path/to/id_rsa --from-literal=passphrase=topsecret
  
  # Create a new secret named my-secret from an env file
  kubectl create secret generic my-secret --from-env-file=path/to/bar.env

Options:
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --append-hash=false: Append a hash of the secret to its name.
      --dry-run='none': Must be "none", "server", or "client". If client strategy, only print the object that would be
sent, without sending it. If server strategy, submit server-side request without persisting the resource.
      --field-manager='kubectl-create': Name of the manager used to track field ownership.
      --from-env-file='': Specify the path to a file to read lines of key=val pairs to create a secret (i.e. a Docker
.env file).
      --from-file=[]: Key files can be specified using their file path, in which case a default name will be given to
them, or optionally with a name and file path, in which case the given name will be used.  Specifying a directory will
iterate each named file in the directory that is a valid secret key.
      --from-literal=[]: Specify a key and literal value to insert in secret (i.e. mykey=somevalue)
  -o, --output='': Output format. One of:
json|yaml|name|go-template|go-template-file|template|templatefile|jsonpath|jsonpath-as-json|jsonpath-file.
      --save-config=false: If true, the configuration of current object will be saved in its annotation. Otherwise, the
annotation will be unchanged. This flag is useful when you want to perform kubectl apply on this object in the future.
      --show-managed-fields=false: If true, keep the managedFields when printing objects in JSON or YAML format.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
      --type='': The type of secret to create
      --validate=true: If true, use a schema to validate the input before sending it

Usage:
  kubectl create secret generic NAME [--type=string] [--from-file=[key=]source] [--from-literal=key1=value1]
[--dry-run=server|client|none] [options]

Use "kubectl options" for a list of global command-line options (applies to all commands).
```

I will use

```text
kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret
```

```text
k create secret generic samrthya --from-literal="supersecret=mypassword"
secret/samrthya created
```

You can look at the details below

```text
k describe secret/samrthya
Name:         samrthya
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
supersecret:  10 bytes
```

I tried editing the file by using `k edit` and the resource name, and in my case it shows up base64 encoded

```text
# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: v1
data:
  supersecret: bXlwYXNzd29yZA==
kind: Secret
metadata:
  creationTimestamp: "2021-04-12T09:12:04Z"
  name: samrthya
  namespace: default
  resourceVersion: "22555526"
  selfLink: /api/v1/namespaces/default/secrets/samrthya
  uid: 09db0ea3-3885-4354-9c16-4a9859c6a201
type: Opaque
~
```

Optionally you can define a `YAML file`

```text
{
    "kind": "Secret",
    "apiVersion": "v1",
    "metadata": {
        "name": "samrthya"
    },
    "data": {
        "supersecret": "bXlwYXNzd29yZA=="
    }
}
```

You can also do a listing

```text
k get secret
```

```text
NAME                            TYPE                                  DATA   AGE
samrthya                        Opaque                                1      3m47s
```

## Help

- <https://v1-18.docs.kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#secret-v1-core>
