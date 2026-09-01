# AWS Machine Learning Engineer – Associate (MLA-C01)

- Pointer-style certification notes: domain map, decision tables, service
  pickers, and exam traps.
- Each section links to official AWS documentation.
- Core VPC, IAM, S3, KMS, and CloudWatch material:
  [AWS interview guide](aws-interview-guide.md).

Official sources:

- [Certification page](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/)
- [MLA-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-01/machine-learning-engineer-associate-01.html)
- [Amazon SageMaker AI Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [Well-Architected Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html)

- **Exam version (dated 1 Sep 2026):** this guide is **MLA-C01** until a C02
  guide exists. English MLA-C01 last day is **28 Sep 2026**.
- MLA-C02 beta registration opens **1 Sep 2026** (exam code ME1-C02). Confirm
  dates on the [certification page](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/).
- **Naming:** at re:Invent 2024 the ML platform became **Amazon SageMaker AI**;
  "Amazon SageMaker" now names the wider data-and-AI platform.
- Exam items still use "Amazon SageMaker" for the ML platform, so both names
  mean the same product here.
- Check [Retired and renamed services](#retired-and-renamed-services) before
  trusting an older practice question.

## Contents

**Framing:** [Exam domain map](#exam-domain-map) · [ML lifecycle](#ml-lifecycle) · [Service picker](#service-picker) · [Retired and renamed services](#retired-and-renamed-services)

**Data:** [Data processing and Glue](#data-processing-and-glue) · [Feature engineering](#feature-engineering)

**Model:** [SageMaker components](#sagemaker-components) · [Built-in algorithms](#built-in-algorithms) · [Training data inputs and compute](#training-data-inputs-and-compute) · [Evaluation and tuning](#evaluation-and-tuning)

**Operations:** [Deployment and inference](#deployment-and-inference) · [Monitoring governance and security](#monitoring-governance-and-security) · [Cost control](#cost-control)

**Practice:** [High-yield exam traps](#high-yield-exam-traps) · [Recall questions](#recall-questions)

## Exam domain map

Docs: [MLA-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-01/machine-learning-engineer-associate-01.html) · [Certification page](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) · [Exam policies](https://aws.amazon.com/certification/policies/)

65 questions (50 scored, 15 unscored), 130 minutes, scaled score 100–1000,
pass mark 720. Question types are multiple choice, multiple response, ordering,
and matching.

| Domain | Weight | What it actually asks |
| :--- | :--- | :--- |
| 1. Data preparation for ML | 28% | Ingest and store data, transform it, validate quality, fix imbalance and leakage |
| 2. ML model development | 26% | Choose an algorithm or pre-trained model, train, tune, evaluate, version |
| 3. Deployment and orchestration of ML workflows | 22% | Pick an endpoint type, provision infrastructure as code, build CI/CD and pipelines |
| 4. ML solution monitoring, maintenance, and security | 24% | Drift monitoring, cost, IAM/KMS/VPC, logging and audit |

Scope boundary the exam enforces: you are an **ML engineer**, not a research
scientist. Questions reward managed services, least operational overhead, and
pre-trained models over hand-written training loops.

## ML lifecycle

Docs: [ML lifecycle](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) · [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html)

| Phase | Work | Primary services |
| :--- | :--- | :--- |
| Process data | Collect, clean, label, engineer features | S3, Glue, EMR, Athena, Data Wrangler, Ground Truth, Feature Store |
| Develop model | Train, tune, evaluate, explain | Training jobs, Automatic Model Tuning, Autopilot, Experiments, Clarify |
| Deploy | Version, approve, serve | Model Registry, endpoints, Batch Transform, Pipelines |
| Monitor | Detect drift, alarm, retrain | Model Monitor, Clarify, CloudWatch, EventBridge |

Two stores and one registry sit in the middle:

- **Offline feature store** — S3-backed for training and batch inference, with
  point-in-time correct queries so you do not leak future values.
- **Online feature store** — low-latency reads for real-time inference. Writes
  fan out to both stores, which is what prevents training/serving skew.
- **Model registry** — versioned artifacts plus approval status; deploy stages
  read a specific approved version, not the latest training job.

Two feedback loops the exam names explicitly: **performance feedback** (monitor
results change preprocessing) and **active learning** (low-confidence
predictions get human labels and rejoin training).

## Service picker

Docs: [AWS AI services](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/machine-learning.html) · [SageMaker AI](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)

Default rule: **pre-trained AI service → SageMaker JumpStart or Bedrock →
SageMaker built-in algorithm → custom container.** Pick the first that meets the
requirement.

| Need | Service | Docs |
| :--- | :--- | :--- |
| Text sentiment, entities, PII, topics | Amazon Comprehend | [dg](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html) |
| Text, tables, forms from scanned documents | Amazon Textract | [dg](https://docs.aws.amazon.com/textract/latest/dg/what-is.html) |
| Images and video labels, moderation, faces | Amazon Rekognition | [dg](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html) |
| Speech to text | Amazon Transcribe | [dg](https://docs.aws.amazon.com/transcribe/latest/dg/what-is.html) |
| Text to speech | Amazon Polly | [dg](https://docs.aws.amazon.com/polly/latest/dg/what-is.html) |
| Machine translation | Amazon Translate | [dg](https://docs.aws.amazon.com/translate/latest/dg/what-is.html) |
| Chatbot or IVR intents and slots | Amazon Lex | [dg](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html) |
| Semantic enterprise search over documents | Amazon Kendra | [dg](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html) |
| Recommendations without building a model | Amazon Personalize | [dg](https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html) |
| Online fraud / fake-account scoring | SageMaker (AutoGluon) or AWS WAF Fraud Control | [availability note](https://docs.aws.amazon.com/frauddetector/latest/ug/frauddetector-availability-change.html) |
| Foundation models, RAG, agents, guardrails | Amazon Bedrock | [ug](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) |
| Human review of low-confidence predictions | Amazon A2I | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html) |
| Human labelling of a training set | SageMaker Ground Truth | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) |
| Custom model, full control of training | SageMaker AI | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) |
| Metric anomaly detection | CloudWatch anomaly detection | [ug](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html) |
| ML on highly connected graph data | Amazon Neptune ML | [ug](https://docs.aws.amazon.com/neptune/latest/userguide/machine-learning.html) |

Disambiguations the exam leans on:

- **Ground Truth vs A2I** — Ground Truth labels data *before* training; A2I
  routes *inference* results to humans when confidence is low.
- **Comprehend vs Kendra** — Comprehend extracts structure from text; Kendra
  answers natural-language questions across a document corpus.
- **Personalize vs Factorization Machines** — Personalize for "no ML expertise"
  or "least operational overhead"; Factorization Machines when a SageMaker
  built-in algorithm is required.
- **Bedrock vs JumpStart** — a serverless API to hosted foundation models vs
  models deployed into *your* SageMaker account and endpoints.

## Retired and renamed services

Docs: [AWS service documentation index](https://docs.aws.amazon.com/) · Check the service page before relying on any entry below.

| Name in older material | Current status | Use instead |
| :--- | :--- | :--- |
| Amazon CodeWhisperer | **Renamed** Amazon Q Developer (April 30, 2024) | Amazon Q Developer |
| Amazon Kinesis Data Firehose | **Renamed** Amazon Data Firehose (2024) | Amazon Data Firehose |
| Amazon Kinesis Data Analytics | **Renamed** Amazon Managed Service for Apache Flink | Managed Service for Apache Flink |
| Amazon SageMaker (ML platform) | **Renamed** Amazon SageMaker AI (re:Invent 2024) | Amazon SageMaker AI |
| SageMaker Edge Manager | **Discontinued** (April 26, 2024) | SageMaker Neo plus IoT Greengrass |
| AWS DeepLens | **Ended support** (January 31, 2024) | IoT Greengrass on supported hardware |
| Amazon Lookout for Vision | **Ended support** (October 31, 2025) | SageMaker AI computer-vision model |
| Amazon Lookout for Metrics | **Ended support** (October 10, 2025) | CloudWatch anomaly detection, OpenSearch, or RCF |
| Amazon Lookout for Equipment | **Closed to new customers**; support ending October 7, 2026 | IoT SiteWise or a custom anomaly detector |
| Amazon Forecast | **Closed to new customers** (2024) | SageMaker Canvas time-series forecasting, or DeepAR |
| Amazon Fraud Detector | **Closed to new customers** (7 Nov 2025) | SageMaker, AutoGluon, or AWS WAF Fraud Control |
| AWS Panorama | **End of support announced** | IoT Greengrass with a SageMaker Neo-compiled model |
| SageMaker Data Wrangler | Capabilities folded into **SageMaker Canvas**; still named on the exam | Canvas data prep, or Processing/Glue for code |

Answer strategy: if a retired service and a current service both fit, the
current service is intended; if the whole question is built on a retired
service, answer as that service behaved.

## Data processing and Glue

Docs: [AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) · [Glue components](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html) · [Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html) · [EMR](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)

| Service | Use when | Avoid when |
| :--- | :--- | :--- |
| **AWS Glue ETL** | Serverless Spark ETL, joins across sources, scheduled batch | You need long-lived clusters or non-Spark frameworks |
| **AWS Glue DataBrew** | No-code visual cleaning and normalisation by analysts | Transformation must live in versioned pipeline code |
| **AWS Glue Data Catalog** | Central schema for Athena, EMR, Redshift Spectrum | — |
| **Glue crawlers** | Infer schema and partitions from S3, JDBC, DynamoDB | Schema is already known and stable |
| **Glue Data Quality** | Rule-based profiling and validation (DQDL) | Ad-hoc one-off checks |
| **Glue Schema Registry** | Enforce schema evolution on streams | Batch-only pipelines |
| **Amazon Athena** | SQL over S3, ad-hoc exploration, CTAS to Parquet | Sub-second serving, heavy iterative jobs |
| **Amazon EMR** | Existing Spark/Hive/Presto code, custom libraries, Spot fleets | Team wants zero cluster management |
| **SageMaker Processing** | Preprocessing that must run inside a training pipeline | General-purpose enterprise ETL |
| **Amazon Data Firehose** | Near-real-time delivery to S3/Redshift/OpenSearch with buffering | Sub-second per-record processing |
| **Kinesis Data Streams** | Ordered, replayable, low-latency stream with custom consumers | You only need managed delivery |
| **Managed Service for Apache Flink** | Stateful streaming transforms, windowed aggregation | Simple format conversion Firehose can do |
| **Lake Formation** | Central data-lake permissions, row/column-level access | Single-team bucket with plain IAM |
| **Step Functions** | Orchestration spanning Glue, Lambda, SageMaker, EMR | Orchestration confined to SageMaker steps (use Pipelines) |

Operational details that appear as answers:

- **Job bookmarks** make Glue jobs incremental by tracking processed data, and
  are the answer to "avoid reprocessing the whole dataset". **Glue workflows
  and triggers** orchestrate crawlers and jobs *within* Glue; Step Functions
  crosses service boundaries.
- **Athena CTAS** or a Glue job converts CSV/JSON to **Parquet or ORC**:
  columnar, compressed, partitioned storage is the standard cost and
  performance answer for repeated queries and training reads. Partition by date
  or tenant; fix small files by compaction, not more DPUs.
- Storage tiers: S3 Standard for hot training data, Intelligent-Tiering for
  unknown access patterns, Glacier classes for archived raw data only.

## Feature engineering

Docs: [Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html) · [Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html) · [Processing jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html)

| Problem | Standard fix |
| :--- | :--- |
| Missing values | Impute mean/median/mode, or drop the column when mostly null; add a missingness indicator |
| Categorical, low cardinality | One-hot encoding |
| Categorical, high cardinality | Target/label encoding, hashing, or learned embeddings |
| Ordinal categories | Ordinal encoding that preserves rank order |
| Different feature scales | Standardisation (z-score) or min–max normalisation |
| Long-tailed numeric feature | Log transform, or binning/quantile buckets |
| Class imbalance | Oversample minority (SMOTE), undersample majority, class weights, `scale_pos_weight`; evaluate with AUC-PR or F1, never plain accuracy |
| Outliers | Winsorise/clip, robust scaling, or isolation via RCF |
| Text | Tokenise, TF-IDF, or embeddings (BlazingText, Object2Vec) |
| Timestamps | Split into cyclical parts (hour, weekday, month) with sine/cosine encoding |
| High dimensionality | PCA, feature selection by importance |

Leakage rules the exam tests:

- Fit scalers and imputers on the **training split only**, then apply them to
  validation and test.
- Never build features from post-outcome columns.
- Use point-in-time joins in the offline feature store so a training row cannot
  see future feature values.

## SageMaker components

Docs: [SageMaker AI Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)

| Component | One-liner | Docs |
| :--- | :--- | :--- |
| Studio | Web IDE for the whole lifecycle | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html) |
| Ground Truth | Human and automated data labelling with active learning | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) |
| Data Wrangler / Canvas data prep | Visual, low-code transform and export | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html) |
| Processing | Managed containers for pre/post-processing and evaluation | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html) |
| Feature Store | Online plus offline feature storage with lineage | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html) |
| Training jobs | Managed, distributed training on ephemeral instances | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html) |
| Automatic Model Tuning | Hyperparameter search (Bayesian, random, grid, Hyperband) | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html) |
| Autopilot | AutoML: candidate models plus generated notebooks | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html) |
| JumpStart | Pre-trained models and solution templates deployed in your account | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html) |
| Experiments | Track runs, parameters, and metrics for comparison | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html) |
| Debugger | Training-time profiling and rules (vanishing gradient, overfit, GPU idle) | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/train-debugger.html) |
| Clarify | Pre- and post-training bias metrics plus SHAP explanations | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html) |
| Model Registry | Versioned model packages with approval status | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html) |
| Pipelines | Native CI/CD DAG for ML steps, with lineage | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html) |
| Model Monitor | Data quality, model quality, bias, and feature-attribution drift | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html) |
| Inference Recommender | Load-tests instance types to size an endpoint | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-recommender.html) |
| Neo | Compiles models for edge and specific hardware targets | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html) |
| Model Cards | Documented intended use, risk rating, and evaluation for governance | [dg](https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html) |

