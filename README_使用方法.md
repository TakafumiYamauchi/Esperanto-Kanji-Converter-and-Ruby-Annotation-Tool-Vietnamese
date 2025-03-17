# HƯỚNG DẪN SỬ DỤNG CÔNG CỤ THAY THẾ VÀ CHÚ THÍCH CHO VĂN BẢN ESPERANTO

## MỤC LỤC
1. Giới thiệu chung
2. Chức năng chính
3. Hướng dẫn sử dụng trang chính
4. Hướng dẫn tạo tệp JSON riêng
5. Các tính năng nâng cao
6. Ví dụ ứng dụng
7. Giải đáp thắc mắc thường gặp

---

## 1. GIỚI THIỆU CHUNG

Công cụ này được thiết kế để hỗ trợ người học và sử dụng tiếng Esperanto, giúp thay thế văn bản Esperanto bằng ký tự Kanji (chữ Hán) hoặc tạo chú thích (ruby) cho từng từ. Phần mềm hoạt động trên nền tảng Streamlit, cho phép bạn:

- Chuyển đổi văn bản Esperanto sang dạng có chú thích ký tự Kanji (chữ Hán)
- Thêm chú thích HTML kiểu Ruby (chữ nhỏ hiển thị trên từng từ)
- Tùy chỉnh định dạng hiển thị (HTML, dấu ngoặc, v.v.)
- Tạo và chỉnh sửa tệp JSON chứa quy tắc thay thế riêng

Ứng dụng này đặc biệt hữu ích cho người học tiếng Esperanto, giúp liên kết trực quan giữa từ gốc Esperanto và ý nghĩa thông qua chú thích bằng chữ Hán hoặc ngôn ngữ khác như tiếng Việt.

---

## 2. CHỨC NĂNG CHÍNH

### 2.1. Thay thế và chú thích văn bản

- **Thay thế từ gốc**: Chuyển đổi các từ gốc Esperanto thành chữ Hán/Kanji hoặc bản dịch tiếng Việt
- **Chú thích Ruby**: Hiển thị ý nghĩa của từ dưới dạng chú thích nhỏ phía trên
- **Đa dạng định dạng**: Hỗ trợ hiển thị kết quả theo nhiều kiểu (HTML, dấu ngoặc, v.v.)
- **Xử lý ký tự đặc biệt**: Hỗ trợ đầy đủ các ký tự đặc thù của Esperanto (ĉ, ĝ, ĥ, ĵ, ŝ, ŭ)

### 2.2. Tạo tệp JSON thay thế

- Tạo tệp JSON chứa quy tắc thay thế từ gốc Esperanto
- Tùy chỉnh cách phân tách gốc từ và định dạng hiển thị
- Hợp nhất nhiều danh sách thay thế khác nhau

### 2.3. Xử lý nâng cao

- Hỗ trợ xử lý song song để tăng tốc độ với văn bản dài
- Cho phép bảo vệ một số phần văn bản không bị thay thế (sử dụng dấu %)
- Cho phép thay thế cục bộ chỉ trong phạm vi đoạn văn bản nhất định (sử dụng dấu @)

---

## 3. HƯỚNG DẪN SỬ DỤNG TRANG CHÍNH

### 3.1. Giao diện trang chính

Khi mở ứng dụng, bạn sẽ thấy tiêu đề "Thay thế văn bản Esperanto bằng ký tự Kanji hoặc thêm chú thích HTML (phiên bản mở rộng)" và các phần cài đặt bên dưới.

### 3.2. Các bước cơ bản

#### Bước 1: Chọn tệp JSON để sử dụng cho việc thay thế

```
Bạn muốn xử lý tệp JSON như thế nào? (Đọc tệp JSON để thay thế)
```

- **Sử dụng tệp JSON mặc định**: Hệ thống sẽ sử dụng tệp JSON có sẵn chứa các quy tắc thay thế cơ bản
- **Tải tệp lên**: Nếu bạn đã có tệp JSON tùy chỉnh, bạn có thể tải lên để sử dụng

Bạn cũng có thể tải xuống tệp JSON mẫu bằng cách mở mục "Tải xuống tệp JSON ví dụ (để thay thế)".

#### Bước 2: Cài đặt nâng cao (tùy chọn)

