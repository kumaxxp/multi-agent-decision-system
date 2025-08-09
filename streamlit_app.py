# streamlit_app.py
import os
import json
import time
import pathlib
import importlib
from typing import Dict, Any, List, Optional

import streamlit as st
import requests

SESSIONS_ROOT = os.environ.get("SESSIONS_DIR", "sessions")

_main_direct = importlib.import_module("main_direct")
run_pipeline = getattr(_main_direct, "run")


# ---------- Utils ----------
def load_json(path: pathlib.Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"failed to read {path.name}: {e}"}

def list_sessions(root: str) -> List[pathlib.Path]:
    p = pathlib.Path(root)
    if not p.exists():
        return []
    sessions = [d for d in p.iterdir() if d.is_dir()]
    sessions.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return sessions

def list_steps(session_dir: pathlib.Path) -> List[pathlib.Path]:
    return sorted(session_dir.glob("step_*.json"))

def format_mtime(p: pathlib.Path) -> str:
    t = time.localtime(p.stat().st_mtime)
    return time.strftime("%Y-%m-%d %H:%M:%S", t)

def role_badge(role: str) -> str:
    colors = {"storyteller": "violet", "checker": "orange", "arbiter": "green", "postprocess": "blue"}
    return f":{colors.get(role,'gray')}[{role}]"

def render_sources(sources: List[Dict[str, Any]]):
    if not sources:
        st.info("sources は空です。プロンプトや検索連携を強化してください。")
        return
    st.write("### 根拠 / Sources")
    for s in sources:
        if "url" in s:
            title = s.get("title") or s["url"]
            st.markdown(f"- [{title}]({s['url']})")
            if s.get("quote"):
                with st.expander("引用プレビュー"):
                    st.write(s["quote"][:400])
        elif "query" in s:
            st.markdown(f"- 🔍 検索クエリ: `{s['query']}`")

def default_base_url(provider: str) -> str:
    if provider == "lmstudio":
        return os.environ.get("BASE_URL", "http://localhost:1234/v1")
    if provider == "ollama":
        return os.environ.get("BASE_URL", "http://localhost:11434/v1")
    return os.environ.get("BASE_URL", "")

def fetch_models(base_url: str) -> List[str]:
    """
    OpenAI互換 API の /v1/models を優先して叩く。
    Ollama旧APIの場合は /api/tags をフォールバック。
    """
    models: List[str] = []
    try:
        r = requests.get(base_url.rstrip("/") + "/models", timeout=8)
        if r.ok:
            js = r.json()
            data = js.get("data", [])
            # LM Studio / vLLM 互換: data: [{id: "..."}]
            for item in data:
                mid = item.get("id")
                if mid:
                    models.append(mid)
    except Exception:
        pass

    if models:
        return sorted(set(models))

    # Ollama native fallback (/api/tags)
    try:
        base = base_url
        if base.endswith("/v1"):
            base = base[:-3]
        r = requests.get(base.rstrip("/") + "/api/tags", timeout=8)
        if r.ok:
            js = r.json()
            for item in js.get("models", []):
                name = item.get("name")
                if name:
                    models.append(name)
    except Exception:
        pass

    return sorted(set(models))


