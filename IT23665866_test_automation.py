from playwright.sync_api import sync_playwright
import time
import os
import argparse
import re
from pathlib import Path
import sys
import openpyxl
from openpyxl.cell.cell import MergedCell

# Configuration
ROOT_DIR = Path(__file__).resolve().parent

DEFAULT_EXCEL_CANDIDATES = [
    str(ROOT_DIR / "IT23665866_Assignment 1 - Test cases.xlsx"),
    str(ROOT_DIR / "Assignment 1 - Test cases.xlsx"),
]


DEFAULT_SHEET_NAME = "Test cases"

DEFAULT_FRONTEND_URL = os.getenv("FRONTEND_URL", "https://www.pixelssuite.com/chat-translator")

DEFAULT_INPUT_COLUMN_CANDIDATES = [
    "Input","Input Column","Singlish Input","Test Input","Singlish","Source","Sentence","Text",
]

DEFAULT_EXPECTED_COLUMN_CANDIDATES = [
    "Sinhala","Expected_Output","Expected Output","Expected output","Expected","Expected Sinhala",
]

DEFAULT_ACTUAL_COLUMN_CANDIDATES = [
    "Actual_Output","Actual Output","Actual output","Actual",
]

DEFAULT_STATUS_COLUMN_CANDIDATES = [
    "Status","Result","Pass/Fail","Pass Fail",
]

DEFAULT_WAIT_MS = 8000
DEFAULT_RETRIES = 8
DEFAULT_RETRY_WAIT_MS = 1000
DEFAULT_TYPE_DELAY_MS = 50
DEFAULT_TIMEOUT_MS = 60000
DEFAULT_SLOW_MO_MS = 300
DEFAULT_SAVE_EVERY = 1



def _configure_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    except:
        pass


def _pick_existing_path(candidates):
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return candidates[0] if candidates else None


def _resolve_path(p):
    if not p:
        return None
    path = Path(p)
    return str(path if path.is_absolute() else (ROOT_DIR / path).resolve())


def _parse_args():
    parser = argparse.ArgumentParser(description="Run chat translator tests from an Excel sheet.")
    parser.add_argument("--excel", default=None, help="Path to the Excel test case file.")
    parser.add_argument("--url", default=DEFAULT_FRONTEND_URL, help="Frontend URL to test.")
    parser.add_argument("--wait-ms", type=int, default=DEFAULT_WAIT_MS, help="Wait time after each test action.")
    parser.add_argument("--type-delay-ms", type=int, default=DEFAULT_TYPE_DELAY_MS, help="Delay between typed characters.")
    parser.add_argument("--slow-mo-ms", type=int, default=DEFAULT_SLOW_MO_MS, help="Playwright slow motion delay.")
    parser.add_argument("--save-every", type=int, default=DEFAULT_SAVE_EVERY, help="Save workbook every N processed rows.")
    parser.add_argument("--keep-open", action="store_true", help="Keep browser open after tests finish.")
    return parser.parse_args()


def _normalize_header(value):
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def _header_values(ws, row):
    return [ws.cell(row=row, column=c).value for c in range(1, ws.max_column + 1)]



def _wait_for_output(page, previous_output=""):
    try:
        page.wait_for_function(
            """(previous) => {
                const textareas = Array.from(document.querySelectorAll('textarea'));
                const output = textareas[1]?.value?.trim() || "";
                return output.length > 0 && output !== previous;
            }""",
            arg=previous_output,
            timeout=30000
        )
        return True
    except:
        return False



def run_test():
    _configure_stdout()
    args = _parse_args()

    excel_path = _resolve_path(args.excel) if args.excel else _resolve_path(_pick_existing_path(DEFAULT_EXCEL_CANDIDATES))

    if not os.path.exists(excel_path):
        print(f"Excel file not found: {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path)
    ws = wb[DEFAULT_SHEET_NAME] if DEFAULT_SHEET_NAME in wb.sheetnames else wb.active

    header_row = 1
    headers = _header_values(ws, header_row)

    def find_col(names):
        norm = [_normalize_header(v) for v in headers]
        for n in names:
            if _normalize_header(n) in norm:
                return norm.index(_normalize_header(n)) + 1
        return None

    input_col = find_col(DEFAULT_INPUT_COLUMN_CANDIDATES)
    expected_col = find_col(DEFAULT_EXPECTED_COLUMN_CANDIDATES)
    actual_col = find_col(DEFAULT_ACTUAL_COLUMN_CANDIDATES) or ws.max_column + 1
    status_col = find_col(DEFAULT_STATUS_COLUMN_CANDIDATES) or ws.max_column + 2

    ws.cell(row=header_row, column=actual_col).value = "Actual Output"
    ws.cell(row=header_row, column=status_col).value = "Status"

    print("Starting test...")

    passed = 0
    failed = 0
    processed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=args.slow_mo_ms)
        page = browser.new_page()

        page.goto(args.url, timeout=DEFAULT_TIMEOUT_MS)
        page.wait_for_selector("textarea")

        input_box = page.locator("textarea").nth(0)
        output_box = page.locator("textarea").nth(1)
        button = page.get_by_role("button", name=re.compile("Transliterate", re.I))

        for row in range(header_row + 1, ws.max_row + 1):
            text = ws.cell(row=row, column=input_col).value
            if not text:
                continue

            expected = ws.cell(row=row, column=expected_col).value
            expected = str(expected).strip() if expected else ""

            print(f"Row {row}: {text}")

            try:
                prev = output_box.input_value()

                input_box.fill("")
                input_box.type(str(text), delay=args.type_delay_ms)

                button.click()

                _wait_for_output(page, prev)

                time.sleep(args.wait_ms / 1000)

                actual = output_box.input_value().strip()

                ws.cell(row=row, column=actual_col).value = actual

               
                if expected:
                    status = "PASS" if actual.strip() == expected.strip() else "FAIL"
                else:
                    status = "COLLECTED"

                ws.cell(row=row, column=status_col).value = status

                if status == "PASS":
                    passed += 1
                elif status == "FAIL":
                    failed += 1

                processed += 1
                print(f" -> {status}")

                if args.save_every > 0 and processed % args.save_every == 0:
                    wb.save(excel_path)

            except Exception as e:
                print(f"Error: {e}")
                ws.cell(row=row, column=status_col).value = "ERROR"
                wb.save(excel_path)

        if args.keep_open:
            print("Browser kept open. Press Ctrl+C to close this script when done.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass

        browser.close()

   
    print("\n=== TEST SUMMARY ===")
    print(f"Total: {processed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    wb.save(excel_path)
    print("Done.")


if __name__ == "__main__":
    run_test()
