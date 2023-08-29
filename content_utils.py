import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urlparse, urljoin

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException:
        return None

def classify_business(content):
    resort_keywords = ["resort", "vacation", "getaway", "holiday", "beachfront", "all-inclusive"]
    spa_keywords = ["spa", "massage", "facial", "manicure", "pedicure", "sauna", "treatment", "wellness", "relaxation"]
    luxury_salon_keywords = ["luxury", "premium", "elite", "high-end", "exclusive", "boutique"]
    waxing_keywords = ["waxing", "bikini wax", "eyebrow wax", "hair removal", "leg wax", "brazilian wax"]
    salon_keywords = ["haircut", "hairdresser", "hairstyle", "hair color", "stylist", "salon"]
    beauty_product_keywords = ["makeup", "cosmetics", "skincare", "beauty products", "lotion", "serum", "foundation", "lipstick"]

    business_types = []

    if any(keyword in content.lower() for keyword in resort_keywords):
        business_types.append("resort")
    if any(keyword in content.lower() for keyword in spa_keywords):
        business_types.append("spa")
    if any(keyword in content.lower() for keyword in luxury_salon_keywords):
        business_types.append("luxury salon")
    if any(keyword in content.lower() for keyword in waxing_keywords):
        business_types.append("waxing salon")
    if any(keyword in content.lower() for keyword in salon_keywords):
        business_types.append("salon")
    if any(keyword in content.lower() for keyword in beauty_product_keywords):
        business_types.append("beauty products")

    return business_types

def extract_text_colors(soup):
    colors = defaultdict(int)
    for style_tag in soup.find_all('style'):
        content = style_tag.string
        if content:
            for rule in content.split('}'):
                if 'color:' in rule:
                    color = rule.split('color:')[1].split(';')[0].strip()
                    colors[color] += 1
    sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    return sorted_colors

def get_logo_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    noscript_tags = soup.find_all('noscript')
    logo_imgs = [tag.find('img', class_='logo__image') for tag in noscript_tags if tag.find('img', class_='logo__image')]
    logo_urls = [img['src'] for img in logo_imgs if img and img.has_attr('src')]
    return logo_urls


