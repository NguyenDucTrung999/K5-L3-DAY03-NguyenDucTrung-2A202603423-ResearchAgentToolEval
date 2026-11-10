"""TODO(student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    clarify_tool = TOOL_FUNCTIONS["clarify"]
    result = clarify_tool(question="Choose one?", response_type="choice", options=["Option A", "Option B"])
    assert result["options"] == ["Option A", "Option B"]
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Item 1", "section": "A"},
        {"title": "Item 2", "section": "B"},
        {"title": "Item 3", "section": "A"},
    ]
    result = format_tool(items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [{"title": "Post 1"}, {"title": "Post 2"}]
    result = format_tool(items=items, template="thread")
    assert result["markdown"].startswith("1/ ")
    assert "\n\n2/ " in result["markdown"]


def test_format_empty_items_does_not_crash() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    res1 = format_tool(items=None)
    assert res1["item_count"] == 0
    res2 = format_tool(items=[])
    assert res2["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    send_tool = TOOL_FUNCTIONS["send"]
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-10012345")
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Test message", confirmed=True)
    assert len(calls) == 1
    assert "123:ABC" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-10012345"
    assert calls[0]["json"]["text"] == "Test message"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    send_tool = TOOL_FUNCTIONS["send"]
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Test", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    lookup_tool = TOOL_FUNCTIONS["lookup"]
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    lookup_tool(query="test", timeframe=None)
    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    fake_http(FakeResponse({
        "data": {
            "markdown": "Page content",
            "metadata": {"title": "Title Page", "sourceURL": "https://example.com/source"},
        }
    }))
    result = fetch_tool(url="https://example.com/test")
    item = result["items"][0]
    assert item["title"] == "Title Page"
    assert item["url"] == "https://example.com/source"
    assert item["source"] == "example.com"
    assert item["summary"] == "Page content"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    fake_http(FakeResponse({"data": {"markdown": "a" * 5000, "metadata": {}}}))
    result = fetch_tool(url="https://example.com")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    timeline_tool = TOOL_FUNCTIONS["timeline"]
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    fake_http(FakeResponse({"timeline": [
        {"text": "no id"},
        {"tweet_id": "1", "screen_name": "user1", "text": "t1"},
        {"tweet_id": "2", "screen_name": "user1", "text": "t2"},
        {"tweet_id": "3", "screen_name": "user1", "text": "t3"},
        {"tweet_id": "4", "screen_name": "user1", "text": "t4"},
    ]}))
    result = timeline_tool(screenname="user1", limit=3)
    assert len(result["items"]) == 3
    for item in result["items"]:
        assert item["url"].startswith("https://x.com/user1/status/")


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    social_tool = TOOL_FUNCTIONS["social_search"]
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    social_tool(query="OpenAI", search_type="Top")
    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "OpenAI"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="data", policy_area="data_privacy")
    assert len(result["results"]) > 0
    for item in result["results"]:
        assert item["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="injection", policy_area="source_citation")
    has_untrusted = any(len(item.get("untrusted_text", [])) > 0 for item in result["results"])
    assert has_untrusted


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_my_new_tool_happy_path(monkeypatch, fake_http) -> None:
    github_tool = TOOL_FUNCTIONS["github"]
    calls = fake_http(FakeResponse({
        "total_count": 1,
        "items": [
            {
                "name": "deepseek-r1",
                "full_name": "deepseek-ai/deepseek-r1",
                "html_url": "https://github.com/deepseek-ai/deepseek-r1",
                "description": "DeepSeek R1 model repo",
                "stargazers_count": 50000,
                "forks_count": 4000,
                "language": "Python",
            }
        ]
    }))
    result = github_tool(query="DeepSeek R1", sort="stars", limit=3)
    assert calls[0]["url"] == "https://api.github.com/search/repositories"
    assert calls[0]["params"]["q"] == "DeepSeek R1"
    assert calls[0]["params"]["sort"] == "stars"
    assert calls[0]["params"]["per_page"] == 3
    assert result["total_count"] == 1
    assert result["items"][0]["name"] == "deepseek-r1"
    assert result["items"][0]["stars"] == 50000
    assert result["items"][0]["url"] == "https://github.com/deepseek-ai/deepseek-r1"


def test_my_new_tool_bad_input_from_model() -> None:
    github_tool = TOOL_FUNCTIONS["github"]
    res_empty = github_tool(query="   ")
    assert res_empty["items"] == []
    assert res_empty["total_count"] == 0


def test_my_new_tool_failure_returns_error_dict(fake_http) -> None:
    github_tool = TOOL_FUNCTIONS["github"]
    fake_http(FakeResponse(status_code=403))
    result = github_tool(query="test")
    assert result["error"] == "HTTPError"
