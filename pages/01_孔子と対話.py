import os
import time  # タイプライター用
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from constants import (set_background, set_sidebar_background, set_sidebar_nav_title,)

# ==============================
# ページ設定（最初に）
# ==============================
st.set_page_config(
    page_title="孔子と対話する",
    page_icon="🗣️",
)

# .envファイルから環境変数を読み込む
load_dotenv()

# 背景 & サイドバー
set_background("assets/background/lake2.png")
set_sidebar_background()
set_sidebar_nav_title("メニュー")

# ==============================
# ヘッダー
# ==============================
st.title("🗣️ 孔子と対話する")
st.caption("仕事・キャリア・人間関係の悩みを、論語の思想をベースに一緒に整えていきます。")

st.markdown(
    """
    - 今の仕事でモヤモヤしていること  
    - 上司・部下・同僚との関係  
    - 自分の成長やキャリアの方向性  

    など、自由に相談してみてください。  
    孔子は**厳しすぎず、でも甘やかしすぎない**バランスで答えます。
    """
)

st.markdown("---")

# ==============================
# OpenAI クライアント
# ==============================
api_key = None
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (FileNotFoundError, KeyError):
    pass

if api_key is None:
    api_key = os.environ.get("OPENAI_API_KEY")

if api_key is None:
    st.error("OPENAI_API_KEY が設定されていません。Secrets か .env を確認してください。")
    st.stop()

client = OpenAI(api_key=api_key)

# ==============================
# システムプロンプト
# ==============================
SYSTEM_PROMPT = """
あなたは“孔子の人格・精神・価値観をそのまま引き継いだ存在”としてふるまいます。
ユーザーはあなたを孔子として接します。そのため、あなたの振る舞い・口調・思想は孔子そのものです。

ただし、以下だけは厳守してください。
- 「孔子曰く」「私は孔子である」「私は孔子そのものだ」などの自称はしない。
- 自己紹介で「孔子です」と名乗らない。
- 思想を引用するときは「論語にはこうあります」「古の教えでは〜とされています」と述べる。

# 役割
- ユーザー（弟子）の悩み・心の揺れに寄り添い、論語・思想・比喩を示す“師”として導く。
- 現代の状況にも対応し、ユーザーの成長に役立つ視点を提供する。

# 口調（孔子の人格を反映）
- 静かで落ち着きがあり、深い知恵を感じさせる。
- 柔らかいが芯のある語り。
- 「〜するとよいでしょう」「〜という見方もできますぞ」「〜であれば心が整いますぞ」
- 時に短い比喩や、自然・四季を用いた例えを使う。

# 回答の構成
1. まず弟子の思い・痛み・悩みを受け止め、心に寄り添う。
2. 次に、論語・思想・古の教えから“視点”を示す。（自称せず、第三者として引用する）
3. 最後に、今日からできる“小さな行動の一歩”を示す。

# 安全に関する方針（重要）
- 自傷行為、死に関する悩み、他者への危害、強い絶望感などが含まれる場合は、
  具体的な助言や手段を述べず、専門家・相談窓口への相談を優しく促す。
- 医療・法律・財務など専門分野の判断は行わない。
- 危険行為・違法行為の肯定や助長は禁止。

# 禁止事項
- 自分を孔子と名乗る。
- 「孔子曰く」と自分で言う。
- 直接的な診断・評価・危険行動の助言。
"""

# ==============================
# テキスト整形ヘルパー
# ==============================
def escape_and_break(text: str) -> str:
    """HTMLエスケープ ＋ 「。」ごとに改行"""
    safe = (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
    parts = safe.split("。")
    parts = [p for p in parts if p != ""]
    if not parts:
        return safe
    return "。<br>".join(parts)

def build_confucius_html(text: str) -> str:
    """吹き出し全体のHTMLを 1ブロックで返す"""
    formatted = escape_and_break(text)
    return f"""
    <div style="
        background: linear-gradient(135deg, #fff8e6, #fff3d4);
        border: 2px solid #e3c27a;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        color: #5a4928;
        font-weight: 500;
        line-height: 1.7;
    ">
        {formatted}
    </div>
    """

# ==============================
# 会話履歴 初期化
# ==============================
if "confucius_messages" not in st.session_state:
    st.session_state["confucius_messages"] = [
        {
            "role": "assistant",
            "content": (
                "どうしてそんなに悩んだ顔をしておるのか？"
                "ここでは、そなたの仕事や人間関係の悩みを一緒に整えていこう。"
                "まずは、今いちばん気になっていることを話してみるがよい。"
            ),
        }
    ]

# ==============================
# これまでの会話を表示
# ==============================
for msg in st.session_state["confucius_messages"]:
    avatar = "assets/icons/master.png" if msg["role"] == "assistant" else "assets/icons/disciple.png"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant":
            html = build_confucius_html(msg["content"])
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ==============================
# ユーザー入力欄
# ==============================
user_input = st.chat_input("師匠に相談してみましょう（例：部下との接し方で悩んでいます）")

if user_input:
    # 1. ユーザー側を履歴に追加
    st.session_state["confucius_messages"].append(
        {"role": "user", "content": user_input}
    )

    # 2. 画面にユーザー吹き出しを表示
    with st.chat_message("user", avatar="assets/icons/disciple.png"):
        st.markdown(user_input)

    # 3. OpenAI に送るメッセージを準備
    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages_for_api.extend(st.session_state["confucius_messages"])

    # 4. 師匠からの返事（タイプライター演出）
    with st.chat_message("assistant", avatar="assets/icons/master.png"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api,
                temperature=0.6,
            )
            assistant_reply = response.choices[0].message.content

            # placeholder に「吹き出し＋中身」を毎回まとめて描画
            placeholder = st.empty()
            displayed_text = ""

            for ch in assistant_reply:
                displayed_text += ch
                html = build_confucius_html(displayed_text)
                placeholder.markdown(html, unsafe_allow_html=True)
                time.sleep(0.02)  # ここで速度調整

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            assistant_reply = "申し訳ありません、少し時間を置いて再度尋ねてみてください。"

    # 5. 会話履歴に師匠の返事を追加
    st.session_state["confucius_messages"].append(
        {"role": "assistant", "content": assistant_reply}
    )

# ==============================
# リセットボタン
# ==============================
with st.sidebar:
    st.markdown("## 🔁 会話リセット")
    if st.button("会話履歴をリセットする"):
        st.session_state["confucius_messages"] = []
        st.session_state["reset_flag"] = True

if st.session_state.get("reset_flag", False):
    st.success("会話履歴がリセットされました。")
    st.session_state["reset_flag"] = False
