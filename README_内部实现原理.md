# HƯỚNG DẪN KỸ THUẬT: CƠ CHẾ HOẠT ĐỘNG CỦA ỨNG DỤNG CHUYỂN ĐỔI ESPERANTO - CHỮ HÁN

## MỤC LỤC
1. Tổng quan kiến trúc hệ thống
2. Cấu trúc mã nguồn và quy trình xử lý
3. Cơ chế thay thế văn bản cốt lõi
4. Xử lý ký tự đặc biệt và định dạng
5. Cơ chế tạo và sử dụng tệp JSON
6. Xử lý song song và tối ưu hóa hiệu suất
7. Kỹ thuật đặc biệt và giải thuật quan trọng

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

### 1.1. Kiến trúc tổng thể

Ứng dụng này được xây dựng dựa trên framework Streamlit, bao gồm hai thành phần chính:

1. **Trang chính** (main.py): Xử lý văn bản Esperanto, thay thế các từ gốc bằng chữ Hán hoặc bản dịch có chú thích ruby.

2. **Trang tạo JSON** (Trang tạo tệp JSON để thay thế...): Công cụ tạo tệp JSON chứa quy tắc thay thế.

Hai module hỗ trợ chính là:

- **esp_text_replacement_module.py**: Cung cấp các hàm xử lý văn bản cốt lõi
- **esp_replacement_json_make_module.py**: Hỗ trợ quá trình tạo JSON với các hàm tiện ích

### 1.2. Luồng dữ liệu

```
[Văn bản Esperanto] → [Tiền xử lý] → [Thay thế theo quy tắc từ tệp JSON] → [Định dạng đầu ra] → [Kết quả]
```

Các quy tắc thay thế được lưu trong tệp JSON có ba danh sách chính:
- Danh sách thay thế toàn cục (全域替换用のリスト)
- Danh sách thay thế cục bộ (局部文字替换用のリスト)
- Danh sách thay thế gốc từ 2 ký tự (二文字词根替换用のリスト)

---

## 2. CẤU TRÚC MÃ NGUỒN VÀ QUY TRÌNH XỬ LÝ

### 2.1. main.py - Trang chính

File `main.py` là điểm vào chính của ứng dụng, có cấu trúc:

```python
# 1. Import và thiết lập Streamlit
import streamlit as st
import multiprocessing
from esp_text_replacement_module import (...)

# 2. Hàm load_replacements_lists với bộ nhớ đệm
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    # Đọc và trả về 3 danh sách thay thế từ tệp JSON

# 3. Thiết lập UI
st.set_page_config(...)
st.title(...)

# 4. Phần tải tệp JSON
json_options = ["デフォルトを使用する", "アップロードする"]
selected_option = st.radio(...)

# 5. Cài đặt nâng cao (xử lý song song)
use_parallel = st.checkbox(...)
num_processes = st.number_input(...)

# 6. Lựa chọn định dạng đầu ra
options = {...}
selected_display = st.selectbox(...)

# 7. Nguồn văn bản đầu vào
source_option = st.radio(...)

# 8. Form xử lý văn bản
with st.form(key='profile_form'):
    # Xử lý văn bản
    if submit_btn:
        if use_parallel:
            processed_text = parallel_process(...)
        else:
            processed_text = orchestrate_comprehensive_esperanto_text_replacement(...)

# 9. Hiển thị kết quả
if processed_text:
    # Hiển thị bản xem trước và tạo nút tải xuống
```

### 2.2. Trang tạo tệp JSON

File `Trang tạo tệp JSON để thay thế văn bản Esperanto bằng chuỗi ký tự (kanji).py` có cấu trúc:

