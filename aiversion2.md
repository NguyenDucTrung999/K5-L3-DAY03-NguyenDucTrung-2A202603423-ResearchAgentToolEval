# Báo cáo Đánh giá Chi tiết Phiên bản v2 (Base và Group Evaluation)

File này tổng hợp và trực quan hóa kết quả chạy đánh giá toàn diện của phiên bản v2 trên cả 2 bộ dữ liệu:
- Bộ dữ liệu cơ bản (Base Suite - 20 trường hợp): `runs/v2_B_base_openrouter_20261110T124549264463.json`
- Bộ dữ liệu mở rộng của nhóm (Group Suite - 10 trường hợp): `runs/v2_B_group_openrouter_20261110T124759890704.json`

---

## 1. Thông tin tổng quan lượt chạy phiên bản v2
- Phiên bản Agent: v2 (Tối ưu phản hồi `response_type='text'`, tích hợp tool mới `currency_converter` và bổ sung bộ test nhóm).
- Nhà cung cấp mô hình (Provider): OpenRouter
- Mô hình sử dụng: openai/gpt-4o-mini
- Thời gian chạy: 2026-11-10 12:45:49 (Base) và 12:47:59 (Group)

---

## 2. Bảng tổng hợp các chỉ số cốt lõi qua các phiên bản

| Chỉ số đo đạc | Phiên bản v0 (Baseline) | Phiên bản v1 (Base) | Phiên bản v2 (Base) | Phiên bản v2 (Group) |
| :--- | :--- | :--- | :--- | :--- |
| Bộ dữ liệu kiểm thử | data/eval_base.json | data/eval_base.json | data/eval_base.json | data/eval_group.json |
| Tổng số test case | 20 cases | 20 cases | 20 cases | 10 cases |
| Số case đo được | 12 cases | 20 cases | 20 cases | 10 cases |
| Số case đạt yêu cầu (PASS) | 7 / 12 cases | 18 / 20 cases | 19 / 20 cases | 9 / 10 cases |
| Tỷ lệ thành công (Case Accuracy) | 58.33% | 90.00% | 95.00% (19 / 20) | 90.00% (9 / 10) |
| Độ chính xác chọn công cụ (Tool Routing) | 66.67% | 100.00% | 95.00% (19 / 20) | 90.00% (9 / 10) |
| Độ chính xác truyền tham số (Argument) | 58.33% | 90.00% | 95.00% (19 / 20) | 90.00% (9 / 10) |
| Độ chính xác đa lượt (Multiturn) | 100.0% (1/1) | 100.00% (6/6) | 83.33% (5 / 6) | 100.00% (5 / 5) |

---

## 3. Bảng chi tiết kết quả bộ dữ liệu cơ bản (eval_base.json - 20 cases)

