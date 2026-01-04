import json
import re
import os

# File đầu vào và đầu ra
input_file = "Crawl and Clean Data/coursera.json"
output_file = "Crawl and Clean Data/coursera_clean.json"

# Xóa file đầu ra nếu đã tồn tại
if os.path.exists(output_file):
    print(f"Xóa file cũ: {output_file}")
    os.remove(output_file)

def convert_reviews(reviews_str):
    """Chuyển '13K reviews' -> 13000.0"""
    if not reviews_str:
        return None
    match = re.search(r'([\d,.]+)\s*([KM]?)', reviews_str, re.IGNORECASE)
    if not match:
        return None
    number, suffix = match.groups()
    number = number.replace(',', '')
    try:
        value = float(number)
        if suffix.upper() == 'K':
            value *= 1_000
        elif suffix.upper() == 'M':
            value *= 1_000_000
        return value
    except:
        return None

def convert_rating(rating_str):
    """Chuyển rating string -> float"""
    if not rating_str:
        return None
    try:
        return float(rating_str)
    except:
        return None

def parse_metadata(metadata_str):
    """Tách metadata thành level, certificate_type, duration"""
    level = certificate_type = duration = None
    if metadata_str:
        parts = [p.strip() for p in metadata_str.split('·')]
        if len(parts) > 0:
            level = parts[0]
        if len(parts) > 1:
            certificate_type = parts[1]
        if len(parts) > 2:
            duration = parts[2]
    return level, certificate_type, duration

def split_skills(skills_str, partner_str, metadata_str):
    """Chuyển skills từ chuỗi thành list, tách theo dấu ','"""
    if not skills_str:
        return []
    # loại bỏ "Skills you'll gain: " nếu có
    skills_str = skills_str.replace("Skills you'll gain: ", "").strip()

    #loại bỏ partner ở đầu nếu Skills_str có chứa
    if partner_str:
        skills_str = skills_str.replace(partner_str, "").strip()

    # Loại bỏ metadata ở cuối nếu skills_str chứa
    if metadata_str:
        skills_str = skills_str.replace(metadata_str, "").strip()

    # tách bằng dấu phẩy và loại bỏ khoảng trắng đầu/cuối
    return [s.strip() for s in skills_str.split(',') if s.strip()]


# Đọc dữ liệu gốc
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Làm sạch dữ liệu
cleaned_data = []
for item in data:
    reviews_clean = convert_reviews(item.get('reviews'))
    rating_clean = convert_rating(item.get('rating'))
    level, certificate_type, duration = parse_metadata(item.get('metadata'))
    skills_list = split_skills(item.get('skills'),item.get('partner')  , item.get('metadata'))

    cleaned_item = {
        "partner": item.get("partner"),
        "title": item.get("title"),
        "url": item.get("url"),
        "skills": skills_list,
        "rating": rating_clean,
        "reviews": reviews_clean,
        "level": level,
        "certificate_type": certificate_type,
        "duration": duration
    }
    cleaned_data.append(cleaned_item)

# Ghi ra file JSON sạch
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

print(f"Làm sạch xong, file xuất ra: {output_file}")