# ---------- Sidebar: New Session ----------
with st.sidebar:
    st.header("新規セッションを開始")

    topic = st.text_area("トピック（議論テーマ）", placeholder="例: 生成AIの学校導入の是非を検討")

    provider = st.radio("Provider", ["openai", "lmstudio", "ollama"], index=0, horizontal=True)

    col_url, col_model = st.columns([1,1])
    with col_url:
        base_url = st.text_input("Base URL", value=default_base_url(provider),
                                 help="OpenAIは空でOK / LM Studio例: http://localhost:1234/v1 / Ollama例: http://localhost:11434/v1")
    with col_model:
        model_input = st.text_input("Model（手入力 or 取得後に選択）", value=os.environ.get("MODEL_NAME", ""))

    # モデル一覧取得
    fetched_models: Optional[List[str]] = None
    if st.button("📥 モデル一覧を取得", use_container_width=True):
        if not base_url.strip():
            st.error("Base URL を入力してください。")
        else:
            with st.spinner("取得中..."):
                fetched_models = fetch_models(base_url.strip())
            if fetched_models:
                st.success(f"取得: {len(fetched_models)} 件")
                sel = st.selectbox("利用するモデルを選択", fetched_models, key="model_select_box")
                if sel:
                    model_input = sel
            else:
                st.warning("モデル一覧の取得に失敗。起動状態や Base URL を確認してください。")

    json_only = st.checkbox("JSONのみ標準出力", value=True)

    if st.button("▶ 実行", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("トピックを入力してください。")
        elif provider != "openai" and not base_url.strip():
            st.error("このプロバイダでは Base URL が必要です。")
        elif not model_input.strip():
            st.error("モデル名を入力するか、一覧を取得して選択してください。")
        else:
            with st.spinner("実行中…（数十秒かかることがあります）"):
                try:
                    run_pipeline(
                        topic=topic.strip(),
                        rounds=1,
                        provider=provider,
                        model=model_input.strip(),
                        base_url=base_url.strip() or None,
                        json_only=json_only,
                    )
                    st.success("新規セッションを作成しました。右側の一覧を更新して確認してください。")
                except Exception as e:
                    st.error(f"実行に失敗しました: {e}")


# ---------- Main: Sessions View ----------
st.title("Multi-Agent Decision System — Sessions")

sessions = list_sessions(SESSIONS_ROOT)
if not sessions:
    st.info(f"セッションがありません。左のフォームから実行してください。\n(SESSIONS_DIR: {SESSIONS_ROOT})")
    st.stop()

session_labels = [f"{s.name}  —  {format_mtime(s)}" for s in sessions]
sel = st.selectbox("セッションを選択", options=range(len(sessions)), format_func=lambda i: session_labels[i])
current_session = sessions[sel]
st.caption(f"セッションディレクトリ: `{current_session}`")

steps = list_steps(current_session)
if not steps:
    st.warning("このセッションにはステップファイルがありません。")
    st.stop()

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("タイムライン")
    for i, sp in enumerate(steps, start=1):
        obj = load_json(sp)
        role = obj.get("role", "unknown")
        st.markdown(f"{i}. {role_badge(role)}  \n`{sp.name}`")

with right:
    st.subheader("詳細")
    step_index = st.slider("表示するステップ", min_value=1, max_value=len(steps), value=len(steps))
    sel_path = steps[step_index - 1]
    data = load_json(sel_path)

    role = data.get("role", "unknown")
    st.markdown(f"**Role**: {role_badge(role)}")
    st.caption(f"ファイル: `{sel_path}`  /  更新: {format_mtime(sel_path)}")

    st.write("### Raw JSON")
    st.code(json.dumps(data, ensure_ascii=False, indent=2), language="json")
    st.download_button("このJSONをダウンロード", data=json.dumps(data, ensure_ascii=False, indent=2),
                       file_name=sel_path.name, mime="application/json")

    if role in ("storyteller", "checker"):
        out = data.get("output", "")
        if isinstance(out, str) and out.strip():
            st.write("### 出力プレビュー")
            st.write(out)
    elif role == "arbiter":
        out = data.get("output", {})
        if isinstance(out, dict):
            st.write("### 結論 / Summary")
            st.success(out.get("summary", "（なし）"))

            if out.get("actions"):
                st.write("### 推奨アクション")
                for a in out["actions"]:
                    st.markdown(f"- {a}")

            if out.get("risks"):
                st.write("### リスク")
                for r in out["risks"]:
                    st.markdown(f"- {r}")

            render_sources(out.get("sources", []))

    elif role == "postprocess":
        out = data.get("output", {})
        st.info("postprocess: query→URL解決後の sources")
        render_sources(out.get("enriched_sources", out.get("sources", [])))

st.divider()
st.caption("💡 ヒント: LM Studio / Ollama の Base URL を入れて「モデル一覧を取得」でローカルモデルが選べます。")