Mở mục "Cài đặt nâng cao (xử lý song song)" nếu bạn muốn xử lý văn bản dài hoặc phức tạp:

- **Sử dụng chế độ xử lý song song**: Đánh dấu vào ô này để kích hoạt xử lý đa luồng
- **Số tiến trình chạy cùng lúc**: Chọn số lượng tiến trình (2-4) tùy theo cấu hình máy tính của bạn

#### Bước 3: Chọn định dạng đầu ra

```
Chọn định dạng đầu ra (giống với định dạng được chỉ định trong tệp JSON thay thế):
```

Các tùy chọn định dạng:
- **Định dạng HTML với chú thích Ruby và điều chỉnh kích thước**: Hiển thị từ gốc Esperanto với chú thích phía trên, tự động điều chỉnh kích thước
- **Định dạng HTML với chú thích Ruby, điều chỉnh kích thước và thay thế ký tự Kanji**: Hiển thị chữ Hán/Kanji làm từ chính với chú thích Esperanto phía trên
- **Định dạng HTML**: Dạng HTML cơ bản không điều chỉnh kích thước
- **Định dạng HTML với thay thế ký tự Kanji**: Dạng HTML với chữ Hán/Kanji làm từ chính
- **Định dạng sử dụng dấu ngoặc**: Hiển thị dạng "từ_gốc(chú_thích)"
- **Định dạng dấu ngoặc với thay thế ký tự Kanji**: Hiển thị dạng "chữ_Hán(từ_gốc)"
- **Chỉ giữ lại văn bản đã được thay thế**: Chỉ hiển thị chữ Hán/bản dịch mà không giữ từ gốc

#### Bước 4: Cung cấp văn bản đầu vào

```
Nguồn văn bản đầu vào
```

- **Nhập thủ công**: Nhập trực tiếp văn bản Esperanto vào ô văn bản
- **Tải tệp lên**: Tải lên tệp văn bản (.txt, .csv, .md) có mã hóa UTF-8

#### Bước 5: Nhập văn bản và cài đặt thêm

```
Vui lòng nhập văn bản Esperanto tại đây
```

- Nhập hoặc dán văn bản Esperanto cần xử lý
- Chọn cách hiển thị các ký tự đặc thù của Esperanto:
  - **Ký hiệu mũ trên chữ cái** (ĉ): Hiển thị dạng mũ trên chữ cái
  - **Định dạng x** (cx): Hiển thị dạng "x" sau chữ cái (cx thay cho ĉ)
  - **Định dạng ^** (c^): Hiển thị dạng "^" sau chữ cái (c^ thay cho ĉ)

#### Bước 6: Xử lý và tải kết quả

- Nhấn nút **Gửi** để bắt đầu xử lý
- Xem kết quả trong các tab hiển thị bên dưới
- Nhấn nút **Tải xuống kết quả** để lưu kết quả dưới dạng tệp HTML

### 3.3. Tính năng đặc biệt với dấu % và @

```
Nếu bạn bao một phần văn bản trong dấu %, thì phần đó sẽ không được thay thế và vẫn giữ nguyên trong kết quả cuối cùng.

Tương tự, nếu bạn bao một phần văn bản trong dấu @, thì phần đó sẽ được thay thế cục bộ (chỉ trong phạm vi đoạn đó).
```

#### Ví dụ:
- `La %plej bona% tago.` - Cụm từ "plej bona" sẽ không bị thay thế
- `La @bela@ tago.` - Từ "bela" sẽ được thay thế theo quy tắc riêng, độc lập với phần còn lại

---

## 4. HƯỚNG DẪN TẠO TỆP JSON RIÊNG

Nếu bạn muốn tùy chỉnh cách thay thế văn bản Esperanto, bạn có thể tạo tệp JSON riêng. Truy cập trang "Tạo tệp JSON dùng để thay thế (chữ Hán) trong văn bản Esperanto" trong menu bên trái.

### 4.1. Giao diện trang tạo JSON

Trang này cho phép bạn tạo tệp JSON tùy chỉnh với quy tắc thay thế riêng.

### 4.2. Các bước tạo tệp JSON

#### Bước 1: Chuẩn bị tệp CSV

```
Bước 1: Chuẩn bị tệp CSV
```

