# HƯỚNG DẪN KỸ THUẬT VỀ CƠ CHẾ HOẠT ĐỘNG CỦA ỨNG DỤNG THAY THẾ VĂN BẢN ESPERANTO

## MỤC LỤC
1. Tổng quan kiến trúc ứng dụng
2. Phân tích cấu trúc dữ liệu chính
3. Luồng xử lý chính và thuật toán
4. Cơ chế thay thế văn bản
5. Kỹ thuật xử lý song song
6. Phân tích mã nguồn chi tiết theo module

---

## 1. TỔNG QUAN KIẾN TRÚC ỨNG DỤNG

### 1.1. Cấu trúc tệp và module

Ứng dụng được xây dựng trên nền tảng Streamlit và có cấu trúc gồm 4 tệp Python chính:

1. **main.py**: 
   - Tệp chính khởi chạy giao diện Streamlit
   - Xử lý tương tác với người dùng trên trang chính
   - Điều phối quá trình thay thế văn bản

2. **Trang tạo tệp JSON để thay thế văn bản Esperanto bằng chuỗi ký tự (kanji).py**:
   - Hiển thị trong thư mục "pages" của Streamlit
   - Cung cấp giao diện tạo tệp JSON chứa quy tắc thay thế
   - Chuyển đổi dữ liệu CSV thành danh sách thay thế tối ưu

3. **esp_text_replacement_module.py**:
   - Module chức năng xử lý thay thế văn bản
   - Cung cấp các hàm chuyển đổi ký tự Esperanto
   - Xử lý placeholder và thực hiện thay thế an toàn

4. **esp_replacement_json_make_module.py**:
   - Module hỗ trợ tạo tệp JSON
   - Xử lý định dạng đầu ra (HTML, dấu ngoặc, v.v.)
   - Hỗ trợ tính toán độ rộng ký tự cho việc căn chỉnh

### 1.2. Kiến trúc tổng thể

Ứng dụng hoạt động theo mô hình luồng xử lý sau:

```
[Input: Văn bản Esperanto] → [Xử lý văn bản] → [Áp dụng quy tắc thay thế] → [Định dạng đầu ra] → [Output: Văn bản đã thay thế]
```

Trong đó:
- Quy tắc thay thế được lưu trữ trong tệp JSON
- Xử lý văn bản bao gồm nhiều bước từ tiền xử lý đến định dạng cuối cùng
- Quá trình có thể được tối ưu hóa bằng xử lý song song

---

## 2. PHÂN TÍCH CẤU TRÚC DỮ LIỆU CHÍNH

### 2.1. Cấu trúc tệp JSON thay thế

Tệp JSON thay thế chứa ba danh sách chính:

```json
{
  "全域替换用のリスト(列表)型配列(replacements_final_list)": [...],
  "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)": [...],
  "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)": [...]
}
```

Mỗi danh sách có mục đích riêng:
1. **replacements_final_list**: Danh sách thay thế toàn cục
2. **replacements_list_for_localized_string**: Danh sách thay thế cục bộ (cho vùng đánh dấu @...@)
3. **replacements_list_for_2char**: Danh sách thay thế các từ gốc 2 ký tự

Mỗi phần tử trong các danh sách có cấu trúc `[old, new, placeholder]`:
- `old`: Chuỗi cần thay thế
- `new`: Chuỗi thay thế
- `placeholder`: Chuỗi đóng vai trò giữ chỗ tạm thời trong quá trình xử lý

### 2.2. Bảng chuyển đổi ký tự Esperanto

Ứng dụng sử dụng các từ điển (dictionary) để chuyển đổi giữa các dạng biểu diễn ký tự đặc biệt của Esperanto:

```python
x_to_circumflex = {
    'cx': 'ĉ', 'gx': 'ĝ', 'hx': 'ĥ', 'jx': 'ĵ', 'sx': 'ŝ', 'ux': 'ŭ',
    'Cx': 'Ĉ', 'Gx': 'Ĝ', 'Hx': 'Ĥ', 'Jx': 'Ĵ', 'Sx': 'Ŝ', 'Ux': 'Ŭ'
}
```

Các từ điển này hỗ trợ chuyển đổi giữa ba dạng biểu diễn:
- Dạng circumflex (ĉ, ĝ...)
- Dạng x (cx, gx...)
- Dạng ^ (c^, g^...)

