# AWS 
--------------------------------------------------------------------------------------

<details>
<summary> How many Subnets can you have per VPC?.</code></summary><br><b>

`200 Subnets per VPC`
</b></details>

<details>
<summary> Relation between the Availability Zone and Region?.</code></summary><br><b>

Each Region is a separate geographic area. 

Availability Zones are multiple, isolated locations within each Region. 
</b></details>

<details>
<summary> What does AMI include?.</code></summary><br><b>

An AMI includes the following things:

* A template for the root volume for the instance.

* Launch permissions to decide which AWS accounts can avail the AMI to launch instances.

* A block device mapping that determines the volumes to attach to the instance when it is launched.
</b></details>

<details>
<summary> What does serverless mean to you ?.</code></summary><br><b>

Serverless is a cloud-native development model that allows developers to build and run applications without having to manage servers.

There are still servers in serverless, but they are abstracted away from app development. A cloud provider handles the routine work of provisioning, maintaining, and scaling the server infrastructure. Developers can simply package their code in containers for deployment.

Once deployed, serverless apps respond to demand and automatically scale up and down as needed. Serverless offerings from public cloud providers are usually metered on-demand through an event-driven execution model. As a result, when a serverless function is sitting idle, it doesn’t cost anything.
</b></details>

<details>
<summary> Different storage classes in AWS ?.</code></summary><br><b>

* `Amazon S3 Standard (S3 Standard)`
* `Amazon S3 Intelligent-Tiering (S3 Intelligent-Tiering)`
* `Amazon S3 Standard-Infrequent Access (S3 Standard-IA)`
* `Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA)`
* `Amazon S3 Glacier (S3 Glacier)`
* `Amazon S3 Glacier Deep Archive (S3 Glacier Deep Archive)`
* `S3 Outposts storage class` : object storage to your on-premises AWS Outposts environment. Using the S3 APIs and features available in AWS Regions today, S3 on Outposts makes it easy to store and retrieve data on your Outpost, as well as secure the data, control access, tag, and report on it. S3 on Outposts provides a single Amazon S3 storage class, named S3 Outposts, which uses the S3 APIs, and is designed to durably and redundantly store data across multiple devices and servers on your Outposts.

