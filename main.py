##  main.py(1つ目)
# main.py (メインの Streamlit アプリ/機能拡充版202502)

import streamlit as st
import re
import io
import json
import pandas as pd  # 必要なら使う
from typing import List, Dict, Tuple, Optional
import streamlit.components.v1 as components
import multiprocessing

#=================================================================
# Streamlit で multiprocessing を使う際、PicklingError 回避のため
# 明示的に 'spawn' モードを設定する必要がある。
#=================================================================
try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    pass  # すでに start method が設定済みの場合はここで無視する

#=================================================================
# エスペラント文の(漢字)置換・ルビ振りなどを行う独自モジュールから
# 関数をインポートする。
# esp_text_replacement_module.py内に定義されているツールをまとめて呼び出す
#=================================================================
from esp_text_replacement_module import (
    x_to_circumflex,
    x_to_hat,
    hat_to_circumflex,
    circumflex_to_hat,
    replace_esperanto_chars,
    import_placeholders,
    orchestrate_comprehensive_esperanto_text_replacement,
    parallel_process,
    apply_ruby_html_header_and_footer
)

#=================================================================
# Streamlit の @st.cache_data デコレータを使い、読み込み結果をキャッシュして
# JSONファイルのロード高速化を図る。大きなJSON(50MB程度)を都度読むと遅いので、
# ここで呼び出す関数をキャッシュする作り。
#=================================================================
@st.cache_data
def load_replacements_lists(json_path: str) -> Tuple[List, List, List]:
    """
    JSONファイルをロードし、以下の3つのリストをタプルとして返す:
    1) replacements_final_list
    2) replacements_list_for_localized_string
    3) replacements_list_for_2char
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    replacements_final_list = data.get(
        "全域替换用のリスト(列表)型配列(replacements_final_list)", []
    )
    replacements_list_for_localized_string = data.get(
        "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)", []
    )
    replacements_list_for_2char = data.get(
        "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)", []
    )
    return (
        replacements_final_list,
        replacements_list_for_localized_string,
        replacements_list_for_2char,
    )

#=================================================================
# Streamlit ページの見た目設定
# page_title: ブラウザタブに表示されるタイトル
# layout="wide" で横幅を広く使えるUIにする
#=================================================================
st.set_page_config(
    page_title="Công cụ thay thế ký tự (kanji) trong văn bản tiếng Esperanto",
    layout="wide"
)

# タイトル部分（GUI表示のみベトナム語に）
st.title("Thay thế văn bản Esperanto bằng ký tự Kanji hoặc thêm chú thích HTML (phiên bản mở rộng)")
st.write("---")

#=================================================================
# 1) JSONファイル (置換ルール) をロード
#   (デフォルトを使うか、ユーザーがアップロードするかの選択)
#=================================================================
json_options = ["デフォルトを使用する", "アップロードする"]

selected_option = st.radio(
    "Bạn muốn xử lý tệp JSON như thế nào? (Đọc tệp JSON để thay thế)",
    json_options,
    format_func=lambda x: "Sử dụng tệp JSON mặc định" if x == "デフォルトを使用する" else "Tải tệp lên"
)

with st.expander("Tải xuống tệp JSON ví dụ (để thay thế)"):
    json_file_path = './Appの运行に使用する各类文件/最终的な替换用リスト(列表)(合并3个JSON文件).json'
    with open(json_file_path, "rb") as file_json:
        btn_json = st.download_button(
            label="Tải xuống tệp JSON ví dụ",
            data=file_json,
            file_name="vi_du_tep_JSON.json",
            mime="application/json"
        )

replacements_final_list: List[Tuple[str, str, str]] = []
replacements_list_for_localized_string: List[Tuple[str, str, str]] = []
replacements_list_for_2char: List[Tuple[str, str, str]] = []

if selected_option == "デフォルトを使用する":
    default_json_path = "./Appの运行に使用する各类文件/最终的な替换用リスト(列表)(合并3个JSON文件).json"
    try:
        (replacements_final_list,
         replacements_list_for_localized_string,
         replacements_list_for_2char) = load_replacements_lists(default_json_path)
        st.success("Đã tải tệp JSON mặc định thành công.")
    except Exception as e:
        st.error(f"Không thể tải tệp JSON mặc định: {e}")
        st.stop()
else:
    uploaded_file = st.file_uploader(
        "Tải lên tệp JSON (định dạng đã hợp nhất 3 danh sách).json",
        type="json"
    )
    if uploaded_file is not None:
        try:
            combined_data = json.load(uploaded_file)
            replacements_final_list = combined_data.get(
                "全域替换用のリスト(列表)型配列(replacements_final_list)", []
            )
            replacements_list_for_localized_string = combined_data.get(
                "局部文字替换用のリスト(列表)型配列(replacements_list_for_localized_string)", []
            )
            replacements_list_for_2char = combined_data.get(
                "二文字词根替换用のリスト(列表)型配列(replacements_list_for_2char)", []
            )
            st.success("Đã tải tệp JSON bạn vừa chọn thành công.")
        except Exception as e:
            st.error(f"Không thể đọc tệp JSON đã tải lên: {e}")
            st.stop()
    else:
        st.warning("Chưa tải lên tệp JSON. Dừng xử lý.")
        st.stop()

#=================================================================
# 2) placeholders (占位符) の読み込み
#    %...% や @...@ で囲った文字列を守るために使用する文字列群を読み込む
#=================================================================
placeholders_for_skipping_replacements: List[str] = import_placeholders(
    './Appの运行に使用する各类文件/占位符(placeholders)_%1854%-%4934%_文字列替换skip用.txt'
)
placeholders_for_localized_replacement: List[str] = import_placeholders(
    './Appの运行に使用する各类文件/占位符(placeholders)_@5134@-@9728@_局部文字列替换结果捕捉用.txt'
)

st.write("---")

#=================================================================
# 設定パラメータ (UI) - 高度な設定
# 並列処理 (multiprocessing) を利用できるかどうかのスイッチと、
# 同時プロセス数の選択
#=================================================================
st.header("Cài đặt nâng cao (xử lý song song)")
with st.expander("Mở cài đặt cho chế độ xử lý song song"):
    st.write("""
    Tại đây, bạn có thể thiết lập số tiến trình sẽ chạy song song
    trong quá trình thay thế ký tự (kanji).
    """)
    use_parallel = st.checkbox("Sử dụng chế độ xử lý song song", value=False)
    num_processes = st.number_input(
        "Số tiến trình chạy cùng lúc",
        min_value=2, max_value=4, value=4, step=1
    )

st.write("---")

#=================================================================
# 例: 出力形式の選択
# (HTMLルビ形式・括弧形式・文字列のみ など)
#=================================================================
options = {
    'HTML格式_Ruby文字_大小调整': 'HTML格式_Ruby文字_大小调整',
    'HTML格式_Ruby文字_大小调整_汉字替换': 'HTML格式_Ruby文字_大小调整_汉字替换',
    'HTML格式': 'HTML格式',
    'HTML格式_漢字替换': 'HTML格式_漢字替换',
    '括弧(号)格式': '括弧(号)格式',
    '括弧(号)格式_漢字替换': '括弧(号)格式_漢字替换',
    '替换后文字列のみ(仅)保留(简单替换)': '替换后文字列のみ(仅)保留(简单替换)'
}

options_vietnamese_labels = {
    'HTML格式_Ruby文字_大小调整': "Định dạng HTML với chú thích Ruby và điều chỉnh kích thước",
    'HTML格式_Ruby文字_大小调整_汉字替换': "Định dạng HTML với chú thích Ruby, điều chỉnh kích thước và thay thế ký tự kanji",
    'HTML格式': "Định dạng HTML",
    'HTML格式_漢字替换': "Định dạng HTML với thay thế ký tự kanji",
    '括弧(号)格式': "Định dạng sử dụng dấu ngoặc",
    '括弧(号)格式_漢字替换': "Định dạng dấu ngoặc với thay thế ký tự kanji",
    '替换后文字列のみ(仅)保留(简单替换)': "Chỉ giữ lại văn bản đã được thay thế (thay thế đơn giản)"
}

display_options = list(options.keys())
selected_display = st.selectbox(
    "Chọn định dạng đầu ra (giống với định dạng được chỉ định trong tệp JSON thay thế):",
    display_options,
    format_func=lambda key: options_vietnamese_labels[key]
)
format_type = options[selected_display]

processed_text = ""

#=================================================================
# 4) 入力テキストのソースを選択 (手動入力 or ファイルアップロード)
#=================================================================
source_options = ["手動入力", "ファイルアップロード"]
st.subheader("Nguồn văn bản đầu vào")
source_option = st.radio(
    "Bạn muốn cung cấp văn bản đầu vào như thế nào?",
    source_options,
    format_func=lambda x: "Nhập thủ công" if x == "手動入力" else "Tải tệp lên"
)

uploaded_text = ""

if source_option == "ファイルアップロード":
    text_file = st.file_uploader("Tải lên tệp văn bản (mã hóa UTF-8)", type=["txt", "csv", "md"])
    if text_file is not None:
        uploaded_text = text_file.read().decode("utf-8", errors="replace")
        st.info("Đã tải tệp văn bản thành công.")
    else:
        st.warning("Chưa tải tệp văn bản. Hãy chuyển sang nhập thủ công hoặc tải tệp lên.")

#=================================================================
# フォーム: 実行ボタン(送信/キャンセル)を配置
#  - テキストエリアにエスペラント文を入力してもらう
#=================================================================
with st.form(key='profile_form'):

    if uploaded_text:
        initial_text = uploaded_text
    else:
        initial_text = st.session_state.get("text0_value", "")

    text0 = st.text_area(
        "Vui lòng nhập văn bản Esperanto tại đây",
        height=150,
        value=initial_text
    )

    st.markdown("""Nếu bạn bao một phần văn bản trong dấu **%** 
    (ví dụ: `%<tối đa 50 ký tự>%`),
    thì phần đó **sẽ không được thay thế** và vẫn giữ nguyên trong kết quả cuối cùng.""")

    st.markdown("""Tương tự, nếu bạn bao một phần văn bản trong dấu **@** 
    (ví dụ: `@<tối đa 18 ký tự>@`),
    thì phần đó sẽ được thay thế **cục bộ** (chỉ trong phạm vi đoạn đó).""")

    letter_type = st.radio(
        'Chọn cách hiển thị các ký tự đặc thù của Esperanto trong kết quả',
        ('上付き文字', 'x 形式', '^形式'),
        format_func=lambda x: (
            "Ký hiệu mũ trên chữ cái (ĉ → c + ˆ)" if x == "上付き文字"
            else ("Định dạng x (ĉ → cx)" if x == "x 形式" else "Định dạng ^ (ĉ → c^)")
        )
    )

    submit_btn = st.form_submit_button('Gửi')
    cancel_btn = st.form_submit_button("Hủy")

    if cancel_btn:
        st.warning("Đã hủy quá trình.")
        st.stop()

    if submit_btn:
        st.session_state["text0_value"] = text0

        if use_parallel:
            processed_text = parallel_process(
                text=text0,
                num_processes=num_processes,
                placeholders_for_skipping_replacements=placeholders_for_skipping_replacements,
                replacements_list_for_localized_string=replacements_list_for_localized_string,
                placeholders_for_localized_replacement=placeholders_for_localized_replacement,
                replacements_final_list=replacements_final_list,
                replacements_list_for_2char=replacements_list_for_2char,
                format_type=format_type
            )
        else:
            processed_text = orchestrate_comprehensive_esperanto_text_replacement(
                text=text0,
                placeholders_for_skipping_replacements=placeholders_for_skipping_replacements,
                replacements_list_for_localized_string=replacements_list_for_localized_string,
                placeholders_for_localized_replacement=placeholders_for_localized_replacement,
                replacements_final_list=replacements_final_list,
                replacements_list_for_2char=replacements_list_for_2char,
                format_type=format_type
            )

        if letter_type == '上付き文字':
            processed_text = replace_esperanto_chars(processed_text, x_to_circumflex)
            processed_text = replace_esperanto_chars(processed_text, hat_to_circumflex)
        elif letter_type == '^形式':
            processed_text = replace_esperanto_chars(processed_text, x_to_hat)
            processed_text = replace_esperanto_chars(processed_text, circumflex_to_hat)

        processed_text = apply_ruby_html_header_and_footer(processed_text, format_type)

#=================================================================
# =========================================
# フォーム外の処理: 結果表示・ダウンロード
# =========================================
#=================================================================
if processed_text:
    MAX_PREVIEW_LINES = 250
    lines = processed_text.splitlines()

    if len(lines) > MAX_PREVIEW_LINES:
        first_part = lines[:247]
        last_part = lines[-3:]
        preview_text = "\n".join(first_part) + "\n...\n" + "\n".join(last_part)
        st.warning(
            f"Văn bản quá dài (tổng số dòng: {len(lines)}). "
            "Chỉ hiển thị bản xem trước rút gọn (247 dòng đầu và 3 dòng cuối)."
        )
    else:
        preview_text = processed_text

    if "HTML" in format_type:
        tab1, tab2 = st.tabs(["Xem trước HTML", "Kết quả (mã HTML)"])
        with tab1:
            components.html(preview_text, height=500, scrolling=True)
        with tab2:
            st.text_area("Mã HTML được tạo:", preview_text, height=300)
    else:
        tab3_list = st.tabs(["Văn bản kết quả"])
        with tab3_list[0]:
            st.text_area("Kết quả:", preview_text, height=300)

    download_data = processed_text.encode('utf-8')
    st.download_button(
        label="Tải xuống kết quả",
        data=download_data,
        file_name="ket_qua_thay_the.html",
        mime="text/html"
    )

st.write("---")
st.title("Ligilo-oj(URL-oj)")
st.markdown("""
#### Ligilo-oj de la aplikaĵo en aliaj lingvaj versioj (Esperanto, English, 日本語, 中文, 한국어, Русский, español, italiano, français, Deutsch, العربية, हिन्दी, polski, Tiếng Việt, Bahasa Indonesia; entute 14 lingvoj) ⇓  
              