### 2.3. Phân loại từ gốc và hậu tố

Ứng dụng phân loại các từ gốc và hậu tố/tiền tố để xử lý riêng:

```python
suffix_2char_roots = ['ad', 'ag', 'am', 'ar', 'as', 'at', 'av', ...] 
prefix_2char_roots = ['al', 'am', 'av', 'bo', 'di', 'du', 'ek', ...]
standalone_2char_roots = ['al', 'ci', 'da', 'de', 'di', 'do', ...]
```

Ngoài ra, còn có các danh sách đặc biệt như:
- `verb_suffix_2l`: Hậu tố động từ (as, is, os, us...)
- `AN` và `ON`: Danh sách các từ có hậu tố đặc biệt "an"/"on"

---

## 3. LUỒNG XỬ LÝ CHÍNH VÀ THUẬT TOÁN

### 3.1. Luồng xử lý trong main.py

Luồng xử lý chính trong trang web gồm các bước:

1. **Khởi tạo giao diện Streamlit**:
   ```python
   st.set_page_config(
       page_title="Công cụ thay thế ký tự (kanji) trong văn bản tiếng Esperanto",
       layout="wide"
   )
   ```

2. **Tải tệp JSON chứa quy tắc thay thế**:
   ```python
   @st.cache_data
   def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
       # Đọc và trả về 3 danh sách thay thế từ tệp JSON
       # ...
   ```

3. **Tải placeholders** (chuỗi giữ chỗ):
   ```python
   placeholders_for_skipping_replacements: List[str] = import_placeholders(
       './Appの运行に使用する各类文件/占位符(placeholders)_%1854%-%4934%_文字列替换skip用.txt'
   )
   ```

4. **Xử lý đầu vào người dùng và áp dụng thay thế**:
   ```python
   with st.form(key='profile_form'):
       # Lấy văn bản đầu vào
       # ...
       if submit_btn:
           # Áp dụng xử lý song song hoặc xử lý tuần tự
           if use_parallel:
               processed_text = parallel_process(...)
           else:
               processed_text = orchestrate_comprehensive_esperanto_text_replacement(...)
   ```

5. **Hiển thị kết quả**:
   ```python
   if processed_text:
       # Hiển thị xem trước
       # Tạo tùy chọn tải xuống
       # ...
   ```

### 3.2. Thuật toán thay thế văn bản

Hàm chính xử lý thay thế văn bản là `orchestrate_comprehensive_esperanto_text_replacement()` trong module `esp_text_replacement_module.py`:

```python
def orchestrate_comprehensive_esperanto_text_replacement(
    text, 
    placeholders_for_skipping_replacements,
    replacements_list_for_localized_string,
    placeholders_for_localized_replacement,
    replacements_final_list,
    replacements_list_for_2char,
    format_type
) -> str:
    # 1, 2) Chuẩn hóa khoảng trắng và chuyển đổi ký tự Esperanto
    text = unify_halfwidth_spaces(text)
    text = convert_to_circumflex(text)
    
    # 3) Thay thế tạm thời phần được bảo vệ bởi %...%
    # ...
    
    # 4) Thay thế cục bộ phần được đánh dấu bởi @...@
    # ...
    
    # 5) Thay thế toàn cục
    # ...
    
    # 6) Thay thế gốc từ 2 ký tự (thực hiện 2 lần)
    # ...
    
    # 7) Khôi phục các placeholder
    # ...
    
    # 8) Định dạng HTML nếu cần
    # ...
    
    return text
```

8 bước xử lý văn bản này tạo nên cốt lõi thuật toán thay thế văn bản của ứng dụng.

### 3.3. Thuật toán tạo tệp JSON thay thế

Quá trình tạo tệp JSON bao gồm các bước chính:

1. **Đọc tệp CSV** chứa từ gốc Esperanto và bản dịch/chữ Hán
2. **Tạo từ điển thay thế tạm thời**:
   ```python
   temporary_replacements_dict = {}
   for *, (E*root, hanzi_or_meaning) in CSV_data_imported.iterrows():
       if pd.notna(E_root) and pd.notna(hanzi_or_meaning) \
          and '#' not in E_root and (E_root != '') and (hanzi_or_meaning != ''):
           temporary_replacements_dict[E_root] = [
               output_format(E_root, hanzi_or_meaning, format_type, char_widths_dict),
               len(E_root)
           ]
   ```

