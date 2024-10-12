import re, requests

def hex_color_validator(value):
    match = re.fullmatch(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value)
    
    if match:
        return True
    return False

def search_filter(params):
    locale = params.get('locale') or ""
    locales = [
        'en-US', 'pt-BR', 'es-ES', 'ca-ES', 'de-DE', 'it-IT', 'fr-FR', 'sv-SE',
        'id-ID', 'pl-PL', 'ja-JP', 'zh-TW', 'zh-CN', 'ko-KR', 'th-TH', 'nl-NL',
        'hu-HU', 'vi-VN', 'cs-CZ', 'da-DK', 'fi-FI', 'uk-UA', 'el-GR', 'ro-RO',
        'nb-NO', 'sk-SK', 'tr-TR', 'ru-RU'
    ]
    if not locale in locales:
        return {"status": "error", "error": f"locales must be either of {locales}"}
    
    orientation = params.get('orientation') or ""
    orientations = ["landscape", "portrait", "square", ""]
    if not orientation in orientations:
        return {"status": "error", "error": f"orientation must be either of {orientations}"}

    size = params.get("size") or ""
    sizes = ["large", "medium", "small", ""]
    if not size in sizes:
        return {"status": "error", "error": f"size must be either of {sizes}"}

    color = params.get("color") or ""
    colors = ["red", "orange", "yellow", "green", "turquoise", "blue",
        "violet", "pink", "brown", "black", "gray", "white", ""]
    if not (color in colors) or (hex_color_validator(color)):
        return {"status": "error", "error": f"colors must be either of {colors} or a valid HEX value"}

    page = params.get("page") or 1
    page_error = "page must be an integrer greater than 0"
    if not isinstance(page, int):
        return {"status": "error", "error": f"{page_error}"}
    elif page < 1:
        return {"status": "error", "error": f"{page_error}"}
    
    per_page = params.get("per_page") or 1
    per_page_error = "per_page must be an integrer greater than 0"
    if not isinstance(per_page, int):
        return {"status": "error", "error": f"{per_page_error}"}
    elif per_page < 1:
       return {"status": "error", "error": f"{per_page_error}"}

    min_width = params.get("min_width") or 200
    min_width_error = "min_width must be an integrer greater than 0"
    if not isinstance(min_width, int):
        return {"status": "error", "error": f"{min_width_error}"}
    elif min_width < 1:
       return {"status": "error", "error": f"{min_width_error}"}

    min_height = params.get("min_height") or 200
    min_height_error = "min_height must be an integrer greater than 0"
    if not isinstance(min_height, int):
        return {"status": "error", "error": f"{min_height_error}"}
    elif min_height < 1:
       return {"status": "error", "error": f"{min_height_error}"}

    min_duration = params.get("min_duration") or 1
    min_duration_error = "min_height must be an integrer greater than 0"
    if not isinstance(min_duration, int):
        return {"status": "error", "error": f"{min_duration_error}"}
    elif min_duration < 1:
       return {"status": "error", "error": f"{min_height_error}"}

    max_duration = params.get("max_duration") or 1
    max_duration_error = "max_duration must be an integrer greater than 0"
    if not isinstance(max_duration, int):
        return {"status": "error", "error": f"{max_duration}"}
    elif max_duration < 1:
       return {"status": "error", "error": f"{max_duration_error}"}
    
    _type = params.get('type') or ""
    _types = ["photo", "video", ""]
    if not _type in _types:
        return {"status": "error", "error": f"type must be either of {_types}"}
    
    _sort = params.get('sort') or ""
    _sorts = ["asc", "desc", ""]
    if not _sort in _sorts:
        return {"status": "error", "error": f"type must be either of {_sorts}"}

    return {
        "locale": locale,
        "orientation":orientation,
        "size":size,
        "color":color,
        "page": page,
        "per_page": per_page,
        "min_width": min_width,
        "min_height": min_height, 
        "min_duration": min_duration,
        "max_duration": max_duration,
        "type":_type,
        "sort":_sort,
    }

def create_request(URL, headers, params={}):
    try:
        res = requests.get(URL, headers=headers, params=params)
        return response_manager(res)
    except Exception as e:
        return response_manager({"status":"error","error":str(e)})
        

def response_manager(res):
    if type(res) == dict:
        return res
    elif isinstance(res, requests.models.Response):
        # manage requests response
        if str(res.status_code) == str(200):
            return {"status":"success", "data":res.json()}
        return {"status":"error","error":str(res.reason)}
    else:
        return {"status":"error","error":res.reason} 

