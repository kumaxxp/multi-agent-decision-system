import os
import json
import argparse
import yaml
from dotenv import load_dotenv

from utils.session import SessionLogger
from utils.json_schema import validate_json_schema
from utils.source_resolver import resolve_queries_to_urls

from providers.openai_provider import OpenAIProvider
from providers.lmstudio_provider import LMStudioProvider


def load_agents(path="config/agents.yaml"):
    """YAML形式で役割定義を読み込む"""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_provider(provider: str, model: str, base_url: str | None):
    """指定されたプロバイダを初期化"""
    if provider == "openai":
        return OpenAIProvider(model, base_url)
    if provider == "lmstudio":
        return LMStudioProvider(model, base_url or "http://localhost:1234/v1")
    raise ValueError(f"unknown provider: {provider}")


def run(topic: str, rounds: int, provider: str, model: str, base_url: str | None, json_only: bool):
    """メインの議論進行処理"""
    cfg = load_agents()
    llm = build_provider(provider, model, base_url)
    log = SessionLogger(root="sessions")

    messages = []
    step = 0

    # === 語り手 ===
    messages = [
        {"role": "system", "content": cfg["roles"]["storyteller"]["system"]},
        {"role": "user", "content": topic}
    ]
    out_story = llm.complete(messages, temperature=cfg["roles"]["storyteller"]["temperature"])
    log.save_step(step := step + 1, {"role": "storyteller", "output": out_story})

    # === 検証者 ===
    messages = [
        {"role": "system", "content": cfg["roles"]["checker"]["system"]},
        {"role": "user", "content": f"以下を厳密に検証して箇条書きで:\n{out_story}"}
    ]
    out_check = llm.complete(messages, temperature=cfg["roles"]["checker"]["temperature"])
    log.save_step(step := step + 1, {"role": "checker", "output": out_check})

    # === 調停者（JSON Schema準拠必須） ===
    arb_sys = cfg["roles"]["arbiter"]["system"]
    arb_user = f"""ユーザーのトピック: {topic}
語り手の主張: {out_story}
検証結果: {out_check}
JSONのみで出力。"""
    messages = [
        {"role": "system", "content": arb_sys},
        {"role": "user", "content": arb_user}
    ]

    decision = None
    for attempt in range(5):
        out = llm.complete(
            messages,
            temperature=cfg["roles"]["arbiter"]["temperature"],
            response_format={"type": "json_object"} if provider == "openai" else None
        )
        try:
            decision = validate_json_schema(out, "schemas/decision_v1.json")
            log.save_step(step := step + 1, {"role": "arbiter", "output": decision})
            break
        except Exception as e:
            messages.append({
                "role": "user",
                "content": (
                    "直前の出力はスキーマ違反です。修正して再出力。\n"
                    f"エラー: {e}\n"
                    "必須条件: actions>=1, risks>=1, sources>=1。\n"
                    "sources は checker の EvidencePlan をもとに {\"query\":\"...\"} 形式でも良い。\n"
                    "JSONのみを返し、不要な文章は書かない。"
                )
            })
    else:
        raise RuntimeError("decision_v1 に適合できませんでした")

    # === ポスト処理：sources が query のままなら URL 解決を試みる ===
    try:
        if any(isinstance(s, dict) and "query" in s for s in decision.get("sources", [])):
            enriched = dict(decision)
            enriched["sources"] = resolve_queries_to_urls(enriched["sources"], max_per_query=1)
            log.save_step(step := step + 1, {"role": "postprocess", "output": {"enriched_sources": enriched["sources"]}})
            decision = enriched
    except Exception as e:
        # 失敗しても処理継続（ログだけ残す）
        log.save_step(step := step + 1, {"role": "postprocess", "error": f"source resolve failed: {e}"} )

    # === 出力 ===
    if json_only:
        print(json.dumps(decision, ensure_ascii=False, indent=2))
    else:
        print("=== 結論 ===\n", decision["summary"])
        print("\n[推奨アクション]")
        for a in decision.get("actions", []):
            print("-", a)


if __name__ == "__main__":
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", nargs="?", help="議論したいトピック")
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--provider", default=os.getenv("PROVIDER", "openai"))
    ap.add_argument("--model", default=os.getenv("MODEL_NAME", "gpt-4o-mini"))
    ap.add_argument("--base-url", default=os.getenv("BASE_URL"))
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()

    if not args.topic:
        args.topic = input("議論したいトピックを入力してください: ")

    run(args.topic, args.rounds, args.provider, args.model, args.base_url, args.json_only)
