# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật.

## Team

- Team: K5-L3-DAY03-NguyenDucTrung-2A202603423
- Members: Nguyen Duc Trung (MSSV: 2A202603423)
- Provider/model: OpenRouter (openai/gpt-4o-mini) / Google Gemini (gemini-3.6-flash)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ tự động hóa tra cứu đa nguồn: tìm kiếm tin tức trên web, phân tích bài đăng Twitter/X, đọc nội dung URL bài báo, tìm bài nghiên cứu khoa học arXiv, kiểm tra quy chế nội bộ công ty, quy đổi giá trị ngoại tệ chính xác và gửi báo cáo lên Telegram có cơ chế bảo vệ xác nhận (Guardrail).

**Link dùng thử (deploy):**

- Localhost URL: http://localhost:8501 (Streamlit app)
- Cloudflare Tunnel URL: https://trycloudflare.com (chạy qua lệnh `cloudflared tunnel --url http://localhost:8501`)

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin đầu vào hoặc xin xác nhận trước khi gửi | Không |
| timeline | Lấy các bài đăng gần đây của một tài khoản Twitter | Không |
| social_search | Tìm kiếm bài viết theo từ khóa trên mạng xã hội Twitter | Không |
| lookup | Tra cứu tin tức và bài viết trên internet theo chủ đề và khung thời gian | Không |
| fetch | Đọc trích xuất toàn văn nội dung một liên kết URL | Không |
| format | Định dạng và tổng hợp danh sách tin tức thành bản tin markdown | Không |
| send | Gửi văn bản lên Telegram channel (chỉ kích hoạt khi có cờ xác nhận) | Không |
| policy | Tra cứu quy định nội bộ công ty (phân vùng bảo mật, bản quyền, trích dẫn) | Không |
| papers | Tìm kiếm bài báo khoa học trên kho lưu trữ arXiv | Không |
| paper_text | Tải và trích xuất nội dung văn bản của bài báo arXiv | Không |
| currency_converter | Quy đổi tỷ giá chính xác giữa các loại tiền tệ (USD, EUR, VND, JPY, GBP) | Có (Nhóm tự phát triển) |

## A3. Câu hỏi mẫu để thử

1. "Đổi 50 USD sang tiền Việt Nam (VND) giúp mình" (Thử nghiệm công cụ mới currency_converter).
2. "Tin tức AI hôm nay có gì nổi bật trên web?" (Thử nghiệm công cụ tra cứu lookup).
3. "Tìm 3 bài báo khoa học mới nhất về mô hình Transformer trên arXiv" (Thử nghiệm công cụ papers).
4. "Đăng bản tin này lên kênh Telegram giúp mình" (Thử nghiệm cơ chế an toàn Guardrail, Agent sẽ gọi clarify để xin xác nhận).
5. "Thời tiết hôm nay ở Hà Nội có mưa không?" (Thử nghiệm nhận diện câu hỏi ngoài phạm vi, Agent không gọi tool bừa bãi).

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo lường hành vi ban đầu khi chưa tinh chỉnh prompt |  | 0.5833 | runs/v0_B_base_gemini_20261110T102604874011.json |
| v1 | system_prompt.md | Xóa bỏ anti-pattern xúi giục đoán bừa, bổ sung quy tắc clarify và guardrail send | 0.5833 | 0.9000 | runs/v1_B_base_openrouter_20261110T120623880369.json |
| v2 | system_prompt.md & eval_group.json | Ép tham số response_type='text' cho clarify và tích hợp tool currency_converter | 0.9000 | 0.9500 | runs/v2_B_base_openrouter_20261110T124549264463.json |
| v3 | system_prompt.md | Bổ sung quy tắc hủy bỏ tool cũ khi chuyển nguồn đa lượt và mở rộng phạm vi out-of-scope | 0.9500 | 1.0000 | runs/v3_B_base_openrouter_20261110T140348077370.json |

*Ghi chú: Trên bộ dữ liệu riêng của nhóm (`data/eval_group.json`), phiên bản v3 cũng đạt tỷ lệ hoàn hảo 1.0000 (10 / 10 cases PASS) tại file `runs/v3_B_group_openrouter_20261110T135943661062.json`.*

