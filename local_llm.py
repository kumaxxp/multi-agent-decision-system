"""
Local LLM support using llama-cpp-python
LM Studioでダウンロードしたモデルファイル（GGUF）を直接使用
"""

import os
from typing import Dict, Any, List, Optional
from llama_cpp import Llama
from pathlib import Path


class LocalLLMProvider:
    """ローカルモデルを管理し、AutoGen互換のインターフェースを提供"""
    
    def __init__(self, model_path: str, n_ctx: int = 2048, n_gpu_layers: int = -1):
        """
        Args:
            model_path: GGUFモデルファイルのパス
            n_ctx: コンテキストサイズ（デフォルト: 2048）
            n_gpu_layers: GPUに載せるレイヤー数（-1で全て）
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        
        print(f"モデルを読み込み中: {model_path}")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )
        print("モデルの読み込み完了")
        
    def create_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """AutoGen/OpenAI互換のチャット完了API"""
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 512)
        
        # llama-cpp-pythonのchat completion APIを使用
        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        
        return response


def get_local_llm_config(model_path: str = None) -> Dict[str, Any]:
    """ローカルモデル用のLLM設定を返す"""
    
    # デフォルトのモデルパス（LM Studioのデフォルトディレクトリ）
    if model_path is None:
        # LM Studioのモデル保存場所を探す
        lm_studio_paths = [
            Path.home() / ".cache" / "lm-studio" / "models",
            Path.home() / "LM Studio" / "models",
            Path("/Users") / os.environ.get("USER", "") / ".cache" / "lm-studio" / "models",
        ]
        
        # 利用可能なモデルを探す
        available_models = []
        for base_path in lm_studio_paths:
            if base_path.exists():
                gguf_files = list(base_path.rglob("*.gguf"))
                available_models.extend(gguf_files)
        
        if available_models:
            print("\n利用可能なモデル:")
            for i, model in enumerate(available_models[:10]):  # 最初の10個まで表示
                print(f"  {i+1}. {model.name} ({model.parent.name})")
            
            # 環境変数でモデル選択
            model_index = int(os.environ.get("MODEL_INDEX", "1")) - 1
            if 0 <= model_index < len(available_models):
                model_path = str(available_models[model_index])
                print(f"\n選択されたモデル: {available_models[model_index].name}")
            else:
                model_path = str(available_models[0])
                print(f"\nデフォルトモデルを使用: {available_models[0].name}")
        else:
            raise FileNotFoundError(
                "LM Studioのモデルが見つかりません。\n"
                "MODEL_PATHを指定するか、LM Studioでモデルをダウンロードしてください。"
            )
    
    # 設定を返す（AutoGenが期待する形式）
    return {
        "model": "local-model",
        "api_type": "custom",
        "model_path": model_path,
        "temperature": float(os.environ.get("TEMPERATURE", "0.7")),
        "max_tokens": int(os.environ.get("MAX_TOKENS", "512")),
        "n_ctx": int(os.environ.get("N_CTX", "2048")),
        "n_gpu_layers": int(os.environ.get("N_GPU_LAYERS", "-1")),
    }


# グローバルなLLMプロバイダーインスタンス
_llm_provider: Optional[LocalLLMProvider] = None


def get_llm_provider(config: Dict[str, Any]) -> LocalLLMProvider:
    """シングルトンのLLMプロバイダーを取得"""
    global _llm_provider
    
    if _llm_provider is None:
        _llm_provider = LocalLLMProvider(
            model_path=config["model_path"],
            n_ctx=config.get("n_ctx", 2048),
            n_gpu_layers=config.get("n_gpu_layers", -1),
        )
    
    return _llm_provider


def local_llm_wrapper(config: Dict[str, Any]):
    """AutoGen用のカスタムLLMラッパー"""
    provider = get_llm_provider(config)
    
    def wrapper(messages, **kwargs):
        # configの値でkwargsを更新
        kwargs.update({
            "temperature": config.get("temperature", 0.7),
            "max_tokens": config.get("max_tokens", 512),
        })
        return provider.create_chat_completion(messages, **kwargs)
    
    return wrapper