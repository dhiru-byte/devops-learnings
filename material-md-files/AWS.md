# AWS 

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

---

<details>
<summary>What is the purpose of feature engineering in machine learning workflows?</summary><br><b>

**Options:**
- **A.** Simplify model deployment  
- **B.** Improve data storage efficiency  
- **C.** Select, transform, and prepare data for training  
- **D.** Manage training infrastructure  

**Answer:**  
**C. Select, transform, and prepare data for training**

**Explanation:**  
Feature engineering involves selecting, transforming, and pre-processing data to make it suitable for training a machine learning model. It is a crucial step in creating high-quality datasets that improve model accuracy.
</b></details>

<details>
<summary>Which AWS service is most suitable for cleaning and normalizing data through a no-code interface?</summary><br><b>

**Options:**
- **A.** Amazon SageMaker  
- **B.** AWS Glue DataBrew  
- **C.** Amazon EMR  
- **D.** AWS Data Pipeline  

**Answer:**  
**B. AWS Glue DataBrew**

**Explanation:**  
AWS Glue DataBrew provides a visual, no-code interface to clean, normalize, and transform data. It is specifically designed for users who require an easy-to-use tool for data preparation without writing complex scripts.
</b></details>

<details>
<summary>You query data stored in Amazon S3 using SQL for lightweight transformation. Which AWS service should you choose?</summary><br><b>

**Options:**
- **A.** Amazon Athena  
- **B.** AWS Glue  
- **C.** AWS Step Functions  
- **D.** Amazon Kinesis Data Analytics  

**Answer:**  
**A. Amazon Athena**

**Explanation:**  
Amazon Athena is a serverless SQL-based query service that allows you to perform lightweight transformations and analysis directly on data stored in Amazon S3.
</b></details>

<details>
<summary>Which AWS service enables on-the-fly data preprocessing and transformation for machine learning workflows?</summary><br><b>

**Options:**
- **A.** Amazon S3  
- **B.** Amazon SageMaker Data Wrangler  
- **C.** AWS Glue Studio  
- **D.** Amazon Redshift  

**Answer:**  
**B. Amazon SageMaker Data Wrangler**

**Explanation:**  
SageMaker Data Wrangler simplifies data preparation and feature engineering by providing an interactive interface for pre-processing datasets and exporting them directly into the machine learning pipeline.
</b></details>

<details>
<summary>How can you ensure data integrity during ETL (Extract, Transform, Load) processes?</summary><br><b>

**Options:**
- **A.** Use Amazon CloudWatch to trigger metrics  
- **B.** Implement checksums or hashes during data transfer  
- **C.** Use AWS Auto Scaling to handle data overflow  
- **D.** Configure Amazon S3 bucket logging  

**Answer:**  
**B. Implement checksums or hashes during data transfer**

**Explanation:**  
Data integrity can be preserved by implementing validation mechanisms like checksums or hashes during and after the data transfer. AWS services like AWS Glue and Amazon S3 integrate integrity checks automatically during certain operations.
</b></details>

<details>
<summary>You need to join multiple datasets and transform them for downstream analysis. Which AWS service is the most suitable?</summary><br><b>

**Options:**
- **A.** Amazon Athena  
- **B.** AWS Glue  
- **C.** Amazon Kinesis Data Streams  
- **D.** Amazon QuickSight  

**Answer:**  
**B. AWS Glue**

**Explanation:**  
AWS Glue is specifically designed for ETL operations required to join, clean, and transform data from multiple sources. It automates workflows and supports transformation at scale.
</b></details>

<details>
<summary>You are preparing a dataset for a regression model. Which preprocessing steps should you perform? (Select TWO)</summary><br><b>

**Options:**
- **A.** One-hot encode categorical features  
- **B.** Normalize continuous features  
- **C.** Apply dropout techniques to the dataset  
- **D.** Use k-means clustering on the dataset  
- **E.** Convert text features to binary files  

**Answer:**  
**A. One-hot encode categorical features**  
**B. Normalize continuous features**

**Explanation:**  
For regression models:
- **One-hot encoding** is used to convert categorical variables into binary format.  
- **Normalization** scales continuous features to bring them within the same range, improving convergence during training.
</b></details>

<details>
<summary>Which AWS service would you use for real-time data transformation in streaming pipelines?</summary><br><b>

**Options:**
- **A.** Amazon Kinesis Data Analytics  
- **B.** AWS Glue  
- **C.** Amazon QuickSight  
- **D.** Amazon S3  

**Answer:**  
**A. Amazon Kinesis Data Analytics**

**Explanation:**  
Amazon Kinesis Data Analytics allows you to process and transform streaming data in real-time using SQL, making it an ideal choice for real-time transformations.
</b></details>

