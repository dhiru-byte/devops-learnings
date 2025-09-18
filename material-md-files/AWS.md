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
<summary>  Lst all AWS Managed Ai Services ?.</code></summary><br><b>

| Service | Key Use Cases | Key Difference |
| :-- | :-- | :-- |
| Amazon Comprehend | Text analytics, sentiment analysis, entity recognition, key phrase extraction. | Focuses on natural language processing (NLP). |
| Amazon Textract | Extract text, tables, and forms from documents. | Specifically designed for extracting text and data from scanned documents and forms using OCR. |
| Amazon Rekognition | Image and video analysis, object detection, facial recognition, label detection. | Focuses on computer vision-based tasks with pre-trained models. |
| Amazon SageMaker | Build, train, and deploy custom machine learning models. | Fully flexible platform for custom ML model development; not pre-trained AI. |
| Amazon Translate | Language translation between multiple languages. | Designed specifically for machine translation. |
| Amazon Polly | Text-to-speech conversion with lifelike voices. | Converts text to speech, enabling the development of voice-enabled applications. |
| Amazon Lex | Build conversational AI, chatbots, and voice bots. | Focused on creating AI-driven virtual assistants with ASR (Automatic Speech Recognition) and NLP. |
| Amazon Transcribe | Automatic speech-to-text transcription from audio/video files. | Specifically enables speech-to-text conversion tasks for audio and video content. |
| Amazon Personalize | Build real-time personalized recommendations (e.g., retail, media). | Designed for recommendation system creation using machine learning models. |
| Amazon Forecast | Time-series data forecasting (e.g., inventory, financial metrics, demand). | Optimized for time-series forecasting with ML models. |
| Amazon CodeWhisperer | AI-powered code completion and generation for developers. | Similar to GitHub Copilot; focuses on developer productivity in writing code. |
| Amazon Kendra | Enterprise search service for retrieving structured and unstructured data. | Focuses on information retrieval to enhance workplace productivity and knowledge management. |
| AWS DeepLens | Develop and deploy deep learning models using a camera-enabled device. | Hardware-integrated solution for edge computing with computer vision applications. |
| Amazon HealthLake | Store, transform, and analyze health-related data. | Healthcare-specific AI service for processing medical data in HL7 FHIR format. |
| Amazon Lookout for Equipment | Predictive maintenance for industrial systems (e.g., monitor IoT device health). | Tailored for anomaly detection in sensor and IoT data to maintain industrial machinery. |
| Amazon Lookout for Metrics | Anomaly detection for business or operational metrics (e.g., revenue, sales). | Focused on finding anomalies in large-scale business/event metric datasets. |
| Amazon Lookout for Vision | Detect quality defects in manufactured products. | Tailored for visual anomaly detection in manufacturing (industrial quality assurance). |
| Amazon Bedrock | Run and scale foundation models (generative AI) like GPT, Claude, etc. | Focused on generative AI, providing different popular models as managed services. |
| AWS Panorama | Computer vision at the edge for analyzing on-premises video streams. | Edge AI solution for computer vision in low-latency environments. |
| AWS Glue DataBrew | Data preparation for ML and analytics through a no-code visual interface. | Preprocessing tool for preparing data before running machine learning workflows. |
| Amazon Fraud Detector | Build and deploy fraud detection models. | Designed to detect fraud in real-time transactions with custom ML models. |
| Amazon Neptune ML | Create, analyze, and query graphs using graph embeddings. | Machine learning for graph-based data in applications like social networks and knowledge graphs. |

AWS Managed AI Service Chart                                                                                                                     
-------------------------------------------------------------------------------------------------------------------------------------------------
| Service                       | NLP    | Computer Vision  | Speech Processing | Time Series Prediction | Anomaly Detection | Generative AI    |
-------------------------------------------------------------------------------------------------------------------------------------------------
| Amazon Comprehend             |   ✔    |                 |                   |                        |                   |                 |
| Amazon Rekognition            |        | ✔               |                   |                        |                   |                 |
| Amazon Polly                  |        |                 | ✔                |                        |                   |                 |
| Amazon Translate              |   ✔    |                 |                   |                        |                   |                 |
| Amazon Forecast               |        |                 |                   |    ✔                   |                   |                 |
| Amazon Lookout for Metrics    |        |                 |                   |                        |      ✔           |                 |
| Amazon Bedrock                |        |                 |                   |                        |                   | ✔               |
| Amazon SageMaker              |   ✔    | ✔               | ✔                |    ✔                   |      ✔           |                 |
| AWS Panorama                  |        | ✔               |                   |                        |                   |                 |
| Amazon Lex                    |   ✔    |                 | ✔                |                        |                   |                 |
| Amazon Textract               |        | ✔               |                   |                        |                   |                 |
-------------------------------------------------------------------------------------------------------------------------------------------------

</b></details>
