| Tiêu chí đánh giá | Prompt Gốc | Bản Nâng Cấp |
| :--- | :--- | :--- |
| **Câu hỏi Toán / Code / Chào hỏi** | Cố ép gọi đại 1 công cụ (Lỗi Over-triggering) | Trả lời trực tiếp bằng văn bản, không gọi tool |
| **Thiếu `screenname` hoặc `url`** | Tự bịa tài khoản (Sam Altman) hoặc tự đoán mò URL | Chặn đoán mò, gọi `clarify` để lấy thông tin đúng |
| **Lệnh gửi tin / đăng bài (`send`)** | Gửi ngay lập tức, rủi ro gửi nhầm không thể thu hồi | Bắt buộc kiểm tra `confirmed=true`, thiếu thì gọi `clarify` |
| **Cách điền tham số `lookup`** | Dễ nhồi nhét cả câu (`"AI news today"`) vào `query` | Tách sạch thực thể (`query="AI"`, `topic="news"`, `timeframe="day"`) |
| **Hiệu năng thực thi (1 bước)** | Nhanh nhưng tỷ lệ sai số và rủi ro cực cao | Vẫn giữ 1 bước/lượt nhưng chính xác, an toàn và đúng chuẩn Schema |