<details>
<summary>Which technique would you use to handle missing data in a dataset? (Select TWO)</summary><br><b>

**Options:**
- **A.** Impute missing values with the median or mean  
- **B.** Use SageMaker Debugger to detect missing data  
- **C.** Remove rows or columns with missing values  
- **D.** Use SageMaker Model Monitoring for missing data adjustments  

**Answer:**  
**A. Impute missing values with the median or mean**  
**C. Remove rows or columns with missing values**

**Explanation:**  
Handling missing data is essential for clean datasets:
- Imputing replaces missing values with the mean or median.
- Removing rows or columns is used when missing data is substantial and cannot be meaningfully imputed.
</b></details>

<details>
<summary>Which AWS service would you use to orchestrate complex ETL workflows across multiple services?</summary><br><b>

**Options:**
- **A.** AWS Step Functions  
- **B.** AWS Glue DataBrew  
- **C.** Amazon SageMaker  
- **D.** Amazon EMR  

**Answer:**  
**A. AWS Step Functions**

**Explanation:**  
AWS Step Functions is a workflow orchestration service that integrates with multiple AWS services, such as Glue, Lambda, and SageMaker, to enable seamless ETL pipeline execution.
</b></details>

<details>
<summary>Which data integrity mechanism can ensure transformed datasets match the original source datasets in AWS Glue?</summary><br><b>

**Options:**
- **A.** Implement AWS Glue crawlers  
- **B.** Configure job bookmarks in Glue  
- **C.** Use S3 Versioning and data validation scripts  
- **D.** Utilize Amazon EMR’s Auto Scaling feature  

**Answer:**  
**C. Use S3 Versioning and data validation scripts**

**Explanation:**  
Versioning in Amazon S3, combined with validation scripts for checksums or row counts, ensures that transformed datasets retain data integrity against their original source datasets during Glue workflows.
</b></details>

<details>
<summary>What is a key reason to use feature scaling in machine learning workflows?</summary><br><b>

**Options:**
- **A.** To improve the interpretability of trained models  
- **B.** To handle highly skewed datasets  
- **C.** To ensure all features contribute equally to model training  
- **D.** To reduce dataset size for faster computation  

**Answer:**  
**C. To ensure all features contribute equally to model training**

**Explanation:**  
Feature scaling ensures equal contribution by bringing all feature values into the same range. This is crucial for models like Logistic Regression or Neural Networks that are sensitive to feature magnitudes.
</b></details>

<details>
<summary>Which AWS service specifically supports feature engineering by creating embeddings for structured relationship data?</summary><br><b>

**Options:**
- **A.** Amazon SageMaker Processing  
- **B.** Amazon Neptune ML  
- **C.** AWS Data Pipeline  
- **D.** Amazon Kinesis Data Firehose  

**Answer:**  
**B. Amazon Neptune ML**

**Explanation:**  
Amazon Neptune ML leverages graph neural networks to generate embeddings for conducting machine learning on highly connected datasets, such as social networks or recommendation systems.
</b></details>

---

<details>
<summary> Lists AWS Glue components and their purposes and use cases:?.</code></summary><br><b>
# AWS Glue Components and Their Use Cases

| **Component**              | **Purpose**                                | **Use Cases**                                                                                 |
|----------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------|
| **AWS Glue Data Catalog**  | Centralized metadata repository            | Stores metadata for all datasets, used for managing schemas and querying datasets with tools like Athena. |
| **AWS Glue Crawlers**      | Automatic schema discovery                 | Identifies and categorizes the structure and format of data in storage (e.g., S3, RDS, Redshift). |
| **AWS Glue ETL Jobs**      | Extract, Transform, Load (ETL) Operations  | Automates the process of extracting, transforming, and loading data with serverless functionality. |
| **AWS Glue Studio**        | Visual Interface for ETL Jobs              | Simplifies ETL job creation through a drag-and-drop interface designed for ease of use.       |
| **AWS Glue DataBrew**      | No-Code Data Preparation                   | Allows users to clean, normalize, and transform datasets visually without coding.             |
| **AWS Glue Workflows**     | Workflow Orchestration                     | Orchestrates complex ETL jobs, crawlers, and triggers in sequence or parallel workflows.      |
| **AWS Glue Triggers**      | Event-Based ETL Job Automation             | Automates running ETL, crawling, or workflows based on specific events or schedules.          |
| **AWS Glue Streaming ETL** | Real-Time Data Transformation              | Processes streaming data from sources like Amazon Kinesis or Apache Kafka for real-time transformations. |
| **AWS Glue Developer/API Access** | Programmatic ETL Job Creation       | Provides APIs and SDKs for developers to create custom ETL workflows using Python or Scala code. |
| **AWS Glue DPU (Data Processing Units)** | Scalable compute for jobs     | Provides distributed and scalable compute for handling large-scale data processing operations. |
| **AWS Glue Connections**   | Data Source Integration                    | Allows connectivity to external data stores like RDS, JDBC, or on-premises databases.         |
| **AWS Glue ML Transforms** | Machine Learning Transforms                | Automates significant transformations using machine learning techniques (e.g., deduplication, linkage). |
| **AWS Glue Schema Registry** | Schema Evolution Management             | Enables management, validation, and enforcement of schemas for streaming and batch data workflows. |
| **AWS Glue Partition Indexing** | Partition Optimization               | Optimizes querying large S3-based datasets with high granularity for faster performance.       |

