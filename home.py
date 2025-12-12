import streamlit as st
from utils.constants import (set_background, set_main_card_style, set_sidebar_background,set_sidebar_nav_title)

st.set_page_config(
    page_title="論語 × キャリア成長ラボ",
    page_icon="📖",
)


set_background("assets/background/bg_washi.png")
set_main_card_style(padding_top=2.2)
set_sidebar_background()
set_sidebar_nav_title("メニュー")

HAS_PAGE_LINK = hasattr(st, "page_link")

# ----------------------------------------
# 共通レイアウト（背景・カード・サイドバー）
# ----------------------------------------
set_background("assets/background/bg_washi.png")
set_main_card_style(padding_top=2.2)
set_sidebar_background()

# ----------------------------------------
# ヘッダー
# ----------------------------------------
st.title("論語 × キャリア成長ラボ")
st.caption("古典の知恵で、仕事と人間関係を少しだけ軽く、少しだけ豊かに。")

st.markdown("---")

# page_link が使えるかどうか（2回目の代入は不要なのでそのまま使う）
HAS_PAGE_LINK = hasattr(st, "page_link")

# セマンティックアイコンを消す CSS
st.markdown(
    """
    <style>
    [data-testid="stHeader"] svg,
    [data-testid="stSubheader"] svg {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------
# メインコンテンツ（2カラム）
# ----------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗣️ 孔子と対話する（メイン機能）")
    st.write(
        "仕事や人間関係のモヤモヤを、孔子の思想とともに整理していくチャットです。\n"
        "少し悩みを書いてみるだけでも、気持ちが軽くなるかもしれません。"
    )

    if HAS_PAGE_LINK:
        st.page_link("pages/01_孔子と対話.py", label="孔子と話してみる", icon="🗨️")
    else:
        st.info("左のサイドバーから「01_孔子と対話」を選んでください。")

    st.markdown("### 📊 ビジネススキル診断")
    st.write(
        "あなたの仕事スタイルを簡単な質問から診断し、\n"
        "いまのあなたに合う論語の一節とアドバイスをお届けします。"
    )
    if HAS_PAGE_LINK:
        st.page_link("pages/02_ビジネススキル診断.py", label="診断を受ける", icon="🧭")
    else:
        st.info("サイドバーから「02_ビジネススキル診断」を選んでください。")

with col2:
    st.subheader("📚 名言図書館")
    st.write(
        "厳選した20の論語の名言を、現代のビジネスやキャリアに合わせて読み解きます。\n"
        "気になるときに、静かに読み返せる “知恵の本棚” です。"
    )
    if HAS_PAGE_LINK:
        st.page_link("pages/04_名言図書館.py", label="名言を読みにいく", icon="📖")
    else:
        st.info("サイドバーから「04_名言図書館」を選んでください。")

    st.markdown("### 👥 部下育成コーチ")
    st.write(
        "中堅・管理職向けに、部下との向き合い方や育成のヒントを論語から引き出します。\n"
        "叱り方・任せ方・信頼関係づくりに悩んだときに。"
    )
    if HAS_PAGE_LINK:
        st.page_link("pages/05_部下育成コーチ.py", label="育成のヒントを見る", icon="🧑‍💼")
    else:
        st.info("サイドバーから「05_部下育成コーチ」を選んでください。")

st.markdown("---")

# ----------------------------------------
# 下部リンク（シーン別相談 & マイページ）
# ----------------------------------------
st.markdown("### その他のメニュー")

col3, col4 = st.columns(2)

with col3:
    st.write("🧭 **シーン別ビジネス相談**")
    st.write("上司・部下・チーム・メンタルなど、状況別に論語のヒントを探せます。")
    if HAS_PAGE_LINK:
        st.page_link("pages/03_シーン別ビジネス相談.py", label="シーン別のヒントを見る", icon="👉️")
    else:
        st.info("サイドバーから「03_シーン別ビジネス相談」を選んでください。")

with col4:
    st.write("📂 **マイページ**")
    st.write("診断結果や、お気に入り登録した名言を振り返るページです。（今後拡張予定）")
    if HAS_PAGE_LINK:
        st.page_link("pages/06_マイページ.py", label="マイページを開く", icon="👉️")
    else:
        st.info("サイドバーから「06_マイページ」を選んでください。")
