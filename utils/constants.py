import streamlit as st
import base64
import os

# ======================================
# Base64 Utility
# ======================================
def _encode_image(image_path: str):
    """画像を base64 に変換して返す"""
    if not os.path.exists(image_path):
        st.warning(f"画像が見つかりません: {image_path}")
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ======================================
# 背景画像（ページ全体）
# ======================================
def set_background(image_path: str):
    encoded = _encode_image(image_path)
    if encoded is None:
        return

    css = f"""
    <style>
    .stApp {{
        background:
            linear-gradient(rgba(255,255,255,0.12), rgba(255,255,255,0.12)),
            url("data:image/png;base64,{encoded}");
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ======================================
# メインの白いカード（1枚の大きなカード）
# ======================================
def set_main_card_style(padding_top: float = 1.2):
    """
    ページの文字ブロックを囲む白いカードを設定。
    padding_top はカード内の文字の上余白を調整できる。
    """
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }}

    .block-container {{
        background: rgba(255, 255, 255, 0.9) !important;
        padding: {padding_top}rem 3rem 2.6rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0,0,0,0.09) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10) !important;
        max-width: 1100px !important;
        margin: 6.25rem auto 3rem auto !important;
    }}

    [data-testid="stMarkdownContainer"] {{
        background: transparent !important;
        padding: 0 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ======================================
# サイドバー背景（白い半透明）
# ======================================
def set_sidebar_background():
    """サイドバーを白い半透明にし、柔らかい雰囲気に統一する"""
    css = """
    <style>
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.72) !important;  /* 白い半透明 */
        backdrop-filter: blur(6px) !important;             /* ほんのりブラーで高級感 */
        border-right: 1px solid rgba(0,0,0,0.08) !important; /* 右側に薄い境界線 */
    }

    /* サイドバーの内側のブロックは透明にする（カードっぽさを消す） */
    [data-testid="stSidebar"] .block-container {
        background: transparent !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ======================================
# サイドバーのナビ上部タイトルを表示する
# ======================================

import streamlit as st

def set_sidebar_nav_title(title: str = "メニュー"):
    css = f"""
    <style>
    /* サイドバーのページナビ全体 */
    [data-testid="stSidebarNav"] {{
        padding-top: 0.75rem;
    }}

    /* ナビの一番上にタイトルを挿入 */
    [data-testid="stSidebarNav"]::before {{
        content: "{title}";
        display: block;
        font-size: 14px;
        font-weight: 700;
        margin: 4px 0 8px 8px;
        color: #333;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