- **Tải lên tệp CSV**: Tải lên tệp CSV chứa từng dòng tương ứng gốc từ Esperanto và nghĩa/chữ Hán
- **Sử dụng mặc định**: Sử dụng tệp CSV mẫu có sẵn

Định dạng CSV cần có ít nhất hai cột:
- Cột 1: Từ gốc Esperanto
- Cột 2: Bản dịch/chữ Hán tương ứng

#### Bước 2: Chuẩn bị tệp JSON về quy tắc phân tách gốc từ

```
Bước 2: Chuẩn bị tệp JSON (quy tắc phân tách gốc từ, v.v.)
```

- **Tải lên tệp JSON**: Tải lên tệp JSON chứa quy tắc phân tách gốc từ Esperanto
- **Sử dụng mặc định**: Sử dụng tệp JSON mẫu có sẵn

Sau đó, cần chọn tệp JSON về chuỗi thay thế riêng:
- **Tải lên tệp JSON**: Tải lên tệp JSON chứa chuỗi thay thế tùy chỉnh
- **Sử dụng mặc định**: Sử dụng tệp JSON mẫu có sẵn

#### Bước 3: Cài đặt nâng cao (tùy chọn)

```
Bước 3: Cài đặt nâng cao (xử lý song song)
```

- **Sử dụng xử lý song song**: Đánh dấu để kích hoạt xử lý đa luồng
- **Số tiến trình chạy đồng thời**: Chọn số lượng tiến trình (2-6)

#### Bước 4: Tạo tệp JSON

- Nhấn nút **Tạo tệp JSON để thay thế**
- Đợi quá trình xử lý hoàn tất (có thể mất vài phút với dữ liệu lớn)
- Sau khi hoàn tất, hệ thống sẽ hiển thị nút **Tải xuống danh sách thay thế cuối cùng**

### 4.3. Hiểu về cấu trúc tệp JSON

Tệp JSON được tạo ra sẽ chứa ba danh sách chính:
- **全域替换用のリスト**: Danh sách dùng cho thay thế toàn cục
- **局部文字替换用のリスト**: Danh sách dùng cho thay thế cục bộ
- **二文字词根替换用のリスト**: Danh sách dùng cho thay thế gốc từ 2 chữ cái

Mỗi mục trong danh sách thường có dạng: `[từ_gốc, bản_thay_thế, placeholder]`

---

## 5. CÁC TÍNH NĂNG NÂNG CAO

### 5.1. Xử lý song song

Để xử lý văn bản dài, bạn có thể bật chế độ xử lý song song. Tính năng này phân tách văn bản thành nhiều đoạn và xử lý đồng thời, giúp giảm đáng kể thời gian xử lý.

```
Cài đặt nâng cao (xử lý song song)
```

- **Sử dụng chế độ xử lý song song**: Bật/tắt xử lý đa luồng
- **Số tiến trình chạy cùng lúc**: Chọn số lượng tiến trình phù hợp với CPU của bạn

### 5.2. Bảo vệ và thay thế cục bộ

Ứng dụng cho phép bạn kiểm soát chính xác cách thay thế từng phần của văn bản:

#### Bảo vệ nội dung (dấu %)

```
Nếu bạn bao một phần văn bản trong dấu % (ví dụ: %<tối đa 50 ký tự>%), thì phần đó sẽ không được thay thế và vẫn giữ nguyên trong kết quả cuối cùng.
```

Ví dụ:
- Văn bản: `Mi amas %la bela floro% en la ĝardeno.`
- Kết quả: Chỉ "Mi amas" và "en la ĝardeno" được thay thế, còn "la bela floro" giữ nguyên.

#### Thay thế cục bộ (dấu @)

```
Tương tự, nếu bạn bao một phần văn bản trong dấu @ (ví dụ: @<tối đa 18 ký tự>@), thì phần đó sẽ được thay thế cục bộ (chỉ trong phạm vi đoạn đó).
```

Ví dụ:
- Văn bản: `La suno @brilas@ super la montoj.`
- Kết quả: Từ "brilas" được thay thế theo quy tắc cục bộ, độc lập với ngữ cảnh chung.

### 5.3. Tùy chỉnh cách hiển thị ký tự đặc biệt

```
Chọn cách hiển thị các ký tự đặc thù của Esperanto trong kết quả
```

