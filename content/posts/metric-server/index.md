---
title: "Metric Server"
date: "2020-12-09T08:01:49Z"
slug: "metric-server"
categories: ["docker", "technical"]
tags: ["k8s", "metricserver"]
aliases: ["/wps/2020/12/09/metric-server/"]
wp_id: 1141
---

For my local K8S cluster of 4 nodes I wanted to get the resource usage metrics. From the official documentation of kubernetes.io

> These metrics can be accessed either directly by the user with the `kubectl top` command, or by a controller in the cluster, for example Horizontal Pod Autoscaler, to make decisions.
>
> https://kubernetes.io

{{< lead >}}
Resource usage metrics, such as container CPU and memory usage, are available in Kubernetes through the Metrics API.
{{< /lead >}}

I deployed Metric Server v0.4.1

```text
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.4.1/components.yaml
```

```text
serviceaccount/metrics-server configured
clusterrole.rbac.authorization.k8s.io/system:aggregated-metrics-reader configured
clusterrole.rbac.authorization.k8s.io/system:metrics-server configured
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader configured
clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator configured
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server configured
service/metrics-server created
deployment.apps/metrics-server created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io configured
```

After installation is complete, fire in to check the top node stats.

```text
k top node
```

For me I was getting

```text
Error from server (ServiceUnavailable): the server is currently unable to handle the request (get nodes.metrics.k8s.io)
```

I could see the POD and deployment

```text
kube-system       pod/metrics-server-5d5c49f488-8dhdf                        0/1     Running        0          16s
```

```text
kube-system       deployment.apps/metrics-server            0/1     1            0           16s
```

A quick describe for pod revealed

```text
k describe pod/metrics-server-5d5c49f488-8dhdf -n kube-system
```

```text
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  37s               default-scheduler  Successfully assigned kube-system/metrics-server-5d5c49f488-8dhdf to i01.samarthya.me
  Normal   Pulling    36s               kubelet            Pulling image "k8s.gcr.io/metrics-server/metrics-server:v0.4.1"
  Normal   Pulled     25s               kubelet            Successfully pulled image "k8s.gcr.io/metrics-server/metrics-server:v0.4.1" in 11.718855147s
  Normal   Created    24s               kubelet            Created container metrics-server
  Normal   Started    24s               kubelet            Started container metrics-server
  Warning  Unhealthy  7s (x2 over 17s)  kubelet            Liveness probe failed: HTTP probe failed with statuscode: 500
  Warning  Unhealthy  5s (x2 over 15s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 500
```

Looking at the logs

```text
k log pod/metrics-server-5d5c49f488-8dhdf  -n kube-system
```

```text
E1209 07:23:57.351296       1 server.go:132] unable to fully scrape metrics: [unable to fully scrape metrics from node mymachine.cluster.samarthya.me: unable to fetch metrics from node mymachine.cluster.samarthya.me: Get "https://10.80.241.70:10250/stats/summary?only_cpu_and_memory=true": x509: cannot validate certificate for 10.80.241.70 because it doesn't contain any IP SANs, unable to fully scrape metrics from node i01.samarthya.me: unable to fetch metrics from node i02.samarthya.me: Get "https://10.80.120.149:10250/stats/summary?only_cpu_and_memory=true": x509: cannot validate certificate for 10.80.120.149 because it doesn't contain any IP SANs, unable to fully scrape metrics from node ibndev003277samarthya.me: unable to fetch metrics from node ibndev003277samarthya.me: Get "https://10.80.120.148:10250/stats/summary?only_cpu_and_memory=true": x509: cannot validate certificate for 10.80.120.148 because it doesn't contain any IP SANs, unable to fully scrape metrics from node i03.samarthya.me: unable to fetch metrics from node i04.samarthya.me: Get "https://10.80.241.80:10250/stats/summary?only_cpu_and_memory=true": x509: cannot validate certificate for 10.80.241.80 because it doesn't contain any IP SANs, unable to fully scrape metrics from node i03.samarthya.me: unable to fetch metrics from node i03.samarthya.me: Get "https://10.80.241.78:10250/stats/summary?only_cpu_and_memory=true": x509: cannot validate certificate for 10.80.241.78 because it doesn't contain any IP SANs]
```

and after some time I could see

```text
kube-system       pod/metrics-server-5d5c49f488-8dhdf                        0/1     CrashLoopBackOff   4          2m48s
```

I could see the selfsigned certificares were problematic for the configuration

```text
k edit deployment.apps/metrics-server -n kube-system
```

Added `

```text
--kubelet-insecure-tls
```

to the deployment and saved it.

```text
 containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --kubelet-insecure-tls
```

It fired up the new container

```text
kube-system       pod/metrics-server-56c59cf9ff-qcxlc                        0/1     ContainerCreating   0          5s
```

```text
k describe  pod/metrics-server-56c59cf9ff-qcxlc  -n kube-system
```

```text
  Normal  Created    23s   kubelet            Created container metrics-server
  Normal  Started    23s   kubelet            Started container metrics-server
```

```text
k logs  pod/metrics-server-56c59cf9ff-qcxlc  -n kube-system
```

```text
I1209 07:27:03.832542       1 serving.go:325] Generated self-signed cert (/tmp/apiserver.crt, /tmp/apiserver.key)
I1209 07:27:04.575200       1 secure_serving.go:197] Serving securely on [::]:4443
I1209 07:27:04.575282       1 requestheader_controller.go:169] Starting RequestHeaderAuthRequestController
I1209 07:27:04.575295       1 shared_informer.go:240] Waiting for caches to sync for RequestHeaderAuthRequestController
I1209 07:27:04.575372       1 dynamic_serving_content.go:130] Starting serving-cert::/tmp/apiserver.crt::/tmp/apiserver.key
I1209 07:27:04.575450       1 tlsconfig.go:240] Starting DynamicServingCertificateController
I1209 07:27:04.575546       1 configmap_cafile_content.go:202] Starting client-ca::kube-system::extension-apiserver-authentication::client-ca-file
I1209 07:27:04.575551       1 shared_informer.go:240] Waiting for caches to sync for client-ca::kube-system::extension-apiserver-authentication::client-ca-file
I1209 07:27:04.575563       1 configmap_cafile_content.go:202] Starting client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file
I1209 07:27:04.575567       1 shared_informer.go:240] Waiting for caches to sync for client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file
I1209 07:27:04.675539       1 shared_informer.go:247] Caches are synced for RequestHeaderAuthRequestController 
I1209 07:27:04.675584       1 shared_informer.go:247] Caches are synced for client-ca::kube-system::extension-apiserver-authentication::client-ca-file 
I1209 07:27:04.675731       1 shared_informer.go:247] Caches are synced for client-ca::kube-system::extension-apiserver-authentication::requestheader-client-ca-file
```

With things appearing to be running fine time to find the top node

```text
k top node
```

```text
NAME              CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
i01.samarthya.me    131m         0%     7004Mi          21%       
i02.samarthya.me    85m          0%     5542Mi          17%       
i03.samarthya.me    163m         1%     13011Mi         40%       
i04.samarthya.me    395m         2%     7191Mi          22%       
i05.samarthya.me    94m          0%     11536Mi         36%
```

## Help

- https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/
- https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/metrics-server.md
