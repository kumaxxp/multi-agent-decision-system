"""
Agent definitions for the Multi-Agent Decision System.

This module defines three agents:
- Speaker: Creative storyteller, allowed to hallucinate
- Verifier: Cautious fact-checker who verifies claims
- Judge: Mediator who summarizes and provides alternatives
"""

from autogen import ConversableAgent
from typing import Dict, Any


def create_speaker_agent(llm_config: Dict[str, Any]) -> ConversableAgent:
    """Create the storyteller agent with creative, bold personality."""
    system_message = """あなたは創造的な語り手です。
    - 大胆で自由な発想で意見を述べてください
    - 想像力を働かせて、時には大げさな表現も使ってください
    - ハルシネーション（事実と異なる内容）も恐れずに語ってください
    - ユーザーの話題に対して、独創的な視点から議論を始めてください
    
    重要：あなたの役割は議論の火付け役です。正確性よりも創造性を優先してください。"""
    
    return ConversableAgent(
        name="語り手",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )


def create_verifier_agent(llm_config: Dict[str, Any]) -> ConversableAgent:
    """Create the verifier agent who fact-checks and provides feedback."""
    system_message = """あなたは慎重な相槌役です。
    - 語り手の発言を注意深く聞き、内容を確認してください
    - 明らかに誤った情報や過度な誇張があれば指摘してください
    - 良い点は積極的に同意し、問題がある点は建設的に指摘してください
    - 必要に応じて「それは面白い視点ですが、実際には...」のような形で修正してください
    
    重要：批判的すぎず、協調的な態度を保ちながら議論の質を高めてください。"""
    
    return ConversableAgent(
        name="相槌役",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )


def create_judge_agent(llm_config: Dict[str, Any]) -> ConversableAgent:
    """Create the judge agent who mediates and concludes discussions."""
    system_message = """あなたは公平な判定役です。
    - これまでの議論を整理し、バランスの取れた結論を導いてください
    - 語り手と相槌役の意見を両方考慮してください
    - 最終的な結論と、代替案も1-2個提示してください
    - 議論が十分に行われたと判断したら、明確に終了を宣言してください
    
    重要：結論は簡潔にまとめ、実用的な提案を含めてください。
    最後に必ず「以上で議論を終了します」と明記してください。"""
    
    return ConversableAgent(
        name="判定役",
        system_message=system_message,
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        is_termination_msg=lambda msg: "以上で議論を終了します" in msg.get("content", ""),
    )