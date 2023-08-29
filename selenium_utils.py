from selenium.webdriver.common.action_chains import ActionChains

from collections import defaultdict
import time
from turtle import bgcolor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from colorthief import ColorThief
from PIL import Image

def seleniumanalyze_website(url):
    driver = webdriver.Chrome()
    driver.get(url)
    results = {}

    js_script = """
    const footer = document.querySelector('footer');
    return footer ? footer.outerHTML : null;
    """

    results['footer_css'] = driver.execute_script(js_script)

    # All anchor links
    anchor_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))
    results['anchor_links'] = [a.get_attribute('href') for a in anchor_elements if a.get_attribute('href')]

    # Most used fonts
    js_script_fonts = """
    let fonts = [];
    let allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        let style = window.getComputedStyle(el);
        fonts.push(style.fontFamily);
    });
    return fonts;
    """
    fonts = driver.execute_script(js_script_fonts)
    font_count = defaultdict(int)
    for font in fonts:
        font_count[font] += 1
    results['sorted_fonts'] = sorted(font_count.items(), key=lambda x: x[1], reverse=True)

    
    # Primary button color
    booking_keywords = ["book", "reserve", "schedule", "register", "signup", "order", "book now"]
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
    results['primary_button_color'] = primary_buttons[0].value_of_css_property('background-color') if primary_buttons else None

    
    # Wait for the page to fully load and for the element containing "BOOK NOW" or "Book" to be present
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'BOOK NOW')] | //*[contains(text(), 'Book')]"))
    )
    time.sleep(14)


    # Fetch the computed background color
    bg_color = element.value_of_css_property('background-color')

    results['primary_button_color'] = (bg_color)

    xpath_expression = "//*[self::button or self::div or self::a or self::span][contains(., 'BOOK NOW') or contains(., 'Book')]"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_expression))
    )

    # Fetch the computed background color
    bg_color = element.value_of_css_property('background-color')
    print(bg_color)
    results['primary_button_color'] = (bg_color)
    element = driver.find_element(By.XPATH, "//*[contains(text(), 'BOOK NOW') or contains(text(), 'Book')]")


    # Use JavaScript to retrieve the computed background color
    bg_color = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", element)

    results['primary_button_color'] = (bg_color)

    # Simulate hover action using ActionChains
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()

    # Now, retrieve the background color while the button is in hover state
    bg_color_on_hover = element.value_of_css_property('background-color')
    print(bg_color_on_hover)
    results['primary_button_color'] = bg_color_on_hover

    # Primary font color across links
    js_script_link_colors = """
    let links = document.querySelectorAll('a');
    let colors = new Set();

    links.forEach(link => {
        const style = window.getComputedStyle(link);
        const color = style.color;
        colors.add(color);
    });

    return Array.from(colors);
    """
    results['primary_font_colors'] = driver.execute_script(js_script_link_colors)

    js_script = """
    let colors = {};
    let allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        let style = window.getComputedStyle(el);
        let bgColor = style.backgroundColor;
        if (bgColor in colors) {
            colors[bgColor] += 1;
        } else {
            colors[bgColor] = 1;
        }
    });
    return colors;
    """

    color_counts = driver.execute_script(js_script)

    # Filtering out transparent or none colors
    filtered_colors = {k: v for k, v in color_counts.items() if 'rgba(0, 0, 0, 0)' not in k and 'transparent' not in k}
    
    # Sorting by occurrence
    sorted_colors = sorted(filtered_colors.items(), key=lambda x: x[1], reverse=True)

    results['primary_color'] =  sorted_colors[0][0] if len(sorted_colors) > 0 else None
    results['secondary_color'] = sorted_colors[1][0] if len(sorted_colors) > 1 else None

    screenshot_path = 'screenshot.png'
    driver.save_screenshot(screenshot_path)
    screenshot = Image.open(screenshot_path)

    # Use ColorThief to extract the most prominent color
    color_thief = ColorThief(screenshot_path)
    palette = color_thief.get_palette(color_count=5, quality=1)
    most_prominent_color = palette[0]


    results['prim_cont_bg_color'] = f"rgb({most_prominent_color[0]}, {most_prominent_color[1]}, {most_prominent_color[2]})"
    """" The Primary color is used to fetch the color of the button for ADA"""
    sec_cont_bg_color_tmp = suggested_button_color(palette[0])
    results['sec_cont_bg_color'] =  f"rgb({sec_cont_bg_color_tmp[0]}, {sec_cont_bg_color_tmp[1]}, {sec_cont_bg_color_tmp[2]})"
    """ The primary color is used to fetch the color of the text for ada"""
    primary_text_color_tmp = ada_compliant_text_color(palette[0])
    
    results["primary_text_color"] = f"rgb({primary_text_color_tmp[0]}, {primary_text_color_tmp[1]}, {primary_text_color_tmp[2]})"

    print(results)
    print(palette)
    
    driver.quit()
    return results
    

def suggested_button_color(bg_color, decrement=20, attempts=10):
    """Suggest a darker button color for a given background color."""
    r, g, b = bg_color
    for _ in range(attempts):
        button_color = (max(r - decrement, 0), max(g - decrement, 0), max(b - decrement, 0))
        bg_luminance = luminance(*bg_color)
        btn_luminance = luminance(*button_color)
        if contrast_ratio(bg_luminance, btn_luminance) >= 3.0:
            return button_color
        r, g, b = button_color
    return None  # After several attempts, no suitable color was found


def contrast_ratio(lum1, lum2):
    """Compute contrast ratio between two luminance values."""
    return (max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05)

def luminance(r, g, b):
    """Calculate the luminance of a color using the WCAG formula."""
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    for i, c in enumerate([r, g, b]):
        if c <= 0.03928:
            c = c / 12.92
        else:
            c = ((c + 0.055) / 1.055) ** 2.4
        [r, g, b][i] = c

    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def luminance1(r, g, b):
    """Calculate the luminance of a color using the WCAG formula."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    def adjust_color(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r, g, b = adjust_color(r), adjust_color(g), adjust_color(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def textColorluminance(rgb):
    r, g, b = [x/255.0 for x in rgb]
    r = (r <= 0.03928) and (r/12.92) or ((r + 0.055)/1.055) ** 2.4
    g = (g <= 0.03928) and (g/12.92) or ((g + 0.055)/1.055) ** 2.4
    b = (b <= 0.03928) and (b/12.92) or ((b + 0.055)/1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(l1, l2):
    return (l1 + 0.05) / (l2 + 0.05)

def ada_compliant_text_color(bg_rgb):
    lum_bg = textColorluminance(bg_rgb)
    lum_black = textColorluminance((0,0,0))
    lum_white = textColorluminance((255,255,255))

    contrast_black = contrast_ratio(lum_bg, lum_black)
    contrast_white = contrast_ratio(lum_bg, lum_white)

    if contrast_black >= contrast_white and contrast_black >= 4.5:
        return (0,0,0) # Black text
    elif contrast_white >= 4.5:
        return (255,255,255) # White text
    else:
        # Neither black nor white provides enough contrast.
        # You might need more sophisticated methods to find a compliant color.
        return None