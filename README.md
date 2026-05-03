# IT23665866_ITPM_ASSIGNMENT_01

Automated test suite using PixelsSuite for IT3040-ITPM to assess PixelsSuite's Singlish-to-Sinhala accuracy. It features 50 negative tests across 24 linguistic categories, including mixed-language content and slang. Designed to identify transliteration failures and evaluate robustness in real-time chat scenarios.

The primary objective is to evaluate the system's transliteration accuracy, UI stability, and robustness under diverse conditions.




## 🧪 Test Suite Overview

The test suite validates 50 distinct negative scenarios focusing on transliteration failures of chat-style Singlish input.

### 🔹 50 Negative Functional Tests
These tests evaluate cases where the system fails to correctly convert Singlish input into Sinhala output. The scenarios cover a wide range of informal language patterns, spelling variations, embedded English words, symbols, and real-world chat inputs.

Each test case is designed to highlight inaccuracies, misinterpretations, or inconsistencies in the transliteration process.

The test suite ensures coverage of all 24 Singlish input types, with at least two test cases per type, including:

- Question forms  
- Commands  
- Greetings  
- Requests and responses  
- Romanization variants  
- English word insertions  
- App/platform names  
- Numbers, currency, dates, and time formats  
- Slang, emojis, and online identifiers  

The remaining test cases include additional edge cases to further evaluate system weaknesses.




## 📋 Prerequisites

Before executing the automated test cases, ensure the following prerequisites are installed and properly configured:

- Python 3.11 or 3.12 – Required to run the Playwright automation scripts  
- pip – Used to install required Python packages  
- Playwright – Automation framework used to execute the transliteration test cases  
- openpyxl library – Used for reading and writing Excel files  
- Google Chrome browser (or Chromium via Playwright) – Required for running browser-based tests  

### Additionally, ensure:
- The provided test automation project folder is extracted properly  
- The system has internet access to access the transliteration web application  




## ⚙️ Installation

- Extract the provided automation project folder  
- Navigate to the project directory using Command Prompt  

### Install required dependencies:

pip install -U pip
pip install playwright openpyxl


### Install browser binaries:

playwright install





## ▶️ Running the Tests

Execute all 50 negative test cases using:


python test_automation.py --excel "test_automation/Assignment 1 - Test cases.xlsx" --url "https://www.pixelssuite.com/chat-translator"




## 📊 Viewing the Test Results

- Open the Excel file after execution  
- Verify **Actual Output** and **Status** columns  
