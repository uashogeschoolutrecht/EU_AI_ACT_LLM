




--------------------------------------------------------------------------------------------------------------------------------------------------


# LLM EU AI Act Application

Welcome to the LLM EU AI Act Application repository. This project falls under the Responsible Applied Artificial Intelligence (RAAIT) program and focuses on the further development and optimization of a chatbot. The goal of this chatbot is to assist organizations in navigating the EU AI Act. We aim to transform this tool into an open-source platform where questions can be asked to a responsibly developed chatbot. Initially, the tool will be used for research experiments by Hogeschool Utrecht (HU).

The emphasis of this project is on the responsible application of AI, with the central question: "How do you ensure that people do not blindly trust a chatbot while also not unnecessarily distrusting it?" We aim to achieve this by fine-tuning the large language model (LLM) on the EU AI Act and applying a transparent method of source referencing. This allows users to see the sources on which the chatbot bases its answers.

The client wants to provide a discussion tool in the form of a chatbot on the website of Responsible Applied Artificial Intelligence (RAAIT). This prototype focuses on unlocking the EU AI Act to help business owners understand this legislation. Additionally, we want to explore how LLMs can provide information to laypeople.
The students need to implement the Mixtrall 7B model in a secure environment, collect user feedback, and securely store data.

The final product should be an LLM that works well with Retrieval Augmented Generation (RAG), can be safely used online, and maintained by someone with basic programming knowledge. It should be immediately usable for experiments but not for serious advice to businesses. It is essential that users are aware that they are using a test tool and that the advice is not intended for actual application within their business.

## Home Page
![Home Page](https://github.com/Xander-de-Keijzer/LLM-EU-AI-Act/assets/162982782/d65e5090-5139-4807-b5f0-63618c49baf1)
On the home page, you can ask your questions about the EU AI Act in English in the text box.

## Contact Page
![Contact Page](https://github.com/Xander-de-Keijzer/LLM-EU-AI-Act/assets/162982782/4dbf2bee-9c43-46b1-98f4-c0f936c3133e)
Find information about who you can contact for further questions on the contact page.

## Disclaimer Page
![Disclaimer Page](https://github.com/Xander-de-Keijzer/LLM-EU-AI-Act/assets/162982782/8585715e-38b9-4e77-8390-601e9612ee57)
The disclaimer page provides details about the purpose of the tool, emphasizing that it is strictly for research purposes and should not be considered as legal advice.

## Feedback Page
![Feedback Page](https://github.com/Xander-de-Keijzer/LLM-EU-AI-Act/assets/162982782/0e10df80-1033-4165-b884-37dd1ccdaf9c)
On the feedback page, you can provide your feedback by adjusting the sliders for response speed and answer quality, and by filling in the text box.

---

# LLM EU AI Act Application Guide

**This guide explains how to set up and use the LLM EU AI Act Application.** This project involves two virtual machines (VM1 and VM2) connected via Flask. Below, you'll find instructions for running the website, working with the LLM, and managing the databases.

## Table of Contents

1. [Installation Requirements](#installation-requirements)
2. [Setting Up the Environment](#setting-up-the-environment)
3. [Running the Website](#running-the-website)
4. [Using the Language Model (LLM)](#using-the-language-model-llm)
5. [Accessing the Databases](#accessing-the-databases)

## Installation Requirements

Make sure you have the following installed on both VMs:

1. Python 3.8/3.9
2. pip (Python package installer)
3. MySQL Server

## Setting Up the Environment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Xander-de-Keijzer/LLM-EU-AI-Act.git
   cd llm-eu-ai-act

2. Create a Virtual Environment on both VMs
   ```bash
   python3 -m venv env    # On VM1
   python3.9 -m venv venv # On VM2
   source env/bin/activate

3. Install Dependencies
    ```bash
    pip install -r requirements.txt

## Running the Website
VM1: Streamlit Application

1. Navigate to the Project Directory
   ```bash
   cd path/to/your/project/llm-eu-ai-act/vm1
   
2. Run Streamlit
   ```bash
   streamlit run home_page.py

VM2: Mixtral Application
1. Navigate to the Project Directory
   ```bash
   cd  path/to/your/project/llm-eu-ai-act/vm2

3. Run Mixtral
   ```bash
   python3 mixtral.py

## Using the Language Model (LLM)

### VM2

1. **Load and Initialize the LLM in your Mixtral app (Ensure paths and parameters are correctly set)**
   - Refer to `TextProcessor` class in your Mixtral application for setting up the LLM.

2. **Generating Responses**
   - Send a POST request from VM1 to the Mixtral server on VM2 with your query to get responses from the LLM.

### Sending a POST Request from VM1

To send a POST request from VM1 to the Mixtral server running on VM2, you can use the following Python code:

```python
import requests

# Define the server URL
url = "http://<vm2_ip>:5000/chat"

# Define your query
query = {
    "message": "Your question about the EU AI Act"
}

# Send the POST request
response = requests.post(url, json=query)

# Check the response
if response.status_code == 200:
    print("Response from LLM:", response.json()["message"])
else:
    print("Failed to get response from LLM:", response.status_code, response.text)
```

Replace <vm2_ip> with the actual IP address of your VM2. This script will send your query to the Mixtral server and print the response.

## Accessing the Databases
Viewing and Managing the Database

Access the MySQL database using the command line:
The username: feedbackuserai and the password: OnsWWvanhetprojectai123!
```bash
mysql -u yourusername -p
```

Show Databases: To see all databases in your MySQL server.
```sql
SHOW DATABASES;
```

Use a Database: To select a database to work with.
```sql
USE vragen_db;
-- or
USE feedback_db;
```

Show Tables: To list all tables in the selected database.
```sql
SHOW TABLES;
```

Select Data: To view the data in a specific table.
```sql
SELECT * FROM yourtable;
```

Exporting Databases
To export a database, you can use the mysqldump command.
```sql
mysqldump -u feedbackuserai -p vragen_db > vragen_db_backup.sql
-- or
mysqldump -u feedbackuserai -p feedback_db > feedback_db_backup.sql
```

## Troubleshooting

1. Common Issues
   - Environment Activation
   - Ensure your virtual environment is activated before running the application.

2. Database Connection
   - Verify your MySQL service is running and accessible.

3. Dependencies
   - Make sure all dependencies are installed via requirements.txt.

4. Logs
   - Check log files for any errors or issues. Logging is configured in both Streamlit and Mixtral applications.
















































# Requirements
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
```bash
pip3 install numpy pandas sparsembed transformers python-socketio streamlit mysql-connector-python httpx flask flask-socketio llama-cpp-python
```