def extract_background_color(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the <body> tag to get its background color
    body_tag = soup.find('body')
    
    if body_tag and body_tag.has_attr('style'):
        style = body_tag['style']
        style_properties = style.split(';')
        
        # Search for the background-color property
        for prop in style_properties:
            if 'background-color' in prop:
                background_color = prop.split(':')[1].strip()
                return background_color
    
    return None


def extract_google_tag_manager_code(url):
    # Look for script tags containing Google Tag Manager code
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Pattern for GTM ID (e.g., GTM-XXXXX)
    gtm_pattern = re.compile(r'GTM-[A-Z0-9]+')

    scripts = soup.find_all('script', text=True)

    gtm_id = None

    for script in scripts:
        if not gtm_id:
            match = gtm_pattern.search(script.string)
            if match:
                gtm_id = match.group(0)

    return gtm_id
        
def extract_GA4_measurementId(url):
    # Look for script tags containing Google Tag Manager code
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    ga4_pattern = re.compile(r'G-[A-Z0-9]+')
    ga4_id = None
    scripts = soup.find_all('script', text=True)

    for script in scripts:
    
        if not ga4_id:
            match = ga4_pattern.search(script.string)
            if match:
                ga4_id = match.group(0)
    return ga4_id
        
def extract_primary_container_color(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    # Look for the primary container element (e.g., main content area)
    primary_container = soup.find('main') or soup.find('section') or soup.find('div')
    
    if primary_container:
        style = primary_container.get('style', '')
        color_property_index = style.find('background-color:')
        
        if color_property_index != -1:
            start_index = color_property_index + len('background-color:')
            end_index = style.find(';', start_index)
            
            if end_index != -1:
                primary_container_color = style[start_index:end_index].strip()
                return primary_container_color
    
    return None

def extract_secondary_container_color(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    # Look for the secondary container element (e.g., sidebar, footer)
    secondary_container = soup.find('aside') or soup.find('footer') or soup.find('nav') or soup.find('section')
    
    if secondary_container:
        style = secondary_container.get('style', '')
        color_property_index = style.find('background-color:')
        
        if color_property_index != -1:
            start_index = color_property_index + len('background-color:')
            end_index = style.find(';', start_index)
            
            if end_index != -1:
                secondary_container_color = style[start_index:end_index].strip()
                return secondary_container_color
    
    return None

def extract_social_media_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Common social media platforms to look for
    platforms = ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'pinterest', 'tumblr']

    social_links = {}

    # Search for all anchor tags with href attribute
    for a in soup.find_all('a', href=True):
        href = a['href']
        for platform in platforms:
            if platform in href:
                # Store the platform and its corresponding URL
                social_links[platform] = href

    return social_links
        
def getFacebookPixelId(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scripts = soup.find_all('script')
    
    # Loop through all the scripts and search for the Facebook Pixel ID using regex
    for script in scripts:
        content = script.string
        if content:
            match = re.search(r"fbq\('init',\s*'(\d+)'\);", content)
            if match:
                return match.group(1)

    return None

def get_org_logo(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Attempt to fetch the logo using Open Graph protocol
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image['content']:
            return og_image['content']

        # If the above fails, you can add more methods to fetch logos. For example:
        # logo_image = soup.find('img', attrs={'id': 'logo' or 'class': 'logo'})  # common patterns
        # if logo_image and logo_image['src']:
        #     return logo_image['src']

        return None


def check_header_keywords(url):
    try:
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        header_tag = soup.find('header')

        if header_tag:
            header_inner_text = header_tag.get_text().lower()

            keywords_to_check = ['Service', 'giftcards', 'membership', 'Package','gift cards']
            lowercase_keywords = [keyword.lower() for keyword in keywords_to_check]

            found_keywords = [keyword for keyword in lowercase_keywords if keyword in header_inner_text]

            # Sort the found keywords in the order they appear in the keywords_to_check list
            sorted_found_keywords = sorted(found_keywords, key=lowercase_keywords.index)

            if sorted_found_keywords:
                print("Keywords found in inner text of <header> tag:", sorted_found_keywords)
            else:
                print("Keywords not found in inner text of <header> tag.")
        else:
            print("<header> tag not found in the HTML content.")

    except requests.RequestException as e:
        print("Error:", e)
    return sorted_found_keywords


def get_favicon_url(site_url):
    try:
        response = requests.get(site_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for a <link> tag with rel attributes "icon", "shortcut icon", etc.
        icon_link = soup.find('link', rel=lambda x: x and x.lower() in ['icon', 'shortcut icon'])
        
        if icon_link and icon_link.has_attr('href'):
            # Combine base URL with the favicon URL (in case it's relative)
            favicon_url = urljoin(site_url, icon_link['href'])
        else:
            # Default favicon location
            favicon_url = urljoin(site_url, '/favicon.ico')
            
        # Check if favicon exists at the determined URL
        response = requests.get(favicon_url)
        if response.status_code != 200:
            return None

        return favicon_url

    except requests.RequestException:
        return None
    
import requests
from bs4 import BeautifulSoup
import re

def business_name_reference(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts and styles for cleaner text
        for script in soup(["script", "style"]):
            script.extract()
        
        page_text = soup.get_text().lower()

        # Common patterns to identify business names or references
        patterns = [
            r'\bwe at (?P<name>[\w\s]+)\b',
            r'\bhere at (?P<name>[\w\s]+)\b',
            r'welcome to (?P<name>[\w\s]+)\b',
            r'\bintroducing (?P<name>[\w\s]+)\b'
        ]

        for pattern in patterns:
            match = re.search(pattern, page_text)
            if match:
                return match.group('name').strip()

        return None

    except requests.RequestException:
        return None

def keywords_exist_in_text(text, keywords_to_check):
    """
    Check if any keyword in the list exists in the provided text.

    Args:
    - text (str): The text to search within.
    - keywords_to_check (list): A list of keywords to search for in the text.

    Returns:
    - bool: True if any keyword exists in the text, False otherwise.
    """
    if text is None or keywords_to_check is None:
        return False

    # Convert the provided text to lowercase for consistent checking
    lowercase_text = text.lower()

    # Check if any keyword from the list exists in the text
    for keyword in keywords_to_check:
        if keyword.lower() in lowercase_text:
            return True

    return False




import requests
from bs4 import BeautifulSoup

def get_cookie_policy(url):
    try:
        # Get the website content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try finding the cookie policy by common tags or identifiers
        cookie_policy_section = soup.find(id="cookie-policy") or \
                                soup.find(class_="cookie-policy") or \
                                soup.find("div", {"class": "cookie-policy-content"})  # Add more as needed

        if cookie_policy_section:
            return cookie_policy_section.get_text()
        else:
            return ""

    except requests.RequestException as e:
        return f"Error fetching the URL: {e}"
    

import requests
from bs4 import BeautifulSoup

def find_us_url(site_url):
    try:
        # Fetch the website content
        response = requests.get(site_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for anchor tags with text or href attributes suggesting a "Find Us" link
        find_us_candidates = soup.find_all('a', string=lambda text: 'find us' in (text or '').lower())
        
        if not find_us_candidates:  # If we haven't found using the string, let's search in href
            find_us_candidates = soup.find_all('a', href=lambda href: href and 'find-us' in href.lower())

        if find_us_candidates:
            find_us_link = find_us_candidates[0]['href']
            
            # Handle relative URLs
            if not find_us_link.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                find_us_link = urljoin(site_url, find_us_link)
            
            return find_us_link
        else:
            return "Find Us link not found."

    except requests.RequestException as e:
        return f"Error fetching the URL: {e}"



def sells_products(site_url):
    try:
        # Fetch the website content
        response = requests.get(site_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Keywords typically found in e-commerce or online shopping sites
        ecommerce_keywords = ['add to cart', 'buy now', 'shop', 'checkout', 'products', 'store', 'purchase', 'order']

        # Check if any of the keywords are in the text of the website
        site_text = soup.get_text().lower()
        for keyword in ecommerce_keywords:
            if keyword in site_text:
                return True

        return False

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return False




# def get_button_background_color(url):
#     response = requests.get(url)
#     response.raise_for_status()  

#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     tags_to_check = ['button', 'div', 'a', 'span']
    
#     for tag in tags_to_check:
#         # Using `recursive=True` to search for text within nested tags
#         elements = soup.find_all(tag, string=lambda text: text and ("Book Now" in text or "Book" in text), recursive=True)
        
#         if not elements:
#             # If the tag doesn't directly contain the text, look if any of its children contain the desired text
#             elements = soup.find_all(tag, recursive=True)
#             elements = [elem for elem in elements if elem.find(string=lambda text: text and ("Book Now" in text or "Book" in text))]
        
#         if elements:
#             style = elements[0].get('style', '')
#             bg_color = next((s.split(":")[1].strip() for s in style.split(";") if "background-color" in s), None)
            
#             if bg_color:
#                 return bg_color

#     return None








