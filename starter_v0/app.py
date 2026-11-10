from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    assistant_tool_message,
    execute_tool_call,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)


# ---------------- Streamlit App Configuration ----------------
st.set_page_config(
    page_title="Research Agent UI — Step 5 Live Chat",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished interface
st.markdown(
    """
    <style>
    .stChatInput { border-radius: 10px; }
    .tool-badge {
        display: inline-block;
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 2px 8px;
        font-family: monospace;
        font-size: 0.85rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .waiting-badge {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🔬 Research Agent")
    st.caption("Day 03 Lab v3 — Intelligent Research Agent UI")

    st.subheader("⚙️ Configuration")
    provider_name = st.selectbox(
        "Provider",
        options=["openai", "openrouter", "anthropic", "gemini", "ollama"],
        index=0,
    )

    default_models = {
        "openai": "gpt-4o-mini",
        "openrouter": "openai/gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-20241022",
        "gemini": "gemini-2.5-flash",
        "ollama": "qwen2.5:7b",
    }
    model_name = st.text_input(
        "Model",
        value=default_models.get(provider_name, "gpt-4o-mini"),
        help="Specify the model identifier for the provider",
    )

    version_label = st.selectbox("Artifact Version", options=["v3", "v2", "v1", "v0"], index=0)
    history_window = st.slider("Context History Window (turns)", min_value=1, max_value=10, value=5)
    max_tool_rounds = st.slider("Max Tool Rounds", min_value=1, max_value=8, value=4)

    # Load artifacts and verify version
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"

    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)
    artifact_ver = build_artifact_version(version_label, system_prompt_path, tools_path)

    st.info(f"**Loaded Artifact:**\n`{artifact_ver.artifact_version}`")

    st.divider()
    st.subheader("🛠️ Active Tools (11)")
    for tool in tool_declarations:
        with st.expander(f"`{tool['name']}`"):
            st.caption(tool.get("description", ""))

    st.divider()
    if st.button("🗑️ Xóa Lịch Sử Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.transcript = None
        st.session_state.turn_index = 0
        st.rerun()


# ---------------- State Initialization ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "turn_index" not in st.session_state:
    st.session_state.turn_index = 0
if "transcript" not in st.session_state or st.session_state.transcript is None:
    now_stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version_label),
        safe_slug(provider_name),
        now_stamp,
    ])
    transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript_path = transcript_path
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_ver),
        "provider": provider_name,
        "model": model_name,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


# ---------------- Main Chat Header ----------------
st.title("🤖 Trợ Lý Nghiên Cứu Đa Nguồn")
st.markdown(
    "Tra cứu **Tin tức Web**, **X/Twitter**, **ArXiv Papers**, **Chính sách nội bộ**, **GitHub Repositories**, và **Gửi Telegram an toàn**."
)

# Quick sample prompts
st.markdown("**Gợi ý thử nhanh:**")
col1, col2, col3, col4 = st.columns(4)
sample_prompt = None
with col1:
    if st.button("🔍 Tin AI hôm nay", use_container_width=True):
        sample_prompt = "Tin tức AI hôm nay có gì nổi bật?"
with col2:
    if st.button("🐦 Tweet Sam Altman", use_container_width=True):
        sample_prompt = "Tweet mới nhất của Sam Altman là gì?"
with col3:
    if st.button("⭐ Repo DeepSeek R1", use_container_width=True):
        sample_prompt = "Tìm 5 repository GitHub nhiều sao nhất về DeepSeek R1"
with col4:
    if st.button("📢 Gửi Telegram", use_container_width=True):
        sample_prompt = "Đăng bản tin này lên Telegram giúp mình"


# ---------------- Render Existing Messages ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("tool_events"):
            with st.expander(f"🔧 Tool Calls ({len(msg['tool_events'])} tools executed)", expanded=False):
                for event in msg["tool_events"]:
                    st.markdown(f"**Tool:** `{event.get('tool')}`")
                    st.code(json.dumps(event.get("args", {}), indent=2, ensure_ascii=False), language="json")
                    st.markdown("**Result:**")
                    st.code(json.dumps(event.get("result", {}), indent=2, ensure_ascii=False, default=str), language="json")
                    st.divider()

        st.markdown(msg["content"])

        if msg.get("status") == "waiting_for_user":
            st.markdown(
                '<div class="waiting-badge">⚠️ Agent đang dừng lại để chờ bạn xác nhận (Yes/No) hoặc bổ sung thông tin!</div>',
                unsafe_allow_html=True,
            )


# ---------------- Chat Input & Execution ----------------
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu nghiên cứu của bạn...")
if sample_prompt:
    user_input = sample_prompt

if user_input:
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.turn_index += 1

    # 2. Build model prompt context
    provider = make_provider(provider_name)
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.chat_history, history_window),
        {"role": "user", "content": user_input},
    ]

    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": user_input,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    # 3. Execute Model Tool Loop with UI feedback
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý và gọi các công cụ liên quan..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=model_name,
                    max_tool_rounds=max_tool_rounds,
                )
                turn_record.update(result)
                assistant_text = result.get("assistant_text", "")
                tool_events = result.get("tool_events", [])
                status = result.get("status", "answered")

                if tool_events:
                    with st.expander(f"🔧 Tool Calls ({len(tool_events)} tools executed)", expanded=True):
                        for event in tool_events:
                            st.markdown(f"**Tool:** `{event.get('tool')}`")
                            st.code(json.dumps(event.get("args", {}), indent=2, ensure_ascii=False), language="json")
                            st.markdown("**Result:**")
                            st.code(json.dumps(event.get("result", {}), indent=2, ensure_ascii=False, default=str), language="json")
                            st.divider()

                st.markdown(assistant_text)

                if status == "waiting_for_user":
                    st.markdown(
                        '<div class="waiting-badge">⚠️ Agent đang dừng lại để chờ bạn xác nhận (Yes/No) hoặc bổ sung thông tin!</div>',
                        unsafe_allow_html=True,
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_text,
                    "tool_events": tool_events,
                    "status": status,
                })
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

            except Exception as exc:
                err_msg = f"{type(exc).__name__}: {str(exc)}"
                turn_record.update({"status": "provider_error", "error": err_msg})
                st.error(f"Lỗi: {err_msg}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Đã xảy ra lỗi: {err_msg}",
                    "status": "error",
                })

            turn_record["ended_at"] = now_iso()
            st.session_state.transcript["turns"].append(turn_record)
            write_transcript(st.session_state.transcript_path, st.session_state.transcript)


# ---------------- Transcript Download in Sidebar ----------------
with st.sidebar:
    st.divider()
    transcript_json = json.dumps(st.session_state.transcript, indent=2, ensure_ascii=False, default=str)
    st.download_button(
        label="📥 Tải Session Transcript JSON",
        data=transcript_json,
        file_name=st.session_state.transcript_path.name,
        mime="application/json",
        use_container_width=True,
    )

