import requests
from bs4 import BeautifulSoup
from collections import defaultdict

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
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    script_tags = soup.find_all('script')
    
    for script_tag in script_tags:
        if 'googletagmanager.com' in str(script_tag):
            script_content = str(script_tag)
            start_index = script_content.find('id="GTM-') + len('id="')
            end_index = script_content.find('"', start_index)
            gtm_id = script_content[start_index:end_index]
            return gtm_id
        
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
        
