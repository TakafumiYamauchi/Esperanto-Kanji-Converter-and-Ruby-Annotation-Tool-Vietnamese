# HƯỚNG DẪN SỬ DỤNG CÔNG CỤ THAY THẾ VĂN BẢN ESPERANTO BẰNG CHỮ HÁN (KANJI) VÀ TẠO CHÚ THÍCH RUBY

## Mục lục
- [HƯỚNG DẪN SỬ DỤNG CÔNG CỤ THAY THẾ VĂN BẢN ESPERANTO BẰNG CHỮ HÁN (KANJI) VÀ TẠO CHÚ THÍCH RUBY](#hướng-dẫn-sử-dụng-công-cụ-thay-thế-văn-bản-esperanto-bằng-chữ-hán-kanji-và-tạo-chú-thích-ruby)
  - [Mục lục](#mục-lục)
  - [1. Giới thiệu chung](#1-giới-thiệu-chung)
  - [2. Trang chính: Thay thế văn bản Esperanto](#2-trang-chính-thay-thế-văn-bản-esperanto)
    - [2.1 Cách chuẩn bị tệp JSON thay thế](#21-cách-chuẩn-bị-tệp-json-thay-thế)
    - [2.2 Các định dạng đầu ra](#22-các-định-dạng-đầu-ra)
    - [2.3 Nhập văn bản Esperanto](#23-nhập-văn-bản-esperanto)
    - [2.4 Xử lý song song (nâng cao)](#24-xử-lý-song-song-nâng-cao)
    - [2.5 Xem và tải xuống kết quả](#25-xem-và-tải-xuống-kết-quả)
  - [3. Trang tạo tệp JSON thay thế](#3-trang-tạo-tệp-json-thay-thế)
    - [3.1 Chuẩn bị tệp CSV](#31-chuẩn-bị-tệp-csv)
    - [3.2 Chuẩn bị tệp JSON quy tắc phân tách gốc từ](#32-chuẩn-bị-tệp-json-quy-tắc-phân-tách-gốc-từ)
    - [3.3 Tạo tệp JSON thay thế cuối cùng](#33-tạo-tệp-json-thay-thế-cuối-cùng)
  - [4. Các tính năng đặc biệt](#4-các-tính-năng-đặc-biệt)
    - [4.1 Ký hiệu % và @ để bảo vệ văn bản](#41-ký-hiệu--và--để-bảo-vệ-văn-bản)
    - [4.2 Hiển thị ký tự đặc thù của Esperanto](#42-hiển-thị-ký-tự-đặc-thù-của-esperanto)
  - [5. Giải thích chi tiết về các định dạng đầu ra](#5-giải-thích-chi-tiết-về-các-định-dạng-đầu-ra)
  - [6. Các phiên bản ngôn ngữ khác](#6-các-phiên-bản-ngôn-ngữ-khác)

## 1. Giới thiệu chung

Công cụ này được thiết kế để biến đổi văn bản tiếng Esperanto thành dạng chữ Hán (kanji) hoặc thêm chú thích ruby. Ứng dụng có hai chức năng chính:

1. **Trang chính**: Thay thế văn bản Esperanto bằng chữ Hán/kanji và tạo chú thích ruby
2. **Trang tạo tệp JSON**: Tạo tệp JSON chứa quy tắc thay thế để sử dụng trong trang chính

Công cụ này đặc biệt hữu ích cho:
- Người học Esperanto muốn liên hệ với các chữ Hán/kanji
- Người muốn tạo tài liệu học Esperanto với chú thích song ngữ
- Người muốn chuyển đổi văn bản Esperanto thành định dạng dễ đọc hơn với chú thích

## 2. Trang chính: Thay thế văn bản Esperanto

Trang chính là nơi bạn sẽ thực hiện việc thay thế văn bản Esperanto. Dưới đây là các bước sử dụng:

### 2.1 Cách chuẩn bị tệp JSON thay thế

Trang chính yêu cầu một tệp JSON chứa quy tắc thay thế. Bạn có hai lựa chọn:

1. **Sử dụng tệp JSON mặc định**: Đây là cách đơn giản nhất để bắt đầu.
   - Chọn "Sử dụng tệp JSON mặc định" trong phần đầu tiên của giao diện.
   - Hệ thống sẽ tự động tải tệp JSON mặc định.

2. **Tải lên tệp JSON tùy chỉnh**:
   - Chọn "Tải tệp lên" trong phần đầu tiên.
   - Nhấp vào "Browse files" để chọn tệp JSON đã được tạo (bạn có thể tạo tệp JSON từ trang thứ hai).
   - Định dạng tệp phải chứa ba danh sách thay thế đã hợp nhất.

Bạn cũng có thể tải xuống tệp JSON mẫu bằng cách:
- Nhấp vào mục "Tải xuống tệp JSON ví dụ (để thay thế)"
- Nhấp vào nút "Tải xuống tệp JSON ví dụ" trong phần mở rộng

### 2.2 Các định dạng đầu ra

Bạn có thể chọn một trong bảy định dạng đầu ra khác nhau:

1. **Định dạng HTML với chú thích Ruby và điều chỉnh kích thước**: Hiển thị gốc từ Esperanto với chú thích Ruby ở trên, tự động điều chỉnh kích thước chú thích.

2. **Định dạng HTML với chú thích Ruby, điều chỉnh kích thước và thay thế ký tự kanji**: Hiển thị chữ Hán/kanji với chú thích Ruby là gốc từ Esperanto, điều chỉnh kích thước tự động.

3. **Định dạng HTML**: Định dạng HTML cơ bản với chú thích Ruby ở kích thước tiêu chuẩn.

4. **Định dạng HTML với thay thế ký tự kanji**: Định dạng HTML cơ bản, nhưng hiển thị chữ Hán/kanji với chú thích Ruby là gốc từ Esperanto.

5. **Định dạng sử dụng dấu ngoặc**: Hiển thị gốc từ Esperanto với bản dịch trong ngoặc, ví dụ: "homo(人)".

6. **Định dạng dấu ngoặc với thay thế ký tự kanji**: Hiển thị chữ Hán/kanji với gốc từ Esperanto trong ngoặc, ví dụ: "人(homo)".

7. **Chỉ giữ lại văn bản đã được thay thế (thay thế đơn giản)**: Chỉ hiển thị bản dịch chữ Hán/kanji, không có gốc từ Esperanto.

Chọn định dạng phù hợp với mục đích của bạn từ menu thả xuống.

### 2.3 Nhập văn bản Esperanto

Bạn có hai cách để cung cấp văn bản Esperanto:

1. **Nhập thủ công**:
   - Chọn "Nhập thủ công" trong phần "Nguồn văn bản đầu vào".
   - Nhập trực tiếp văn bản Esperanto vào ô văn bản.

2. **Tải tệp lên**:
   - Chọn "Tải tệp lên" trong phần "Nguồn văn bản đầu vào".
   - Nhấp vào "Browse files" để chọn tệp văn bản (UTF-8) có đuôi .txt, .csv, hoặc .md.
   - Nội dung tệp sẽ được tự động nạp vào ô văn bản.

**Lưu ý quan trọng**: 
- Bạn có thể bao một phần văn bản trong dấu **%** (ví dụ: `%Không thay thế phần này%`) để phần đó **không được thay thế** và vẫn giữ nguyên trong kết quả cuối cùng.
- Tương tự, nếu bạn bao một phần văn bản trong dấu **@** (ví dụ: `@Thay thế riêng phần này@`), thì phần đó sẽ được thay thế **cục bộ** (chỉ trong phạm vi đoạn đó).

### 2.4 Xử lý song song (nâng cao)

Để tăng tốc độ xử lý với văn bản dài, bạn có thể bật tính năng xử lý song song:

1. Nhấp vào "Mở cài đặt cho chế độ xử lý song song".
2. Đánh dấu vào ô "Sử dụng chế độ xử lý song song".
3. Điều chỉnh số tiến trình chạy cùng lúc (từ 2 đến 4).

Tính năng này đặc biệt hữu ích khi xử lý văn bản có kích thước lớn.

### 2.5 Xem và tải xuống kết quả

Sau khi nhấn nút "Gửi", hệ thống sẽ xử lý văn bản và hiển thị kết quả:

1. **Xem kết quả**:
   - Nếu định dạng đầu ra là HTML, bạn sẽ thấy hai tab: "Xem trước HTML" và "Kết quả (mã HTML)".
   - Nếu định dạng đầu ra không phải HTML, kết quả sẽ hiển thị trong một tab duy nhất "Văn bản kết quả".

2. **Tải xuống kết quả**:
   - Nhấp vào nút "Tải xuống kết quả" để lưu kết quả thành tệp.
   - Tệp sẽ được lưu với định dạng HTML (nếu bạn chọn định dạng HTML) hoặc văn bản thuần túy.

## 3. Trang tạo tệp JSON thay thế

Trang thứ hai của ứng dụng cho phép bạn tạo tệp JSON tùy chỉnh chứa quy tắc thay thế. Đây là công cụ mạnh mẽ để tùy biến cách thay thế văn bản Esperanto.

### 3.1 Chuẩn bị tệp CSV

Bước đầu tiên là chuẩn bị tệp CSV chứa danh sách từ gốc Esperanto và bản dịch tương ứng:

1. **Chọn nguồn CSV**:
   - Chọn "Tải lên tệp CSV" nếu bạn muốn sử dụng tệp CSV riêng.
   - Chọn "Sử dụng mặc định" nếu muốn dùng tệp CSV mẫu có sẵn.

2. **Định dạng CSV**:
   - Cột đầu tiên: Gốc từ Esperanto
   - Cột thứ hai: Bản dịch tiếng Việt/chữ Hán/kanji

Bạn có thể tham khảo các tệp CSV mẫu trong phần "Danh sách tệp ví dụ (có thể tải về)":
- Ví dụ CSV 1: Danh sách gốc từ Esperanto với bản dịch tiếng Việt và chú thích ruby
- Ví dụ CSV 2: Gốc từ Esperanto - Chữ Hán (của Mingeo)
- Ví dụ CSV 3: Gốc từ Esperanto - Chữ Hán (chung)

### 3.2 Chuẩn bị tệp JSON quy tắc phân tách gốc từ

Tiếp theo, bạn cần chuẩn bị tệp JSON quy định cách phân tách gốc từ Esperanto:

1. **Chọn tệp JSON về quy tắc phân tách gốc từ Esperanto**:
   - Chọn "Tải lên tệp JSON" nếu bạn muốn sử dụng tệp tùy chỉnh.
   - Chọn "Sử dụng mặc định" nếu muốn dùng tệp mẫu có sẵn.

2. **Chọn tệp JSON về chuỗi thay thế riêng**:
   - Tương tự như trên, bạn có thể tải lên tệp tùy chỉnh hoặc sử dụng mặc định.

Bạn có thể tham khảo tệp JSON mẫu:
- Ví dụ JSON 1: Cài đặt quy tắc phân tách gốc từ Esperanto
- Ví dụ JSON 2: Cài đặt chuỗi sau khi thay thế

### 3.3 Tạo tệp JSON thay thế cuối cùng

Sau khi đã chuẩn bị các tệp CSV và JSON:

1. **Cài đặt xử lý song song (tùy chọn)**:
   - Mở mục "Mở cài đặt về xử lý song song".
   - Bật "Sử dụng xử lý song song" nếu muốn tăng tốc quá trình với dữ liệu lớn.
   - Điều chỉnh số tiến trình chạy đồng thời (từ 2 đến 6).

2. **Tạo tệp JSON cuối cùng**:
   - Nhấp vào nút "Tạo tệp JSON để thay thế".
   - Hệ thống sẽ xử lý dữ liệu và tạo tệp JSON kết hợp 3 danh sách thay thế.
   - Khi hoàn tất, nhấp vào nút "Tải xuống danh sách thay thế cuối cùng (kết hợp 3 tệp JSON)" để lưu tệp.

Tệp JSON này sẽ chứa ba danh sách thay thế:
- Danh sách thay thế toàn cục
- Danh sách thay thế cục bộ
- Danh sách thay thế gốc từ hai ký tự

## 4. Các tính năng đặc biệt

### 4.1 Ký hiệu % và @ để bảo vệ văn bản

Khi xử lý văn bản Esperanto, bạn có thể sử dụng các ký hiệu đặc biệt:

1. **Dấu %**: Bao quanh văn bản bạn muốn giữ nguyên không thay thế.
   - Ví dụ: `Mi %ne volas% ŝanĝi tiun parton` sẽ giữ nguyên từ "ne volas" trong kết quả.
   - Giới hạn tối đa 50 ký tự giữa các dấu %.

2. **Dấu @**: Bao quanh văn bản bạn muốn thay thế cục bộ.
   - Ví dụ: `Mi volas @speciale trakti@ tiun parton` sẽ thay thế riêng "speciale trakti".
   - Giới hạn tối đa 18 ký tự giữa các dấu @.

### 4.2 Hiển thị ký tự đặc thù của Esperanto

Bạn có thể chọn cách hiển thị các ký tự đặc thù của Esperanto trong kết quả:

1. **Ký hiệu mũ trên chữ cái**: Hiển thị các ký tự Esperanto đặc biệt với dấu mũ (ĉ, ĝ, ĥ, ĵ, ŝ, ŭ).

2. **Định dạng x**: Chuyển đổi ký tự Esperanto đặc biệt thành dạng "x" (ví dụ: ĉ → cx).

3. **Định dạng ^**: Chuyển đổi ký tự Esperanto đặc biệt thành dạng "^" (ví dụ: ĉ → c^).

Lựa chọn này không ảnh hưởng đến quá trình thay thế, chỉ thay đổi cách hiển thị kết quả cuối cùng.

## 5. Giải thích chi tiết về các định dạng đầu ra

Ứng dụng cung cấp 7 định dạng đầu ra khác nhau, mỗi định dạng phù hợp với các mục đích sử dụng khác nhau:

1. **Định dạng HTML với chú thích Ruby và điều chỉnh kích thước**:
   - Hiển thị: `<ruby>homo<rt class="M_M">人</rt></ruby>`
   - Kết quả hiển thị: Từ "homo" với chú thích "人" phía trên
   - Kích thước chú thích tự động điều chỉnh theo tỷ lệ độ dài của gốc từ và bản dịch
   - Phù hợp cho tài liệu học tập với chú thích rõ ràng

2. **Định dạng HTML với chú thích Ruby, điều chỉnh kích thước và thay thế ký tự kanji**:
   - Hiển thị: `<ruby>人<rt class="M_M">homo</rt></ruby>`
   - Kết quả hiển thị: Chữ "人" với chú thích "homo" phía trên
   - Phù hợp cho người đã biết chữ Hán muốn học Esperanto

3. **Định dạng HTML (cơ bản)**:
   - Hiển thị: `<ruby>homo<rt>人</rt></ruby>`
   - Đơn giản hơn, không điều chỉnh kích thước chú thích

4. **Định dạng HTML với thay thế ký tự kanji**:
   - Hiển thị: `<ruby>人<rt>homo</rt></ruby>`
   - Tương tự định dạng 3 nhưng đảo ngược vị trí

5. **Định dạng sử dụng dấu ngoặc**:
   - Hiển thị: `homo(人)`
   - Đơn giản, dễ đọc trong các trình soạn thảo thông thường
   - Phù hợp khi bạn không cần định dạng HTML

6. **Định dạng dấu ngoặc với thay thế ký tự kanji**:
   - Hiển thị: `人(homo)`
   - Đảo ngược vị trí so với định dạng 5

7. **Thay thế đơn giản**:
   - Hiển thị: `人`
   - Chỉ hiển thị bản dịch, bỏ qua gốc từ Esperanto
   - Phù hợp khi bạn chỉ quan tâm đến bản dịch

## 6. Các phiên bản ngôn ngữ khác

Công cụ này có sẵn trong 14 ngôn ngữ khác nhau. Bạn có thể truy cập phiên bản phù hợp qua các liên kết ở cuối trang chính:

- Esperanto: https://esperanto-kanji-converter-and-ruby-annotation-tool-esperanto.streamlit.app/
- English: https://esperanto-kanji-converter-and-ruby-annotation-tool-english.streamlit.app/
- 日本語: https://esperanto-kanji-converter-and-ruby-annotation-tool.streamlit.app/
- 中文: https://esperanto-hanzi-converter-and-ruby-annotation-tool-chinese-dgw.streamlit.app/
- 한국어: https://esperanto-kanji-converter-and-ruby-annotation-tool-korean-yrrx.streamlit.app/
- Русский: https://esperanto-kanji-converter-and-ruby-annotation-tool-russian.streamlit.app/
- Español: https://esperanto-kanji-converter-and-ruby-annotation-tool-spanish.streamlit.app/
- Italiano: https://esperanto-kanji-converter-and-ruby-annotation-tool-italian.streamlit.app/
- Français: https://esperanto-kanji-converter-and-ruby-annotation-tool-french.streamlit.app/
- Deutsch: https://esperanto-kanji-converter-and-ruby-annotation-tool-german.streamlit.app/
- العربية: https://esperanto-kanji-converter-and-ruby-annotation-tool-arabic.streamlit.app/
- हिन्दी: https://esperanto-kanji-converter-and-ruby-annotation-tool-hindi.streamlit.app/
- Polski: https://esperanto-kanji-converter-and-ruby-annotation-tool-polish.streamlit.app/
- Tiếng Việt: https://esperanto-kanji-converter-and-ruby-annotation-tool-vietnamese.streamlit.app/
- Bahasa Indonesia: https://esperanto-kanji-converter-and-ruby-annotation-tool-indonesian.streamlit.app/

Mã nguồn và hướng dẫn chi tiết (README.md) cho mỗi phiên bản đều có sẵn trong các kho lưu trữ GitHub tương ứng, được liệt kê ở cuối trang chính.

---

Hy vọng hướng dẫn này giúp bạn sử dụng hiệu quả công cụ thay thế văn bản Esperanto và tạo chú thích Ruby. Nếu có bất kỳ câu hỏi hoặc gặp vấn đề nào, vui lòng tham khảo kho lưu trữ GitHub của dự án hoặc liên hệ với nhà phát triển.