[AWS S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
</b></details>

<details>
<summary>  Diff types of EC2 instances ?..</code></summary><br><b>

* `General Purpose`: The most popular; used for web servers, development environments, etc.
* `Compute Optimized`: Good for compute-intensive applications such as some scientific modeling or high-performance web servers.
* `Memory Optimized`: Used for anything that needs memory-intensive applications, such as real-time big data analytics, or running Hadoop or Spark.
* `Accelerated Computing`: Include additional hardware (GPUs, FPGAs) to provide massive amounts of parallel processing for tasks such as graphics processing.
* `Storage Optimized`: Ideal for tasks that require huge amounts of storage, specifically with sequential read-writes, such as log processing.

[EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
</b></details>

<details>
<summary>  Diff. between fault tolerance and Disaster recovery ?.</code></summary><br><b>

Fault tolerant design ensures that system is up and working even in faulty scenarios. When you app / business can afford some time otherwise High Availablity will be required if don’t want any downtime.

Disaster recovery ensures that in situation when there is damage beyond repair, system is able to preserve key data and bring up servers in same state. Disaster can be failure of components or entire physical infrastructure.

[fault tolerance and Disaster recovery](https://www.nakivo.com/blog/disaster-recovery-vs-high-availability-vs-fault-tolerance/)
</b></details>

<details>
<summary>  Diff. between Service Principal and Managed Identity ?.</code></summary><br><b>

Service principal is a security identity used by user-created apps, services, and automation tools to access specific Azure resources. 

- SP's are created manually by users/administrators through Azure portal, Azure CLI, PowerShell, or Azure SDKs.

- SP's are typically used in scenarios where an application needs to access Azure resources. They can be assigned roles and permissions, enabling applications to interact with Azure services securely.

- SP's are authenticated using either a client secret (a password) or a certificate. They can authenticate without the need for interactive sign-ins.

Managed identities for Azure resources, also known as Managed Service Identity (MSI), are a feature in Azure Active Directory that allow services to authenticate to cloud services (e.g., Azure Key Vault) without needing to insert credentials into the code.

- MI's are created directly on Azure resources (like Virtual Machines, App Services, Functions, etc.). There's no need for manual creation or management.

- MI's are used in scenarios where an Azure resource needs to access other Azure resources securely. The identity is automatically managed by Azure and doesn’t require explicit management by users.

- MI's use the Azure AD authentication flow. When enabled, Azure automatically handles the authentication process for the resource using the identity.

##Key Differences:

1.Creation and Management:
- Service Principal: Created manually and requires explicit management by the user.
- Managed Identity: Created directly on Azure resources, and Azure handles the management automatically.

2.Scope:
- Service Principal: Can be created for various scenarios and doesn’t have a specific scope in Azure.
- Managed Identity: Tied to a specific Azure resource and can only be used by that resource and its child resources.

3.Authentication:
- Service Principal: Requires manual configuration of authentication methods (client secret or certificate).
- Managed Identity: Authentication is automatically handled by Azure AD.

4.Use Cases:
- Service Principal: Typically used for broader scenarios where applications or services need to access various Azure resources.
- Managed Identity: Ideal for scenarios where a specific Azure resource (e.g., a VM or an App Service) needs secure access to other Azure resources.

[fault tolerance and Disaster recovery](https://www.nakivo.com/blog/disaster-recovery-vs-high-availability-vs-fault-tolerance/)
</b></details>

<details>
<summary> List all AWS Managed Data Transformation Integration and Feature Engineering Services ?.</code></summary><br><b>
# AWS Services for Data Transformation, Integration, and Feature Engineering

| **Service**                   | **Category**                    | **Use Cases**                                                                                          | **Key Differences**                                                                                  |
|-------------------------------|----------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **AWS Glue**                  | Data Integration and ETL        | Data integration, ETL (Extract, Transform, Load), automate workflows, schema discovery.                | A fully managed ETL service designed for large-scale data integration and transformation tasks.      |
| **AWS Glue DataBrew**         | Data Preparation (No-Code)      | Visual, no-code preparation of datasets for ML workflows or analytics.                                | A no-code data transformation tool focusing on cleaning, normalizing, and profiling data.            |
| **Amazon EMR**                | Big Data Processing             | Process large-scale data using frameworks like Apache Spark, Hadoop, etc.                             | Highly scalable big data processing for analytics and transformation using open-source frameworks.   |
| **Amazon Redshift**           | Data Warehousing               | Query large-scale structured or semi-structured datasets, create data models for ML.                  | Provides built-in transformation through SQL-based operations within a managed data warehouse setup. |
| **Amazon Redshift Spectrum**  | Query over S3 Data              | Query S3-based structured data directly without loading it into Redshift.                             | Extends Redshift's capabilities by allowing you to query data already hosted in Amazon S3.           |
| **AWS Lambda**                | Event-Driven Data Processing    | Perform custom data transformations and lightweight feature engineering using serverless compute.      | No infrastructure required for workflows with small-scale custom transformation tasks.               |
| **Amazon Kinesis Data Analytics** | Real-Time Data Integration   | Analyze streaming data and perform transformations in real-time.                                      | Focused on Kinesis streams for real-time analytics and transformations.                             |
| **Amazon QuickSight**         | Data Visualization & Analytics | Create visualizations, perform lightweight transformations, and build dashboards from datasets.        | Primarily used for business intelligence with minor transformation capabilities.                     |
| **Amazon Sagemaker Data Wrangler** | Feature Engineering for ML | Aggregate, clean, normalize, and transform datasets specifically for machine learning workflows.       | A tool within SageMaker specifically designed for feature engineering in ML.                         |
| **AWS Step Functions**        | Workflow Orchestration         | Orchestrate ETL pipelines by integrating multiple services like AWS Glue, Lambda, and SageMaker.       | Mainly used for combining and managing workflows across multiple data transformation services.        |
| **AWS Data Pipeline**         | Data Workflow Automation       | Create end-to-end data workflows for transformation and integration with periodic scheduling.          | Older ETL automation tool with support for batch processing.                                         |
| **Amazon Athena**             | Interactive Query Service       | Query and transform S3 data using SQL.                                                                | Serverless service to perform lightweight data transformation using SQL queries.                      |
| **AWS Lake Formation**        | Centralized Data Repository     | Build a centralized data lake, clean and catalog data from various sources.                           | Focuses on managing, cataloging, and transforming data at scale in data lakes.                       |
| **Amazon OpenSearch Service** | Search and Analytics            | Perform structured searches and real-time analytics on transformed data (e.g., logs, JSON, metrics).   | Optimized for structured search queries and visual analytics.                                        |
| **Amazon DynamoDB Streams**   | Real-Time Streaming Data        | Integrate and transform change data captured in real-time from DynamoDB tables.                       | Specifically tied to DynamoDB for real-time data transformation and integration workflows.            |
| **Amazon AppFlow**            | SaaS Data Integration           | Transfer and transform data between SaaS applications (e.g., Salesforce) and AWS services.            | A specialized tool for integrating and transferring data from SaaS platforms to AWS.                 |
| **AWS Batch**                 | Batch Processing                | Execute large-scale data processing or transformation workflows in batch jobs.                        | Designed for large-scale compute-intensive, batch-driven workflows.                                  |  
</b></details>

<details>
<summary>  List all AWS Managed AI Services ?.</code></summary><br><b>
| Service | Key Use Cases | Key Difference |
| :-- | :-- | :-- |
| Amazon Comprehend | NLP/Text Analytics | Text analytics, sentiment analysis, entity recognition, and language processing. |
| Amazon Rekognition | Computer Vision | Image/video analysis, object detection, facial recognition, and label detection. |
| Amazon Polly | Speech AI | Text-to-speech conversion with lifelike voices for interactive applications. |
| Amazon Translate | NLP/Language Translation | Language translation across multiple languages. |
| Amazon Forecast | Time Series Forecasting | Predict future outcomes like financial metrics, inventory, and demand planning. |
| Amazon Lookout for Metrics | Anomaly Detection | Detection of anomalies in metrics like revenue, sales, and operational data. |
| Amazon Lookout for Vision | Computer Vision | Detect quality defects in manufactured products with computer vision. |
| Amazon Bedrock | Generative AI | Run and scale generative AI models like GPT, Claude, and others on AWS infrastructure. |
| Amazon SageMaker | End-to-End ML Platform | Build, train, and deploy custom machine learning models. |
| AWS Panorama | Edge AI | Edge computer vision for analyzing on-premises video streams locally in low-latency environments. |
| Amazon Lex | Conversational AI | Conversational AI for creating chatbots or voice bots for customer service and virtual assistants. |
| Amazon Textract | Document Processing | Extract text, tables, and forms from scanned documents. |
| Amazon Personalize | Recommendations | Build personalized recommendations for users (e.g., e-commerce, media). |
| Amazon CodeWhisperer | Developer Productivity | AI-powered code suggestions and completions to enhance developer productivity. |
| Amazon HealthLake | Healthcare AI | Process and analyze health-related data, store, and transform data in HL7 FHIR format. |
| AWS Q Business | Business Optimization | Optimization and quantum-inspired solutions for solving complex computational problems in logistics, finance, and manufacturing. |
| Amazon Fraud Detector | Fraud Detection | Detect and prevent online fraud in real time. |
| Amazon Transcribe | Speech-to-Text Conversion | Automatic transcription of spoken language from audio files. |
| AWS DeepLens | Computer Vision/Hardware | Edge hardware for computer vision modeling and deployment. |
| Amazon Kendra | Enterprise Search | Enhances enterprise productivity with machine learning-powered contextual search across large data sources. |
| AWS Glue DataBrew | Data Preparation | No-code data preparation for machine learning workflows and analytics. |
| Amazon Neptune ML | Graph ML | Use graph machine learning models to analyze relationships in highly connected data. |

# AWS Managed AI Services (Including AWS Q Business)

| **Service**                   | **Category**                | **NLP** | **Computer Vision** | **Speech Processing** | **Time Series Prediction** | **Anomaly Detection** | **Generative AI** | **Optimization** |
|-------------------------------|-----------------------------|---------|----------------------|------------------------|----------------------------|-----------------------|-------------------|------------------|
| **Amazon Comprehend**         | NLP/Text Analytics         | ✔       |                      |                        |                            |                       |                   |                  |
| **Amazon Rekognition**        | Computer Vision            |         | ✔                    |                        |                            |                       |                   |                  |
| **Amazon Polly**              | Speech AI                 |         |                      | ✔                      |                            |                       |                   |                  |
| **Amazon Translate**          | NLP/Language Translation   | ✔       |                      |                        |                            |                       |                   |                  |
| **Amazon Forecast**           | Time Series Forecasting    |         |                      |                        | ✔                          |                       |                   |                  |
| **Amazon Lookout for Metrics**| Anomaly Detection          |         |                      |                        |                            | ✔                     |                   |                  |
| **Amazon Lookout for Vision** | Computer Vision            |         | ✔                    |                        |                            |                       |                   |                  |
| **Amazon Bedrock**            | Generative AI              |         |                      |                        |                            |                       | ✔                 |                  |
| **Amazon SageMaker**          | End-to-End ML Platform     | ✔       | ✔                    | ✔                      | ✔                          | ✔                     |                   | ✔                |
| **AWS Panorama**              | Edge AI                   |         | ✔                    |                        |                            |                       |                   |                  |
| **Amazon Lex**                | Conversational AI          | ✔       |                      | ✔                      |                            |                       |                   |                  |
| **Amazon Textract**           | Document Processing        |         | ✔                    |                        |                            |                       |                   |                  |
| **Amazon Personalize**        | Recommendations            | ✔       |                      |                        |                            | ✔                     |                   |                  |
| **Amazon CodeWhisperer**      | Developer Productivity     |         |                      |                        |                            |                       |                   |                  |
| **Amazon HealthLake**         | Healthcare AI              | ✔       |                      |                        | ✔                          | ✔                     |                   |                  |
| **AWS Q Business**            | Business Optimization      |         |                      |                        |                            |                       |                   | ✔                |
| **Amazon Fraud Detector**     | Fraud Detection            |         |                      |                        |                            | ✔                     |                   |                  |
| **Amazon Transcribe**         | Speech-to-Text Conversion  |         |                      | ✔                      |                            |                       |                   |                  |
| **AWS DeepLens**              | Computer Vision/Hardware   |         | ✔                    |                        |                            |                       |                   |                  |
| **Amazon Kendra**             | Enterprise Search          | ✔       |                      |                        |                            |                       |                   |                  |
| **AWS Glue DataBrew**         | Data Preparation           |         |                      |                        |                            |                       |                   |                  |
| **Amazon Neptune ML**         | Graph ML                  |         |                      |                        |                            |                       |                   |                  |
</b></details>
