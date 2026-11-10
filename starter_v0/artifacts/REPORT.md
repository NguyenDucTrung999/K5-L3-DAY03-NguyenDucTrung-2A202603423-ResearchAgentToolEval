# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
>
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: K5-L3-DAY03-NguyenDucTrung-2A202603423
- Members: Phạm Công Dũng (MSSV: 2A202603428)
- Provider/model: OpenRouter (openai/gpt-4o-mini) / Google Gemini (gemini-3.6-flash)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ tìm kiếm tin tức khoa học/công nghệ, tra cứu tỷ giá hối đoái trực tiếp, tóm tắt bài báo và gửi báo cáo tổng hợp qua Telegram khi có xác nhận của người dùng.

**Link dùng thử (deploy):**

- Localhost URL: http://localhost:8501 (Streamlit app)

## A2. Tool agent có

| Tên tool           | Làm được gì                                                                                        | Tool mới nhóm thêm? |
| ------------------ | -------------------------------------------------------------------------------------------------- | ------------------- |
| clarify            | Hỏi lại người dùng khi thiếu thông tin bắt buộc                                                    | không               |
| search_web         | Tìm kiếm thông tin và tin tức trực tuyến theo từ khóa                                              | không               |
| read_url           | Đọc và trích xuất nội dung từ một liên kết trang web                                               | không               |
| currency_converter | Chuyển đổi số tiền giữa các loại tiền tệ (USD, EUR, VND, JPY, GBP) với kiểm tra định dạng chặt chẽ | **có (Người 2)**    |
| send_telegram      | Gửi thông báo digest báo cáo lên kênh Telegram được định sẵn                                       | có                  |

## A3. Câu hỏi mẫu để thử

1. "Quy đổi 150 USD sang VND giúp tôi."
2. "Tìm cho tôi 3 bài báo mới nhất về LLM Agent trong tuần này và tóm tắt."
3. "Đổi 50 EUR sang JPY rồi gửi tóm tắt tỷ giá này qua Telegram cho tôi."

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact                   | Hypothesis                                                | Metric Before | Metric After | Run File                |
| ------- | ---------------------------------- | --------------------------------------------------------- | ------------: | -----------: | ----------------------- |
| v0      | baseline                           | Chạy thử nghiệm ban đầu                                   |         60.0% |        60.0% | `runs/v0_baseline.json` |
| v1      | `tools.yaml`                       | Thêm mô tả tham số chi tiết cho tool `currency_converter` |         60.0% |        80.0% | `runs/v1_tools.json`    |
| v2      | `system_prompt.md`                 | Bổ sung rule bắt buộc dùng `clarify` khi thiếu mã tiền tệ |         80.0% |        90.0% | `runs/v2_prompt.json`   |
| v3      | `tools/currency_converter/tool.py` | Sửa logic validation regex + bắt lỗi ngoại lệ linh hoạt   |         90.0% |       100.0% | `runs/v3_final.json`    |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type       | Actual Tool Calls                     | What Failed                                              | Fix                                                                                     |
| ------- | ------------------ | ------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| C02     | `wrong_tool`       | `search_web`                          | Gọi web search thay vì `currency_converter` khi đổi tiền | Cập nhật `tools.yaml` mô tả rõ mục đích của `currency_converter`                        |
| C05     | `missing_clarify`  | `currency_converter(amount=100)`      | Trực tiếp gọi tool khi chưa có mã tiền tệ đích           | Thêm ràng buộc vào `system_prompt.md` yêu cầu gọi `clarify` nếu thiếu tham số `to_curr` |
| C08     | `invalid_argument` | `currency_converter(from_curr='usd')` | Mã tiền tệ chữ thường gây lỗi validation                 | Chuẩn hóa `from_curr.upper()` và dùng Regex `^[A-Z]{3}$` trong `tool.py`                |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests                                      | Expected Tool/Behavior                                           | Result |
| ------- | -------------------------------------------------- | ---------------------------------------------------------------- | ------ |
| TC01    | Đổi tiền đơn giản                                  | `currency_converter(amount=100, from_curr='USD', to_curr='VND')` | PASS   |
| TC02    | Thiếu tiền tệ đích (Single turn)                   | `clarify`                                                        | PASS   |
| TC03    | Mã tiền tệ chữ thường                              | `currency_converter(amount=50, from_curr='EUR', to_curr='JPY')`  | PASS   |
| TC04    | Số tiền âm/không hợp lệ                            | Báo lỗi tham số không hợp lệ                                     | PASS   |
| TC05    | Tiền tệ không hỗ trợ                               | Báo lỗi UNSUPPORTED_CURRENCY                                     | PASS   |
| TC06    | Đổi tiền + Gửi Telegram (Multi turn - Turn 1)      | `currency_converter`                                             | PASS   |
| TC07    | Đổi tiền + Gửi Telegram (Multi turn - Turn 2)      | `send_telegram`                                                  | PASS   |
| TC08    | Hỏi tỷ giá thiếu thông tin (Multi turn - Turn 1)   | `clarify`                                                        | PASS   |
| TC09    | Hỏi tỷ giá bổ sung thông tin (Multi turn - Turn 2) | `currency_converter`                                             | PASS   |
| TC10    | Tìm tin tức + Quy đổi kinh phí (Multi turn)        | `search_web` -> `currency_converter`                             | PASS   |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request                      | Tool Calls                                                       | Version Evidence | Outcome                         |
| ---- | --------------------------------- | ---------------------------------------------------------------- | ---------------- | ------------------------------- |
| 1    | "Tôi muốn đổi 200 USD sang VND"   | `currency_converter(amount=200, from_curr="USD", to_curr="VND")` | v3               | Trả về 5,090,000 VND thành công |
| 2    | "Nhiêu đó tiền EUR là bao nhiêu?" | `currency_converter(amount=200, from_curr="USD", to_curr="EUR")` | v3               | Trả về 184 EUR thành công       |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus                      | Evidence File               | What Worked                                 | Risk / Guardrail                                      |
| -------------------------- | --------------------------- | ------------------------------------------- | ----------------------------------------------------- |
| send (Telegram)            | `transcripts/telegram.json` | Gửi báo cáo thành công lên Telegram Channel | Cần user confirm trước khi gửi thực tế                |
| arXiv/company policy       | -                           | -                                           | -                                                     |
| UI                         | `artifacts/poster.html`     | Đã dựng giao diện poster giới thiệu agent   | -                                                     |
| Tool unit tests (`tests/`) | `pytest` output             | Passed 100% (6/6 tests passed)              | Bắt lỗi validation input & regex format trước khi gửi |