```python
# 1. Import và biến toàn cục
import streamlit as st
import pandas as pd
from esp_text_replacement_module import (...)
from esp_replacement_json_make_module import (...)

# 2. Định nghĩa biến và danh sách
verb_suffix_2l = {...}
AN = [...]  # Danh sách từ kết thúc bằng "an"
ON = [...]  # Danh sách từ kết thúc bằng "on"
suffix_2char_roots = [...]
prefix_2char_roots = [...]
standalone_2char_roots = [...]

# 3. Đọc placeholders từ tệp
imported_placeholders_for_global_replacement = import_placeholders(...)

# 4. UI và luồng xử lý
st.set_page_config(...)
st.title(...)

# 5. Tải tệp CSV (Esperanto roots + translations)
csv_choice = st.radio(...)

# 6. Tải tệp JSON (quy tắc phân tách gốc từ)
json_choice = st.radio(...)

# 7. Nút tạo JSON
if st.button("Tạo tệp JSON để thay thế"):
    # Quá trình xử lý phức tạp để tạo tệp JSON
    # Kết quả cuối cùng là 3 danh sách thay thế
    combined_data = {
        "全域替换用のリスト(列表)型配列(replacements_final_list)": replacements_final_list,
        "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)": replacements_list_for_2char,
        "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)": replacements_list_for_localized_string
    }
    # Tạo nút tải xuống
```

### 2.3. Module hỗ trợ

Hai module hỗ trợ cung cấp các hàm xử lý cốt lõi:

**esp_text_replacement_module.py**:
- Các bộ chuyển đổi ký tự đặc biệt Esperanto
- Hàm thay thế văn bản an toàn `safe_replace()`
- Hàm xử lý các phần được đánh dấu bằng % hoặc @
- Hàm thay thế tổng hợp `orchestrate_comprehensive_esperanto_text_replacement()`
- Hàm xử lý song song `parallel_process()`

**esp_replacement_json_make_module.py**:
- Các hàm đo độ rộng văn bản và chèn ngắt dòng
- Hàm định dạng đầu ra `output_format()`
- Hàm hỗ trợ xử lý song song cho việc tạo JSON
- Hàm loại bỏ ruby dư thừa

---

## 3. CƠ CHẾ THAY THẾ VĂN BẢN CỐT LÕI

### 3.1. Quy trình thay thế tổng thể

Hàm trung tâm của ứng dụng là `orchestrate_comprehensive_esperanto_text_replacement()` trong module `esp_text_replacement_module.py`, thực hiện các bước:

1. **Tiền xử lý**:
   - Chuẩn hóa khoảng trắng với `unify_halfwidth_spaces()`
   - Chuyển đổi ký tự Esperanto về dạng thống nhất với `convert_to_circumflex()`

2. **Xử lý đoạn văn bản đặc biệt**:
   - Tìm và thay thế tạm thời các đoạn được đánh dấu bằng % (để bảo vệ không bị thay thế)
   - Tìm và xử lý các đoạn được đánh dấu bằng @ (để thay thế cục bộ)

3. **Thay thế chính**:
   - Áp dụng danh sách thay thế toàn cục (replacements_final_list)
   - Áp dụng danh sách thay thế gốc từ 2 ký tự (replacements_list_for_2char) trong hai lượt

4. **Khôi phục và định dạng sau cùng**:
   - Khôi phục các placeholder thành văn bản thích hợp
   - Thêm định dạng HTML và các thẻ nếu cần thiết

```python
def orchestrate_comprehensive_esperanto_text_replacement(
    text, 
    placeholders_for_skipping_replacements,
    replacements_list_for_localized_string,
    placeholders_for_localized_replacement,
    replacements_final_list,
    replacements_list_for_2char,
    format_type
):
    # 1, 2) Chuẩn hóa văn bản
    text = unify_halfwidth_spaces(text)
    text = convert_to_circumflex(text)
    
    # 3) Xử lý đoạn %...% (không thay thế)
    replacements_list_for_intact_parts = create_replacements_list_for_intact_parts(...)
    for original, place_holder_ in sorted_replacements_list_for_intact_parts:
        text = text.replace(original, place_holder_)
    
    # 4) Xử lý đoạn @...@ (thay thế cục bộ)
    tmp_replacements_list_for_localized_string_2 = create_replacements_list_for_localized_replacement(...)
    for original, place_holder_, replaced_original in sorted_replacements_list_for_localized_string:
        text = text.replace(original, place_holder_)
    
    # 5) Thay thế toàn cục (sử dụng placeholders để tránh thay thế lồng nhau)
    valid_replacements = {}
    for old, new, placeholder in replacements_final_list:
        if old in text:
            text = text.replace(old, placeholder)
            valid_replacements[placeholder] = new
    
    # 6) Thay thế gốc từ 2 ký tự (hai lượt)
    # ...
    
    # 7) Khôi phục placeholders
    # ...
    
    # 8) Định dạng HTML nếu cần
    if "HTML" in format_type:
        text = text.replace("\n", "<br>\n")
        # ...
    
    return text
```

