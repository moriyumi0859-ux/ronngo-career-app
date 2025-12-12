import streamlit as st
import base64
import os
from utils.constants import (set_background, set_sidebar_background,set_sidebar_nav_title,)

set_background("assets/background/bg_washi2.png")
set_sidebar_background()
set_sidebar_nav_title("メニュー")

# ==============================
# ページ設定
# ==============================
st.set_page_config(
    page_title="ビジネススキル診断",
    page_icon="🧭",
)

# 背景だけ適用
set_background("assets/background/bg_washi2.png")
set_sidebar_background()


# ==============================
# 診断タイプ定義
# ==============================
TYPE_INFO = {
    "learning": {
        "name": "探究・学び型",
        "emoji": "📚",
        "summary": "学ぶこと・理解すること自体に喜びを感じるタイプ。",
        "detail": (
            "あなたは知識を糧に前へ進むタイプであり、学びによって自分の世界を広げていく力があります。"
            "その探究心は周囲にも良い刺激を与え、チームに深みや視野の広さをもたらします。"
            "一方で、思考が深まるほど慎重になりすぎて足が止まることもあるかもしれません。"
            "大切なのは、「理解」で終わらず小さくても一歩動いてみることです。"
        ),
        "analects": "「学びて時にこれを習う、また説ばしからずや。」",
        "analects_exp": "学びを折に触れて振り返ることで心は自然と満たされる、という意味です。",
        "next_steps": [
            "学んだことを1日1回は誰かに共有する。",
            "インプットのあとに、明日からやることを1つ書き出す。",
        ],
    },

    "coordination": {
        "name": "調整・俯瞰型",
        "emoji": "🎐",
        "summary": "人や状況のバランスを感じ取り、場を整えるのが得意なタイプ。",
        "detail": (
            "あなたは人間関係や状況の機微を捉える力に優れています。"
            "その繊細な感受性はチームに安心感をもたらし、摩擦を和らげる貴重な存在です。"
            "ただし、自分を後回しにしすぎると心がすり減ることも。"
            "調和を保ちつつ、自分の軸を守ることがより大きな影響力につながります。"
        ),
        "analects": "「君子は和して同ぜず。」",
        "analects_exp": "立派な人は調和は図るが、ただ周りに合わせるだけではない、という意味です。",
        "next_steps": [
            "会議後に本音をノートに書き出す。",
            "誰かの意見をまとめつつ、自分の意見も一言添えてみる。",
        ],
    },

    "execution": {
        "name": "実行・前進型",
        "emoji": "🚀",
        "summary": "まず動くことで道を切り開く、推進力のあるタイプ。",
        "detail": (
            "あなたは動きながら状況を切り開き、チームの停滞を打破する力を持っています。"
            "不確実さを恐れず進む姿勢は、組織に勢いをもたらします。"
            "しかしスピードが早いほど周囲に温度差が生まれやすいため、共有のひと息が大切です。"
            "推進力と丁寧さが合わさると、より大きな成果を生み出します。"
        ),
        "analects": "「知る者はこれを好む者に如かず、好む者はこれを楽しむ者に如かず。」",
        "analects_exp": "知っているだけよりも、好きな者が勝り、楽しむ者にはかなわないという意味です。",
        "next_steps": [
            "1日の終わりに「うまくいったこと」を3つ振り返る。",
            "動き出す前に目的を一言共有してから着手する。",
        ],
    },

    "trust": {
        "name": "信頼・育成型",
        "emoji": "🤝",
        "summary": "人との信頼や育成を大切にし、関係性を土台に仕事を進めるタイプ。",
        "detail": (
            "あなたは誠実さと温かさで周囲に安定感をもたらす存在です。"
            "相手の成長に寄り添う力は、組織にとって揺るぎない信頼の柱となります。"
            "ただし、人のために動きすぎて自分を削ってしまうことも。"
            "適度に頼る勇気を持つことで、優しさが守られ、影響力はさらに強くなります。"
        ),
        "analects": "「信なくば立たず。」",
        "analects_exp": "信頼がなければ組織も人も成り立たないという意味です。",
        "next_steps": [
            "任せられる仕事を1つ探して、誰かに託してみる。",
            "週に一度、感謝のメッセージを誰かに送る。",
        ],
    },
}

# ==============================
# 質問内容
# ==============================
QUESTIONS = [
    {"key": "q1", "text": "新しい知識やスキルを学ぶことが純粋に好きだ。", "dim": "learning"},
    {"key": "q2", "text": "分からないことがあると深く調べる方だ。", "dim": "learning"},
    {"key": "q3", "text": "チームの空気やバランスが気になってしまう。", "dim": "coordination"},
    {"key": "q4", "text": "人の意見の間を取る役割を担うことが多い。", "dim": "coordination"},
    {"key": "q5", "text": "考えるよりもまず動くタイプだ。", "dim": "execution"},
    {"key": "q6", "text": "多少荒くても物事を前に進める役割になりがちだ。", "dim": "execution"},
    {"key": "q7", "text": "人を育てたり成長を見守るのが好きだ。", "dim": "trust"},
    {"key": "q8", "text": "約束や誠実さを大切にしている。", "dim": "trust"},
]

CHOICES = {
    "まったくそう思わない": 1,
    "あまりそう思わない": 2,
    "どちらとも言えない": 3,
    "ややそう思う": 4,
    "とてもそう思う": 5,
}

# ==============================
# session state
# ==============================
if "diagnosed" not in st.session_state:
    st.session_state["diagnosed"] = False
if "diagnosis_result" not in st.session_state:
    st.session_state["diagnosis_result"] = None
if "diagnosis_scores" not in st.session_state:
    st.session_state["diagnosis_scores"] = None

# ==============================
# 質問画面
# ==============================
if not st.session_state["diagnosed"]:

    st.title("📊 ビジネススキル診断")
    st.caption("いまのあなたの『仕事スタイル』をざっくり把握し、論語の視点から成長のヒントを見つけましょう。")

    st.markdown("### 📝 質問に答えてください")

    answers = {}
    for q in QUESTIONS:
        st.markdown(f"**{q['text']}**")
        choice = st.radio("", options=list(CHOICES.keys()), key=q["key"], horizontal=True)
        answers[q["key"]] = CHOICES[choice]
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔍 診断する"):
        dim_scores = {dim: 0 for dim in TYPE_INFO.keys()}
        for q in QUESTIONS:
            dim_scores[q["dim"]] += answers[q["key"]]

        best_dim = max(dim_scores, key=lambda d: dim_scores[d])
        st.session_state["diagnosed"] = True
        st.session_state["diagnosis_result"] = {"dim": best_dim, **TYPE_INFO[best_dim]}
        st.session_state["diagnosis_scores"] = dim_scores

        st.rerun()

# ==============================
# 結果画面
# ==============================
else:
    result = st.session_state["diagnosis_result"]
    scores = st.session_state["diagnosis_scores"]

    st.title("📊 診断結果")

    st.header(f"{result['emoji']} {result['name']}")

    st.write(f"**{result['summary']}**")
    st.write(result["detail"])

    st.markdown("---")

    st.subheader("📖 関連する論語の一節")
    st.markdown(f"> {result['analects']}")
    st.caption(result["analects_exp"])

    st.subheader("🚶‍♀️ 明日からできること")
    for step in result["next_steps"]:
        st.markdown(f"- {step}")

    st.markdown("---")

    if st.button("↩ もう一度診断する"):
        st.session_state["diagnosed"] = False
        st.session_state["diagnosis_result"] = None
        st.session_state["diagnosis_scores"] = None
        st.rerun()