## Built-in algorithms

Docs: [Built-in algorithms](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) · [Choosing an algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/algorithms-choose.html) · [Common information](https://docs.aws.amazon.com/sagemaker/latest/dg/common-info-all-im-models.html)

| Algorithm | Task | Notes that decide the answer |
| :--- | :--- | :--- |
| Linear Learner | Regression, binary and multiclass classification | Trains many models in parallel; supports class weights |
| XGBoost | Tabular regression and classification, ranking | Default answer for structured/tabular data; handles missing values |
| K-Nearest Neighbors | Classification, regression | Index-based, exact or approximate search |
| Factorization Machines | Recommendations on sparse high-dimensional data | Pairwise interactions; expects `recordIO-protobuf` float32 |
| Object2Vec | Embeddings for pairs of objects | Similarity, matching, recommendation |
| K-Means | Clustering | Unsupervised segmentation |
| PCA | Dimensionality reduction | Preprocessing step, not a predictor |
| Random Cut Forest | Anomaly detection | Unsupervised, streaming and tabular; returns an anomaly score |
| IP Insights | Anomalous IP–entity pairings | Account-takeover and fraud signals |
| BlazingText | Word embeddings, text classification | Fast Word2Vec and supervised fastText modes |
| Sequence-to-Sequence | Translation, summarisation, speech to text | Encoder-decoder over token sequences |
| Neural Topic Model / LDA | Topic modelling | Unsupervised topics from a document corpus |
| DeepAR | Time-series forecasting | Trains one global model over many related series; probabilistic output |
| Image Classification | Whole-image labels | Supports transfer learning |
| Object Detection | Bounding boxes plus classes | "Where is it" questions |
| Semantic Segmentation | Pixel-level masks | Medical imaging, autonomous driving |
| Text Classification (TabTransformer, LightGBM, CatBoost) | Tabular and text via built-in frameworks | Available alongside the classic algorithms |

Picker by phrasing:

| Question says | Answer |
| :--- | :--- |
| "tabular", "structured", "churn", "high accuracy" | XGBoost |
| "sparse", "click-through", "collaborative filtering", built-in required | Factorization Machines |
| "no ML expertise", "fully managed recommendations" | Amazon Personalize |
| "many related time series", "probabilistic forecast" | DeepAR |
| "unlabelled", "group customers" | K-Means |
| "unusual", "rare", "no labelled anomalies" | Random Cut Forest |
| "classify the whole image" / "bounding boxes" / "per-pixel mask" | Image Classification / Object Detection / Semantic Segmentation |
| "word vectors", "document category" | BlazingText |
| "translate", "summarise" | Sequence-to-Sequence |
| "discover themes in documents" | Neural Topic Model or LDA |
| "reduce features before clustering" | PCA |

## Training data inputs and compute

Docs: [Access training data](https://docs.aws.amazon.com/sagemaker/latest/dg/model-access-training-data.html) · [Distributed training](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training.html) · [Managed spot training](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html)

| Input mode | Behaviour | Choose when |
| :--- | :--- | :--- |
| **File** | Downloads the full dataset to the instance volume before training starts | Small datasets; code needs ordinary file access |
| **FastFile** | Streams from S3 on demand behind a read-only POSIX view | Large datasets, mostly sequential reads, File-mode code unchanged; **no augmented-manifest support** |
| **Pipe** | Streams sequentially into FIFO pipes | Managed shuffling/sharding, RecordIO or augmented manifests; code must read pipes |
| **FSx for Lustre** | High-throughput shared filesystem linked to S3 | Repeated epochs over the same very large dataset, many instances |
| **EFS** | Existing shared filesystem | Data already lives in EFS |

- **RecordIO** is a record format, not an input mode: set
  `RecordWrapperType=RecordIO` only when raw objects must be wrapped for an
  algorithm that expects it. **Augmented manifests** stream labels alongside
  records in Pipe mode without building RecordIO files first.
- **`ShardedByS3Key`** splits objects across instances for data-parallel
  training; `FullyReplicated` sends everything to every instance.
- **Data parallelism** for large datasets that fit in memory per device;
  **model parallelism** when a single model does not fit on one GPU.
- **Managed spot training** with **checkpointing** to S3 is the standard
  "reduce training cost" answer; **warm pools** cut repeated start-up latency;
  **local mode** debugs a script before paying for a cluster.

## Evaluation and tuning

Docs: [Model tuning](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html) · [Tuning strategies](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html) · [Clarify bias](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html) · [Clarify explainability](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html)

| Metric | Formula in words | Use when |
| :--- | :--- | :--- |
| Accuracy | Correct / total | Balanced classes only |
| Precision | TP / (TP + FP) | False positives are expensive (spam blocking, blocking a legitimate payment) |
| Recall | TP / (TP + FN) | False negatives are expensive (disease screening, fraud detection) |
| F1 | Harmonic mean of precision and recall | Imbalanced classes, one summary number |
| AUC-ROC | Ranking quality across thresholds | Threshold-independent comparison, moderate imbalance |
| AUC-PR | Precision–recall trade-off | Severe class imbalance |
| MAE | Mean absolute error | Regression, all errors weighted equally |
| MSE / RMSE | Squared error | Regression, penalise large errors |
| R² | Variance explained | Regression, interpretability of fit |
| Confusion matrix | Raw TP/FP/TN/FN counts | Diagnosing which error type dominates |

| Symptom | Diagnosis | Fix |
| :--- | :--- | :--- |
| Train high, validation low | Overfitting | More data, regularisation (L1/L2, dropout), early stopping, simpler model |
| Train low, validation low | Underfitting | More features, more capacity, train longer, less regularisation |
| Great offline, poor in production | Train/serve skew or drift | Shared feature pipeline, Feature Store, Model Monitor |
| Accuracy 99% but minority class missed | Imbalance | Resample or weight classes, switch to F1/AUC-PR |
| Validation better than training | Leakage or bad split | Re-split with stratification; check for post-outcome features |

- **Tuning strategies:** Bayesian (sample-efficient default), Random (parallel,
  large spaces), Grid (small discrete spaces), Hyperband (early-stops weak
  candidates, best for iterative training); **warm start** reuses a previous job.
- **Cross-validation** (k-fold) for small datasets, a fixed held-out split for
  large ones, forward-chaining splits for time series, never random.
- **Clarify** reports **pre-training bias** (class imbalance, difference in
  proportions of labels) on the dataset, plus **post-training bias** and
  **SHAP** attributions on the model.

## Deployment and inference

Docs: [Deploy models](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html) · [Batch Transform](https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html) · [Asynchronous inference](https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html) · [Serverless inference](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html)

| Option | Latency and shape | Choose when |
| :--- | :--- | :--- |
| **Real-time endpoint** | Milliseconds, always on, auto-scaling | Steady online traffic, strict latency SLA |
| **Serverless inference** | Milliseconds after a cold start, scales to zero | Intermittent or unpredictable traffic, no idle cost |
| **Asynchronous inference** | Queued, near-real-time, scales to zero | Large payloads (up to 1 GB), long processing, bursty load |
| **Batch Transform** | Offline job over a dataset in S3 | Scoring a whole dataset, no endpoint needed |
| **Multi-model endpoint** | One container, many models loaded on demand | Many small models sharing a framework, cost-sensitive |
| **Multi-container endpoint** | Different containers behind one endpoint | Distinct frameworks, invoked directly or as a chain |
| **Inference pipeline** | Ordered containers in one endpoint | Preprocessing plus model plus postprocessing in one hop |
| **Edge (Neo + IoT Greengrass)** | On-device | Disconnected or latency-critical local inference |

- **Deployment guardrails:** blue/green with all-at-once, canary, or linear
  traffic shifting, plus CloudWatch alarms and **auto-rollback**.
- **Shadow tests** send a copy of production traffic to a candidate variant
  without returning its responses; **production variants** with weights do A/B
  tests on one endpoint.
- **Auto scaling** tracks `SageMakerVariantInvocationsPerInstance` as the
  standard target-tracking metric; **Inference Recommender** only sizes the
  instance type.
- IaC and CI/CD: CloudFormation or CDK for infrastructure, SageMaker Projects
  for templated MLOps, CodePipeline or GitHub Actions for the build, ECR for
  custom containers, Pipelines for the ML DAG, EventBridge to trigger
  retraining on drift alarms or new data.

## Monitoring governance and security

Docs: [Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html) · [SageMaker security](https://docs.aws.amazon.com/sagemaker/latest/dg/security.html) · [SageMaker and VPC](https://docs.aws.amazon.com/sagemaker/latest/dg/infrastructure-give-access.html)

| Monitor type | Detects | Needs |
| :--- | :--- | :--- |
| Data quality | Schema and distribution drift in inputs | Baseline stats and constraints from training data |
| Model quality | Accuracy decay | Ground-truth labels merged with captured predictions |
| Bias drift | Fairness metrics moving over time | Clarify configuration |
| Feature attribution drift | Feature importance shifting | Clarify SHAP baseline |

- **Data capture** writes endpoint requests and responses to S3; Model Monitor
  jobs run on a schedule, emit CloudWatch metrics, and alarms trigger
  retraining through EventBridge.
- **Debugger** watches *training*, **Model Monitor** watches *production*, and
  **Clarify** explains bias and attributions in both.
- **CloudWatch Logs** hold training and endpoint logs, **CloudWatch metrics** carry
  invocations and latency, **CloudTrail** records API calls for audit.

Security answers, in the order the exam expects them:

- **IAM execution roles** scoped per job with condition keys; never long-lived
  access keys in a notebook.
- **KMS** for encryption at rest on S3, training EBS volumes, and endpoint
  storage; TLS in transit; `EnableInterContainerTrafficEncryption` for
  distributed training.
- **VPC mode plus S3 gateway or interface VPC endpoints** keeps traffic off the
  internet; `EnableNetworkIsolation` blocks all container egress.
- **Macie** finds PII in S3, **Comprehend PII detection** redacts text, Ground
  Truth private workforces handle sensitive labelling.
- **Lake Formation** for row and column-level data-lake permissions, over a
  baseline of S3 bucket policies and block public access.

## Cost control

Docs: [SageMaker pricing model](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html) · [Managed spot training](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html)

| Lever | Effect |
| :--- | :--- |
| Managed spot training plus checkpoints | Large training savings, tolerant of interruption |
| Serverless or asynchronous inference | No charge while idle |
| Multi-model endpoints, or Batch Transform instead of an endpoint | Models share one instance; periodic scoring needs no standing infrastructure |
| Auto scaling with a sane minimum, plus SageMaker Savings Plans | Right-sized capacity and a commitment discount on training and hosting |
| Parquet plus partitioning | Fewer bytes scanned by Athena and read during training |
| Shut down idle Studio apps and notebook instances | Idle compute is the most common surprise bill |

## High-yield exam traps

- **Reinforcement Learning is not a built-in algorithm.** SageMaker supports RL
  through frameworks and toolkits, so a "built-in algorithm" option naming RL
  is usually wrong.
- **BlazingText does not fix overfitting.** Regularisation, more data, and
  early stopping do.
- **XGBoost, not Linear Learner, is the default for tabular accuracy.** Linear
  Learner does support multiclass, but "high accuracy on structured data" is
  XGBoost.
- **FastFile does not support augmented manifests.** If the question mentions
  augmented manifests or managed shuffling, the answer is Pipe mode.
- **Batch Transform vs asynchronous inference** — a whole dataset on a schedule
  vs per-request large payloads and long processing behind a queue.
- **Ground Truth vs A2I** — training labels vs human review of predictions.
- **Data Wrangler vs DataBrew vs Processing** — low-code inside SageMaker vs
  analyst-facing no-code in Glue vs code in a managed container.
- **Model Registry vs Experiments** — versioned, approved artifacts vs run
  tracking and metric comparison.
- **Neo compiles, Edge Manager (retired) managed fleets.** Pair Neo with IoT
  Greengrass in current answers.
- **Accuracy is the wrong metric for imbalanced data.** Expect F1 or AUC-PR.
- **Scaling before the train/test split is leakage**, and **random splits break
  time series**: fit on train only, split chronologically.
- **Job bookmarks, not custom checkpoints, make Glue incremental.**
- **Inference Recommender sizes, auto scaling scales.** Not substitutes.
- **Network isolation blocks all outbound traffic**, including S3 downloads
  mid-job; VPC endpoints keep traffic private without blocking it.
- **Least operational overhead** in the stem points to a managed AI service or
  AutoML, not a custom container.

## Recall questions

Answer before reading the right-hand column.

| Prompt | Answer |
| :--- | :--- |
| Detect prediction drift in production | Model Monitor |
| Find training bottlenecks and vanishing gradients | Debugger |
| Orchestrate an ML DAG native to SageMaker | Pipelines |
| Store and reuse features online and offline | Feature Store |
| Filesystem-style access to a large S3 dataset without downloading it | FastFile mode |
| Input mode required for augmented manifests | Pipe mode |
| Label a training dataset with humans | Ground Truth |
| AutoML with generated, inspectable notebooks | Autopilot |
| Score a full S3 dataset with no endpoint | Batch Transform |
| Endpoint that scales to zero for spiky traffic | Serverless inference |
| 500 MB payload with several minutes of processing | Asynchronous inference |
| Sparse recommendation data, built-in algorithm required | Factorization Machines |
| Fraud or network anomalies with no labelled anomalies | Random Cut Forest |
| Explain individual feature contributions | Clarify (SHAP) |
| Metric for a severely imbalanced classifier | AUC-PR or F1, not accuracy |
| Cheapest way to run long training that tolerates interruption | Managed spot training with checkpointing |
| Make a Glue job process only new data | Job bookmarks |
| Convert CSV in S3 to Parquet with SQL | Athena CTAS |
| Near-real-time delivery of streams to S3 with buffering | Amazon Data Firehose |
| Orchestrate Glue, Lambda, and SageMaker together | Step Functions |
| Choose an endpoint instance type by load testing | Inference Recommender |
| Compare a candidate against live traffic without returning its responses | Shadow test |
| Keep training traffic off the public internet | VPC mode with S3/interface VPC endpoints |
| Audit which principal called a SageMaker API | CloudTrail |
| Track versions and approval before deployment | Model Registry |