### 3.2. Cơ chế thay thế an toàn

Hàm `safe_replace()` là nền tảng của quy trình thay thế, ngăn chặn các vấn đề thay thế lồng nhau:

```python
def safe_replace(text: str, replacements: List[Tuple[str, str, str]]) -> str:
    """
    Thay thế an toàn với 3 bước:
    1. old -> placeholder (thay thế tạm thời bằng mã đặc biệt)
    2. Lưu mapping placeholder -> new
    3. placeholder -> new (thay thế placeholders bằng nội dung mới)
    """
    valid_replacements = {}
    
    # Bước 1 & 2: Thay thế tạm thời và lưu mapping
    for old, new, placeholder in replacements:
        if old in text:
            text = text.replace(old, placeholder)
            valid_replacements[placeholder] = new
    
    # Bước 3: Thay thế placeholders bằng nội dung mới
    for placeholder, new in valid_replacements.items():
        text = text.replace(placeholder, new)
    
    return text
```

Kỹ thuật này rất quan trọng vì đảm bảo rằng văn bản đã thay thế không bị thay thế lại trong cùng một lượt xử lý, tránh các vấn đề thay thế lồng nhau.

---

## 4. XỬ LÝ KÝ TỰ ĐẶC BIỆT VÀ ĐỊNH DẠNG

### 4.1. Xử lý ký tự Esperanto

Esperanto có các ký tự đặc biệt (ĉ, ĝ, ĥ, ĵ, ŝ, ŭ) có thể được biểu diễn theo nhiều cách khác nhau:

1. **Dạng mũ trên chữ cái** (circumflex): ĉ, ĝ, ĥ, ĵ, ŝ, ŭ
2. **Dạng x** (x-notation): cx, gx, hx, jx, sx, ux
3. **Dạng ^** (hat notation): c^, g^, h^, j^, s^, u^

Các bộ chuyển đổi được định nghĩa trong các từ điển:

```python
x_to_circumflex = {'cx': 'ĉ', 'gx': 'ĝ', 'hx': 'ĥ', 'jx': 'ĵ', 'sx': 'ŝ', 'ux': 'ŭ', ...}
circumflex_to_x = {'ĉ': 'cx', 'ĝ': 'gx', 'ĥ': 'hx', 'ĵ': 'jx', 'ŝ': 'sx', 'ŭ': 'ux', ...}
hat_to_circumflex = {'c^': 'ĉ', 'g^': 'ĝ', 'h^': 'ĥ', 'j^': 'ĵ', 's^': 'ŝ', 'u^': 'ŭ', ...}
# ...và các từ điển khác
```

Hàm chuyển đổi:

```python
def replace_esperanto_chars(text, char_dict: Dict[str, str]) -> str:
    for original_char, converted_char in char_dict.items():
        text = text.replace(original_char, converted_char)
    return text

def convert_to_circumflex(text: str) -> str:
    """Chuyển đổi tất cả dạng ký tự Esperanto về dạng mũ trên chữ cái"""
    text = replace_esperanto_chars(text, hat_to_circumflex)
    text = replace_esperanto_chars(text, x_to_circumflex)
    return text
```

### 4.2. Định dạng đầu ra và Ruby

Hàm `output_format()` trong `esp_replacement_json_make_module.py` xử lý việc định dạng đầu ra:

```python
def output_format(main_text, ruby_content, format_type, char_widths_dict):
    """
    Định dạng văn bản chính và chú thích Ruby theo định dạng được chọn
    """
    if format_type == 'HTML格式_Ruby文字_大小调整':
        # Tính toán độ rộng và tỷ lệ
        width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
        width_main = measure_text_width_Arial16(main_text, char_widths_dict)
        ratio_1 = width_ruby / width_main
        
        # Điều chỉnh kích thước Ruby dựa trên tỷ lệ
        if ratio_1 > 6:
            return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
        elif ratio_1 > (9/3):
            return f'<ruby>{main_text}<rt class="XXS_S">{insert_br_at_half_width(ruby_content, char_widths_dict)}</rt></ruby>'
        # ... các điều kiện khác
        else:
            return f'<ruby>{main_text}<rt class="XXL_L">{ruby_content}</rt></ruby>'
    
    # Các định dạng khác...
```