**Tool unit tests detailed info:**

- **Số test đã viết:** 4 test cases mới trong `tests/test_tools_todo.py` cho `currency_converter` + 2 contract tests sẵn có trong `tests/test_tool_contract.py`.
- **Số bug tìm được trong tool:** 2 bug (Lỗi ném Exception unhandled khi truyền chữ thường `usd` và lỗi chấp nhận số tiền âm `amount <= 0`).
- **Ví dụ lỗi Unit Test bắt được nhưng Eval không bắt được:** Khi người dùng nhập `amount = -100` hoặc kiểu dữ liệu chuỗi `"100USD"`, Unit test bắt chặn ngay tại lớp kiểm tra kiểu dữ liệu và regex validation của `tool.py`, trong khi Eval dataset chuẩn thường chỉ chứa câu hỏi dạng ngôn ngữ tự nhiên đúng format nên bỏ qua trường hợp biên này.

---

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  Các quy tắc về hành vi hội thoại, chẳng hạn như yêu cầu bắt buộc phải gọi tool `clarify` khi người dùng không cung cấp đủ mã tiền tệ nguồn/đích.
- **Which fixes belonged in `tools.yaml`?**
  Việc mô tả chi tiết schema tham số, quy định rõ enum/định dạng (ví dụ: `ISO 4217 3-letter code`) để LLM truyền đúng tên tham số.
- **Which failure needed manual review instead of automatic grading?**
  Các câu phản hồi đa bước (multi-turn) có tính sáng tạo trong câu từ tổng hợp thông tin tóm tắt kết quả quy đổi tiền tệ.
- **What would you improve next?**
  Tích hợp API tỷ giá hối đoái thời gian thực (Real-time Exchange Rate API) thay cho bảng tỷ giá tĩnh và thêm cơ chế caching để giảm độ trễ.

---
