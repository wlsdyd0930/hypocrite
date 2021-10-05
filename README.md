# ICLR 2022 Artifact for HYPOCRITE

## Title

HYPOCRITE: Homoglyph Adversarial Examples for Natural Language Web Services in the Physical World

## Authors

JINYONG KIM \<timkim@skku.edu\>

JEONGHYEON KIM \<jeonghyeon12@skku.edu\>

MOSE GU \<rna0415@g.skku.edu\>

SANGHAK OHH \<sanghak@skku.edu\>

GILTEUN CHOI \<gilteun@pusan.ac.kr\>

JAEHOON JEONG \<pauljeong@skku.edu\>

# Overview

Recently, as Artificial Intelligence (AI) develops, many companies in various industries are trying to use AI by grafting it into their domains.
Also, for these companies, various cloud companies (e.g., Amazon, Google, IBM, and Microsoft) are providing AI services as the form of Machine-Learning-as-a-Service (MLaaS).
However, although these AI services are very advanced and well-made, security vulnerabilities such as adversarial examples still exist, which can interfere with normal AI services.
This paper demonstrates a HYPOCRITE for hypocrisy that generates homoglyph adversarial examples for natural language web services in the physical world. This  hypocrisy can disrupt normal AI services provided by the cloud companies.
The key idea of HYPOCRITE is to replace English characters with other international  characters that look similar to them in order to give the data set noise to the AI engines.
By using this key idea, parts of text can be appropriately substituted for subtext with malicious meaning through black-box attacks for natural language web services in order to cause misclassification.
In order to show attack potential by HYPOCRITE, this paper implemented a framework that makes homoglyph adversarial examples for natural language web services in the physical world and evaluated the performance under various conditions.
Through extensive experiments, it is shown that HYPOCRITE is more effective than other baseline in terms of both attack success rate and perturbed ratio.

# Build Environment

We tested with the following versions of software:

1. Ubuntu 18.04.5 LTS

2. Python 3.9.7

# Prerequisites

Get API Key from each web service platform.

1. Amazon
   - Reference: https://aws.amazon.com/ko/comprehend

2. Google
   - Reference: https://cloud.google.com/natural-language

3. IBM
   - Reference: https://www.ibm.com/kr-ko/cloud/watson-natural-language-understanding

3. Microsoft
   - Reference: https://azure.microsoft.com/services/cognitive-services/text-analytics

# How to build

`pip install -r requirements.txt`

# How to run
1. To use APIs of each web service platform, set up the environment.

2. Change directory to Root directory 

3. To Configure HYPOCRITE, revise main.py 
    - dataset
        * IMDB
    - target_model
        * amazon - Amazone Comprehend
        * google - Google Cloud NLP
        * ibm - IBM Waston Natural Language Understanding
        * microsoft - Microsoft Azure Text Analytics
    - source
        * None
        * positive
        * negative
    - target_result
        * None - Non-target
        * positive
        * negative
        * mixed
        * neutral
    - length: Text Length Group
        * 1 - x < 500 
        * 2 - 500 <= x < 800
        * 3 - 800 <= x < 1100
        * 4 - 1100 <= x < 1400
        * 5 - 1400 <= x < 1700
        * 6 - 1700 <= x < 2000
        * 7 - 2000 <= x < 2500
    - num: # of text

4. Execute the HYPOCRTIE
    - python main.py

# ICLR 2022 Evaluation

## To Reproduce the measurement

1. Revise performance_evaluation_script.py
    - dataset
        * IMDB
    - target_model
        * amazon - Amazone Comprehend
        * google - Google Cloud NLP
        * ibm - IBM Waston Natural Language Understanding
        * microsoft - Microsoft Azure Text Analytics
    - source
        * None
        * positive
        * negative
    - target_result
        * None - Non-target
        * positive
        * negative
        * mixed
        * neutral
    - length: Text Length Group
        * 1 - x < 500 
        * 2 - 500 <= x < 800
        * 3 - 800 <= x < 1100
        * 4 - 1100 <= x < 1400
        * 5 - 1400 <= x < 1700
        * 6 - 1700 <= x < 2000
        * 7 - 2000 <= x < 2500
    - num: # of text
2. Execute the HYPOCRTIE
    - python performance_evaluation_script.py
    