# IT23665866_ITPM_ASSIGNMENT_01

Automated Playwright test suite for IT3040 ITPM Assignment 1, designed to evaluate the accuracy and reliability of PixelsSuite Chat Translator when translating chat-style Singlish into Sinhala.

## Application Under Test

https://www.pixelssuite.com/chat-translator

## Test Scope

This project contains 50 negative test cases that identify situations where the system fails to correctly convert Singlish input into Sinhala output.

The test cases cover all 24 required Singlish input types, with at least two test cases for each type. The coverage includes question forms, command forms, greetings, requests, responses, repeated words, punctuation, spelling variants, mixed English content, platform names, abbreviations, numbers, currency, dates, time formats, measurements, slang, online identifiers, and emojis.

## Files

- `IT23665866_test_automation.py` - Playwright automation script
- `IT23665866_Assignment 1 - Test cases.xlsx` - completed test case Excel file with actual output, status, input type coverage, and evidence/rationale
- `IT23665866_Github_link.txt` - public GitHub repository link
- `requirements.txt` - required Python packages

## Prerequisites

- Python 3.11 or 3.12
- pip
- Google Chrome or Playwright Chromium
- Internet access

## Install Dependencies

```powershell
pip install -U pip
pip install -r requirements.txt
playwright install
```

## Run the Test Suite

From this project folder, run:

```powershell
python IT23665866_test_automation.py --excel "IT23665866_Assignment 1 - Test cases.xlsx" --url "https://www.pixelssuite.com/chat-translator" --wait-ms 5000 --type-delay-ms 80 --slow-mo-ms 200 --save-every 1 --keep-open
```

## View Results

After execution, open `IT23665866_Assignment 1 - Test cases.xlsx` and review the `Actual Output` and `Status` columns.
