import os, requests, time

# 例: Tavily を使う（https://docs.tavily.com/）
# .env に TAVILY_API_KEY を入れると有効化。無ければそのまま query を返すだけ。
def resolve_queries_to_urls(sources: list, max_per_query: int = 1) -> list:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return sources  # そのまま返す（URL化なし）

    resolved = []
    for s in sources:
        if "url" in s:
            resolved.append(s); continue
        q = s.get("query")
        if not q:
            continue
        try:
            r = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": api_key, "query": q, "search_depth": "advanced", "max_results": max_per_query},
                timeout=30
            )
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if results:
                top = results[0]
                resolved.append({
                    "url": top.get("url", ""),
                    "title": top.get("title", "") or q,
                    "quote": top.get("content", "")[:400]
                })
            else:
                resolved.append(s)  # 見つからなければ query のまま
        except Exception:
            resolved.append(s)      # 失敗しても落とさない
        time.sleep(0.3)  # 雑なレート制御
    return resolved
