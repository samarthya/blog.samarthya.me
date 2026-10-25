---
title: "Writing Helm Charts"
date: "2020-09-14T18:07:54Z"
slug: "writing-charts"
categories: ["technical"]
tags: ["charts", "example", "helm", "k8s"]
aliases: ["/wps/2020/09/14/writing-charts/"]
wp_id: 1033
---

{{< lead >}}
Helm is a dedicated package manager for Kubernetes.
{{< /lead >}}

Although the `Kubernetes` objects are deployed in YAML's there was a need to package and club them together and customise the deployment (not the K8S deployment).

Helm uses `Go templates`.

{{< lead >}}
Please refer to official go documentation on template package for details. You can also look at examples in my [repo here.](https://github.com/samarthya/gotemplates.git)
{{< /lead >}}

Actions from the official documentation

```text
{{/* a comment */}}
{{- /* a comment with white space trimmed from preceding and following text */ -}}
	A comment; discarded. May contain newlines.
	Comments do not nest and must start and end at the
	delimiters, as shown here.

{{pipeline}}
	The default textual representation (the same as would be
	printed by fmt.Print) of the value of the pipeline is copied
	to the output.

{{if pipeline}} T1 {{end}}
	If the value of the pipeline is empty, no output is generated;
	otherwise, T1 is executed. The empty values are false, 0, any
	nil pointer or interface value, and any array, slice, map, or
	string of length zero.
	Dot is unaffected.

{{if pipeline}} T1 {{else}} T0 {{end}}
	If the value of the pipeline is empty, T0 is executed;
	otherwise, T1 is executed. Dot is unaffected.

{{if pipeline}} T1 {{else if pipeline}} T0 {{end}}
	To simplify the appearance of if-else chains, the else action
	of an if may include another if directly; the effect is exactly
	the same as writing
		{{if pipeline}} T1 {{else}}{{if pipeline}} T0 {{end}}{{end}}

{{range pipeline}} T1 {{end}}
	The value of the pipeline must be an array, slice, map, or channel.
	If the value of the pipeline has length zero, nothing is output;
	otherwise, dot is set to the successive elements of the array,
	slice, or map and T1 is executed. If the value is a map and the
	keys are of basic type with a defined order, the elements will be
	visited in sorted key order.

{{range pipeline}} T1 {{else}} T0 {{end}}
	The value of the pipeline must be an array, slice, map, or channel.
	If the value of the pipeline has length zero, dot is unaffected and
	T0 is executed; otherwise, dot is set to the successive elements
	of the array, slice, or map and T1 is executed.

{{template "name"}}
	The template with the specified name is executed with nil data.

{{template "name" pipeline}}
	The template with the specified name is executed with dot set
	to the value of the pipeline.

{{block "name" pipeline}} T1 {{end}}
	A block is shorthand for defining a template
		{{define "name"}} T1 {{end}}
	and then executing it in place
		{{template "name" pipeline}}
	The typical use is to define a set of root templates that are
	then customized by redefining the block templates within.

{{with pipeline}} T1 {{end}}
	If the value of the pipeline is empty, no output is generated;
	otherwise, dot is set to the value of the pipeline and T1 is
	executed.

{{with pipeline}} T1 {{else}} T0 {{end}}
	If the value of the pipeline is empty, dot is unaffected and T0
	is executed; otherwise, dot is set to the value of the pipeline
	and T1 is executed.
```

## Example

Let's show a go template example before we move to the `Helm`

```text
// Letter a template for the automatic reply.
const Letter = `
Dear {{.Name}},
{{/* Check if the person identified by .Name attended the event. */}}
{{if .Attended}}
It was a pleasure to meet you at the wedding.
{{- else}}
{{/* Person identified by .Name did not attended the event. */}}
It is a shame you couldn't make it to the wedding.
{{- end}}
{{with .Gift -}}
Thank you for the lovely {{.}}.
{{end}}
Best wishes,
Josie
`

// Recipient Identifies the recipient
type Recipient struct {
	Name, Gift string
	Attended   bool
}
```

If I need to evaluate this template which is nothing just a letter template that works on some values provided.

Will use sample values for the struct Recipient as under

```text
var recipients = []two.Recipient{
		{"Aunt Mildred", "bone china tea set", true},
		{"Uncle John", "moleskin pants", false},
		{"Cousin Rodney", "", false},
	}
```

```text
// exampleTwo - Uses the actions and pipelines
func exampleTwo() {
	t := template.Must(template.New("letter").Parse(two.Letter))

	// Execute the template for each recipient.
	for _, r := range recipients {
		err := t.Execute(os.Stdout, r)
		if err != nil {
			log.Println("executing template:", err)
		}
	}
}
```

Once invoked it will print on the console.

```text
Dear Aunt Mildred,

It was a pleasure to meet you at the wedding.
Thank you for the lovely bone china tea set.

Best wishes,
Josie
```

```text
Dear Uncle John,

It is a shame you couldn't make it to the wedding.
Thank you for the lovely moleskin pants.

Best wishes,
Josie
```

```text
Dear Cousin Rodney,

It is a shame you couldn't make it to the wedding.

Best wishes,
Josie
```

## Local - `helm` version

The local helm version I am using on my box - `helm version`

```text
version.BuildInfo{Version:"v3.3.1", GitCommit:"249e5215cde0c3fa72e27eb7a30e8d55c9696144", GitTreeState:"dirty", GoVersion:"go1.15"}
```

```text
helm version --short
v3.3.1+g249e521
```

### Creating my chart

```text
helm create epserver
```

It creates some files as mentioned below

```text
.
├── Chart.yaml
├── charts
├── templates
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   └── tests
│       └── test-connection.yaml
└── values.yaml
```

I will give a brief about most of the file I edit, but you read more anytime from the official Helm documentation

#### Chart.yaml

{{< lead >}}
A YAML file containing information about the chart
{{< /lead >}}

#### templates/ [DIRECTORY]

{{< lead >}}
A directory of templates that, when combined with values, will generate valid Kubernetes manifest files.
{{< /lead >}}

#### values.yaml

{{< lead >}}
The default configuration values for this chart
{{< /lead >}}

#### charts/ [DIRECTORY]

{{< lead >}}
A directory containing any charts upon which this chart depends.
{{< /lead >}}

Added some details in the `Chart.yaml`, which are self explanatory

```text
# Minimum Version 3 required so v2
apiVersion: v2
name: epserver
description: A sample go server that exposes few endpoints.
type: application
version: 2.0.0
kubeVersion: ~1.18.x
appVersion: 3.0.0
```

#### serviceaccount.yaml

```text
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "epserver.serviceAccountName" . }}
  labels:
    {{- include "epserver.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

I will use my application `epserver` and create a chart for it just to check if simple modifications work.

> All, code is available in [my github repo](https://github.com/samarthya/epserver.git).

#### Values.yaml

```text
# Replica count
replicaCount: 1
# Only 1 replica required

# Labels for container
appname: epserver

# define the environment variable.
env:
  defined: true
  vars:
    - name: SERVERPORT
      value: "9090"

image:
  repository: samarthya/epserver
  pullPolicy: Always
  # Overrides the image tag whose default is the chart appVersion.
  tag: "2.0"

imagePullSecrets: []
nameOverride: "samarthya"
fullnameOverride: "eps"

# Samarthya: Added v1
environment: "test"

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: sa-epserver

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 9090

ingress:
  enabled: false
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths: []
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources:
# define limits
  limits:
    memory: "250Mi"
    cpu: "2000m"

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}
```

Can you spot the changes done?

- I have added `resources, limits, memory`
- Have added `service` port
- Added Image

```text
image:
  repository: samarthya/epserver
  pullPolicy: Always
  # Overrides the image tag whose default is the chart appVersion.
  tag: "2.0"