</b></details>

<details>
<summary> List all AWS SageMaker's components and their use cases for various purposes .</code></summary><br><b>
# Amazon SageMaker Components and Their Use Cases

| **Component**                       | **Purpose**                               | **Use Cases**                                                                                         |
|-------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **SageMaker Studio**                | Integrated Development Environment (IDE) | Allows data scientists and developers to build, train, debug, and deploy ML models in a unified interface. |
| **SageMaker Data Wrangler**         | Data Preparation and Feature Engineering  | Simplifies data preparation, cleaning, and feature engineering for machine learning workflows.         |
| **SageMaker Autopilot**             | Build Models Automatically                | Automatically trains and tunes the best ML model based on your data while providing visibility into the process. |
| **SageMaker Training**              | Model Training                            | Trains ML models at scale with support for distributed training and custom training scripts.           |
| **SageMaker Processing**            | Data Preprocessing and Post-processing    | Run data preprocessing, post-processing tasks, or batch inference workloads using managed infrastructure. |
| **SageMaker Feature Store**         | Feature Management                        | Centralize, create, and reuse features for ML models across teams and projects.                        |
| **SageMaker Debugger**              | Debugging and Insights                    | Analyzes and debugs training jobs by identifying performance bottlenecks and providing actionable insights. |
| **SageMaker Model Monitor**         | Model Monitoring in Production            | Detects deviations, concept drift, and anomalies in model predictions to ensure accurate and reliable production models. |
| **SageMaker Pipelines**             | Machine Learning Pipelines                | Automates and orchestrates workflows for data preparation, model building, training, optimization, and deployment. |
| **SageMaker Ground Truth**          | Data Labeling                             | Builds accurate ground truth datasets for supervised learning by enabling human labeling tasks or semi-automation. |
| **SageMaker Neo**                   | Model Optimization for Edge               | Optimizes machine learning models to run faster and at lower latency on edge devices and hardware.      |
| **SageMaker JumpStart**             | Prebuilt Solutions and Models             | Provides pre-trained models, solution templates, and example notebooks for various ML use cases.        |
| **SageMaker Inference Recommender** | Recommendation for Deployment             | Automates the selection of the best resources for deploying machine learning models.                    |
| **SageMaker Hosting/Inferences**    | Model Deployment and Inference            | Deploys trained models as endpoints for real-time, batch, and asynchronous inference.                   |
| **SageMaker Clarify**               | Data Bias and Model Explainability        | Detects bias in your data and explains model predictions for fairness and transparency.                 |
| **SageMaker Model Registry**        | Centralized Model Repository              | Tracks and manages ML models and their versions for streamlined deployment and governance.              |
| **SageMaker Marketplace**           | External Model Use                        | Allows you to use and deploy pre-trained machine learning models and algorithms from third-party vendors. |
| **SageMaker Edge Manager**          | Edge Device Management                    | Deploys, manages, and monitors models on thousands of edge devices.                                    |

</b></details>

<details>
<summary> List all AWS Managed Data Transformation Integration and Feature Engineering Services ?.</code></summary><br><b>
  
| Use Case | Recommended Service |
| :-- | :-- |
| Automating ETL and large-scale integration | AWS Glue |
| No-code data transformation and cleaning | AWS Glue DataBrew |
| Batch processing of large datasets | AWS Batch |
| Real-time data streaming and transformation | Amazon Kinesis Data Analytics, DynamoDB Streams |
| Feature engineering for ML models | Amazon SageMaker Data Wrangler |
| Data querying with transformation | Amazon Athena, Redshift Spectrum |
| SaaS platform integration | Amazon AppFlow |
| Big data frameworks (Spark, Hadoop) | Amazon EMR |
| Centralized data repository for integration | AWS Lake Formation |
| Workflow orchestration and scheduling | AWS Step Functions, AWS Data Pipeline |
| Data visualization with lightweight prep | Amazon QuickSight |

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
| **AWS Batch**                 | Batch Processing                | Execute large-scale data processing or transformation workflows in batch jobs.                        | Designed for large-scale compute-intensive, batch-driven workflows.</b></details>

---

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

</b></details>