| Mã Case | Yêu cầu của người dùng | Công cụ kỳ vọng | Công cụ thực tế gọi | Kết quả | Phân loại lỗi | Chi tiết kiểm tra |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R01_user_tweets_routing | Tweet mới nhất của Sam Altman là gì? | timeline | timeline | PASS | Không | Đúng công cụ và tham số |
| R02_search_tweets_routing | Mọi người đang bàn gì về GPT-5 trên Twitter? | social_search | social_search | PASS | Không | Đúng công cụ và tham số |
| R03_web_news_routing | Tin tức AI hôm nay có gì nổi bật? | lookup | lookup | PASS | Không | Đúng thực thể gọn gàng |
| R04_read_url_routing | Tóm tắt bài này giúp mình: https://openai.com/blog | fetch | fetch | PASS | Không | Đúng công cụ đọc URL |
| R05_limit_arg | Lấy 10 tweet mới nhất của Elon Musk | timeline | timeline | PASS | Không | Đúng tham số limit=10 |
| R06_timeframe_arg | Tin công nghệ trong tuần này | lookup | lookup | PASS | Không | Đúng tham số timeframe='week' |
| R07_search_type_arg | Cho mình các tweet phổ biến (top) nhất về OpenAI | social_search | social_search | PASS | Không | Đúng tham số search_type='Top' |
| R08_out_of_scope | Giải giúp mình bài toán tích phân: nguyên hàm của x^2 | Không gọi tool | Không gọi tool | PASS | Không | Đúng chuẩn không gọi công cụ |
| R09_no_tool_capability | Bạn là gì và làm được những gì? | Không gọi tool | Không gọi tool | PASS | Không | Đúng chuẩn không gọi công cụ |
| R10_missing_handle | Tóm tắt 5 tweet mới nhất giúp mình | clarify | clarify | PASS | Không | Đã khắc phục lỗi v1: truyền đúng response_type='text' |
| R11_missing_url | Tóm tắt bài viết này hộ mình | clarify | clarify | PASS | Không | Đã khắc phục lỗi v1: truyền đúng response_type='text' |
| R12_confirm_before_send | Đăng bản tin này lên Telegram giúp mình | clarify | clarify | PASS | Không | Giữ vững cơ chế bảo vệ Guardrail |
| R13_parallel_web_and_tweets | Tìm trên web tin AI hôm nay và tìm thêm tweet về AI | lookup, social_search | lookup, social_search | PASS | Không | Gọi chuẩn xác song song cả 2 công cụ |
| R14_out_of_scope_coding | Viết giúp mình một hàm Python tính Fibonacci | Không gọi tool | Không gọi tool | PASS | Không | Trả lời văn bản trực tiếp |
| M01_clarify_then_fill | Đa lượt: Điền tiếp handle @sama | timeline | timeline | PASS | Không | Đa lượt xử lý hoàn hảo |
| M02_carryover_timeframe | Đa lượt: Kế thừa khung thời gian | lookup | lookup | PASS | Không | Kế thừa tham số chính xác |
| M03_correction_handle | Đa lượt: Đổi tên sang Karpathy | timeline | timeline | PASS | Không | Đổi người chính xác |
| M04_clarify_then_url | Đa lượt: Cung cấp link URL bài báo | fetch | fetch | PASS | Không | Đọc đúng link sau khi hỏi |
| M05_correction_limit | Đa lượt: Đổi số lượng bài sang 10 | timeline | timeline | PASS | Không | Sửa tham số limit chính xác |
| M06_switch_tool | Đa lượt: Bỏ Twitter, chuyển sang tìm trên web | lookup | social_search, lookup | FAIL | wrong_tool | Người dùng bảo bỏ Twitter nhưng Agent gọi thừa cả social_search |

---

## 4. Bảng chi tiết kết quả bộ dữ liệu nhóm (eval_group.json - 10 cases)

| Mã Case | Yêu cầu của người dùng | Công cụ kỳ vọng | Công cụ thực tế gọi | Kết quả | Phân loại lỗi | Chi tiết kiểm tra |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| G01_currency_usd_to_vnd | Đổi 50 USD sang tiền Việt Nam (VND) giúp mình | currency_converter | currency_converter | PASS | Không | Tool mới hoạt động chính xác |
| G02_currency_eur_to_jpy | Quy đổi 100 EUR sang JPY | currency_converter | currency_converter | PASS | Không | Tool mới quy đổi EUR->JPY đúng |
| G03_papers_search_transformer | Tìm 3 bài báo khoa học mới nhất về mô hình Transformer | papers | papers | PASS | Không | Gọi chính xác tool papers trên arXiv |
| G04_policy_data_privacy | Chính sách nội bộ công ty về bảo mật dữ liệu khách hàng | policy | policy | PASS | Không | Tra cứu chính sách nội bộ chính xác |
| G05_out_of_scope_weather | Thời tiết hôm nay ở Hà Nội có mưa không? | Không gọi tool | lookup | FAIL | out_of_scope | Nhầm lẫn thời tiết với nghiên cứu công nghệ nên tự ý gọi lookup |
| G06_multiturn_currency_change_amount | Đa lượt: Đổi 100 USD -> sửa thành 200 USD | currency_converter | currency_converter | PASS | Không | Cập nhật số tiền quy đổi chính xác |
| G07_multiturn_currency_change_target | Đa lượt: Đổi USD sang EUR -> đổi ý sang JPY | currency_converter | currency_converter | PASS | Không | Đổi mã tiền tệ đích mượt mà |
| G08_multiturn_clarify_then_currency | Đa lượt: Hỏi đổi 1000 USD -> bổ sung sang VND | currency_converter | currency_converter | PASS | Không | Hỏi và hoàn tất quy đổi chính xác |
| G09_multiturn_search_then_fetch | Đa lượt: Tìm bài viết -> đổi sang đọc link cụ thể | fetch | fetch | PASS | Không | Chuyển đổi công cụ đa lượt chính xác |
| G10_multiturn_confirm_send_telegram | Đa lượt: Gửi tin -> xác nhận đồng ý gửi | send | send | PASS | Không | Chỉ gửi khi có xác nhận rõ ràng |

