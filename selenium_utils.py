from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_footer_css(url):
    driver = webdriver.Chrome()
    driver.get(url)
    js_script = """
    function getStyles(element) {
        const styles = window.getComputedStyle(element);
        let styleString = '';
        for (let property of styles) {
            styleString += `${property}: ${styles.getPropertyValue(property)}; `;
        }
        return styleString;
    }
    const footer = document.querySelector('footer');
    return footer ? getStyles(footer) : 'Footer not found';
    """
    footer_css = driver.execute_script(js_script)
    driver.quit()
    return footer_css

def get_all_anchor_links(url):
    driver = webdriver.Chrome()
    driver.get(url)
    anchor_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))
    anchor_links = [a.get_attribute('href') for a in anchor_elements if a.get_attribute('href')]
    driver.quit()
    return anchor_links

def get_most_used_fonts(url):
    driver = webdriver.Chrome()
    driver.get(url)
    js_script = """
    let fonts = [];
    let allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        let style = window.getComputedStyle(el);
        fonts.push(style.fontFamily);
    });
    return fonts;
    """
    fonts = driver.execute_script(js_script)
    driver.quit()
    font_count = defaultdict(int)
    for font in fonts:
        font_count[font] += 1
    sorted_fonts = sorted(font_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_fonts

def get_header_content(url):
    driver = webdriver.Chrome()
    driver.get(url)
    header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'header')))
    header_content = header.text
    driver.quit()
    return header_content

def get_header_with_inline_styles(url):
    driver = webdriver.Chrome()
    driver.get(url)
    js_script = """
    function applyInlineStyles(element) {
        const styles = window.getComputedStyle(element);
        let styleString = '';
        for (let property of styles) {
            styleString += `${property}: ${styles.getPropertyValue(property)}; `;
        }
        element.setAttribute('style', styleString);
        for (let child of element.children) {
            applyInlineStyles(child);
        }
    }
    function removeElementWithText(node, searchText) {
        if (node.nodeType === Node.TEXT_NODE && node.nodeValue.includes(searchText)) {
            node.parentNode.removeChild(node);
            return;
        }
        node.childNodes.forEach(child => removeElementWithText(child, searchText));
    }
    const header = document.querySelector('header');
    if (header) {
        removeElementWithText(header, 'services');
    }
    if (header) applyInlineStyles(header);
    return header ? header.outerHTML : 'Header not found';
    """
    header_content = driver.execute_script(js_script)
    driver.quit()
    return header_content

def get_primary_button_color(url):
    driver = webdriver.Chrome()
    driver.get(url)
    booking_keywords = ["book", "reserve", "schedule", "register", "signup", "order"]
    primary_buttons = []
    for keyword in booking_keywords:
        try:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword}')]")))
            primary_buttons.append(button)
        except:
            pass
        try:
            link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{keyword}')]")))
            primary_buttons.append(link)
        except:
            pass
    if not primary_buttons:
        driver.quit()
        return None
    color = primary_buttons[0].value_of_css_property('background-color')
    driver.quit()
    return color

def get_primary_font_color_across_links(url):
    driver = webdriver.Chrome()
    driver.get(url)

    js_script = """
    let links = document.querySelectorAll('a');
    let colors = new Set();

    links.forEach(link => {
        const style = window.getComputedStyle(link);
        const color = style.color;
        colors.add(color);
    });

    return Array.from(colors);
    """

    primary_font_colors = driver.execute_script(js_script)
    driver.quit()

    return primary_font_colors


def get_most_used_font(url):
    driver = webdriver.Chrome()
    driver.get(url)

    js_script = """
    // Add code to extract most used font here
    """

    # Execute the JavaScript code
    result = driver.execute_script(js_script)
    driver.quit()

    # Process the result and return
    return result