3. **Tạo danh sách thay thế sơ bộ** và sắp xếp theo độ dài:
   ```python
   temporary_replacements_list_1 = []
   for old, new in temporary_replacements_dict.items():
       temporary_replacements_list_1.append((old, new[0], new[1]))
   temporary_replacements_list_2 = sorted(temporary_replacements_list_1, key=lambda x: x[2], reverse=True)
   ```

4. **Gán placeholders** cho từng cặp thay thế:
   ```python
   temporary_replacements_list_final = []
   for kk in range(len(temporary_replacements_list_2)):
       temporary_replacements_list_final.append([
           temporary_replacements_list_2[kk][0],
           temporary_replacements_list_2[kk][1],
           imported_placeholders_for_global_replacement[kk]
       ])
   ```

5. **Xử lý các dạng từ đặc biệt** (từ gốc 2 ký tự, hậu tố động từ, v.v.):
   ```python
   # Xử lý từ gốc 2 ký tự
   replacements_list_for_suffix_2char_roots = []
   for i in range(len(suffix_2char_roots)):
       replaced_suffix = remove_redundant_ruby_if_identical(safe_replace(suffix_2char_roots[i], temporary_replacements_list_final))
       # ...
   ```

6. **Kết hợp các danh sách** thành một tệp JSON

---

## 4. CƠ CHẾ THAY THẾ VĂN BẢN

### 4.1. Thay thế an toàn với placeholders

Cốt lõi của quá trình thay thế là hàm `safe_replace()`:

```python
def safe_replace(text: str, replacements: List[Tuple[str, str, str]]) -> str:
    valid_replacements = {}
    # Bước 1: Thay old bằng placeholder
    for old, new, placeholder in replacements:
        if old in text:
            text = text.replace(old, placeholder)
            valid_replacements[placeholder] = new
    # Bước 2: Thay placeholder bằng new
    for placeholder, new in valid_replacements.items():
        text = text.replace(placeholder, new)
    return text
```

Quy trình 2 bước này ngăn chặn các xung đột trong quá trình thay thế, đặc biệt khi có từ ngắn là một phần của từ dài hơn.

### 4.2. Xử lý vùng đặc biệt với % và @

Ứng dụng xử lý hai kiểu vùng đặc biệt:

1. **Vùng được bảo vệ (%...%)**:
   ```python
   def find_percent_enclosed_strings_for_skipping_replacement(text: str) -> List[str]:
       """Trích xuất tất cả chuỗi có dạng '%foo%'. Giới hạn 50 ký tự."""
       # ...
   ```

2. **Vùng thay thế cục bộ (@...@)**:
   ```python
   def find_at_enclosed_strings_for_localized_replacement(text: str) -> List[str]:
       """Trích xuất tất cả chuỗi có dạng '@foo@'. Giới hạn 18 ký tự."""
       # ...
   ```

Các chuỗi này được xử lý đặc biệt:
- Chuỗi %...% được giữ nguyên không thay đổi
- Chuỗi @...@ được thay thế theo quy tắc riêng, độc lập với phần còn lại

### 4.3. Định dạng đầu ra

Hàm `output_format()` trong module `esp_replacement_json_make_module.py` xử lý các định dạng đầu ra:

```python
def output_format(main_text, ruby_content, format_type, char_widths_dict):
    if format_type == 'HTML格式_Ruby文字_大小调整':
        width_ruby = measure_text_width_Arial16(ruby_content, char_widths_dict)
        width_main = measure_text_width_Arial16(main_text, char_widths_dict)
        ratio_1 = width_ruby / width_main
        if ratio_1 > 6:
            return f'<ruby>{main_text}<rt class="XXXS_S">{insert_br_at_third_width(ruby_content, char_widths_dict)}</rt></ruby>'
        # ... các trường hợp khác dựa trên tỷ lệ
    elif format_type == 'HTML格式_Ruby文字_大小调整_汉字替换':
        # Tương tự nhưng đảo ngược main_text và ruby_content
    # ... các định dạng khác
```

Hàm này xử lý:
- Các định dạng HTML với chú thích Ruby
- Tùy chỉnh kích thước chú thích dựa trên tỷ lệ độ rộng
- Thêm ngắt dòng khi cần thiết
- Các định dạng đơn giản hơn (dấu ngoặc, thay thế đơn thuần)

