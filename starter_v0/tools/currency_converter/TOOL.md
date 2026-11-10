---
name: currency_converter
track: extension
kind: pure_function
requires_env: []
inputs: [amount, from_currency, to_currency]
outputs: [amount, from_currency, to_currency, converted_amount, exchange_rate, status, error_message]
side_effect: false
---
# currency_converter

Chuyển đổi giá trị tiền tệ giữa các loại tiền phổ biến (USD, EUR, VND, JPY, GBP) dựa trên tỷ giá tham chiếu.
Sử dụng biểu thức chính quy (regex) để kiểm tra tính hợp lệ của mã tiền tệ đầu vào (phải là 3 chữ cái viết hoa).
Trả về kết quả quy đổi chi tiết kèm theo tỷ giá và thông báo lỗi nếu dữ liệu đầu vào không hợp lệ.

