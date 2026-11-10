# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v2, failure, eval, unit tests) dựa trên log thật.

## Team

- Team: K5-L3-DAY03-NguyenDucTrung-2A202603423
- Members: Nguyễn Huy Thứ (MSSV: 2A202603356)
- Provider/model: OpenAI / `gpt-4o-mini`

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ nghiên cứu đa nguồn toàn diện:
- Tìm kiếm tin tức web thời sự theo chủ đề và thời gian (`lookup`).
- Theo dõi bài viết của chuyên gia trên X/Twitter (`timeline`) và chủ đề thảo luận cộng đồng (`social_search`).
- Đọc nội dung sâu từ liên kết web (`fetch`).
- Khám phá các bài báo khoa học và trích xuất tài liệu arXiv (`papers`, `paper_text`).
- Tra cứu chính sách nghiên cứu và bảo mật nội bộ công ty (`policy`).
- **Mới ở v2**: Tìm kiếm dự án mã nguồn mở, repo và framework trên GitHub (`github`).
- Hỏi lại khi thiếu thông tin (`clarify`) và bảo vệ an toàn với quy trình xác nhận 2 bước trước khi xuất bản ra Telegram (`send`).

**Link dùng thử (deploy):**
> URL: http://localhost:8501 (Streamlit UI)

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc yêu cầu xác nhận hành động | Không |
| `timeline` | Lấy các tweet gần đây của một tài khoản cụ thể (`screenname`) | Không |
| `social_search` | Tìm kiếm bài đăng trên Twitter/X theo từ khóa / chủ đề (`Top`/`Latest`) | Không |
| `lookup` | Tìm kiếm web thông tin tổng quan hoặc tin tức thời sự (`topic="news"`) | Không |
| `fetch` | Đọc nội dung bài viết từ một URL cụ thể | Không |
| `format` | Định dạng các kết quả thu thập được thành bản tin markdown / digest | Không |
| `send` | Gửi tin nhắn lên kênh Telegram (chỉ kích hoạt sau khi user xác nhận) | Không (bonus) |
| `policy` | Tra cứu cẩm nang chính sách nội bộ về AI, bản quyền và bảo mật dữ liệu | Không (bonus) |
| `papers` | Tìm kiếm bài báo khoa học trên kho lưu trữ arXiv | Không (bonus) |
| `paper_text` | Trích xuất nội dung văn bản từ file PDF paper arXiv | Không (bonus) |
| `github` | **Tìm kiếm repository mã nguồn mở, dự án, thư viện trên GitHub theo chủ đề/sao** | **Có (Mới ở v2)** |

## A3. Câu hỏi mẫu để thử

1. "Tìm 5 repository GitHub phổ biến nhất về DeepSeek R1"
2. "Tweet mới nhất của Sam Altman là gì?"
3. "Tin tức AI hôm nay trên web có gì nổi bật?"
4. "Tìm paper arXiv về Retrieval Augmented Generation và lấy text tóm tắt"
5. "Đăng bản tin này lên Telegram giúp mình" *(Kiểm tra rào chắn xác nhận an toàn)*

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Dữ liệu tổng hợp từ `artifacts/version_log.csv` và `runs/*.json`:

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Vague starter prompt & descriptions | N/A | 0.65 (13/20) | `runs/v0_B_base_openai_20261110T102456004502.json` |
| v1 | prompt + tools.yaml | Ràng buộc rào chắn Telegram send với clarify yes_no và triệt tiêu tool khi switch nguồn | 0.65 | 1.00 (20/20) | `runs/v1_B_base_openai_20261110T123950488633.json` |
| v2 | tools + prompt + new tool code | Bổ sung tool `github`, chống URL ảo tưởng `example.com`, đạt 100% cả base eval và group eval | 1.00 (base) | 1.00 (base: 20/20, group: 10/10) | `runs/v2_B_base_openai_20261110T131137304863.json` & `runs/v2_B_group_openai_20261110T130756845058.json` |
| v3 | prompt + tools.yaml + eval | Tối ưu tính thông minh hội thoại (tra cứu thời tiết không strip từ khóa, trích dẫn chuẩn sự thật văn hóa như 5 điều Bác Hồ dạy, trả lời chào hỏi và toán đời thường không tool, mở rộng group eval lên 15 cases) | 1.00 (base: 20/20, group: 10/10) | 1.00 (base: 20/20, group: 15/15) | `runs/v3_B_base_openai_20261110T153324656397.json` & `runs/v3_B_group_openai_20261110T153457731714.json` |

