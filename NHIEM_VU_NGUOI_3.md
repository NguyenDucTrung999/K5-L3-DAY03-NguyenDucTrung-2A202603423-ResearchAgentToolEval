# Kế hoạch và Nhiệm vụ: Người 3 - Giao diện Streamlit, Cloudflare Tunnel, Trình diễn Trực tiếp và Báo cáo Tổng hợp

## 1. Thông tin chung
- Vai trò: Chịu trách nhiệm xây dựng giao diện tương tác người dùng (Streamlit), cấu hình đường hầm công khai (Cloudflare Tunnel), ghi lại nhật ký hội thoại thực tế (Transcripts), và tổng hợp nội dung Báo cáo (REPORT.md Phần A và Phần B).
- Thư mục làm việc chính: starter_v0/ và starter_v0/artifacts/.

---

## 2. Danh sách file phụ trách trực tiếp
- starter_v0/app.py
- starter_v0/artifacts/REPORT.md
- starter_v0/transcripts/ (các file hội thoại sinh ra từ chat.py hoặc app.py)

---

## 3. Lộ trình thực hiện chi tiết theo từng mốc thời gian

### Giai đoạn 1: Khởi động và cấu hình môi trường Giao diện (00 - 20 phút)
- Kiểm tra cài đặt các thư viện phục vụ giao diện:
  pip install streamlit
- Kiểm tra công cụ tạo đường hầm cloudflared trên hệ điều hành Linux:
  cloudflared --version
- Đọc file starter_v0/chat.py để hiểu cách gọi Agent và cơ chế ghi log transcript.

### Giai đoạn 2: Xây dựng Giao diện Streamlit cơ bản (20 - 60 phút)
- Tạo mới file starter_v0/app.py:
  - Hiển thị khung chat trực tiếp giữa người dùng và Research Agent.
  - Có khung chọn phiên bản mô hình (v0, v1, v2, v3).
  - Có khu vực hiển thị các công cụ đã được gọi (tên công cụ, tham số truyền vào, kết quả trả về từ công cụ).
  - Hiển thị thời gian phản hồi (latency) của từng lượt gọi công cụ.
- Chạy thử nghiệm cục bộ:
  streamlit run app.py --server.port 8501
- Kiểm tra giao diện trên trình duyệt tại địa chỉ http://localhost:8501.

### Giai đoạn 3: Thiết lập Cloudflare Tunnel và Live Transcript (60 - 90 phút)
- Mở đường hầm mạng công khai bằng lệnh:
  cloudflared tunnel --url http://localhost:8501
- Lưu lại đường dẫn công khai (dạng https://<random-subdomain>.trycloudflare.com) để chuẩn bị cung cấp cho giảng viên và điền vào báo cáo.
- Chạy tương tác thử nghiệm và sinh file transcript:
  python chat.py --version v1 --save-transcript
- Đảm bảo các file transcript được lưu trữ đầy đủ trong thư mục starter_v0/transcripts/.

### Giai đoạn 4: Hoàn thành Báo cáo Phần A trước giờ Showdown (90 - 150 phút, Hạn chót 16:30)
- Mở file starter_v0/artifacts/REPORT.md.
- Thu thập số liệu từ Người 1 và Người 2 để hoàn thiện toàn bộ Phần A (Part A):
  1. Thông tin thành viên nhóm và phân công nhiệm vụ.
  2. Bảng mô tả thiết kế Tool mới (lấy từ Người 2).
  3. Bảng so sánh kết quả đo đạc giữa phiên bản v0 và v1 trên bộ dữ liệu base (lấy từ Người 1 trong version_log.csv).
  4. Đường dẫn công khai Cloudflare Tunnel đang hoạt động.
- Nộp đường dẫn báo cáo Phần A đúng hạn quy định trước 16:30.

### Giai đoạn 5: Tham gia Showdown và Hoàn thiện Báo cáo Phần B (150 - 240 phút, Hạn chót nộp LMS 17:30)
- Trực tiếp vận hành giao diện Streamlit trong phần thi đấu Showdown:
  - Nhập các câu hỏi thách đấu từ giảng viên hoặc nhóm bạn.
  - Theo dõi nhật ký cuộc gọi công cụ xem có xảy ra lỗi hay không.
- Phối hợp với Người 1 và Người 2 ghi nhận các trường hợp thất bại (Failure Cases) xuất hiện trong lúc thi đấu.
- Hoàn thành Phần B (Part B) trong starter_v0/artifacts/REPORT.md:
  - Bảng so sánh toàn diện qua cả 4 phiên bản v0, v1, v2, v3 trên cả 2 bộ dữ liệu base và group.
  - Phân tích chi tiết ít nhất 2 trường hợp agent đưa ra kết quả sai hoặc gọi sai công cụ.
  - Đánh giá bài học kinh nghiệm về việc thiết kế schema, kiểm thử biên và prompt engineering.
- Kiểm tra toàn bộ mã nguồn trước khi đẩy lên hệ thống nộp bài:
  - Xác nhận file .env không bị thêm vào git (kiểm tra git status).
  - Kiểm tra đường dẫn repository theo đúng định dạng quy định.
  - Nộp link bài tập lên hệ thống aithucchien.vinuni.edu.vn trước 17:30.

---

## 4. Bàn giao kết quả
1. File starter_v0/app.py chạy ổn định, hiển thị trực quan cuộc hội thoại và nhật ký gọi tool.
2. Đường hầm Cloudflare Tunnel sẵn sàng hoạt động phục vụ đánh giá trực tiếp.
3. Thư mục starter_v0/transcripts/ có ít nhất 2 cuộc hội thoại mẫu.
4. File starter_v0/artifacts/REPORT.md được hoàn thiện cả Phần A và Phần B.

