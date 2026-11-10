# Kế hoạch và Nhiệm vụ: Người 2 - Phát triển Tool mới, Định nghĩa Contract và Viết Unit Test

## 1. Thông tin chung
- Vai trò: Chịu trách nhiệm thiết kế, lập trình công cụ mới (Custom Tool), viết tài liệu hướng dẫn công cụ (TOOL.md), đăng ký công cụ vào hệ thống và viết toàn bộ các bài kiểm thử tự động (Unit Test).
- Thư mục làm việc chính: starter_v0/tools và starter_v0/tests.

---

## 2. Danh sách file phụ trách trực tiếp
- starter_v0/tools/<ten_tool_moi>/tool.py
- starter_v0/tools/<ten_tool_moi>/TOOL.md
- starter_v0/tools/__init__.py
- starter_v0/tests/test_tools_todo.py
- Chạy kiểm tra với starter_v0/tests/test_tool_contract.py

---

## 3. Lộ trình thực hiện chi tiết theo từng mốc thời gian

### Giai đoạn 1: Khởi động và chuẩn bị (00 - 20 phút)
- Kiểm tra môi trường kiểm thử hiện có bằng lệnh:
  pytest tests/test_tool_contract.py
- Đọc các công cụ mẫu sẵn có trong starter_v0/tools/ để hiểu cấu trúc một Tool:
  - Mỗi tool là một thư mục riêng chứa tool.py và TOOL.md.
  - Hàm thực thi chính hoặc lớp xử lý nhận đầu vào là dictionary tham số và trả về kết quả dạng dictionary hoặc chuỗi văn bản chuẩn.
  - Đọc file starter_v0/tests/test_tools_todo.py để xác định các bài test đang chờ hoàn thiện (todo).

### Giai đoạn 2: Lựa chọn nghiệp vụ và thiết kế Tool mới (20 - 60 phút)
- Lựa chọn 1 công cụ nghiệp vụ mới phù hợp với chủ đề của nhóm (ví dụ: currency_converter, stock_price_lookup, sentiment_analyzer, text_summarizer, v.v.).
- Tạo thư mục mới trong starter_v0/tools/<ten_tool_moi>/.
- Viết file starter_v0/tools/<ten_tool_moi>/TOOL.md:
  - Tên công cụ.
  - Mục đích sử dụng.
  - Định nghĩa chi tiết các tham số đầu vào (tên biến, kiểu dữ liệu, bắt buộc hay tùy chọn).
  - Định nghĩa định dạng kết quả trả về.
  - Các trường hợp lỗi có thể xảy ra và cách xử lý.
- Cung cấp mô tả tham số và schema này cho Người 1 để cập nhật vào file tools.yaml.

### Giai đoạn 3: Hiện thực mã nguồn Tool (60 - 90 phút)
- Viết logic thực thi trong file starter_v0/tools/<ten_tool_moi>/tool.py:
  - Kiểm tra tính hợp lệ của tham số đầu vào bằng biểu thức chính quy (regex) hoặc kiểm tra kiểu dữ liệu rõ ràng.
  - Viết đầy đủ cấu trúc rẽ nhánh if/else, không viết tắt, không sử dụng else pass.
  - Đảm bảo bắt mọi ngoại lệ có thể xảy ra, trả về thông báo lỗi rõ ràng thay vì để chương trình bị dừng đột ngột (crash).
  - Tên biến và giá trị trả về phải rõ nghĩa, không viết tắt.
- Đăng ký công cụ vào file starter_v0/tools/__init__.py để hàm get_tool hoặc danh sách công cụ nhận diện được tool mới.

### Giai đoạn 4: Viết Unit Test và Mocking (90 - 120 phút)
- Mở file starter_v0/tests/test_tools_todo.py:
  - Hoàn thiện tất cả các hàm kiểm thử đang để trống hoặc đánh dấu todo.
  - Viết tối thiểu 3 ca kiểm thử cho tool mới:
    1. Ca thành công với dữ liệu đầu vào hợp lệ chuẩn.
    2. Ca kiểm tra biên hoặc dữ liệu đầu vào thiếu/sai định dạng.
    3. Ca xử lý lỗi ngoại lệ hoặc sự cố dịch vụ ngoài.
- Áp dụng kỹ thuật giả lập (Mocking / fake_http fixture) cho các lệnh gọi mạng bên ngoài:
  - Tuyệt đối không để unit test phụ thuộc vào mạng internet thật hoặc dịch vụ API bên ngoài.
  - Test phải độc lập và chạy nhanh trên máy nội bộ.
- Chạy toàn bộ các bài kiểm thử:
  pytest tests/test_tool_contract.py
  pytest tests/test_tools_todo.py
- Mục tiêu bắt buộc: 0 bài thất bại (0 failed), 0 bài bị bỏ qua (0 skipped).

### Giai đoạn 5: Hỗ trợ Showdown và phối hợp báo cáo (120 - 240 phút)
- Bàn giao kết quả kiểm thử (lệnh chạy và đầu ra thành công) cho Người 3 để đưa vào Báo cáo Phần A và Phần B.
- Luôn sẵn sàng hỗ trợ Người 1 và Người 3 trong trường hợp có lỗi phát sinh liên quan đến việc gọi hàm của tool mới trong quá trình chạy thử nghiệm trực tiếp.

---

## 4. Bàn giao kết quả
1. Thư mục tool mới gồm tool.py và TOOL.md hoàn chỉnh.
2. File starter_v0/tools/__init__.py đã đăng ký tool mới.
3. Toàn bộ bài test trong starter_v0/tests/test_tools_todo.py đều vượt qua thành công khi chạy pytest.

