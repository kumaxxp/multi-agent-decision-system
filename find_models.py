"""
モデルファイルを探すヘルパースクリプト
"""

import os
from pathlib import Path

# 一般的なモデル保存場所
search_paths = [
    Path.home() / ".cache" / "lm-studio" / "models",
    Path.home() / "LM Studio" / "models",
    Path.home() / "models",
    Path.home() / "Downloads",
    Path("/opt/models"),
    Path("/usr/local/models"),
    # Windowsの場合
    Path("C:/Users") / os.environ.get("USERNAME", "") / ".cache" / "lm-studio" / "models",
    Path("C:/models"),
]

print("=== モデルファイル検索 ===\n")

found_any = False

for base_path in search_paths:
    if base_path.exists():
        # GGUFファイルを探す
        try:
            gguf_files = list(base_path.rglob("*.gguf"))
            if gguf_files:
                print(f"✓ {base_path} で {len(gguf_files)} 個のモデルを発見:")
                for gguf in gguf_files[:5]:  # 最初の5個まで表示
                    print(f"  - {gguf}")
                found_any = True
                print()
        except PermissionError:
            pass

if not found_any:
    print("GGUFモデルファイルが見つかりませんでした。\n")
    print("LM Studioでモデルをダウンロードするか、")
    print("MODEL_PATH環境変数で直接パスを指定してください。")
    print("\n例:")
    print("export MODEL_PATH=/path/to/your/model.gguf")