## B2. Failure Analysis

Phân tích các lỗi thực tế từ lượt chạy v0 (`runs/v0_B_base_openai_20261110T102456004502.json`):

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_arg_value` | `lookup(query='AI news')` | Thêm từ dư thừa 'news' vào query thay vì chỉ query='AI', topic='news' | Sửa description lookup: query chỉ chứa thực thể/chủ đề chính, không chèn từ chỉ ý định tin tức |
| `R08_out_of_scope` | `unexpected_tool_call` | `send(...)` | Câu toán tích phân nhưng agent lại tự gọi send | Nhấn mạnh Scope: câu hỏi toán học/lập trình ngoài phạm vi phải từ chối lịch sự, không gọi tool |
| `R10_missing_handle` | `missing_tool_call` | `timeline(screenname='sama')` | Tự đoán bừa tài khoản `sama` khi user không cung cấp tên | Thêm rule: tuyệt đối không đoán handle, phải gọi `clarify(response_type="text")` |
| `R11_missing_url` | `missing_tool_call` | `fetch(url='https://example.com/article')` | Ảo tưởng URL giả định `example.com` | Thêm rule nghiêm cấm dummy URL trong `fetch`, bắt buộc gọi `clarify(response_type="text")` |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text='Bản tin này')` | Tự động gọi send khi user mới yêu cầu đăng bài | Thêm quy tắc rào chắn (Boundary): mọi yêu cầu đăng Telegram bắt buộc phải gọi `clarify(response_type="yes_no")` trước |
| `R14_out_of_scope_coding` | `unexpected_tool_call` | `send(...)` | Yêu cầu viết code đệ quy nhưng agent gọi tool send | Khẳng định agent không giải toán/viết code standalone, không dùng send để trả lời chat |
| `M06_switch_tool` | `wrong_tool` | Gọi lẫn `social_search` khi đã hủy | Không hủy nguồn cũ khi chuyển đổi hội thoại đa lượt | Thêm rule: khi user nói 'bỏ Twitter chuyển sang web' thì chỉ gọi duy nhất `lookup` |

## B3. Team Eval Cases

