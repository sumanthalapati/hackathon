from flask import Flask, Response, request, jsonify
import content_utils 
import selenium_utils
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def hello():
    return "Hello, World!"


@app.after_request
def set_referrer_policy(response):
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

@app.route('/analyze', methods=['POST'])
def analyze_website():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL not provided"}), 400
    data = selenium_utils.seleniumanalyze_website(url)

    # Assigning the results to individual variables:
    anchor_links = data['anchor_links']
    most_used_fonts = data['sorted_fonts']  # Adjusted from previous code.
    primary_button_color = data['primary_button_color']
    primary_font_colors = data['primary_font_colors']
    secondary_color = data['primary_font_colors']
    primary_color = data['primary_color']
    prim_cont_bg_color = data['prim_cont_bg_color']
    sec_cont_bg_color = data['sec_cont_bg_color']
    primary_text_color = data['primary_text_color']
    # For non-selenium related tasks:
    content = content_utils.get_website_content(url)
    business_types = content_utils.classify_business(content)
    background_color= content_utils.extract_background_color(url)
    if background_color is None:
        background_color = "#FFF"
    extract_google_tag_manager_code = content_utils.extract_google_tag_manager_code(url)
    primary_container_color = content_utils.extract_primary_container_color(url)
    secondary_container_color = content_utils.extract_secondary_container_color(url)
    social_media_links = content_utils.extract_social_media_links(url)
    extract_GA4_tag_manager_code = content_utils.extract_GA4_measurementId(url)
    getFacebookPixelId = content_utils.getFacebookPixelId(url)
    org_logo_url = content_utils.get_org_logo(url)
    header_go_to_url =url
    headerwords= content_utils.check_header_keywords(url)
    if primary_container_color is None:
        primary_container_color = primary_button_color
    if secondary_container_color is  None:
        primary_container_color = primary_button_color
    faviconurl = content_utils.get_favicon_url(url)
    if content_utils.business_name_reference(url)  is None:
        centerlabel =content_utils.business_name_reference(url)
    else:
        centerlabel = "Center"
    if extract_google_tag_manager_code is None:
        enable_google_analytics = "false"
        
    else:
        enable_google_analytics = "true"
        extract_google_tag_manager_code = ""

    cookie_policy = content_utils.get_cookie_policy(url)
    isServiceEnabled = content_utils.keywords_exist_in_text('Service', headerwords)
    ismembershipsaleEnabled = content_utils.keywords_exist_in_text('membership', headerwords)
    isGiftCardsaleEnabled = content_utils.keywords_exist_in_text('giftcards', headerwords)
    isGiftCardsaleEnabled = content_utils.keywords_exist_in_text('gift cards', headerwords)
    isPackagesaleEnabled = content_utils.keywords_exist_in_text('Package', headerwords)
    #primary_button_color = content_utils.get_button_background_color(url)
    findUsURL = content_utils.find_us_url(url)
    checkProducts = content_utils.sells_products(url)
    return jsonify({
        "business_types": business_types,
        "anchor_links": anchor_links,
        "font": most_used_fonts[0][0],
        "secondary_font": most_used_fonts[1],
        "prim_btn_color": primary_button_color,
        "primary_font_color": primary_font_colors[0],
        "secondary_font_color": primary_font_colors[1],
        "background_color": background_color,
        "google_tag_manager_code": extract_google_tag_manager_code,
        "social_media_links":social_media_links,
        "extract_GA4_tag_manager_code":extract_GA4_tag_manager_code,
        "primary_color":primary_color,
        "secondary_color": secondary_color,
        "header_goto_url": header_go_to_url,
        "facebook_pixel_id": "",
        "header_img_url": org_logo_url,
        "favicon_url":faviconurl,
        "business_label": "Center",
        "isServiceSaleEnabled": isServiceEnabled,
        "enable_giftcards": isGiftCardsaleEnabled,
        "enableMembershipSales": ismembershipsaleEnabled,
        "enable_series_package_sales": isPackagesaleEnabled,
        "enable_google_analytics": enable_google_analytics,
        "service_label": "Service",
        "cookie_policy": cookie_policy,
        "header_findus": findUsURL,
        "enable_giftcards_in_profile": isGiftCardsaleEnabled,
        "enable_products_in_profile": checkProducts,
        "products_page": checkProducts,
        "headerwords": headerwords,
        "prim_cont_bg_color": prim_cont_bg_color,
        "sec_cont_bg_color":sec_cont_bg_color,
        "prim_text_color":primary_text_color
    })

if __name__ == '__main__':
    app.run(debug=True)