```

- Added a network policy for allow all traffic to the pods.

```text
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector:
    matchLabels:
      app: {{ .Values.appname }}
  ingress:
  - {}
  policyTypes:
  - Ingress
```

## Publishing Chart

### Step 1

```text
helm package .
```

This should generate the chart packaging like

```text
epserver-2.0.0.tgz
```

You can update the local repo or publish to your own [helm-git-repo](https://github.com/samarthya/hlmepserver.git).

#### Command that come in handy

```text
helm repo search samarthya
```

Where samarthya is my local repo

```text
helm repo list
```

```text
NAME     	URL                                                           
bitnami  	https://charts.bitnami.com/bitnami                            
samarthya	https://raw.githubusercontent.com/samarthya/hlmepserver/master
```

```text
helm repo index .
```

This you can run in the local directory where the `tgz` was generated.

```text
helm install eps samarthya/epserver
```

```text
NAME: eps
LAST DEPLOYED: Mon Sep 14 17:48:05 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=samarthya,app.kubernetes.io/instance=eps" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:80
```

You can check all the objects created

```text
k get all
NAME                       READY   STATUS              RESTARTS   AGE
pod/eps-58fbc9cfb4-2jbdz   0/1     ContainerCreating   0          3s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/eps          ClusterIP   10.111.254.111   <none>        9090/TCP   3s
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    28d

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/eps   0/1     1            0           3s

NAME                             DESIRED   CURRENT   READY   AGE
replicaset.apps/eps-58fbc9cfb4   1         1         0       3s
```

```text
curl -m 2 http://10.111.254.111:9090/hello?msg=My_message_my_rule
```

```text
{"message":"My_message_my_rule","timestamp":"2020-09-14T18:00:27.929269256Z"}
```

You can see the output will reflect the message is working.

```text
k logs service/eps
2020/09/14 17:48:12  DBG: Accepting traffic for /hello
2020/09/14 17:48:12  DBG: Accepting traffic for /health
 -------- Welcome to my server ------- 
2020/09/14 17:48:12  DBG: Accepting for /any.html
2020/09/14 17:48:12  DBG: Port  :9090
2020/09/14 17:48:12 My Simple Http Server
2020/09/14 17:48:14  DBG: Method -  GET
2020/09/14 17:48:14  DBG: Body -  {}
2020/09/14 17:48:14  DBG: URL -  /health
2020/09/14 17:48:14     { 
2020/09/14 17:48:14      DBG: Server is Healthy!
2020/09/14 17:48:14      DBG: 2020-09-14 17:48:14.594181453 +0000 UTC
2020/09/14 17:48:14     }
```

## References

- https://masterminds.github.io/sprig/
- https://helm.sh/docs/chart\_template\_guide/builtin\_objects/
- [ServiceAccountName](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
- https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#serviceaccount-v1-core
