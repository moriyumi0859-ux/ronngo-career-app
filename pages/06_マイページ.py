import streamlit as st
from utils.constants import (set_background, set_main_card_style, set_sidebar_background,set_sidebar_nav_title)

# ==============================
# ページ設定
# ==============================
st.set_page_config(
    page_title="マイページ",
    page_icon="📂",
)

# 背景・カード・サイドバー
set_background("assets/background/my_page_washi.png")
set_sidebar_background()
set_main_card_style(padding_top=1.4)
set_sidebar_nav_title("メニュー")

HAS_PAGE_LINK = hasattr(st, "page_link")

# ==============================
# ヘッダー
# ==============================
st.title("📂 マイページ")
st.caption("あなたの診断結果や、最近の対話をふりかえるページです。")

st.markdown("---")

# ==============================
# セクション1：最新のビジネススキル診断
# ==============================
st.subheader("🧭 最新のビジネススキル診断")

if "diagnosis_result" in st.session_state and st.session_state["diagnosis_result"]:
    result = st.session_state["diagnosis_result"]
    scores = st.session_state.get("diagnosis_scores", {})

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**現在のメインスタイル**")
        st.markdown(f"### {result.get('emoji', '📊')} {result.get('name', '')}")
        if scores:
            st.markdown("**スコアの内訳（参考）**")
            st.write(
                f"- 探究・学び: {scores.get('learning', 0)}\n"
                f"- 調整・俯瞰: {scores.get('coordination', 0)}\n"
                f"- 実行・前進: {scores.get('execution', 0)}\n"
                f"- 信頼・育成: {scores.get('trust', 0)}"
            )

    with col2:
        st.markdown("**タイプの特徴**")
        summary = result.get("summary", "")
        detail = result.get("detail", "")
        if summary:
            st.write(f"**{summary}**")
        if detail:
            st.write(detail)

        st.markdown("---")
        st.markdown("**関連する論語の一節**")
        if result.get("analects"):
            st.markdown(f"> {result['analects']}")
        if result.get("analects_exp"):
            st.caption(result["analects_exp"])

    st.markdown("---")
    st.markdown("**このタイプに合う “明日からの一歩”**")
    steps = result.get("next_steps", [])
    if steps:
        for step in steps:
            st.markdown(f"- {step}")

else:
    st.info("まだビジネススキル診断の結果がありません。")
    if HAS_PAGE_LINK:
        st.page_link(
            "pages/02_ビジネススキル診断.py",
            label="🧭 診断を受けにいく",
        )

st.markdown("---")

# ==============================
# セクション2：最近の孔子との対話
# ==============================
st.subheader("🗣️ 最近の孔子との対話（ダイジェスト）")

conf_msgs = st.session_state.get("confucius_messages", [])

if conf_msgs:
    # 師匠（assistant）のメッセージだけ抜き出して、直近3件を表示
    master_msgs = [m for m in conf_msgs if m.get("role") == "assistant"]
    master_msgs = master_msgs[-3:]  # 直近3件

    if not master_msgs:
        st.info("まだ師匠からのメッセージがありません。")
    else:
        for i, msg in enumerate(master_msgs, start=1):
            with st.expander(f"師匠からのことば {i}", expanded=(i == len(master_msgs))):
                st.write(msg.get("content", ""))
else:
    st.info("まだ孔子との対話はありません。")
    if HAS_PAGE_LINK:
        st.page_link(
            "pages/01_孔子と対話.py",
            label="🗣️ 孔子に相談しにいく"
        )

st.markdown("---")

# ==============================
# セクション3：お気に入り名言（今後拡張予定）
# ==============================
st.subheader("📚 お気に入り名言（準備中）")

st.write(
    "今後、このページでは「名言図書館」で気に入った言葉をブックマークして、\n"
    "自分だけの “論語ノート” のように振り返れるようにしていく予定です。"
)

if HAS_PAGE_LINK:
    st.page_link(
        "pages/04_名言図書館.py",
        label="📖 名言図書館をひらく",
    )

st.markdown("---")

st.caption("※ このページの内容は、同じブラウザ内での利用中セッションに基づいています。")
