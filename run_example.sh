#!/bin/bash

# 実行例スクリプト

echo "=== Multi-Agent Decision System - 実行例 ==="
echo ""

# 仮想環境のアクティベート（存在する場合）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# LM Studio接続チェック
echo "LM Studioの接続を確認中..."
python check_lmstudio.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=== 対話開始 ==="
    # サンプルトピックで実行
    echo "サンプルトピック: 「リモートワークと出社勤務、どちらが生産的か？」"
    echo ""
    
    python main.py "リモートワークと出社勤務、どちらが生産的か？"
else
    echo ""
    echo "LM Studioが正しく設定されていません。"
    echo "lmstudio_setup.mdを参照して設定してください。"
    exit 1
fi