# Báo cáo Đánh giá Chi tiết Phiên bản v1 (Optimization Evaluation)

File này tổng hợp và trực quan hóa kết quả chạy đánh giá phiên bản cải tiến v1 từ file nhật ký thực thi `runs/v1_B_base_openrouter_20261110T120623880369.json`.

---

## 1. Thông tin tổng quan lượt chạy
- Mã lượt chạy (Run ID): v1_B_base_openrouter_20261110T120623880369
- Phiên bản Agent: v1 (Phiên bản đã tối ưu hóa Prompt và bổ sung Tool mới)
- Nhà cung cấp mô hình (Provider): OpenRouter
- Mô hình sử dụng: openai/gpt-4o-mini
- Bộ dữ liệu đánh giá: data/eval_base.json (Giai đoạn B - 20 trường hợp kiểm thử)
- Thời gian tạo: 2026-11-10 12:06:23

---

## 2. Bảng so sánh các chỉ số cốt lõi giữa v0 và v1

| Chỉ số đo đạc | Phiên bản v0 (Baseline) | Phiên bản v1 (Optimized) | Mức độ cải thiện |
| :--- | :--- | :--- | :--- |
| Tổng số test case | 20 cases | 20 cases | Hoàn thành trọn vẹn 20/20 cases |
| Số case bị lỗi API (Provider Error) | 8 cases (Gemini 429) | 0 cases | Khắc phục hoàn toàn lỗi mạng |
| Số case đạt yêu cầu (PASS) | 7 / 12 cases | 18 / 20 cases | Tăng thêm 11 ca thành công |
| Tỷ lệ thành công tổng thể (Case Accuracy) | 58.33% | 90.00% (18 / 20) | Tăng +31.67% |
| Độ chính xác chọn công cụ (Tool Routing Accuracy) | 66.67% | 100.00% (20 / 20) | Đạt độ chính xác tuyệt đối 100% |
| Độ chính xác truyền tham số (Argument Accuracy) | 58.33% | 90.00% (18 / 20) | Tăng +31.67% |
| Độ chính xác xử lý đa lượt (Multiturn Accuracy) | 100.0% (1 / 1 case) | 100.00% (6 / 6 cases) | Vượt qua toàn bộ 6/6 kịch bản đa lượt |

---

## 3. Bảng chi tiết toàn bộ 20 trường hợp kiểm thử phiên bản v1

| Mã Case | Yêu cầu của người dùng | Công cụ kỳ vọng | Công cụ thực tế gọi | Kết quả | Phân loại lỗi | Chi tiết kiểm tra |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R01_user_tweets_routing | Tweet mới nhất của Sam Altman là gì? | timeline | timeline | PASS | Không | Đúng công cụ và tham số |
| R02_search_tweets_routing | Mọi người đang bàn gì về GPT-5 trên Twitter? | social_search | social_search | PASS | Không | Đúng công cụ và tham số |
| R03_web_news_routing | Tin tức AI hôm nay có gì nổi bật? | lookup | lookup | PASS | Không | Khắc phục thành công lỗi nhồi nhét từ khóa ở v0 |
| R04_read_url_routing | Tóm tắt bài này giúp mình: https://openai.com/blog | fetch | fetch | PASS | Không | Đúng công cụ và URL |
| R05_limit_arg | Lấy 10 tweet mới nhất của Elon Musk | timeline | timeline | PASS | Không | Đúng tham số limit=10 |
| R06_timeframe_arg | Tin công nghệ trong tuần này | lookup | lookup | PASS | Không | Đúng tham số timeframe='week' |
| R07_search_type_arg | Cho mình các tweet phổ biến (top) nhất về OpenAI | social_search | social_search | PASS | Không | Đúng tham số search_type='Top' |
| R08_out_of_scope | Giải giúp mình bài toán tích phân: nguyên hàm của x^2 | Không gọi tool | Không gọi tool | PASS | Không | Khắc phục triệt để: không tự ý gọi tool send như ở v0 |
| R09_no_tool_capability | Bạn là gì và làm được những gì? | Không gọi tool | Không gọi tool | PASS | Không | Khắc phục triệt để: không tự ý gọi tool policy như ở v0 |
| R10_missing_handle | Tóm tắt 5 tweet mới nhất giúp mình | clarify | clarify | FAIL | missing_info | Đã chọn đúng tool clarify, nhưng thiếu tham số response_type='text' |
| R11_missing_url | Tóm tắt bài viết này hộ mình | clarify | clarify | FAIL | missing_info | Đã chọn đúng tool clarify, nhưng thiếu tham số response_type='text' |
| R12_confirm_before_send | Đăng bản tin này lên Telegram giúp mình | clarify | clarify | PASS | Không | Khắc phục triệt để: đã hỏi xác nhận trước khi gửi |
| R13_parallel_web_and_tweets | Tìm trên web tin AI hôm nay và tìm thêm tweet về AI | lookup, social_search | lookup, social_search | PASS | Không | Gọi chính xác đồng thời cả 2 công cụ |
| R14_out_of_scope_coding | Viết giúp mình một hàm Python tính Fibonacci | Không gọi tool | Không gọi tool | PASS | Không | Trả lời trực tiếp, không gọi công cụ thừa |
| M01_clarify_then_fill | Đa lượt: Điền tiếp handle @sama | timeline | timeline | PASS | Không | Hoàn thành chính xác |
| M02_carryover_timeframe | Đa lượt: Kế thừa khung thời gian | lookup | lookup | PASS | Không | Hoàn thành chính xác |
| M03_correction_handle | Đa lượt: Đổi sang handle mới | timeline | timeline | PASS | Không | Hoàn thành chính xác |
| M04_clarify_then_url | Đa lượt: Cung cấp link URL bài báo | fetch | fetch | PASS | Không | Hoàn thành chính xác |
| M05_correction_limit | Đa lượt: Đổi số lượng bài sang 10 | timeline | timeline | PASS | Không | Hoàn thành chính xác |
| M06_switch_tool | Đa lượt: Đổi từ Twitter sang tra cứu web | lookup | lookup | PASS | Không | Hoàn thành chính xác |

