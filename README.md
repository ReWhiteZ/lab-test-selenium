# Lab 02 — Selenium with Python

คู่มือเริ่มโปรเจกต์ Selenium ด้วย Python ตั้งแต่สร้างโฟลเดอร์ใหม่ พร้อมแนวทางเขียน browser test เบื้องต้น เนื้อหาเน้น Python และ Selenium โดยตัวอย่างหน้าเว็บเป็นเพียงตัวอย่างประกอบ

## สิ่งที่ต้องมี

- Python 3.10 ขึ้นไป (โปรเจกต์นี้กำหนด Python 3.14)
- `uv` สำหรับจัดการ environment และ dependencies
- Google Chrome หรือ Chromium

ติดตั้ง `uv` ตามคำแนะนำในเอกสารทางการ แล้วตรวจสอบด้วย `uv --version` และ `python --version` โดย Selenium รุ่นใหม่มี Selenium Manager ช่วยจัดหา WebDriver ให้เมื่อเปิดเบราว์เซอร์ครั้งแรก จึงไม่จำเป็นต้องดาวน์โหลด ChromeDriver แยกในกรณีทั่วไป

## สร้างโปรเจกต์จากศูนย์

เปิด PowerShell ในตำแหน่งที่ต้องการเก็บงาน แล้วรัน:

```powershell
uv init --python 3.14 selenium-python-tests
cd selenium-python-tests
uv add selenium
```

คำสั่งจะสร้างโฟลเดอร์โปรเจกต์และ `.venv` ให้เมื่อเรียก `uv run` ครั้งแรก จากนั้นสร้างไฟล์ `test_browser.py` ที่ root ของโปรเจกต์ เพื่อเขียนสคริปต์ทดสอบ

หากต้องการโครงสร้างทดสอบแยกจากไฟล์อื่น สามารถสร้าง `tests/` แล้ววางไฟล์ไว้ภายในได้

## โครงสร้างโปรเจกต์ตัวอย่าง

```text
selenium-python-tests/
├── .venv/
├── pyproject.toml
├── uv.lock
└── test_browser.py
```

ควร commit `pyproject.toml` และ `uv.lock` เพื่อบันทึก dependency แต่ไม่ควร commit `.venv/`

## หลักการเขียน Selenium test

ลำดับทั่วไปของ browser test คือ เปิด WebDriver, เข้า URL, หา element ด้วย locator, ทำ action, รอผลลัพธ์, ตรวจด้วย assertion แล้วปิด browser เสมอ ใช้ explicit wait แทนการหน่วงด้วย `sleep` เพราะรอเฉพาะเงื่อนไขที่ต้องการและลดความไม่เสถียร

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_page_title():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://example.com")
        heading = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert heading.text == "Example Domain"
    finally:
        driver.quit()
```

- `By.ID`, `By.CSS_SELECTOR`, `By.XPATH` ใช้ระบุตำแหน่ง element
- `WebDriverWait` และ `expected_conditions` ใช้รอ element หรือสถานะหน้า
- `assert` ใช้ยืนยันผลที่คาดหวัง หากไม่ตรง test จะล้มเหลวพร้อม traceback
- `try/finally` ช่วยปิด browser แม้ระหว่าง test จะเกิดข้อผิดพลาด

## รันโปรเจกต์นี้

ไฟล์ตัวอย่างใน Lab นี้เป็นสคริปต์ Selenium แบบตรงไปตรงมา โดยใช้ `assert` เป็นจุดตรวจสอบ:

```powershell
uv add selenium
uv run python 67160134.py
```

สคริปต์เปิด Chrome, ทำขั้นตอนต่าง ๆ ผ่าน locator และ explicit wait, ตรวจ URL/ข้อความ/จำนวนสินค้า แล้วปิด browser ใน `finally`

## แนะนำต่อยอดเป็น pytest

Selenium เป็น browser automation library ไม่ได้จัดการโครงสร้าง test หรือรายงานผลให้ครบในตัว หากต้องการแยกกรณีทดสอบและรันเป็นชุด ให้เพิ่ม pytest:

```powershell
uv add --dev pytest
uv run pytest -v
```

ตั้งชื่อไฟล์ `test_*.py` และชื่อฟังก์ชัน `test_*` เพื่อให้ pytest ค้นพบ จากนั้นย้ายแต่ละ scenario ไปเป็นฟังก์ชันแยก และใช้ fixture สำหรับเตรียม/ปิด WebDriver

## แนวทางที่ควรทำ

- เลือก locator ที่เสถียร เช่น `id` หรือ `data-test` ก่อน XPath ที่ผูกกับโครงสร้างหน้า
- รอ condition ที่ต้องการแทนการใช้เวลาหน่วงตายตัว
- ให้แต่ละ test ตรวจผลที่สังเกตได้ เช่น URL, ข้อความ, หรือค่าบนหน้า
- ปิด browser ทุกครั้ง และอย่าเก็บรหัสผ่านจริงไว้ใน source code