Esperanta versio    
https://esperanto-kanji-converter-and-ruby-annotation-tool-esperanto.streamlit.app/  
English version  
https://esperanto-kanji-converter-and-ruby-annotation-tool-english.streamlit.app/  
日本語版    
https://esperanto-kanji-converter-and-ruby-annotation-tool.streamlit.app/  
中文版  
https://esperanto-hanzi-converter-and-ruby-annotation-tool-chinese-dgw.streamlit.app/  
한국어 버전  
https://esperanto-kanji-converter-and-ruby-annotation-tool-korean-yrrx.streamlit.app/    
Русская версия  
https://esperanto-kanji-converter-and-ruby-annotation-tool-russian.streamlit.app/  
Versión en español  
https://esperanto-kanji-converter-and-ruby-annotation-tool-spanish.streamlit.app/  
Versione italiana  
https://esperanto-kanji-converter-and-ruby-annotation-tool-italian.streamlit.app/  
Version française  
https://esperanto-kanji-converter-and-ruby-annotation-tool-french.streamlit.app/  
Deutsche Version  
https://esperanto-kanji-converter-and-ruby-annotation-tool-german.streamlit.app/  
إصدار عربي  
https://esperanto-kanji-converter-and-ruby-annotation-tool-arabic.streamlit.app/  
हिन्दी संस्करण  
https://esperanto-kanji-converter-and-ruby-annotation-tool-hindi.streamlit.app/  
Polska wersja  
https://esperanto-kanji-converter-and-ruby-annotation-tool-polish.streamlit.app/  
**Phiên bản tiếng Việt**  
https://esperanto-kanji-converter-and-ruby-annotation-tool-vietnamese.streamlit.app/  
Versi Bahasa Indonesia  
https://esperanto-kanji-converter-and-ruby-annotation-tool-indonesian.streamlit.app/  

#### Uzadaj instrukcioj de la aplikaĵo (README.md en la GitHub-deponejo) ⇓    
  
Esperanta versio  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Esperanto  
English version  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-English  
日本語版    
https://github.com/Takatakatake/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-  
中文版  
https://github.com/Takatakatake/Esperanto-Hanzi-Converter-and-Ruby-Annotation-Tool-Chinese  
한국어 버전  
https://github.com/Takatakatake/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Korean  
Русская версия    
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Russian  
Versión en español  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Spanish  
Versione italiana  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Italian  
Version française  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-French  
Deutsche Version  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-German  
إصدار عربي  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Arabic  
हिन्दी संस्करण  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Hindi  
Polska wersja  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Polish  
**Phiên bản tiếng Việt**  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Vietnamese  
Versi Bahasa Indonesia  
https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Indonesian  
""")