Hàm `apply_ruby_html_header_and_footer()` thêm các thẻ HTML cần thiết vào kết quả cuối cùng, bao gồm CSS cho định dạng Ruby.

### 4.3. Đo độ rộng văn bản

Ứng dụng sử dụng từ điển `char_widths_dict` để tính toán độ rộng văn bản, hỗ trợ cho việc tự động ngắt dòng và định dạng Ruby:

```python
def measure_text_width_Arial16(text, char_widths_dict: Dict[str, int]) -> int:
    """
    Tính tổng độ rộng của văn bản dựa trên độ rộng của từng ký tự
    """
    total_width = 0
    for ch in text:
        char_width = char_widths_dict.get(ch, 8)  # Mặc định là 8px nếu không tìm thấy
        total_width += char_width
    return total_width
```

Có hai hàm ngắt dòng tự động dựa trên độ rộng:
- `insert_br_at_half_width()`: Chèn `<br>` ở giữa văn bản
- `insert_br_at_third_width()`: Chia văn bản thành ba phần và chèn `<br>` ở hai điểm chia

---

## 5. CƠ CHẾ TẠO VÀ SỬ DỤNG TỆP JSON

### 5.1. Cấu trúc tệp JSON

Tệp JSON chính chứa ba danh sách thay thế:

```json
{
  "全域替换用のリスト(列表)型配列(replacements_final_list)": [
    ["palavra", "<ruby>palavra<rt>単語</rt></ruby>", "$26721$"],
    ...
  ],
  "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)": [
    ["$ad", "$<ruby>ad<rt>継続行為</rt></ruby>", "$13246$"],
    ...
  ],
  "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)": [
    ["lingvo", "<ruby>lingvo<rt>言語</rt></ruby>", "@20374@"],
    ...
  ]
}
```

Mỗi mục có cấu trúc `[từ_gốc, văn_bản_thay_thế, placeholder]`.

### 5.2. Quy trình tạo JSON

Quá trình tạo tệp JSON rất phức tạp và bao gồm nhiều bước:

1. **Đọc dữ liệu đầu vào**:
   - Đọc tệp CSV chứa các gốc từ Esperanto và bản dịch
   - Đọc các tệp JSON cấu hình (quy tắc phân tách gốc từ, chuỗi thay thế tùy chỉnh)
   - Đọc danh sách placeholder từ các tệp văn bản

2. **Xử lý gốc từ cơ bản**:
   - Tạo dictionary cho tất cả gốc từ Esperanto từ tệp văn bản
   - Cập nhật với các gốc từ và bản dịch từ tệp CSV
   - Sắp xếp theo độ dài (dài đến ngắn để ưu tiên thay thế)

3. **Xử lý phức tạp**:
   - Xử lý các từ có hậu tố đặc biệt (-an, -on)
   - Xử lý các động từ với nhiều dạng chia (-as, -is, -os, -us, v.v.)
   - Xử lý các gốc từ 2 ký tự đặc biệt (tiền tố, hậu tố, từ độc lập)
   - Áp dụng các quy tắc phân tách gốc tùy chỉnh từ tệp JSON

4. **Tạo các biến thể chữ hoa**:
   - Mỗi mục được nhân lên thành 3 phiên bản: thường, HOA, Viết_Hoa_Đầu_Từ
   - Điều chỉnh các thẻ Ruby phù hợp cho từng dạng

5. **Kết hợp các danh sách**:
   - Tạo danh sách thay thế toàn cục
   - Tạo danh sách thay thế cho gốc từ 2 ký tự
   - Tạo danh sách thay thế cục bộ
   - Kết hợp vào một tệp JSON duy nhất

### 5.3. Ưu tiên thay thế

Một điểm quan trọng là việc đặt ưu tiên thay thế. Trong mã nguồn, điều này được thực hiện bằng cách:

