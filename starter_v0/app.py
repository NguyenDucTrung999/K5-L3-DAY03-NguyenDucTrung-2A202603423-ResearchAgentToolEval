from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop


ROOT_DIRECTORY = Path(__file__).resolve().parent
ARTIFACTS_DIRECTORY = ROOT_DIRECTORY / "artifacts"
load_lab_env(ROOT_DIRECTORY)


st.set_page_config(
    page_title="Research Agent UI",
    layout="wide",
)

st.title("Research Agent - Lab Showdown Demo")
st.caption("He thong danh gia va thuc thi Tool-Calling Research Agent phien ban v3")

# Sidebar cau hinh
st.sidebar.header("Cau hinh he thong")

selected_provider = st.sidebar.selectbox(
    "Nha cung cap mo hinh (Provider)",
    options=["openrouter", "gemini", "openai"],
    index=0,
)

if selected_provider == "openrouter":
    default_model_name = "openai/gpt-4o-mini"
else:
    if selected_provider == "gemini":
        default_model_name = "gemini-2.5-flash"
    else:
        default_model_name = "gpt-4o-mini"

input_model_name = st.sidebar.text_input(
    "Ten mo hinh (Model)",
    value=default_model_name,
)

if st.sidebar.button("Xoa lich su tro chuyen"):
    st.session_state["chat_messages"] = []
    st.session_state["history_turns"] = []
    st.rerun()

# Khoi tao session state
if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = []

if "history_turns" not in st.session_state:
    st.session_state["history_turns"] = []

# Hien thi lich su tro chuyen
for message_item in st.session_state["chat_messages"]:
    role = message_item["role"]
    content = message_item["content"]
    with st.chat_message(role):
        st.markdown(content)
        if "tool_events" in message_item:
            tool_events = message_item["tool_events"]
            if len(tool_events) > 0:
                with st.expander("Nhat ky goi cong cu (Tool Events)"):
                    st.json(tool_events)

# Xu ly khi nguoi dung nhap cau hoi
user_input_prompt = st.chat_input("Nhap yeu cau nghien cuu cua ban tai day...")

if user_input_prompt is not None and user_input_prompt.strip() != "":
    # Hien thi tin nhan nguoi dung
    st.session_state["chat_messages"].append({"role": "user", "content": user_input_prompt})
    with st.chat_message("user"):
        st.markdown(user_input_prompt)

    # Tai system prompt va declarations
    system_prompt_text = (ARTIFACTS_DIRECTORY / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations_list = load_tool_declarations(ARTIFACTS_DIRECTORY / "tools.yaml")
    openai_tools_list = to_openai_tools(tool_declarations_list)

    provider_instance = make_provider(selected_provider)

    full_conversation_messages = [{"role": "system", "content": system_prompt_text}]
    for past_turn in st.session_state["history_turns"]:
        full_conversation_messages.append(past_turn)
    full_conversation_messages.append({"role": "user", "content": user_input_prompt})

    with st.chat_message("assistant"):
        with st.spinner("Agent dang suy nghi va goi cong cu..."):
            try:
                execution_result = run_model_tool_loop(
                    provider=provider_instance,
                    messages=full_conversation_messages,
                    tools=openai_tools_list,
                    model=input_model_name,
                    max_tool_rounds=4,
                )

                assistant_reply_text = execution_result.get("assistant_text", "")
                observed_tool_events = execution_result.get("tool_events", [])

                st.markdown(assistant_reply_text)

                if len(observed_tool_events) > 0:
                    with st.expander("Nhat ky goi cong cu (Tool Events)"):
                        st.json(observed_tool_events)

                # Luu lai vao session
                st.session_state["chat_messages"].append({
                    "role": "assistant",
                    "content": assistant_reply_text,
                    "tool_events": observed_tool_events,
                })
                st.session_state["history_turns"].append({"role": "user", "content": user_input_prompt})
                st.session_state["history_turns"].append({"role": "assistant", "content": assistant_reply_text})

            except Exception as exception_error:
                error_display_text = f"Loi khi thuc thi mo hinh: {str(exception_error)}"
                st.error(error_display_text)
                st.session_state["chat_messages"].append({
                    "role": "assistant",
                    "content": error_display_text,
                })

