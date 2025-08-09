"""
ローカルモデルの動作テストスクリプト
LM Studioでダウンロードしたモデルが正しく使えるか確認
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def test_local_models():
    """利用可能なローカルモデルをリストアップしてテスト"""
    
    print("=== ローカルモデル検出テスト ===\n")
    
    # LM Studioのモデル保存場所を探す
    lm_studio_paths = [
        Path.home() / ".cache" / "lm-studio" / "models",
        Path.home() / "LM Studio" / "models",
        Path("/Users") / os.environ.get("USER", "") / ".cache" / "lm-studio" / "models",
        Path("C:/Users") / os.environ.get("USERNAME", "") / ".cache" / "lm-studio" / "models",
    ]
    
    found_models = []
    
    for base_path in lm_studio_paths:
        if base_path.exists():
            print(f"✓ モデルディレクトリを発見: {base_path}")
            
            # GGUFファイルを探す
            gguf_files = list(base_path.rglob("*.gguf"))
            
            if gguf_files:
                print(f"  {len(gguf_files)}個のモデルファイルを検出\n")
                
                for gguf in gguf_files[:10]:  # 最初の10個まで
                    model_info = {
                        "path": str(gguf),
                        "name": gguf.name,
                        "size_mb": gguf.stat().st_size / (1024 * 1024),
                        "parent": gguf.parent.name,
                    }
                    found_models.append(model_info)
    
    if not found_models:
        print("✗ モデルファイルが見つかりません")
        print("\nLM Studioでモデルをダウンロードしてください:")
        print("1. LM Studioを開く")
        print("2. 'Discover'タブでモデルを検索")
        print("3. ダウンロードボタンをクリック")
        return
    
    print("=== 検出されたモデル ===\n")
    for i, model in enumerate(found_models, 1):
        print(f"{i}. {model['name']}")
        print(f"   場所: {model['parent']}")
        print(f"   サイズ: {model['size_mb']:.1f} MB")
        print()
    
    # 簡単な読み込みテスト
    print("\n=== モデル読み込みテスト ===")
    print("最初のモデルで読み込みテストを実行...")
    
    try:
        from llama_cpp import Llama
        
        test_model_path = found_models[0]['path']
        print(f"テストモデル: {found_models[0]['name']}")
        
        # 最小限の設定で読み込み（メモリ節約）
        print("読み込み中...")
        llm = Llama(
            model_path=test_model_path,
            n_ctx=512,  # 小さいコンテキスト
            n_gpu_layers=0,  # CPUのみでテスト
            verbose=False,
        )
        
        print("✓ モデルの読み込みに成功しました！")
        
        # 簡単な推論テスト
        print("\n簡単な推論テスト...")
        response = llm("Hello", max_tokens=10, temperature=0.7)
        print(f"応答: {response['choices'][0]['text'][:50]}...")
        
        print("\n✓ 推論テストも成功しました！")
        print("\nmain_local.pyを実行できます:")
        print("python main_local.py \"議論したいトピック\"")
        
    except ImportError:
        print("✗ llama-cpp-pythonがインストールされていません")
        print("以下のコマンドでインストールしてください:")
        print("pip install llama-cpp-python")
        print("\nGPU使用の場合:")
        print("CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" pip install llama-cpp-python --force-reinstall")
        
    except Exception as e:
        print(f"✗ エラーが発生しました: {e}")
        print("\nトラブルシューティング:")
        print("1. メモリ不足の場合は、より小さいモデルを使用してください")
        print("2. local_model_setup.mdを参照してください")


if __name__ == "__main__":
    test_local_models()