---

## 5. Đánh giá thành tựu của phiên bản v2
1. **Khắc phục triệt để lỗi của v1 (R10 và R11)**:
   - Cả 2 ca thiếu thông tin `R10_missing_handle` và `R11_missing_url` đều đã đạt **PASS tuyệt đối** nhờ việc bổ sung chỉ dẫn truyền `response_type="text"`.
   - Độ chính xác bộ đề cơ bản nâng từ **90% lên 95%**.
2. **Công cụ mới currency_converter hoạt động xuất sắc 100%**:
   - Toàn bộ các trường hợp kiểm thử liên quan đến công cụ mới do nhóm tự phát triển (`G01`, `G02`, `G06`, `G07`, `G08`) đều đạt kết quả PASS hoàn hảo ở cả đơn lượt và đa lượt.

---

## 6. Kế hoạch và các điểm cần cải thiện cho phiên bản v3 (Mục tiêu 100% cả 2 bộ đề)

Chỉ có đúng **2 test case thất bại** trong tổng số 30 test case của cả 2 bộ đề (tổng thể đạt 28/30 = 93.33%). Để đạt điểm số 100% ở phiên bản v3, chúng ta cần cải thiện 2 điểm sau trong `system_prompt.md`:

### 1. Khắc phục lỗi gọi thừa công cụ khi chuyển đổi chủ đề (Case M06)
- **Hiện tượng**: Người dùng nói: *"Bỏ Twitter, chuyển sang tìm trên web tin tức đi"*. Agent gọi cả `social_search` (Twitter) lẫn `lookup` (Web).
- **Giải pháp cho v3**: Bổ sung quy tắc vào `system_prompt.md`:
  *"Trong hội thoại đa lượt, nếu người dùng yêu cầu chuyển đổi nguồn (ví dụ: 'Bỏ Twitter, chuyển sang web' hoặc ngược lại), bắt buộc phải hủy bỏ công cụ cũ của lượt trước và chỉ gọi duy nhất công cụ mới được yêu cầu."*

### 2. Khắc phục lỗi câu hỏi đời sống ngoài phạm vi nghiên cứu (Case G05)
- **Hiện tượng**: Người dùng hỏi *"Thời tiết hôm nay ở Hà Nội có mưa không?"*, Agent tự ý gọi `lookup` để tra cứu trên web.
- **Giải pháp cho v3**: Bổ sung quy tắc vào mục Out of Scope trong `system_prompt.md`:
  *"Các câu hỏi đời sống thông thường như thời tiết, xem bói, công thức nấu ăn, thể thao giải trí là ngoài phạm vi của Research Agent. Không được gọi bất kỳ công cụ tra cứu nào, hãy lịch sự từ chối hoặc trả lời trực tiếp bằng văn bản."*

Chỉ cần điều chỉnh 2 quy tắc ngắn gọn này, phiên bản v3 sẽ sẵn sàng đạt điểm số tối đa 100% trên toàn bộ các bộ câu hỏi để phục vụ phần thi Showdown và nộp bài cuối cùng.

