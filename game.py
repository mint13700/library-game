import os
import sys
import base64
import random
import textwrap

os.environ["PYTHONUTF8"] = "1"
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import streamlit as st

# ========================= 基础配置 =========================
st.set_page_config(
    page_title="图书馆寻宝大闯关",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 图片资源
IMAGE_PATH = {
    "map": "bg_lobby.jpg",
    "level1": "bg_level1.jpg",
    "level2": "bg_level2.jpg",
    "level3": "bg_level3.jpg",
    "level4": "bg_level4.jpg",
    "cert": "bg_cert.jpg",
    "hero": "hero.png"
}

# ========================= 工具函数 =========================
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def show_bg_image(page_name):
    path = IMAGE_PATH.get(page_name)
    b64 = get_base64_image(path)
    if not b64:
        return
    css = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    clean_css = textwrap.dedent(css).strip()
    st.markdown(clean_css, unsafe_allow_html=True)

def show_hero(chat_text=""):
    """右下角人物 + 右上角气泡对话框，不遮挡中间闯关界面"""
    b64 = get_base64_image(IMAGE_PATH["hero"])
    if not b64:
        return

    # 右上角固定闯关提示
    top_tip = (
        '<div style="position: fixed; top: 24px; right: 24px; background: rgba(31, 78, 121, 0.92); '
        'color: #ffffff; padding: 12px 20px; border-radius: 14px; font-size: 18px; font-weight: 800; '
        'z-index: 300; box-shadow: 0 6px 16px rgba(0,0,0,0.25);">🎮 闯关进行中</div>'
    )
    st.markdown(top_tip, unsafe_allow_html=True)

    # 右下角人物（尺寸优化，减少遮挡）
    hero_html = (
        f'<div style="position: fixed; bottom: 20px; right: 20px; width: 300px; z-index: 210;">'
        f'<img src="data:image/png;base64,{b64}" style="width:100%; animation: floatHero 2.6s ease-in-out infinite; '
        f'filter: drop-shadow(0 10px 14px rgba(0,0,0,0.3));"></div>'
    )

    # 气泡对话框：移至右上角，箭头朝上，完全避开中间答题区
    bubble_html = ""
    if chat_text:
        bubble_html = (
            f'<div style="position: fixed; top: 90px; right: 40px; background: #ffffff; '
            f'border: 3px solid #1f4e79; border-radius: 22px; padding: 14px 18px; font-size: 18px; '
            f'font-weight: 800; color: #1f4e79; box-shadow: 0 8px 20px rgba(0,0,0,0.25); z-index: 220; '
            f'max-width: 320px; animation: fadeIn 0.4s ease-in-out;">{chat_text}'
            f'<div style="position: absolute; right: 18px; top: -14px; width: 0; height: 0; '
            f'border-left: 14px solid transparent; border-right: 14px solid transparent; '
            f'border-bottom: 18px solid #1f4e79;"></div></div>'
        )

    # 动画样式 + 内容合并
    full_html = (
        '<style>'
        '@keyframes floatHero {0% {transform: translateY(0);} 50% {transform: translateY(-10px);} 100% {transform: translateY(0);}}'
        '@keyframes fadeIn {from {opacity: 0; transform: translateY(-6px);} to {opacity: 1; transform: translateY(0);}}'
        '</style>'
        + bubble_html + hero_html
    )
    st.markdown(full_html, unsafe_allow_html=True)

def autoplay_audio(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f'<audio autoplay loop><source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
        st.markdown(audio_html, unsafe_allow_html=True)

def play_sound_effect(type="correct"):
    path = f"sounds/{type}.mp3"
    if os.path.exists(path):
        autoplay_audio(path)
    else:
        if type == "correct":
            st.success("✅ 回答正确！")
        elif type == "wrong":
            st.error("❌ 回答错误！")
        elif type == "levelup":
            st.success("🎉 恭喜过关！")
        elif type == "start":
            st.info("🚀 冒险开始！")

# ========================= 全局样式 =========================
def global_style():
    css = '''
    <style>
    /* 标题特效 */
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 10px #1f4e79, 0 0 20px #1f4e79; }
        50% { text-shadow: 0 0 20px #f4c430, 0 0 30px #f4c430; }
    }
    .start-title {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        animation: titleGlow 2s ease-in-out infinite;
    }

    /* 顶部单行标题栏 */
    .top-title-bar {
        background: #ffffff;
        border-radius: 18px;
        padding: 14px 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 28px;
    }
    .top-title-bar .level-name {
        font-size: 26px;
        font-weight: 900;
        color: #1f4e79;
        white-space: nowrap;
    }
    .top-title-bar .q-count {
        background: #e8f0f8;
        color: #1f4e79;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 18px;
        font-weight: 800;
    }

    /* 白色答题对话框 */
    .question-dialog {
        background: #ffffff;
        border-radius: 24px;
        padding: 32px 36px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        margin: 0 auto 24px auto;
    }

    /* 题目字体 */
    .question-text {
        font-size: 24px;
        font-weight: 900;
        color: #143656;
        line-height: 1.5;
        margin-bottom: 28px;
    }

    /* 题型标签 */
    .tag-type {
        display: inline-block;
        background: #1f4e79;
        color: white;
        padding: 6px 18px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 18px;
    }

    /* 单选按钮样式 */
    div[role="radiogroup"] input {
        display: none !important;
    }
    div[role="radiogroup"] label {
        width: 100% !important;
        background: #e8f0f8 !important;
        border-radius: 16px !important;
        padding: 14px 22px !important;
        margin-bottom: 14px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #1f4e79 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        border: 2px solid transparent !important;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: #b9d5f0 !important;
        border-color: #1f4e79 !important;
        color: #143656 !important;
    }
    div[role="radiogroup"] label:hover {
        background: #d4e4f4 !important;
    }
    div[role="radiogroup"] label:has(input:disabled) {
        cursor: default !important;
        opacity: 0.85 !important;
    }

    /* 提交按钮 */
    .stButton > button {
        width: 100%;
        border-radius: 16px !important;
        background: #1f4e79 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        padding: 12px 0 !important;
        border: none !important;
        box-shadow: 0 6px 16px rgba(31, 78, 121, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #163a5c !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(31, 78, 121, 0.4) !important;
    }

    /* 横排关卡进度 */
    .level-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    .step-dot {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #c8d6e5;
        color: #ffffff;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    .step-dot.active {
        background: #f4c430;
        box-shadow: 0 0 0 4px rgba(244, 196, 48, 0.3);
        animation: pulse 1.5s infinite;
    }
    .step-dot.done {
        background: #1f4e79;
    }
    .step-line {
        width: 40px;
        height: 4px;
        background: #c8d6e5;
        border-radius: 2px;
    }
    .step-line.done {
        background: #1f4e79;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    /* 地图卡片 */
    .map-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        text-align: center;
        transition: all 0.3s;
    }
    .map-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 14px 30px rgba(0,0,0,0.28);
    }
    .map-card.locked {
        filter: grayscale(0.8);
        opacity: 0.7;
    }

    /* 特效层 */
    .effect-layer {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 999;
    }
    @keyframes confetti {
        0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        animation: confetti 3s ease-out forwards;
    }
    @keyframes slash {
        0% { transform: scale(0) rotate(0deg); opacity: 1; }
        100% { transform: scale(2) rotate(45deg); opacity: 0; }
    }
    .slash-effect {
        position: absolute;
        font-size: 80px;
        animation: slash 0.6s ease-out forwards;
    }

    /* 隐藏原生冗余元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    .stRadio > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    </style>
    '''
    clean_css = textwrap.dedent(css).strip()
    st.markdown(clean_css, unsafe_allow_html=True)

# ========================= 游戏状态 =========================
if "page" not in st.session_state:
    st.session_state.page = "map"
if "current_level" not in st.session_state:
    st.session_state.current_level = 1
if "level_score" not in st.session_state:
    st.session_state.level_score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "hero_talk" not in st.session_state:
    st.session_state.hero_talk = ""
if "show_effect" not in st.session_state:
    st.session_state.show_effect = ""
if "unlocked_levels" not in st.session_state:
    st.session_state.unlocked_levels = [1]

# ========================= 题库 =========================
question_bank = {
    1: {
        "title": "第1关｜馆藏探索·借阅小达人",
        "desc": "熟悉图书馆借阅、馆藏与校外访问规则",
        "bg": "level1",
        "icon": "📚",
        "questions": [
            {
                "type": "single",
                "q": "广西师范大学图书馆研究生的图书借阅权限一般为多少册？",
                "opts": ["A. 5册", "B. 10册", "C. 15册", "D. 20册"],
                "ans": "B. 10册",
                "explain": "研究生通常可借阅10册，具体以图书馆当前规则为准。"
            },
            {
                "type": "judge",
                "q": "图书超期未还，可能影响后续借阅权限。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "A. 正确",
                "explain": "超期未还会产生逾期记录，会影响后续图书借阅。"
            },
            {
                "type": "scenario",
                "q": "寒假前你借了3本参考书，但假期期间到期。最合理的做法是？",
                "opts": ["A. 等开学后再说", "B. 登录图书馆系统尝试线上续借", "C. 直接还到馆外邮箱", "D. 转给同学不用管"],
                "ans": "B. 登录图书馆系统尝试线上续借",
                "explain": "假期到期图书，大部分情况可以线上续借延长借阅时间。"
            },
            {
                "type": "single",
                "q": "想查找图书馆是否有某本纸质书，应优先使用什么系统？",
                "opts": ["A. 百度", "B. 馆藏检索系统", "C. 知网", "D. 万方"],
                "ans": "B. 馆藏检索系统",
                "explain": "纸质图书优先查馆藏检索系统，查看索书号、馆藏位置。"
            },
            {
                "type": "single",
                "q": "在校外访问图书馆电子资源，通常需要什么条件？",
                "opts": ["A. 任何网络都可直接访问", "B. 校园VPN或机构认证", "C. 只需要身份证", "D. 必须买数据库账号"],
                "ans": "B. 校园VPN或机构认证",
                "explain": "图书馆采购的电子资源有IP限制，校外需要VPN/机构认证访问。"
            },
            {
                "type": "scenario",
                "q": "你不小心把图书馆的书弄丢了，应该怎么做？",
                "opts": ["A. 假装没发生", "B. 尽快联系图书馆说明情况", "C. 随便买一本旧书代替", "D. 拖到毕业再说"],
                "ans": "B. 尽快联系图书馆说明情况",
                "explain": "丢失馆藏图书需要第一时间联系馆员，按图书馆遗失规则处理。"
            }
        ]
    },
    2: {
        "title": "第2关｜检索秘境·数据库探险家",
        "desc": "学会选择数据库与检索策略",
        "bg": "level2",
        "icon": "🔍",
        "questions": [
            {
                "type": "single",
                "q": "查找中文硕士、博士学位论文，优先选择哪个数据库？",
                "opts": ["A. 维普", "B. 知网", "C. 超星读书", "D. 百度百科"],
                "ans": "B. 知网",
                "explain": "CNKI知网是国内硕博学位论文最主要的收录平台。"
            },
            {
                "type": "single",
                "q": "Web of Science 更适合用于查找什么类型的文献？",
                "opts": ["A. 中文小说", "B. 外文核心期刊与高影响力文献", "C. 报纸", "D. 专利"],
                "ans": "B. 外文核心期刊与高影响力文献",
                "explain": "Web of Science适合外文核心文献检索、引文分析。"
            },
            {
                "type": "single",
                "q": "检索表达式中“AND”表示什么逻辑关系？",
                "opts": ["A. 或者", "B. 并且", "C. 排除", "D. 模糊匹配"],
                "ans": "B. 并且",
                "explain": "AND代表逻辑与，检索结果需要同时满足两边条件。"
            },
            {
                "type": "scenario",
                "q": "你想查找某位老师发表的全部论文，最合理的检索方式是？",
                "opts": ["A. 只搜关键词", "B. 使用作者字段检索", "C. 只搜标题", "D. 只搜机构"],
                "ans": "B. 使用作者字段检索",
                "explain": "限定作者字段检索，精准定位目标学者的成果。"
            },
            {
                "type": "judge",
                "q": "检索时关键词越多，结果一定越多。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "B. 错误",
                "explain": "关键词越多，限制条件越严格，检索出来文献数量一般变少。"
            },
            {
                "type": "scenario",
                "q": "你找到一篇英文论文，但无法直接下载全文，最合理的做法是？",
                "opts": ["A. 放弃阅读", "B. 通过图书馆文献传递服务求助", "C. 直接转发全文到论坛", "D. 只看图片不看内容"],
                "ans": "B. 通过图书馆文献传递服务求助",
                "explain": "图书馆提供文献传递服务，可以帮你获取未购买的外文文献全文。"
            }
        ]
    },
    3: {
        "title": "第3关｜学术守护·诚信守门员",
        "desc": "学术规范、版权与引用",
        "bg": "level3",
        "icon": "🛡️",
        "questions": [
            {
                "type": "single",
                "q": "直接复制他人论文大段文字且不标注出处，属于什么行为？",
                "opts": ["A. 合理引用", "B. 抄袭", "C. 综述写作", "D. 转述"],
                "ans": "B. 抄袭",
                "explain": "不加标注直接复制原文，属于学术不端中的抄袭行为。"
            },
            {
                "type": "judge",
                "q": "查重系统可以直接作为论文发表依据。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "B. 错误",
                "explain": "查重仅为自查工具，不能替代审稿，不能直接作为发表依据。"
            },
            {
                "type": "scenario",
                "q": "同学把下载的期刊论文全文发到微信群里供大家随意下载，这种行为？",
                "opts": ["A. 完全合理", "B. 可能涉及版权问题", "C. 鼓励传播", "D. 只算小事"],
                "ans": "B. 可能涉及版权问题",
                "explain": "数据库文献受版权保护，禁止私自批量分发传播。"
            },
            {
                "type": "judge",
                "q": "只要把别人的观点改写了文字，就不需要标注参考文献。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "B. 错误",
                "explain": "观点来源于他人，哪怕改写语句，依然需要标注参考文献。"
            },
            {
                "type": "single",
                "q": "我国研究生学位论文参考文献标注常用标准是？",
                "opts": ["A. GB/T 7714", "B. GB 2312", "C. GB 18030", "D. ISO 9001"],
                "ans": "A. GB/T 7714",
                "explain": "GB/T 7714是国内通用的参考文献著录国家标准。"
            },
            {
                "type": "scenario",
                "q": "你想把网上找到的一张统计图放进论文，最稳妥的做法是？",
                "opts": ["A. 直接截图使用", "B. 确认版权并注明来源", "C. 只改颜色不标注", "D. 放大后使用"],
                "ans": "B. 确认版权并注明来源",
                "explain": "图表同样受版权保护，使用前确认授权、标注来源。"
            }
        ]
    },
    4: {
        "title": "第4关｜科研助手·文献管理大师",
        "desc": "文献管理工具与阅读方法",
        "bg": "level4",
        "icon": "⚙️",
        "questions": [
            {
                "type": "single",
                "q": "Zotero、NoteExpress 等工具的主要功能是？",
                "opts": ["A. 查重", "B. 管理文献并辅助生成参考文献", "C. 下载图书", "D. 翻译论文"],
                "ans": "B. 管理文献并辅助生成参考文献",
                "explain": "文献管理软件用来整理文献、笔记，一键生成规范参考文献。"
            },
            {
                "type": "judge",
                "q": "Zotero 是免费开源的文献管理工具。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "A. 正确",
                "explain": "Zotero开源免费，无付费门槛，非常适合研究生使用。"
            },
            {
                "type": "scenario",
                "q": "软件自动生成的参考文献格式是否一定正确？",
                "opts": ["A. 一定正确", "B. 需要人工核对", "C. 不需要看", "D. 只看作者"],
                "ans": "B. 需要人工核对",
                "explain": "AI/软件生成的参考文献偶尔出错，提交前必须人工核对GB/T7714格式。"
            },
            {
                "type": "judge",
                "q": "阅读论文时，摘要和结论通常能帮助你快速判断文章价值。",
                "opts": ["A. 正确", "B. 错误"],
                "ans": "A. 正确",
                "explain": "摘要+结论可以快速把握研究目的、方法与结论，筛选文献效率更高。"
            },
            {
                "type": "scenario",
                "q": "你希望长期跟踪某个研究方向的最新文献，最有效的方法是？",
                "opts": ["A. 每天随机浏览网页", "B. 设置数据库提醒或RSS订阅", "C. 只看朋友圈", "D. 等老师通知"],
                "ans": "B. 设置数据库提醒或RSS订阅",
                "explain": "数据库订阅提醒会自动推送该方向新文献，是科研追踪的标准方法。"
            },
            {
                "type": "scenario",
                "q": "第一次读一篇英文长论文，比较合理的顺序是？",
                "opts": ["A. 从第一页逐字读到最后", "B. 先看摘要、结论和图表，再决定是否精读", "C. 只看参考文献", "D. 只读中文翻译"],
                "ans": "B. 先看摘要、结论和图表，再决定是否精读",
                "explain": "先抓核心结论，判断是否和你的研究相关，再决定精读全文。"
            }
        ]
    }
}

# ========================= 特效组件 =========================
def render_effects():
    effect = st.session_state.show_effect
    if effect == "start":
        html = '''
        <div class="effect-layer">
            <div style="position:absolute; top:20%; left:10%; font-size:40px; animation: floatHero 2s infinite;">📚</div>
            <div style="position:absolute; top:30%; right:15%; font-size:40px; animation: floatHero 2.2s infinite;">✨</div>
            <div style="position:absolute; bottom:30%; left:20%; font-size:40px; animation: floatHero 2.4s infinite;">🔍</div>
            <div style="position:absolute; bottom:20%; right:25%; font-size:40px; animation: floatHero 2.6s infinite;">🏆</div>
        </div>
        '''
        st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
    elif effect == "correct":
        parts = ['<div class="effect-layer">']
        for i in range(20):
            left = i * 5
            color = ["#f4c430", "#1f4e79", "#2ecc71", "#e74c3c"][i % 4]
            parts.append(f'<div class="confetti" style="left:{left}%; background:{color};"></div>')
        for i in range(5):
            left = random.randint(20, 80)
            top = random.randint(20, 60)
            parts.append(f'<div class="slash-effect" style="left:{left}%; top:{top}%;">✨</div>')
        parts.append('</div>')
        st.markdown("\n".join(parts), unsafe_allow_html=True)
    elif effect == "wrong":
        html = '''
        <div class="effect-layer" style="background: rgba(231, 76, 60, 0.15);">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:80px;">❌</div>
        </div>
        '''
        st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)
    elif effect == "levelup":
        parts = ['<div class="effect-layer">']
        for i in range(30):
            left = i * 3.3
            color = ["#f4c430", "#1f4e79", "#2ecc71", "#e67e22"][i % 4]
            parts.append(f'<div class="confetti" style="left:{left}%; background:{color};"></div>')
        for i in range(8):
            left = random.randint(10, 90)
            top = random.randint(10, 70)
            parts.append(f'<div class="slash-effect" style="left:{left}%; top:{top}%;">⭐</div>')
        parts.append('</div>')
        st.markdown("\n".join(parts), unsafe_allow_html=True)

# ========================= 横排进度节点 =========================
def render_level_steps(current_lv):
    html = '<div class="level-steps">'
    for i in range(1, 5):
        if i < current_lv:
            html += f'<div class="step-dot done">{i}</div>'
        elif i == current_lv:
            html += f'<div class="step-dot active">{i}</div>'
        else:
            html += f'<div class="step-dot">{i}</div>'
        if i < 4:
            if i < current_lv:
                html += '<div class="step-line done"></div>'
            else:
                html += '<div class="step-line"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ========================= 页面组件 =========================
def map_page():
    show_bg_image("map")
    show_hero("欢迎来到图书馆冒险地图！选择关卡开始挑战！")
    global_style()
    st.session_state.show_effect = "start"
    render_effects()

    if os.path.exists("sounds/bg_music.mp3"):
        autoplay_audio("sounds/bg_music.mp3")

    col1, col_mid, col3 = st.columns([1, 1.2, 1])
    with col_mid:
        title_html = '''
        <div style="text-align:center; margin-bottom: 32px; margin-top: 60px;">
            <h1 class="start-title">📖 图书馆寻宝大闯关</h1>
            <p style="font-size:20px; color:#ffffff; font-weight:800; text-shadow: 0 2px 8px rgba(0,0,0,0.3);">广西师大研一新生入馆教育 · 信息素养闯关游戏</p>
        </div>
        '''
        st.markdown(textwrap.dedent(title_html).strip(), unsafe_allow_html=True)

        cols = st.columns(4)
        for i, col in enumerate(cols):
            level_num = i + 1
            info = question_bank[level_num]
            unlocked = level_num in st.session_state.unlocked_levels
            status = "✅ 已通关" if level_num < st.session_state.current_level else ("🔓 可挑战" if unlocked else "🔒 未解锁")
            card_class = "map-card" if unlocked else "map-card locked"

            with col:
                card_html = f'''
                <div class="{card_class}">
                    <div style="font-size:40px;">{info['icon']}</div>
                    <h3 style="color:#1f4e79; margin:12px 0;">第{level_num}关</h3>
                    <p style="font-size:16px; color:#445566;">{info['title'].split('｜')[1]}</p>
                    <p style="font-size:14px; color:#f4c430; font-weight:800;">{status}</p>
                </div>
                '''
                st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)

                if unlocked:
                    if st.button(f"开始第{level_num}关", key=f"map_level_{level_num}"):
                        st.session_state.current_level = level_num
                        st.session_state.level_score = 0
                        st.session_state.q_index = 0
                        st.session_state.answered = False
                        st.session_state.hero_talk = f"第{level_num}关开始，加油！"
                        st.session_state.show_effect = "start"
                        play_sound_effect("start")
                        st.session_state.page = "level"
                        st.rerun()