1. Sắp xếp dựa trên độ dài của chuỗi cần thay thế (dài hơn được ưu tiên hơn)
2. Áp dụng hệ số ưu tiên: `length * 10000 + modifier`
3. Sử dụng các modifier khác nhau cho các loại từ khác nhau:
   - Từ có dạng đầy đủ (có hậu tố): +10000 * (độ dài hậu tố)
   - Từ được thay thế đặc biệt: ưu tiên tùy chỉnh
   - Từ không thay đổi: -3000 (giảm ưu tiên)

Đoạn mã xử lý ưu tiên phức tạp nhất là trong phần xử lý cập nhật `pre_replacements_dict_2` -> `pre_replacements_dict_3`.

---

## 6. XỬ LÝ SONG SONG VÀ TỐI ƯU HÓA HIỆU SUẤT

### 6.1. Xử lý song song

Đối với văn bản dài, ứng dụng cung cấp cơ chế xử lý song song:

```python
def parallel_process(
    text: str,
    num_processes: int,
    placeholders_for_skipping_replacements,
    # ... các tham số khác ...
) -> str:
    # Kiểm tra nếu không cần xử lý song song
    if num_processes <= 1:
        return orchestrate_comprehensive_esperanto_text_replacement(...)
    
    # Chia văn bản thành các dòng
    lines = re.findall(r'.*?\n|.+$', text)
    num_lines = len(lines)
    
    # Chia thành các đoạn cho từng tiến trình
    lines_per_process = max(num_lines // num_processes, 1)
    ranges = [(i * lines_per_process, (i + 1) * lines_per_process) 
              for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], num_lines)  # Đảm bảo tiến trình cuối lấy hết phần còn lại
    
    # Khởi chạy các tiến trình
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            process_segment,
            [(lines[start:end], ...) for (start, end) in ranges]
        )
    
    # Kết hợp kết quả
    return ''.join(results)
```

Mỗi phân đoạn được xử lý bởi hàm `process_segment()` trên một tiến trình riêng.

### 6.2. Bộ nhớ đệm

Ứng dụng sử dụng bộ nhớ đệm Streamlit để tăng hiệu suất:

```python
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    """
    Đọc và lưu vào bộ nhớ đệm các danh sách thay thế từ tệp JSON
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # ... xử lý dữ liệu
    return (replacements_final_list, 
            replacements_list_for_localized_string,
            replacements_list_for_2char)
```

Điều này đảm bảo rằng các tệp JSON lớn chỉ được đọc một lần, giảm đáng kể thời gian xử lý khi người dùng thực hiện nhiều thao tác.

### 6.3. Tối ưu hóa thay thế

Các kỹ thuật tối ưu hóa chính cho phép xử lý nhanh:

1. **Sắp xếp trước khi thay thế**: Các mục thay thế được sắp xếp theo độ dài (dài đến ngắn)
2. **Kiểm tra sự tồn tại trước**: Chỉ áp dụng thay thế nếu chuỗi cần thay thế thực sự tồn tại trong văn bản
3. **Sử dụng placeholders**: Ngăn thay thế lồng nhau và xung đột
4. **Xử lý đặc biệt cho chuỗi ngắn**: Các gốc từ 2 ký tự được xử lý riêng

---

## 7. KỸ THUẬT ĐẶC BIỆT VÀ GIẢI THUẬT QUAN TRỌNG

### 7.1. Bảo vệ đoạn văn bản (Placeholders)

Một kỹ thuật quan trọng là sử dụng placeholders để bảo vệ một số đoạn văn bản:

1. **Đoạn được đánh dấu %...%**: Không bị thay thế
2. **Đoạn được đánh dấu @...@**: Thay thế cục bộ

Các placeholders được đọc từ tệp văn bản riêng biệt:

```python
def import_placeholders(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        placeholders = [line.strip() for line in file if line.strip()]
    return placeholders
```

Các hàm xử lý đoạn văn bản đặc biệt:

```python
def find_percent_enclosed_strings_for_skipping_replacement(text: str) -> List[str]:
    """Tìm tất cả chuỗi được bao bởi dấu % (tối đa 50 ký tự)"""
    matches = []
    used_indices = set()
    for match in PERCENT_PATTERN.finditer(text):
        start, end = match.span()
        if start not in used_indices and end-2 not in used_indices:
            matches.append(match.group(1))
            used_indices.update(range(start, end))
    return matches
```