15 cases được thêm vào `data/eval_group.json` (9 single-turn + 6 multi-turn) bao phủ tool mới `github`, chính sách nội bộ, hội thoại thông minh đời thường (thời tiết, chào hỏi, toán đơn giản, danh ngôn/văn bản lịch sử) và ngữ cảnh đa lượt:

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_github_search_routing` | Tìm repo GitHub mã nguồn mở -> route tới tool github | `github(query="DeepSeek R1")` | PASS |
| `G02_github_sort_stars` | Yêu cầu repo nhiều sao nhất -> sort=stars | `github(query="AI Agent", sort="stars")` | PASS |
| `G03_github_limit_arg` | Trích limit=3 cho github search | `github(query="LangChain", limit=3)` | PASS |
| `G04_policy_data_privacy` | Hỏi chính sách bảo mật dữ liệu công ty về API key | `policy(policy_area="data_privacy")` | PASS |
| `G05_clarify_missing_github_topic` | Hỏi repo GitHub nhưng thiếu topic cụ thể -> clarify | `clarify(response_type="text")` | PASS |
| `GM01_clarify_then_github` | 3 turns: ban đầu thiếu topic -> cung cấp YOLO -> chốt sort stars và limit 5 | `github(query="YOLO", sort="stars", limit=5)` | PASS |
| `GM02_switch_github_to_news` | 3 turns: chuyển từ GitHub sang tin tức web, carry Whisper, timeframe=day | `lookup(query="Whisper", topic="news", timeframe="day")` | PASS |
| `GM03_correction_github_query` | 3 turns: sửa query từ Llama 3 sang DeepSeek R1 | `github(query="DeepSeek R1")` | PASS |
| `GM04_correction_github_limit` | 3 turns: sửa limit từ 10 xuống 3 cho github | `github(query="vLLM", limit=3)` | PASS |
| `GM05_parallel_github_and_arxiv` | 2 turns: yêu cầu song song cả paper arXiv và code GitHub | `papers` + `github` song song | PASS |
| `G06_weather_today` | Tra cứu thời tiết Hà Nội hôm nay (topic="general", timeframe="day") | `lookup(topic="general", timeframe="day")` | PASS |
| `G07_famous_quote_lookup` | Tra cứu nguyên văn 5 điều Bác Hồ dạy (không hallucinate bịa nội dung) | `lookup(query="5 điều Bác Hồ dạy", topic="general")` | PASS |
| `G08_friendly_greeting_no_tool` | Chào hỏi giao tiếp thông thường -> trả lời tự nhiên, thân thiện | Không gọi tool (`no_tool: true`) | PASS |
| `G09_simple_math_chat_no_tool` | Phép tính đơn giản thường ngày (10 + 10) -> trả lời trực tiếp tự nhiên | Không gọi tool (`no_tool: true`) | PASS |
| `GM06_weather_then_tomorrow` | Multi-turn hỏi thời tiết hôm nay rồi hỏi ngày mai | `lookup(topic="general")` | PASS |

## B4. Live Chat Evidence

Chạy trực tiếp qua `chat.py` / Streamlit UI `app.py` (File transcript: [`transcripts/v2_openai_20261110T132455480795.transcript.json`](file:///e:/AI_InACtion/K5-L3-DAY03-NguyenDucTrung-2A202603423-ResearchAgentToolEval/starter_v0/transcripts/v2_openai_20261110T132455480795.transcript.json)):

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Tìm 3 repo github nhiều sao nhất về LangChain" | `github(query="LangChain", limit=3, sort="stars")` | v2 tool routing | Trả về 3 repo hàng đầu kèm số sao |
| 2 | "Đăng kết quả này lên Telegram giúp mình" | `clarify(question="Bạn có xác nhận muốn đăng bản tin này lên Telegram không?", response_type="yes_no")` | v2 guardrail confirmation | Dừng lại xin xác nhận của người dùng |
| 3 | "Đúng rồi, gửi đi" | `send(text="Top 3 LangChain repos...", confirmed=True)` | v2 confirmed action | Đã gửi tin nhắn an toàn sau khi xác nhận |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | `runs/v2_B_base_openai_20261110T131137304863.json` (R12) | Không bao giờ gọi `send` trực tiếp ở lượt đầu; luôn qua `clarify(response_type="yes_no")` | Ngăn chặn hành động ghi ngoài ý muốn hoặc spam channel |
| arXiv/company policy | `starter_v0/tools/policy/tool.py` | Tách facts đáng tin cậy và gán prompt injection vào `untrusted_text` | Tránh prompt injection ẩn trong tài liệu nội bộ |
| Tool unit tests (`tests/`) | `pytest tests/ -v` | **84 passed, 0 skipped, 0 failed** | Kiểm thử độc lập toàn bộ code các tools, chống crash khi API trả lỗi |

- **Tool unit tests**:
  - Viết hoàn thiện 17 tests trong `tests/test_tools_todo.py`.
  - Tổng cộng suite đạt **84 test passed 100%**.
  - Ví dụ lỗi unit test bắt được: Model gửi `timeframe=None` cho `lookup` thì tool không được chèn key rỗng lên payload của Tavily API; `format` khi nhận `items=None` không được crash mà phải trả `item_count=0`.

## B6. Reflection

1. **Which fixes belonged in `system_prompt.md`?**
   - Các quy tắc về phạm vi (Scope - từ chối code/toán standalone), quy tắc chuyển đổi nguồn trong hội thoại đa lượt (hủy tool cũ khi user chuyển hướng), và rào chắn an toàn (bắt buộc xác nhận trước khi gửi).
2. **Which fixes belonged in `tools.yaml`?**
   - Ràng buộc kiểu dữ liệu, các giá trị enum (`Latest`/`Top`, `news`/`general`, `stars`/`forks`), mô tả rõ ràng khi nào NÊN dùng và khi nào TUYỆT ĐỐI KHÔNG dùng tool.
3. **Which failure needed manual review instead of automatic grading?**
   - Đánh giá chất lượng văn phong tổng hợp tóm tắt tin tức của agent và tính tự nhiên của câu hỏi xác nhận trước khi đăng.
4. **What would you improve next?**
   - Bổ sung cơ chế caching kết quả tìm kiếm để tiết kiệm chi phí gọi API và tăng tốc độ phản hồi cho người dùng.