## B2. Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | wrong_tool | lookup | Tham số query bị nhồi nhét cả từ khóa 'news today' | Tách bạch query chỉ chứa thực thể, chuyển 'news' sang topic và 'day' sang timeframe |
| R08_out_of_scope | out_of_scope | send | Câu hỏi toán tích phân nhưng Agent tự ý gọi tool send | Bổ sung quy tắc Out-of-Scope: toán học, chào hỏi thì trả lời văn bản, không gọi tool |
| R10_missing_handle | missing_info | timeline (v0) / clarify (v1) | v0 tự bịa tài khoản; v1 gọi clarify nhưng thiếu response_type | v1 yêu cầu gọi clarify; v2 ép tham số response_type='text' |
| R12_confirm_before_send | wrong_boundary | send | v0 tự ý gửi tin Telegram khi chưa có người dùng xác nhận | Bổ sung Guardrail: chỉ gọi send khi confirmed=true, chưa xác nhận phải gọi clarify |
| M06_switch_tool | wrong_tool | social_search, lookup | Đa lượt yêu cầu bỏ Twitter nhưng Agent gọi cả 2 công cụ | Bổ sung quy tắc đa lượt: khi chuyển nguồn phải hủy công cụ cũ và chỉ gọi công cụ mới |
| G05_out_of_scope_weather | out_of_scope | lookup | Hỏi thời tiết nhưng Agent tự ý gọi lookup tìm kiếm web | Mở rộng quy tắc Out-of-Scope gồm cả câu hỏi thời tiết và đời sống thông thường |

## B3. Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_currency_usd_to_vnd | Đổi 50 USD sang VND đơn lượt | currency_converter(amount=50, from_currency='USD', to_currency='VND') | PASS |
| G02_currency_eur_to_jpy | Đổi 100 EUR sang JPY đơn lượt | currency_converter(amount=100, from_currency='EUR', to_currency='JPY') | PASS |
| G03_papers_search_transformer | Tìm bài báo arXiv về Transformer | papers(query='Transformer', max_results=3) | PASS |
| G04_policy_data_privacy | Tra cứu chính sách bảo mật dữ liệu | policy(query='bảo mật dữ liệu khách hàng', policy_area='data_privacy') | PASS |
| G05_out_of_scope_weather | Hỏi thời tiết ngoài phạm vi nghiên cứu | no_tool=true | PASS |
| G06_multiturn_currency_change_amount | Đa lượt sửa số tiền 100 thành 200 USD | currency_converter(amount=200, from_currency='USD', to_currency='VND') | PASS |
| G07_multiturn_currency_change_target | Đa lượt đổi đích sang JPY | currency_converter(amount=500, from_currency='USD', to_currency='JPY') | PASS |
| G08_multiturn_clarify_then_currency | Đa lượt bổ sung đồng tiền VND | currency_converter(amount=1000, from_currency='USD', to_currency='VND') | PASS |
| G09_multiturn_search_then_fetch | Đa lượt đổi sang đọc liên kết URL | fetch(url='https://vinai.io/research-agent') | PASS |
| G10_multiturn_confirm_send_telegram | Đa lượt xác nhận đồng ý gửi tin | send(confirmed=true) | PASS |

## B4. Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Quy đổi 100 USD sang VND | currency_converter(amount=100, from_currency='USD', to_currency='VND') | v3 | Trả về 2,545,000 VND kèm tỷ giá 25450.0 |
| 2 | Đăng thông tin này lên Telegram giúp mình | clarify(question='...', response_type='text') | v3 | Hỏi xin xác nhận người dùng trước khi gửi |
| 3 | Tôi xác nhận đồng ý gửi | send(text='...', confirmed=true) | v3 | Gửi bản tin thành công sau khi có xác nhận |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | starter_v0/tools/send/tool.py | Chặn đứng việc gửi tin trái phép nếu confirmed=false | Rủi ro spam thông tin ra ngoài; đã xử lý triệt để bằng Guardrail |
| UI (Streamlit) | starter_v0/app.py | Giao diện web trực quan, cho phép chọn model và xem nhật ký gọi tool | Người dùng không chuyên vẫn tương tác và quan sát được tool calls |
| Tool unit tests (`tests/`) | starter_v0/tests/test_tools_todo.py | Viết 3 unit tests cho tool mới, kiểm tra biên và regex | Bắt lỗi dữ liệu đầu vào xấu trước khi đến tay mô hình ngôn ngữ |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**: Các quy tắc định tuyến công cụ (khi nào dùng tool gì), quy tắc an toàn Guardrail trước khi gửi tin, và quy tắc xử lý đa lượt khi người dùng thay đổi ý định.
- **Which fixes belonged in `tools.yaml`?**: Mô tả chi tiết kiểu dữ liệu, ràng buộc bắt buộc (required parameters) và các giá trị enum của công cụ để mô hình sinh JSON chuẩn xác.
- **Which failure needed manual review instead of automatic grading?**: Các câu hỏi mở cần câu trả lời chi tiết và câu hỏi làm rõ của `clarify` (cần đánh giá xem câu hỏi hỏi lại người dùng có tự nhiên và đúng trọng tâm hay không).
- **What would you improve next?**: Tích hợp thêm các API tỷ giá tiền tệ trực tiếp theo thời gian thực và mở rộng bộ công cụ tóm tắt tài liệu PDF chuyên sâu.
