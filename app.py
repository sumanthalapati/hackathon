from flask import Flask, request, jsonify
import content_utils 
import selenium_utils

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_website():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL not provided"}), 400

    content = content_utils.get_website_content(url)
    business_types = content_utils.classify_business(content)
    footer_css = selenium_utils.get_footer_css(url)
    background_color = content_utils.extract_background_color(url)
    anchor_links = selenium_utils.get_all_anchor_links(url)
    most_used_fonts = selenium_utils.get_most_used_fonts(url)
    header_content = selenium_utils.get_header_content(url)
    header_with_inline_styles = selenium_utils.get_header_with_inline_styles(url)
    primary_button_color = selenium_utils.get_primary_button_color(url)
    most_used_font = selenium_utils.get_most_used_font(url)
    primary_font_colors = selenium_utils.get_primary_font_color_across_links(url)
    extract_google_tag_manager_code = content_utils.extract_google_tag_manager_code(url)
    primary_container_color = content_utils.extract_primary_container_color(url)
    secondary_container_color = content_utils.extract_secondary_container_color(url)
    
    return jsonify({
        "business_types": business_types,
        "footer_css": footer_css,
        "anchor_links": anchor_links,
        "most_used_fonts": most_used_fonts,
        "header_content": header_content,
        "header_with_inline_styles": header_with_inline_styles,
        "primary_button_color": primary_button_color,
        "most_used_font": most_used_font,
        "primary_font_colors": primary_font_colors,
        "background_color": background_color,
        "google_tag_manager_code": extract_google_tag_manager_code,
        "primary_container_color":primary_container_color,
        "secondary_container_color":secondary_container_color
    })

if __name__ == '__main__':
    app.run(debug=True)
