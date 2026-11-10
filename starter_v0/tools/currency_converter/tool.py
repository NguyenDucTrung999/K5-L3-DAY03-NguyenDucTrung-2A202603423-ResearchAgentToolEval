from __future__ import annotations

import re
from typing import Any


EXCHANGE_RATES_TO_USD: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "VND": 25450.0,
    "JPY": 155.0,
    "GBP": 0.79,
}

CURRENCY_CODE_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z]{3}$")


def convert_currency(
    amount: float | int = 0.0,
    from_currency: str = "",
    to_currency: str = "",
) -> dict[str, Any]:
    """Chuyen doi gia tri tien te giua cac loai tien te tham chieu."""
    if not isinstance(amount, (int, float)):
        return {
            "tool": "currency_converter",
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": 0.0,
            "exchange_rate": 0.0,
            "status": "error",
            "error_message": "Gia tri so tien (amount) phai la mot so hop le.",
        }
    else:
        if amount < 0:
            return {
                "tool": "currency_converter",
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted_amount": 0.0,
                "exchange_rate": 0.0,
                "status": "error",
                "error_message": "Gia tri so tien (amount) khong duoc am.",
            }
        else:
            normalized_from_currency = str(from_currency).strip().upper()
            normalized_to_currency = str(to_currency).strip().upper()

            is_valid_from_currency = bool(CURRENCY_CODE_PATTERN.match(normalized_from_currency))
            is_valid_to_currency = bool(CURRENCY_CODE_PATTERN.match(normalized_to_currency))

            if not is_valid_from_currency:
                return {
                    "tool": "currency_converter",
                    "amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "converted_amount": 0.0,
                    "exchange_rate": 0.0,
                    "status": "error",
                    "error_message": "Ma tien te nguon (from_currency) khong hop le theo dinh dang 3 chu cai.",
                }
            else:
                if not is_valid_to_currency:
                    return {
                        "tool": "currency_converter",
                        "amount": amount,
                        "from_currency": from_currency,
                        "to_currency": to_currency,
                        "converted_amount": 0.0,
                        "exchange_rate": 0.0,
                        "status": "error",
                        "error_message": "Ma tien te dich (to_currency) khong hop le theo dinh dang 3 chu cai.",
                    }
                else:
                    is_supported_from = normalized_from_currency in EXCHANGE_RATES_TO_USD
                    is_supported_to = normalized_to_currency in EXCHANGE_RATES_TO_USD

                    if not is_supported_from:
                        return {
                            "tool": "currency_converter",
                            "amount": amount,
                            "from_currency": from_currency,
                            "to_currency": to_currency,
                            "converted_amount": 0.0,
                            "exchange_rate": 0.0,
                            "status": "error",
                            "error_message": f"He thong chua ho tro ma tien te nguon: {normalized_from_currency}.",
                        }
                    else:
                        if not is_supported_to:
                            return {
                                "tool": "currency_converter",
                                "amount": amount,
                                "from_currency": from_currency,
                                "to_currency": to_currency,
                                "converted_amount": 0.0,
                                "exchange_rate": 0.0,
                                "status": "error",
                                "error_message": f"He thong chua ho tro ma tien te dich: {normalized_to_currency}.",
                            }
                        else:
                            rate_from_to_usd = EXCHANGE_RATES_TO_USD[normalized_from_currency]
                            rate_to_to_usd = EXCHANGE_RATES_TO_USD[normalized_to_currency]

                            # Chuyen tu dong goc sang USD roi tu USD sang dong dich
                            calculated_exchange_rate = rate_to_to_usd / rate_from_to_usd
                            calculated_converted_amount = round(float(amount) * calculated_exchange_rate, 4)

                            return {
                                "tool": "currency_converter",
                                "amount": float(amount),
                                "from_currency": normalized_from_currency,
                                "to_currency": normalized_to_currency,
                                "converted_amount": calculated_converted_amount,
                                "exchange_rate": round(calculated_exchange_rate, 6),
                                "status": "success",
                                "error_message": None,
                            }

