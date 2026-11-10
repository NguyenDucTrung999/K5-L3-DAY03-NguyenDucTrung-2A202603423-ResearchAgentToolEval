# Kế hoạch và Nhiệm vụ: Người 1 - Prompt Engineering, Tool Schema, Version Log và Đánh giá Dataset

## 1. Thông tin chung
- Vai trò: Chịu trách nhiệm về System Prompt, Tool Schema (tools.yaml), quản lý phiên bản (version_log.csv) và bộ dữ liệu đánh giá nhóm (data/eval_group.json).
- Thư mục làm việc chính: starter_v0/artifacts và starter_v0/data.

---

## 2. Danh sách file phụ trách trực tiếp
- starter_v0/artifacts/system_prompt.md
- starter_v0/artifacts/tools.yaml
- starter_v0/artifacts/version_log.csv
- starter_v0/data/eval_group.json

---

## 3. Lộ trình thực hiện chi tiết theo từng mốc thời gian

### Giai đoạn 1: Khởi động và chuẩn bị (00 - 20 phút)
- Sao chép file môi trường và điền khóa API:
  cp .env.example .env
- Kiểm tra các biến môi trường:
  PROVIDER_DEFAULT=gemini
  OPENAI_API_KEY=...
  GEMINI_API_KEY=...
- Đọc kỹ cấu trúc starter_v0/artifacts/tools.yaml hiện tại để nắm rõ 5 công cụ cơ bản ban đầu:
  1. web_search
  2. fetch_web_page
  3. retrieve_internal_policy
  4. calculate_financial_metrics
  5. compute_compound_growth

### Giai đoạn 2: Chạy Baseline v0 (20 - 60 phút)
- Chạy đánh giá phiên bản ban đầu v0 với bộ câu hỏi cơ bản:
  python run_eval.py --agent-version v0 --suite base
- Kiểm tra kết quả tạo ra tại:
  starter_v0/artifacts/eval_results_v0_base.json
- Phân tích các trường hợp thất bại theo 5 loại lỗi quy định:
  1. WRONG_TOOL: Gọi sai công cụ.
  2. BAD_ARGS: Sai định dạng hoặc thiếu tham số yêu cầu.
  3. HALLUCINATED_TOOL: Tự bịa ra tên công cụ không tồn tại trong schema.
  4. MISSING_CALL: Cần gọi công cụ nhưng agent chỉ suy đoán trả lời dạng văn bản thô.
  5. UNPARSEABLE: Cú pháp JSON hoặc phản hồi của model bị lỗi cú pháp.
- Ghi nhận thông số v0 vào file starter_v0/artifacts/version_log.csv:
  - version: v0
  - tool_call_accuracy
  - task_success_rate
  - avg_tool_latency_ms
  - change_summary: Baseline ban đầu chưa tinh chỉnh prompt hoặc schema.

### Giai đoạn 3: Tinh chỉnh Prompt lên v1 (60 - 90 phút)
- Phối hợp với Người 2 để lấy thông tin tool mới do Người 2 phát triển (tên tool, mô tả tham số, kiểu dữ liệu).
- Cập nhật định nghĩa tool mới vào starter_v0/artifacts/tools.yaml theo định dạng chuẩn YAML.
- Cập nhật starter_v0/artifacts/system_prompt.md:
  - Thêm quy tắc hướng dẫn agent khi nào cần dùng tool mới.
  - Thêm ràng buộc bắt buộc chỉ dùng đúng tham số trong schema.
  - Bổ sung ít nhất 2 ví dụ few-shot chuẩn xác vào system prompt.
- Chạy đánh giá v1 với bộ câu hỏi cơ bản:
  python run_eval.py --agent-version v1 --suite base
- Cập nhật kết quả đo được vào starter_v0/artifacts/version_log.csv.

### Giai đoạn 4: Xây dựng bộ đánh giá nhóm eval_group.json và v2 (90 - 120 phút)
- Tạo mới file starter_v0/data/eval_group.json gồm tối thiểu 10 câu hỏi đánh giá theo miền nghiệp vụ của nhóm.
- Đảm bảo trong 10 câu hỏi có ít nhất 2 câu hỏi yêu cầu sử dụng tool mới do Người 2 tạo ra.
- Chạy đánh giá v2 trên cả hai bộ dữ liệu:
  python run_eval.py --agent-version v2 --suite base
  python run_eval.py --agent-version v2 --suite group
- Cập nhật kết quả vào starter_v0/artifacts/version_log.csv.

### Giai đoạn 5: Chuẩn bị Showdown và hoàn thiện v3 (120 - 240 phút)
- Chuyển giao các chỉ số chính xác và đường dẫn file kết quả cho Người 3 điền vào Báo cáo Phần A (trước 16:30).
- Sau phần thi đấu Showdown hoặc sau khi nhận phản hồi thất bại từ test case lạ, tinh chỉnh tiếp system prompt để hoàn thiện phiên bản v3.
- Chạy đánh giá v3:
  python run_eval.py --agent-version v3 --suite base
  python run_eval.py --agent-version v3 --suite group
- Kiểm tra lại file starter_v0/artifacts/version_log.csv đủ thông tin các hàng v0, v1, v2, v3.

---

## 4. Bàn giao kết quả
1. File starter_v0/artifacts/system_prompt.md hoàn chỉnh, có few-shot, không bịa tên công cụ.
2. File starter_v0/artifacts/tools.yaml chứa đầy đủ schema của các tool ban đầu và tool mới.
3. File starter_v0/data/eval_group.json đủ ít nhất 10 câu hỏi có ground truth rõ ràng.
4. File starter_v0/artifacts/version_log.csv có đủ lịch sử đo đạc từ v0 đến v3.