def level_page():
    lv = st.session_state.current_level
    info = question_bank[lv]
    show_bg_image(info["bg"])
    show_hero(st.session_state.hero_talk)
    global_style()
    render_effects()

    q_list = info["questions"]
    idx = st.session_state.q_index
    total_q = len(q_list)

    col1, col_mid, col3 = st.columns([1, 1.4, 1])
    with col_mid:
        # 顶部单行标题栏（下移避开右上角气泡）
        title_bar = f'''
        <div class="top-title-bar" style="margin-top: 80px;">
            <div class="level-name">{info['title']}</div>
            <div class="q-count">题目 {idx+1}/{total_q}</div>
        </div>
        '''
        st.markdown(textwrap.dedent(title_bar).strip(), unsafe_allow_html=True)

        if idx >= total_q:
            right = st.session_state.level_score
            rate = right / total_q
            result_html = f'''
            <div class="question-dialog" style="text-align:center;">
                <h3 style="color:#1f4e79; font-size:28px; margin-bottom:16px;">本关挑战结束</h3>
                <p style="font-size:22px; font-weight:800; color:#143656;">答对：{right} / {total_q}</p>
                <p style="font-size:22px; font-weight:800; color:#143656;">正确率：{int(rate*100)}%</p>
            </div>
            '''
            st.markdown(textwrap.dedent(result_html).strip(), unsafe_allow_html=True)
            
            if rate >= 0.6:
                st.session_state.hero_talk = "太棒啦！顺利通关！"
                st.session_state.show_effect = "levelup"
                play_sound_effect("levelup")
                st.success("🎉 恭喜通关！")
                if lv < 4:
                    if (lv + 1) not in st.session_state.unlocked_levels:
                        st.session_state.unlocked_levels.append(lv + 1)
                    st.button("返回冒险地图", use_container_width=True, on_click=lambda: (
                        st.session_state.update({"page":"map", "show_effect":"start"}),
                        st.rerun()
                    ))
                else:
                    st.button("领取通关证书", use_container_width=True, on_click=lambda: (
                        st.session_state.update({"page":"cert", "hero_talk":"恭喜你完成全部闯关！", "show_effect":"levelup"}),
                        st.rerun()
                    ))
            else:
                st.session_state.hero_talk = "还差一点点，再试一次！"
                st.session_state.show_effect = "wrong"
                play_sound_effect("wrong")
                st.error("❌ 正确率不足60%，需要重闯本关")
                st.button("重新挑战本关", use_container_width=True, on_click=lambda: (
                    st.session_state.update({"level_score":0, "q_index":0, "answered":False, "hero_talk":"重新出发，你可以的！", "show_effect":""}),
                    st.rerun()
                ))
            return

        q = q_list[idx]
        q_type_name = {"single": "单选题", "judge": "判断题", "scenario": "情景题"}.get(q["type"], "题目")

        # 白色答题框：题型+题干+选项全部在内
        st.markdown('<div class="question-dialog">', unsafe_allow_html=True)
        st.markdown(f'<span class="tag-type">{q_type_name}</span>', unsafe_allow_html=True)
        st.markdown(f'<p class="question-text">{q["q"]}</p>', unsafe_allow_html=True)

        selected = st.radio(
            "请选择答案：",
            q["opts"],
            key=f"q_{lv}_{idx}",
            disabled=st.session_state.answered,
            index=None,
            label_visibility="collapsed"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if not st.session_state.answered:
            if st.button("提交答案", use_container_width=True):
                if selected is None:
                    st.warning("请先选择一个答案！")
                    st.stop()
                st.session_state.answered = True
                if selected == q["ans"]:
                    st.session_state.level_score += 1
                    st.session_state.total_score += 1
                    st.session_state.hero_talk = "🎉 恭喜答对了！"
                    st.session_state.show_effect = "correct"
                    play_sound_effect("correct")
                else:
                    st.session_state.hero_talk = f"💡 答错啦，正确答案是：{q['ans']}"
                    st.session_state.show_effect = "wrong"
                    play_sound_effect("wrong")
                st.rerun()
        else:
            st.info(f"📖 解析：{q['explain']}")
            st.button("下一题", use_container_width=True, on_click=lambda: (
                st.session_state.update({"q_index":idx+1, "answered":False, "hero_talk":"继续加油！", "show_effect":""}),
                st.rerun()
            ))

def cert_page():
    show_bg_image("cert")
    show_hero("你太厉害了！全部闯关完成！")
    global_style()
    st.session_state.show_effect = "levelup"
    render_effects()

    col1, col_mid, col3 = st.columns([1, 1.2, 1])
    with col_mid:
        cert_html = '''
        <div class="question-dialog" style="text-align:center; margin-top: 80px;">
            <h1 style="font-size:36px; color:#1f4e79;">🏆 入馆达人证书</h1>
            <p style="font-size:20px; color:#445566; font-weight:800;">恭喜你完成全部4关信息素养闯关！</p>
            <div style="border:3px solid #f4c430; border-radius:18px; padding:24px; background:#fffbe6; margin:24px 0;">
                <h3 style="color:#7a5c00;">授予称号</h3>
                <p style="font-size:26px; font-weight:900; color:#b8860b;">广西师大图书馆入馆达人</p>
            </div>
        </div>
        '''
        st.markdown(textwrap.dedent(cert_html).strip(), unsafe_allow_html=True)
        
        st.button("🔁 重新开始冒险", use_container_width=True, on_click=lambda: (
            st.session_state.update({"page":"map", "current_level":1, "level_score":0, "q_index":0, "answered":False, "total_score":0, "hero_talk":"欢迎回来！", "show_effect":"start", "unlocked_levels":[1]}),
            st.rerun()
        ))

# 页面路由
if st.session_state.page == "map":
    map_page()
elif st.session_state.page == "level":
    level_page()
elif st.session_state.page == "cert":
    cert_page()
