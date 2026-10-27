---
title: "AI in practice, part 2: ML pipelines on Google Vertex AI"
date: 2026-10-26T18:10:00-04:00
description: "What a machine-learning pipeline is, how Vertex AI Pipelines runs one, and a small train-evaluate-deploy example with the Kubeflow Pipelines SDK."
categories: ["technical"]
tags: ["ai", "ml", "vertex", "pipeline", "gcp", "python"]
series: ["AI in practice"]
series_order: 2
draft: false
---

{{< lead >}}
A notebook that trains a good model once is an experiment. A pipeline that trains it again next week, on new
data, and tells you whether it got better: that's a system. Here's how Google's Vertex AI turns one into the other.
{{< /lead >}}

## Why pipelines

Training a model is never one step. Data is extracted, cleaned and split; a model is trained, evaluated and
compared with the current one; if it's better, it's registered and deployed. Done by hand in a notebook, that
sequence is easy to get subtly wrong and impossible to audit.

A **pipeline** writes the sequence down as a graph of steps with typed inputs and outputs. Each run records
which data, code and parameters produced which model. You get repeatability, lineage ("where did this model
come from?") and automation: the same pipeline can run on a schedule or when new data lands.

## Vertex AI in one picture

Vertex AI is Google Cloud's platform for building and running ML. The parts that matter for this post:

| Piece | Job |
|---|---|
| **Workbench** | Managed Jupyter notebooks for exploring data and prototyping |
| **Pipelines** | Runs pipelines written with the Kubeflow Pipelines (KFP) SDK, serverless: no cluster to manage |
| **Training** | Custom training jobs on CPUs, GPUs or TPUs |
| **Experiments / Metadata** | Tracks runs, parameters, metrics and lineage |
| **Model Registry** | Versions of trained models, with their lineage |
| **Endpoints** | Deployed models answering online prediction requests |
| **Batch prediction** | Scores large datasets without keeping an endpoint running |
| **Model Garden** | Ready-made models, including Google's Gemini models for generative AI |

## The building blocks of a KFP pipeline

- **Component:** one step, packaged as a container. With the KFP v2 SDK, a decorated Python function is enough.
- **Artifact:** a typed output that is too big for a parameter: a dataset, a model, metrics. Stored in Cloud
  Storage under the pipeline root.
- **Pipeline:** a function that wires components together by passing outputs to inputs.
- **Compiled spec:** the pipeline compiled to a YAML file that Vertex AI runs.

## A small example: train, evaluate, decide

```python
from kfp import compiler, dsl


@dsl.component(base_image="python:3.11", packages_to_install=["pandas", "scikit-learn"])
def train(data_uri: str, model: dsl.Output[dsl.Model]):
    import pickle
    import pandas as pd
    from sklearn.linear_model import LogisticRegression

    df = pd.read_csv(data_uri)
    clf = LogisticRegression(max_iter=1000).fit(df.drop(columns="label"), df["label"])
    with open(model.path, "wb") as f:
        pickle.dump(clf, f)


@dsl.component(base_image="python:3.11", packages_to_install=["pandas", "scikit-learn"])
def evaluate(data_uri: str, model: dsl.Input[dsl.Model]) -> float:
    import pickle
    import pandas as pd

    df = pd.read_csv(data_uri)
    with open(model.path, "rb") as f:
        clf = pickle.load(f)
    return float(clf.score(df.drop(columns="label"), df["label"]))


@dsl.pipeline(name="train-and-evaluate")
def pipeline(train_uri: str, test_uri: str):
    trained = train(data_uri=train_uri)
    evaluate(data_uri=test_uri, model=trained.outputs["model"])


compiler.Compiler().compile(pipeline, "pipeline.yaml")
```

Submitting it to Vertex AI:

```python
from google.cloud import aiplatform

aiplatform.init(project="my-project", location="us-central1", staging_bucket="gs://my-bucket")

job = aiplatform.PipelineJob(
    display_name="train-and-evaluate",
    template_path="pipeline.yaml",
    pipeline_root="gs://my-bucket/pipeline-root",
    parameter_values={"train_uri": "gs://my-bucket/train.csv", "test_uri": "gs://my-bucket/test.csv"},
)
job.submit()
```

The console then shows the graph, each step's logs, and the artifacts with their lineage. Re-running with new
data is a new `PipelineJob`; schedules can trigger it automatically.

## From model to endpoint

When a run produces a better model, the usual next steps are to upload it to the **Model Registry** and
deploy it to an **Endpoint**:

```python
model = aiplatform.Model.upload(
    display_name="churn-model",
    artifact_uri="gs://my-bucket/models/churn/",
    serving_container_image_uri="<a prebuilt scikit-learn prediction image>",
)
endpoint = model.deploy(machine_type="n1-standard-4")
print(endpoint.predict(instances=[[0.3, 12, 1, 0]]))
```

Both steps can themselves become pipeline components, with a condition so that deployment only happens
when evaluation beats the model in production.

## Generative AI on the same platform

Vertex AI also hosts Google's Gemini models (and others from Model Garden). Calling one goes through the Gen AI
SDK pointed at your project, so usage, quotas and data stay inside your Google Cloud setup:

```python
from google import genai

client = genai.Client(vertexai=True, project="my-project", location="us-central1")
reply = client.models.generate_content(model="gemini-2.5-flash", contents="Summarise this pipeline run: …")
print(reply.text)
```

Model names change often; check Model Garden for the current ones. Every call is billed in tokens, which is the
subject of [part 3](/posts/ai-in-practice-3-tokens-and-tokenomics/).

## Lessons worth knowing early

- **Endpoints cost money while deployed**, even when idle. Undeploy experiments, or use batch prediction.
- **Keep components small and typed.** A component that does one thing is easy to cache, rerun and replace.
- **Pin package versions** in components; "it worked last month" depends on it.
- **Separate data from code.** Pass `gs://` paths as parameters; never bake data into images.
- **Compare before you deploy.** The evaluation step is the whole point; make deployment depend on it.

## Further reading

- [Introduction to Vertex AI Pipelines](https://cloud.google.com/vertex-ai/docs/pipelines/introduction)
- [Kubeflow Pipelines documentation](https://www.kubeflow.org/docs/components/pipelines/)

Previous: [part 1, choosing a framework](/posts/ai-in-practice-1-choosing-a-framework/). Next:
[part 3](/posts/ai-in-practice-3-tokens-and-tokenomics/), tokens and tokenomics.