### 7.2. Tự động điều chỉnh kích thước Ruby

Một tính năng thú vị là việc tự động điều chỉnh kích thước chú thích Ruby dựa trên tỷ lệ độ rộng của chú thích so với văn bản chính:

```python
if format_type == 'HTML格式_Ruby文字_大小调整':
    width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
    width_main = measure_text_width_Arial16(main_text, char_widths_dict)
    ratio_1 = width_ruby / width_main
    
    if ratio_1 > 6:
        # Chú thích rất dài - chia thành 3 phần và dùng font rất nhỏ
        return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
    elif ratio_1 > (9/3):
        # Chú thích dài - chia đôi và dùng font nhỏ hơn
        return f'<ruby>{main_text}<rt class="XXS_S">{insert_br_at_half_width(ruby_content, char_widths_dict)}</rt></ruby>'
    # ... các trường hợp khác
```

Phần CSS đi kèm sẽ định dạng các lớp khác nhau (XXXS_S, XXS_S, v.v.) với kích thước, vị trí và kiểu hiển thị phù hợp.

### 7.3. Loại bỏ Ruby dư thừa

Một tối ưu hóa thông minh là loại bỏ các thẻ Ruby khi văn bản chính và chú thích giống hệt nhau:

```python
def remove_redundant_ruby_if_identical(text: str) -> str:
    """
    Loại bỏ thẻ Ruby khi văn bản chính và chú thích giống nhau
    <ruby>xxx<rt class="XXL_L">xxx</rt></ruby> -> xxx
    """
    def replacer(match: re.Match) -> str:
        group1 = match.group(1)  # Văn bản chính
        group2 = match.group(2)  # Chú thích
        if group1 == group2:
            return group1  # Trả về chỉ văn bản, không có thẻ Ruby
        else:
            return match.group(0)  # Giữ nguyên
    
    replaced_text = IDENTICAL_RUBY_PATTERN.sub(replacer, text)
    return replaced_text
```

### 7.4. Xử lý từ điển với RegEx

Khi xử lý các từ có hậu tố đặc biệt và phân tách gốc từ, mã nguồn sử dụng các regex hiệu quả:

```python
def capitalize_ruby_and_rt(text: str) -> str:
    """Viết hoa ký tự đầu trong thẻ Ruby và RT"""
    def replacer(match):
        # ... xử lý các nhóm
        parent_text = g3.capitalize()
        rt_text = g5.capitalize()
        return g1 + g2 + parent_text + g4 + rt_text + g6 + (g7 if g7 else '') + g8
    
    replaced_text = RUBY_PATTERN.sub(replacer, text)
    if replaced_text == text:
        replaced_text = text.capitalize()
    return replaced_text
```

Mẫu regex được thiết kế cẩn thận để nhận diện và xử lý các thành phần HTML phức tạp.

---

## TÓM TẮT KỸ THUẬT

Ứng dụng Esperanto-Kanji này là một ví dụ tuyệt vời về việc xây dựng một công cụ xử lý văn bản phức tạp với Streamlit. Những điểm nổi bật về mặt kỹ thuật bao gồm:

1. **Thiết kế module hóa** rõ ràng với sự phân tách giữa giao diện người dùng và logic xử lý
2. **Cơ chế thay thế an toàn** sử dụng placeholders để tránh xung đột và thay thế lồng nhau
3. **Xử lý song song** để tăng hiệu suất với văn bản lớn
4. **Khả năng tùy chỉnh nâng cao** thông qua tệp JSON và CSV
5. **Định dạng Ruby thông minh** với điều chỉnh kích thước tự động dựa trên độ rộng
6. **Kỹ thuật lưu vào bộ nhớ đệm** để tối ưu hiệu suất
7. **Xử lý đặc biệt cho các trường hợp phức tạp** như hậu tố động từ và gốc từ 2 ký tự

Ứng dụng này có thể là mô hình tham khảo tuyệt vời cho việc phát triển các công cụ xử lý văn bản đa ngôn ngữ phức tạp.