---

## 5. KỸ THUẬT XỬ LÝ SONG SONG

### 5.1. Cơ chế xử lý song song

Để tăng hiệu suất với văn bản lớn, ứng dụng sử dụng `multiprocessing`:

```python
def parallel_process(
    text: str,
    num_processes: int,
    # ... các tham số khác
) -> str:
    # Chia văn bản thành các đoạn theo dòng
    lines = re.findall(r'.*?\n|.+$', text)
    num_lines = len(lines)
    
    # Tính toán số dòng cho mỗi tiến trình
    lines_per_process = max(num_lines // num_processes, 1)
    ranges = [(i * lines_per_process, (i + 1) * lines_per_process) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], num_lines)  # Tiến trình cuối xử lý các dòng còn lại
    
    # Xử lý song song
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            process_segment,
            [
                (lines[start:end], ...) for (start, end) in ranges
            ]
        )
    
    # Kết hợp kết quả
    return ''.join(results)
```

Ở đây, văn bản được chia thành các đoạn nhỏ và xử lý đồng thời bởi nhiều tiến trình.

### 5.2. Hàm xử lý đoạn văn bản

Mỗi tiến trình gọi hàm `process_segment()` để xử lý phần của mình:

```python
def process_segment(
    lines: List[str],
    # ... các tham số khác
) -> str:
    segment = ''.join(lines)
    result = orchestrate_comprehensive_esperanto_text_replacement(
        segment,
        # ... các tham số khác
    )
    return result
```

### 5.3. Xử lý song song trong việc tạo tệp JSON

Tương tự, quá trình tạo tệp JSON cũng sử dụng xử lý song song:

```python
def parallel_build_pre_replacements_dict(
    E_stem_with_Part_Of_Speech_list: List[List[str]],
    replacements: List[Tuple[str, str, str]],
    num_processes: int = 4
) -> Dict[str, List[str]]:
    # Chia dữ liệu thành num_processes phần
    # Xử lý song song mỗi phần
    # Kết hợp kết quả từ các tiến trình
    # ...
```

---

## 6. PHÂN TÍCH MÃ NGUỒN CHI TIẾT THEO MODULE

### 6.1. Module main.py

#### 6.1.1. Cấu trúc chung

```python
# Import các thư viện cần thiết
import streamlit as st
import re
import io
import json
import pandas as pd
from typing import List, Dict, Tuple, Optional
import streamlit.components.v1 as components
import multiprocessing

# Cài đặt multiprocessing
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass

# Import các hàm từ module esp_text_replacement_module
from esp_text_replacement_module import (
    x_to_circumflex,
    x_to_hat,
    # ... các hàm khác
)

# Hàm cache để tải danh sách thay thế
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    # ...

# Cài đặt giao diện Streamlit
st.set_page_config(...)
st.title(...)

# Đọc tệp JSON thay thế
# ...

# Đọc placeholders
# ...

# Cài đặt xử lý song song
# ...

# Chọn định dạng đầu ra
# ...

# Xử lý nguồn văn bản đầu vào
# ...

# Form xử lý văn bản
with st.form(key='profile_form'):
    # ...

# Hiển thị kết quả
if processed_text:
    # ...
```

#### 6.1.2. Điểm quan trọng

- Sử dụng `@st.cache_data` để tối ưu hóa hiệu suất khi tải tệp JSON
- Xử lý đa định dạng đầu vào (nhập thủ công/tải tệp)
- Xử lý song song có thể được bật/tắt
- Hỗ trợ nhiều định dạng đầu ra (HTML, dấu ngoặc, v.v.)
- Xử lý đặc biệt cho các ký tự Esperanto

### 6.2. Module esp_text_replacement_module.py

#### 6.2.1. Các hàm chính

- **Chuyển đổi ký tự**:
  ```python
  def replace_esperanto_chars(text, char_dict: Dict[str, str]) -> str:
      # Thay thế ký tự theo từ điển
  
  def convert_to_circumflex(text: str) -> str:
      # Chuyển đổi sang dạng circumflex (ĉ, ĝ, v.v.)
  ```

- **Xử lý placeholder**:
  ```python
  def safe_replace(text: str, replacements: List[Tuple[str, str, str]]) -> str:
      # Thay thế an toàn sử dụng placeholders
  
  def import_placeholders(filename: str) -> List[str]:
      # Đọc danh sách placeholders từ tệp
  ```