---

## 4. Những cải tiến vượt bậc so với phiên bản v0

1. **Độ chính xác chọn công cụ (Tool Routing) đạt 100%**:
   - Ở bản v0, mô hình bị hoang tưởng gọi linh tinh `send` và `policy` khi gặp các câu hỏi ngoài phạm vi (R08, R09). Ở v1, mô hình đã nhận biết chính xác và không gọi công cụ nào.
2. **Khắc phục lỗi an toàn gửi tin (Guardrail - Case R12)**:
   - Ở bản v0, khi người dùng bảo "Đăng bài lên Telegram", Agent tự ý gửi ngay lập tức. Ở v1, Agent đã chủ động dừng lại và gọi `clarify` để yêu cầu xác nhận.
3. **Khắc phục lỗi tham số tìm kiếm (Case R03)**:
   - Ở bản v0, Agent nhồi cả cụm từ dài vào trường `query`. Ở v1, Agent đã truyền đúng thực thể gọn gàng và phân chia đúng `topic` và `timeframe`.
4. **Vượt qua 100% các kịch bản đàm thoại đa lượt (Multi-turn M01 - M06)**:
   - Agent duy trì mạch hội thoại xuất sắc, biết nhớ lại ngữ cảnh của lượt trước và thay đổi tham số theo yêu cầu mới của người dùng.

---

## 5. Phân tích 2 trường hợp chưa đạt và hướng nâng cấp lên v2 (Mục tiêu 100%)

Hai trường hợp duy nhất chưa đạt điểm tối đa ở phiên bản v1 là **R10** và **R11**:
- **Hiện tượng**: Agent đã rất thông minh khi nhận ra yêu cầu thiếu thông tin và **đã chủ động gọi công cụ `clarify`** kèm câu hỏi hỏi lại người dùng rất chuẩn xác ("Bạn có thể cho biết tên tài khoản Twitter không?" / "Bạn có thể cung cấp liên kết bài viết không?").
- **Nguyên nhân FAIL**: Khi gọi hàm `clarify(question=...)`, Agent để tham số `response_type=None` trong khi đề bài kiểm tra nghiêm ngặt bắt buộc phải có `response_type="text"`.
- **Giải pháp đưa v2 lên 100%**:
  Bổ sung một quy tắc ngắn vào `artifacts/system_prompt.md`:
  *"Khi gọi công cụ clarify để hỏi lại người dùng câu hỏi mở bằng văn bản, luôn bắt buộc truyền tham số response_type='text'".*
  Chỉ cần sửa điểm này, Agent sẽ đạt độ chính xác tuyệt đối **20/20 (100%)** ở phiên bản v2.