- **Ký hiệu mũ trên chữ cái**: ĉ, ĝ, ĥ, ĵ, ŝ, ŭ
- **Định dạng x**: cx, gx, hx, jx, sx, ux
- **Định dạng ^**: c^, g^, h^, j^, s^, u^

---

## 6. VÍ DỤ ỨNG DỤNG

### 6.1. Ví dụ 1: Thay thế đơn giản với chú thích Ruby

**Văn bản đầu vào:**
```
La suno brilas en la blua ĉielo. Birdo kantas sur la arbo.
```

**Cài đặt:**
- Định dạng: Định dạng HTML với chú thích Ruby và điều chỉnh kích thước
- Ký tự Esperanto: Ký hiệu mũ trên chữ cái

**Kết quả:**
Văn bản hiển thị với từng từ Esperanto kèm chú thích ý nghĩa phía trên.

### 6.2. Ví dụ 2: Thay thế với chữ Hán làm từ chính

**Văn bản đầu vào:**
```
Mi lernas Esperanton ĉiutage.
```

**Cài đặt:**
- Định dạng: Định dạng HTML với chú thích Ruby, điều chỉnh kích thước và thay thế ký tự Kanji
- Ký tự Esperanto: Định dạng x

**Kết quả:**
Chữ Hán được hiển thị làm từ chính với từ gốc Esperanto ở dạng chú thích nhỏ phía trên.

### 6.3. Ví dụ 3: Sử dụng dấu % và @ để kiểm soát thay thế

**Văn bản đầu vào:**
```
%La vortaro% estas tre @utila@ por la @lernantoj@.
```

**Cài đặt:**
- Định dạng: Định dạng sử dụng dấu ngoặc
- Ký tự Esperanto: Ký hiệu mũ trên chữ cái

**Kết quả:**
- "La vortaro" giữ nguyên không thay đổi
- "utila" và "lernantoj" được thay thế theo quy tắc riêng
- Các từ còn lại được thay thế bình thường

---

## 7. GIẢI ĐÁP THẮC MẮC THƯỜNG GẶP

### 7.1. Không thấy thay đổi sau khi xử lý?

- Kiểm tra tệp JSON đã được tải đúng cách
- Đảm bảo từ gốc Esperanto có trong tệp JSON
- Thử sử dụng tệp JSON mặc định để kiểm tra

### 7.2. Kết quả hiển thị không đúng ký tự Esperanto?

- Chọn lại cách hiển thị ký tự đặc thù phù hợp
- Đảm bảo văn bản nguồn sử dụng mã hóa UTF-8
- Thử chuyển đổi giữa các định dạng ký tự (ĉ, cx, c^)

### 7.3. Thời gian xử lý quá lâu?

- Bật chế độ xử lý song song
- Tăng số lượng tiến trình (nếu máy tính có nhiều lõi CPU)
- Chia nhỏ văn bản thành nhiều phần để xử lý riêng biệt

### 7.4. Làm thế nào để tạo tệp CSV riêng?

1. Tạo một tệp spreadsheet (Excel, Google Sheets, v.v.)
2. Tạo hai cột: từ gốc Esperanto và bản dịch/chữ Hán
3. Lưu dưới dạng CSV với mã hóa UTF-8
4. Tải lên trong ứng dụng

### 7.5. Cách khắc phục lỗi khi tạo tệp JSON?

- Kiểm tra định dạng CSV (phải có đúng hai cột)
- Đảm bảo không có ký tự đặc biệt gây xung đột
- Sử dụng mã hóa UTF-8 cho tất cả các tệp
- Thử sử dụng tệp mẫu có sẵn và chỉnh sửa dần

---

## LIÊN KẾT HỮU ÍCH

Ứng dụng có các phiên bản ngôn ngữ khác và tài liệu hướng dẫn chi tiết tại các liên kết được liệt kê ở cuối trang. Đặc biệt:

- **Phiên bản tiếng Việt**:
  https://esperanto-kanji-converter-and-ruby-annotation-tool-vietnamese.streamlit.app/

- **Tài liệu hướng dẫn trên GitHub (tiếng Việt)**:
  https://github.com/TakafumiYamauchi/Esperanto-Kanji-Converter-and-Ruby-Annotation-Tool-Vietnamese

---

Chúc bạn sử dụng ứng dụng hiệu quả trong việc học và làm việc với tiếng Esperanto!