- **Xử lý vùng đặc biệt**:
  ```python
  def find_percent_enclosed_strings_for_skipping_replacement(text: str) -> List[str]:
      # Tìm chuỗi được bảo vệ bởi %...%
  
  def find_at_enclosed_strings_for_localized_replacement(text: str) -> List[str]:
      # Tìm chuỗi thay thế cục bộ bởi @...@
  ```

- **Xử lý song song**:
  ```python
  def parallel_process(text: str, num_processes: int, ...) -> str:
      # Xử lý song song văn bản
  
  def process_segment(lines: List[str], ...) -> str:
      # Xử lý một đoạn văn bản
  ```

#### 6.2.2. Thuật toán chính

Hàm chủ đạo `orchestrate_comprehensive_esperanto_text_replacement()` thực hiện quy trình thay thế văn bản 8 bước.

### 6.3. Module esp_replacement_json_make_module.py

#### 6.3.1. Các hàm chính

- **Đo độ rộng văn bản**:
  ```python
  def measure_text_width_Arial16(text, char_widths_dict: Dict[str, int]) -> int:
      # Tính toán độ rộng văn bản dựa trên từ điển độ rộng ký tự
  ```

- **Chèn ngắt dòng**:
  ```python
  def insert_br_at_half_width(text, char_widths_dict: Dict[str, int]) -> str:
      # Chèn <br> khi độ rộng vượt quá một nửa
  
  def insert_br_at_third_width(text, char_widths_dict: Dict[str, int]) -> str:
      # Chèn <br> tại vị trí 1/3 và 2/3 độ rộng
  ```

- **Định dạng đầu ra**:
  ```python
  def output_format(main_text, ruby_content, format_type, char_widths_dict):
      # Định dạng đầu ra theo kiểu chỉ định
  ```

- **Xử lý đặc biệt cho Ruby**:
  ```python
  def capitalize_ruby_and_rt(text: str) -> str:
      # Viết hoa ký tự đầu tiên trong các thẻ Ruby
  
  def remove_redundant_ruby_if_identical(text: str) -> str:
      # Loại bỏ Ruby dư thừa nếu nội dung giống nhau
  ```

### 6.4. Trang tạo tệp JSON

#### 6.4.1. Cấu trúc chung

```python
# Import thư viện
import streamlit as st
import pandas as pd
import io
import os
import re
import json
# ...

# Import hàm từ các module
from esp_text_replacement_module import (...)
from esp_replacement_json_make_module import (...)

# Định nghĩa các biến và từ điển
verb_suffix_2l = {...}
AN = [...]
ON = [...]
suffix_2char_roots = [...]
prefix_2char_roots = [...]
standalone_2char_roots = [...]

# Import placeholders
imported_placeholders_for_global_replacement = import_placeholders(...)
# ...

# Cài đặt giao diện Streamlit
st.set_page_config(...)
st.title(...)

# Tải tệp CSV
# ...

# Tải tệp JSON về quy tắc phân tách gốc từ
# ...

# Xử lý song song
# ...

# Tạo tệp JSON
if st.button("Tạo tệp JSON để thay thế"):
    # Đọc dữ liệu
    # Tạo từ điển thay thế tạm thời
    # Xử lý và sắp xếp danh sách
    # Tạo danh sách thay thế cuối cùng
    # ...
```

#### 6.4.2. Điểm quan trọng

- Xử lý nhiều loại từ gốc (thông thường, 2 ký tự, hậu tố, v.v.)
- Áp dụng quy tắc phân tách gốc từ từ tệp JSON
- Áp dụng chuỗi thay thế tùy chỉnh từ tệp JSON
- Tối ưu hóa thứ tự thay thế (từ dài trước, từ ngắn sau)
- Hỗ trợ chữ hoa/thường và viết hoa chữ cái đầu
- Tạo ba danh sách thay thế cho các mục đích khác nhau

---

Đây là phân tích chi tiết về cơ chế hoạt động của ứng dụng. Hy vọng bạn đã hiểu rõ hơn về cách thức hoạt động bên trong của ứng dụng này. Nếu bạn cần thêm thông tin về bất kỳ phần nào, hãy cho tôi biết để tôi có thể giải thích sâu hơn.