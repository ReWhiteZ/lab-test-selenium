from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    # 1. เปิดหน้าเข้าสู่ระบบ
    driver.get("https://www.saucedemo.com/")

    # 2. รอให้ช่อง Username ปรากฏ แล้วกรอกข้อมูล
    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    username_input.send_keys("standard_user")

    # 3. กรอก Password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("secret_sauce")

    # 4. คลิกปุ่ม Login
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # 5. รอจนกว่าจะเข้าสู่หน้าสินค้า
    wait.until(
        EC.url_to_be("https://www.saucedemo.com/inventory.html")
    )

    # 6. ตรวจสอบ URL อีกครั้งด้วย Assertion
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", (
        f"เข้าสู่หน้าสินค้าไม่สำเร็จ URL ปัจจุบันคือ {driver.current_url}"
    )

    print("เข้าสู่ระบบและเปิดหน้าสินค้าสำเร็จ")

     # 7. ค้นหาสินค้าจากชื่อ ไม่ใช้ลำดับตำแหน่งของสินค้า
    backpack_item = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//div[@data-test='inventory-item'"
            " and .//div[@data-test='inventory-item-name'"
            " and normalize-space()='Sauce Labs Backpack']]"
        ))
    )

    # 8. คลิกปุ่ม Add to cart ภายในกล่องสินค้าที่ค้นพบ
    add_to_cart_button = backpack_item.find_element(By.TAG_NAME, "button")
    add_to_cart_button.click()

    # 9. รอให้ปุ่มเปลี่ยนเป็น Remove เพื่อยืนยันว่าเพิ่มสินค้าแล้ว
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "remove-sauce-labs-backpack"),
            "Remove"
        )
    )

    # 10. ตรวจสอบว่าตะกร้ามีสินค้า 1 ชิ้น
    cart_badge = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert cart_badge.text == "1", (
        f"จำนวนสินค้าในตะกร้าไม่ถูกต้อง พบ: {cart_badge.text}"
    )

    print("เพิ่ม Sauce Labs Backpack ลงตะกร้าสำเร็จ จำนวน 1 ชิ้น")

     # 11. คลิกไอคอนตะกร้าสินค้า
    cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_link.click()

    # 12. รอให้เปิดหน้าตะกร้า
    wait.until(
        EC.url_to_be("https://www.saucedemo.com/cart.html")
    )

    # 13. ตรวจสอบว่าสินค้าในตะกร้าคือ Sauce Labs Backpack
    cart_item_name = wait.until(
        EC.visibility_of_element_located((
            By.CLASS_NAME,
            "inventory_item_name"
        ))
    )
    assert cart_item_name.text == "Sauce Labs Backpack", (
        f"สินค้าในตะกร้าไม่ถูกต้อง พบ: {cart_item_name.text}"
    )

    print("เปิดหน้าตะกร้าและพบ Sauce Labs Backpack แล้ว")

    # 14. คลิกปุ่ม Checkout
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()

    # 15. รอให้เปิดหน้ากรอกข้อมูลการจัดส่ง
    wait.until(
        EC.url_to_be("https://www.saucedemo.com/checkout-step-one.html")
    )

    print("กด Checkout และเปิดหน้ากรอกข้อมูลการจัดส่งสำเร็จ")

     # กรอกข้อมูลการจัดส่ง
    first_name_input = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )
    first_name_input.send_keys("Somchai")

    last_name_input = driver.find_element(By.ID, "last-name")
    last_name_input.send_keys("Testing")

    postal_code_input = driver.find_element(By.ID, "postal-code")
    postal_code_input.send_keys("10110")

    # ไปหน้า Overview
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()

    wait.until(
        EC.url_to_be("https://www.saucedemo.com/checkout-step-two.html")
    )

    # ตรวจสอบว่าสินค้าในหน้า Overview ถูกต้อง
    overview_item_name = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )
    assert overview_item_name.text == "Sauce Labs Backpack", (
        f"สินค้าในหน้า Overview ไม่ถูกต้อง พบ: {overview_item_name.text}"
    )

    print("กรอกข้อมูลจัดส่งและตรวจพบ Sauce Labs Backpack ในหน้า Overview แล้ว")

     # ยืนยันคำสั่งซื้อ
    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()

    # รอและตรวจข้อความยืนยัน
    success_message = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order!" in success_message.text, (
        f"ไม่พบข้อความยืนยันคำสั่งซื้อ พบ: {success_message.text}"
    )

    print("Thank you for your order!")

finally:
    driver.quit()