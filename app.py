import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import requests, io, warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Gekko Finance", page_icon="🦎", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&display=swap');
:root {
    --cream:#faf6ef;--cream2:#f3ede2;--cream3:#ede4d3;
    --gold:#c9a84c;--gold2:#e8c97a;--gold3:#7a5c1e;
    --brown:#6b4f2e;--brown2:#3d2b10;--text:#2c1f0e;
    --muted:#8a7560;--border:#d4c4a8;--pos:#3d6b3a;
    --neg:#b84c3a;--surface:#f7f0e4;--blue:#2a5298;--blue2:#4a90d9;
    --nav-w:240px;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'DM Mono',monospace;background:var(--cream);color:var(--text);}
.stApp{background:var(--cream);}

/* Hide default Streamlit sidebar completely */
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapsedControl"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
#MainMenu,footer,header{visibility:hidden;}

/* Global inputs */
.stTextInput input,.stNumberInput input,.stTextArea textarea{
    background:var(--surface)!important;border:1px solid var(--border)!important;
    color:var(--text)!important;border-radius:8px!important;
    font-family:'DM Mono',monospace!important;font-size:13px!important;}
.stSelectbox>div>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;}
.stButton>button{background:transparent;border:1px solid var(--gold);color:var(--gold3);
    border-radius:6px;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1px;
    transition:all 0.2s;padding:8px 16px;}
.stButton>button:hover{background:var(--gold);color:var(--brown2);}
.stTabs [data-baseweb="tab-list"]{background:var(--cream2);border-radius:8px;padding:4px;border:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent;color:var(--muted);border-radius:6px;font-family:'DM Mono',monospace;font-size:11px;}
.stTabs [aria-selected="true"]{background:var(--gold)!important;color:var(--brown2)!important;font-weight:500;}
.stDataFrame{border:1px solid var(--border);border-radius:10px;overflow:hidden;}

/* Cards */
.gk-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px 20px;position:relative;overflow:hidden;margin-bottom:8px;}
.gk-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--blue2),transparent);}
.gk-label{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.gk-value{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:600;color:var(--text);line-height:1;}
.gk-sub{font-size:12px;margin-top:5px;}
.pos{color:var(--pos)!important;}.neg{color:var(--neg)!important;}.gold{color:var(--gold)!important;}
.gk-section{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--gold3);padding-bottom:8px;border-bottom:1px solid var(--border);margin:20px 0 14px 0;}
.gk-row{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:11px 16px;margin:4px 0;display:flex;align-items:center;justify-content:space-between;transition:border-color 0.2s;}
.gk-row:hover{border-color:var(--gold);}
.teach{background:rgba(201,168,76,0.07);border-left:3px solid var(--gold);border-radius:0 10px 10px 0;padding:12px 16px;margin:12px 0;font-size:12px;line-height:1.85;color:var(--brown);}
.teach strong{color:var(--gold3);}
.chat-wrap{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:18px;height:460px;overflow-y:auto;margin-bottom:10px;}
.chat-user{background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--brown2);border-radius:14px 14px 2px 14px;padding:11px 15px;margin:7px 0 7px auto;max-width:75%;font-size:13px;line-height:1.6;width:fit-content;}
.chat-ai{background:var(--cream2);border:1px solid var(--border);border-left:3px solid var(--blue2);border-radius:0 14px 14px 14px;padding:13px 17px;margin:7px auto 7px 0;max-width:92%;font-size:13px;line-height:1.85;}
.chat-lbl{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:3px;}
details{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;margin-bottom:6px!important;}
summary{font-family:'DM Mono',monospace!important;font-size:12px!important;padding:10px 14px!important;}

/* ── CUSTOM LEFT NAV ── */
.gk-nav{
    position:fixed;top:0;left:0;width:var(--nav-w);height:100vh;
    background:var(--brown2);border-right:1px solid rgba(201,168,76,0.18);
    z-index:1000;display:flex;flex-direction:column;padding:0;
    overflow-y:auto;
}
.gk-nav-logo{padding:22px 20px 16px 20px;border-bottom:1px solid rgba(201,168,76,0.12);}
.gk-nav-logo-title{font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;color:#e8c97a;letter-spacing:-0.5px;}
.gk-nav-logo-sub{font-size:8px;letter-spacing:3px;color:rgba(243,237,226,0.3);text-transform:uppercase;margin-top:2px;}
.gk-nav-section{font-size:8px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(232,201,122,0.35);padding:16px 20px 6px 20px;}
.gk-nav-item{display:flex;align-items:center;gap:10px;padding:10px 20px;cursor:pointer;
    transition:all 0.15s;border-left:3px solid transparent;color:rgba(243,237,226,0.55);font-size:12px;letter-spacing:0.5px;}
.gk-nav-item:hover{background:rgba(201,168,76,0.08);color:rgba(243,237,226,0.85);border-left-color:rgba(201,168,76,0.4);}
.gk-nav-item.active{background:rgba(201,168,76,0.12);color:#e8c97a;border-left-color:var(--gold);}
.gk-nav-icon{font-size:14px;width:18px;text-align:center;}
.gk-nav-bottom{margin-top:auto;padding:16px 20px;border-top:1px solid rgba(201,168,76,0.12);}
.gk-nav-api{background:rgba(255,255,255,0.05);border:1px solid rgba(201,168,76,0.2);
    border-radius:8px;padding:10px 12px;font-size:10px;color:rgba(243,237,226,0.4);}

/* Main content offset */
.gk-main{margin-left:var(--nav-w);padding:28px 32px;min-height:100vh;}
.gk-header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:22px;}
.gk-title{font-family:'Cormorant Garamond',serif;font-size:44px;font-weight:300;letter-spacing:-2px;color:var(--brown2);line-height:1;}
.gk-title em{color:var(--gold);font-style:italic;}
.gk-page-title{font-family:'Cormorant Garamond',serif;font-size:32px;font-weight:400;color:var(--brown2);margin-bottom:4px;}
.gk-page-sub{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);}

/* Demo banner */
.demo-banner{background:rgba(201,168,76,0.1);border:1px solid rgba(201,168,76,0.3);border-left:4px solid var(--gold);
    border-radius:0 10px 10px 0;padding:12px 18px;margin-bottom:18px;display:flex;align-items:center;gap:12px;}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
DEMO_PORTFOLIO = {
    "ASML": {"sector":"Semiconductor Equipment","shares":2.0, "avg_cost":850.0},
    "AMAT": {"sector":"Semiconductor Equipment","shares":5.0, "avg_cost":195.0},
    "LRCX": {"sector":"Semiconductor Equipment","shares":3.0, "avg_cost":820.0},
    "KLAC": {"sector":"Semiconductor Equipment","shares":2.0, "avg_cost":680.0},
    "ENTG": {"sector":"Semiconductor Materials","shares":8.0, "avg_cost":110.0},
    "ADI":  {"sector":"Chip Components",        "shares":6.0, "avg_cost":190.0},
    "TXN":  {"sector":"Chip Components",        "shares":5.0, "avg_cost":165.0},
    "AVGO": {"sector":"Chip Components",        "shares":2.0, "avg_cost":1100.0},
    "ALB":  {"sector":"Battery Materials",      "shares":4.0, "avg_cost":135.0},
    "BHP":  {"sector":"Critical Metals",        "shares":10.0,"avg_cost":58.0},
    "SPY":  {"sector":"ETF / Index",            "shares":3.0, "avg_cost":480.0},
    "BIL":  {"sector":"Fixed Income",           "shares":20.0,"avg_cost":91.5},
}
SECTOR_OPTIONS=["Semiconductor Equipment","Semiconductor Materials","Chip Components",
    "Battery Materials","Critical Metals","ETF / Index","Fixed Income",
    "Technology","Healthcare","Energy","Financials","Consumer","Industrial","Other"]
SECTOR_COLORS={"Semiconductor Equipment":"#c9a84c","Semiconductor Materials":"#5c6b3a",
    "Chip Components":"#6b4f2e","Battery Materials":"#8a9e5a","Critical Metals":"#a0896a",
    "ETF / Index":"#2a5298","Fixed Income":"#4a90d9","Technology":"#7a5c1e",
    "Healthcare":"#6b3a3a","Energy":"#6b5a2e","Financials":"#3a506b",
    "Consumer":"#506b3a","Industrial":"#4a4a6b","Other":"#8a7560"}
PLOT=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(243,237,226,0.5)",
    font=dict(family="DM Mono",color="#8a7560",size=11),
    xaxis=dict(gridcolor="#d4c4a8",zeroline=False),
    yaxis=dict(gridcolor="#d4c4a8",zeroline=False),
    margin=dict(t=30,b=30,l=10,r=10),
    colorway=["#c9a84c","#5c6b3a","#6b4f2e","#8a9e5a","#2a5298","#e8c97a","#b84c3a","#4a90d9"])
SYSTEM_PROMPT="""You are Gekko, an elite AI financial advisor and teacher built into a portfolio management platform.
You have full access to the user's real portfolio data. You combine Wall Street sharpness with professor-level clarity.
Rules: 1. Give accurate sharp financial advice 2. ALWAYS explain jargon plainly — users are learning
3. Reference actual portfolio data when relevant 4. Bold key terms and numbers 5. Be direct warm witty — be the mentor they need"""

NAV_PAGES=["Dashboard","Performance","Quant Analysis","Monte Carlo","IB Models","Financials","AI Advisor"]
NAV_ICONS=["◈","📈","🧮","🎲","🏦","📁","🤖"]

# ── Session State ──────────────────────────────────────────────────────────────
if "portfolio"    not in st.session_state: st.session_state.portfolio    = DEMO_PORTFOLIO.copy()
if "is_demo"      not in st.session_state: st.session_state.is_demo      = True
if "page"         not in st.session_state: st.session_state.page         = "Dashboard"
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "api_key"      not in st.session_state: st.session_state.api_key      = ""
if "ib_memo"      not in st.session_state: st.session_state.ib_memo      = ""
if "show_add"     not in st.session_state: st.session_state.show_add     = False

# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_prices(tt):
    prices,changes={},{}
    for t in tt:
        try:
            fi=yf.Ticker(t).fast_info; prices[t]=fi.last_price; prev=fi.previous_close
            changes[t]=((fi.last_price-prev)/prev*100) if prev else 0
        except: prices[t]=None; changes[t]=0
    return prices,changes

@st.cache_data(ttl=300)
def get_hist(tt,period="1y"):
    if not tt: return pd.DataFrame()
    try:
        raw=yf.download(list(tt),period=period,auto_adjust=True,progress=False)
        close=raw["Close"] if isinstance(raw.columns,pd.MultiIndex) else raw
        return close.dropna(how="all")
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_info(t):
    try: return yf.Ticker(t).info
    except: return {}

@st.cache_data(ttl=3600)
def get_fins(t):
    try:
        tk=yf.Ticker(t)
        return {"income":tk.financials,"balance":tk.balance_sheet,"cashflow":tk.cashflow}
    except: return {}

def ps(p): return f"${p:,.2f}" if p else "N/A"
def fmv(v,d=1):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    if abs(v)>=1e12: return f"${v/1e12:.{d}f}T"
    if abs(v)>=1e9: return f"${v/1e9:.{d}f}B"
    if abs(v)>=1e6: return f"${v/1e6:.{d}f}M"
    return f"${v:,.{d}f}"
def fpct(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    return f"{v*100:.1f}%"
def card(col,lbl,val,sub,cls):
    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value">{val}</div><div class="gk-sub {cls}">{sub}</div></div>',unsafe_allow_html=True)
def ask_ai(messages,system,api_key):
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1500,"system":system,"messages":messages},timeout=45)
        return r.json()["content"][0]["text"] if r.status_code==200 else f"Error {r.status_code}"
    except Exception as e: return f"Error: {e}"
def portfolio_ctx():
    p=st.session_state.portfolio
    if not p: return "No holdings."
    try:
        prices,changes=get_prices(tuple(p.keys()))
        lines=["Portfolio:"]
        for t,d in p.items():
            val=(prices.get(t) or 0)*d["shares"]
            lines.append(f"  {t}|{d['sector']}|{d['shares']:.2f}sh|{ps(prices.get(t))}|{changes.get(t,0):+.2f}%|${val:,.0f}")
        return "\n".join(lines)
    except: return "Portfolio data unavailable."

def clear_demo_if_needed():
    if st.session_state.is_demo:
        st.session_state.portfolio={}
        st.session_state.is_demo=False

def export_xlsx():
    p=st.session_state.portfolio
    if not p: return None
    try:
        prices,changes=get_prices(tuple(p.keys()))
        rows=[{"Ticker":t,"Sector":d["sector"],"Shares":d["shares"],"Avg Cost":d["avg_cost"],
            "Current Price":prices.get(t) or 0,"Value":(prices.get(t) or 0)*d["shares"],
            "Day %":f"{changes.get(t,0):+.2f}%"} for t,d in p.items()]
    except:
        rows=[{"Ticker":t,"Sector":d["sector"],"Shares":d["shares"],"Avg Cost":d["avg_cost"]} for t,d in p.items()]
    buf=io.BytesIO()
    pd.DataFrame(rows).to_excel(buf,index=False,engine="openpyxl")
    return buf.getvalue()

# ── Build sectors map ──────────────────────────────────────────────────────────
tickers=list(st.session_state.portfolio.keys())
sectors_map={}
for t,d in st.session_state.portfolio.items():
    sectors_map.setdefault(d["sector"],[]).append(t)

# ── LEFT NAV (rendered as HTML + Streamlit buttons) ───────────────────────────
with st.container():
    # Nav HTML shell
    nav_items_html=""
    for icon,page in zip(NAV_ICONS,NAV_PAGES):
        active="active" if st.session_state.page==page else ""
        nav_items_html+=f'<div class="gk-nav-item {active}" id="nav-{page}"><span class="gk-nav-icon">{icon}</span>{page}</div>'

    holdings_html=""
    for sec,ts in list(sectors_map.items())[:5]:
        color=SECTOR_COLORS.get(sec,"#c9a84c")
        holdings_html+=f'<div style="font-size:8px;letter-spacing:2px;text-transform:uppercase;color:{color};margin:8px 0 3px 0;padding-left:20px">{sec[:18]}</div>'
        for t in ts[:3]:
            sh=st.session_state.portfolio[t]["shares"]
            holdings_html+=f'<div style="font-size:10px;color:rgba(243,237,226,0.4);padding-left:28px;margin:1px 0">→ {t} ({sh:.1f}sh)</div>'

    api_status='<span style="color:#5c6b3a">● Connected</span>' if st.session_state.api_key else '<span style="color:rgba(243,237,226,0.3)">○ No API key</span>'
    demo_badge='<div style="background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.3);border-radius:4px;padding:3px 8px;font-size:9px;letter-spacing:1px;color:#c9a84c;text-align:center;margin-bottom:8px">DEMO MODE</div>' if st.session_state.is_demo else ""

    st.markdown(f"""
    <div class="gk-nav">
      <div class="gk-nav-logo">
        <div class="gk-nav-logo-title">🦎 Gekko</div>
        <div class="gk-nav-logo-sub">Finance Intelligence</div>
      </div>
      <div class="gk-nav-section">Navigation</div>
      {nav_items_html}
      <div class="gk-nav-section" style="margin-top:16px">Holdings</div>
      {holdings_html}
      <div class="gk-nav-bottom">
        {demo_badge}
        <div class="gk-nav-api">AI Advisor {api_status}</div>
      </div>
    </div>
    <div class="gk-main">
    """, unsafe_allow_html=True)

# ── Nav buttons (invisible, overlay on nav items) ─────────────────────────────
# We use a column trick: render actual buttons in the sidebar area
with st.sidebar:
    st.markdown('<style>[data-testid="stSidebar"]{display:flex!important;}</style>', unsafe_allow_html=True)

# Use query params for navigation since we can't do true overlay buttons
# Instead, render compact nav buttons at top of main area
nav_cols = st.columns(len(NAV_PAGES))
for i,(icon,page) in enumerate(zip(NAV_ICONS,NAV_PAGES)):
    with nav_cols[i]:
        active_style = "background:var(--gold);color:var(--brown2)" if st.session_state.page==page else ""
        if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

st.markdown("<hr style='border-color:#d4c4a8;margin:10px 0 18px 0'>", unsafe_allow_html=True)

# ── Fetch live data ────────────────────────────────────────────────────────────
if tickers:
    with st.spinner(""):
        prices,changes=get_prices(tuple(tickers))
        hist  =get_hist(tuple(tickers),st.session_state.get("period","1y"))
        hist1y=get_hist(tuple(tickers),"1y")
    total_value=sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in tickers)
    total_cost =sum(st.session_state.portfolio[t]["avg_cost"]*st.session_state.portfolio[t]["shares"]
        if st.session_state.portfolio[t]["avg_cost"]>0
        else (prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in tickers)
    total_pnl=total_value-total_cost
    pnl_pct=(total_pnl/total_cost*100) if total_cost>0 else 0
    day_chg=sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]*(changes.get(t,0)/100) for t in tickers)
    best_t=max(tickers,key=lambda x:changes.get(x,0))
    worst_t=min(tickers,key=lambda x:changes.get(x,0))
else:
    prices,changes,hist,hist1y={},{},pd.DataFrame(),pd.DataFrame()
    total_value=total_cost=total_pnl=pnl_pct=day_chg=0
    best_t=worst_t="—"

page=st.session_state.page

# ── Demo banner ────────────────────────────────────────────────────────────────
if st.session_state.is_demo:
    st.markdown("""
    <div class="demo-banner">
      <div style="font-size:20px">🦎</div>
      <div>
        <div style="font-size:11px;font-weight:600;color:#7a5c1e;letter-spacing:1px">DEMO MODE — Explore freely</div>
        <div style="font-size:11px;color:#8a7560;margin-top:2px">Viewing a sample supply chain portfolio. All features active.
        Use <strong style="color:#c9a84c">Manage Portfolio</strong> below to add your own stocks and replace the demo.</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ── Manage Portfolio panel (always accessible) ─────────────────────────────────
with st.expander("⚙️ Manage Portfolio — Add · Edit · Remove · Settings", expanded=False):
    m1,m2,m3,m4=st.tabs(["➕ Add Single","📋 Bulk Add","✏️ Edit / Remove","🔑 AI Key & Settings"])

    with m1:
        c1,c2,c3,c4,c5=st.columns([2,2,1,1,1])
        with c1: nt=st.text_input("Ticker",placeholder="SPY, NVDA, BIL...",key="nt_add").upper().strip()
        with c2: ns=st.selectbox("Sector",SECTOR_OPTIONS,key="ns_add")
        with c3: nsh=st.number_input("Shares",min_value=0.0,value=1.0,step=0.1,key="nsh_add",format="%.4f")
        with c4: nco=st.number_input("Avg Cost ($)",min_value=0.0,value=0.0,step=0.01,key="nco_add",format="%.2f")
        with c5:
            st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
            if st.button("ADD ➕",key="add_btn",use_container_width=True):
                if nt:
                    clear_demo_if_needed()
                    st.session_state.portfolio[nt]={"sector":ns,"shares":nsh,"avg_cost":nco}
                    st.success(f"✓ {nt} added!"); st.rerun()
                else: st.error("Enter a ticker symbol")

    with m2:
        bc1,bc2=st.columns([3,1])
        with bc1: bulk_in=st.text_area("Tickers (one per line or comma separated)",placeholder="ASML\nAMAT\nLRCX\nor: ASML, AMAT, LRCX",key="bulk_in",height=80)
        with bc2:
            bulk_sec=st.selectbox("Sector",SECTOR_OPTIONS,key="bulk_sec")
            if st.button("BULK ADD ➕",key="bulk_btn",use_container_width=True):
                raw=[x.strip().upper() for x in bulk_in.replace(",","\n").split("\n") if x.strip()]
                if raw: clear_demo_if_needed()
                added=sum(1 for t in raw if t and t not in st.session_state.portfolio and not st.session_state.portfolio.update({t:{"sector":bulk_sec,"shares":0.0,"avg_cost":0.0}}))
                st.success(f"✓ Added {added} stocks — edit shares below"); st.rerun()

    with m3:
        if st.session_state.portfolio:
            ec1,ec2,ec3,ec4,ec5=st.columns([2,2,1,1,1])
            with ec1: et=st.selectbox("Stock",list(st.session_state.portfolio.keys()),key="et_sel")
            cur=st.session_state.portfolio[et]
            with ec2: es=st.selectbox("Sector",SECTOR_OPTIONS,index=SECTOR_OPTIONS.index(cur["sector"]) if cur["sector"] in SECTOR_OPTIONS else 0,key="es_sel")
            with ec3: esh=st.number_input("Shares",value=float(cur["shares"]),step=0.1,key="esh",format="%.4f")
            with ec4: eco=st.number_input("Avg Cost",value=float(cur["avg_cost"]),step=0.01,key="eco",format="%.2f")
            with ec5:
                st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
                sc1,sc2=st.columns(2)
                with sc1:
                    if st.button("✓",key="save_e",use_container_width=True):
                        st.session_state.portfolio[et].update({"shares":esh,"avg_cost":eco,"sector":es})
                        st.success("Saved"); st.rerun()
                with sc2:
                    if st.button("🗑",key="rem_e",use_container_width=True):
                        del st.session_state.portfolio[et]; st.rerun()
            if st.button("⚠️ Clear Entire Portfolio",key="clear_all"):
                st.session_state.portfolio={}; st.session_state.is_demo=False; st.rerun()
        else:
            st.info("No holdings yet — add stocks above.")

    with m4:
        ak1,ak2=st.columns([3,1])
        with ak1: key_in=st.text_input("Anthropic API Key",value=st.session_state.api_key,type="password",placeholder="sk-ant-...",key="api_key_in")
        with ak2:
            st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
            if st.button("SAVE KEY",key="save_key_btn",use_container_width=True):
                st.session_state.api_key=key_in; st.success("✓ Saved!")
        period_sel=st.select_slider("Default Chart Period",["1mo","3mo","6mo","1y","2y","5y"],value=st.session_state.get("period","1y"),key="period_slider")
        st.session_state["period"]=period_sel
        xlsx=export_xlsx()
        if xlsx:
            st.download_button("⬇ Download Portfolio (Excel)",data=xlsx,file_name="gekko_portfolio.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="dl_port")

st.markdown("<br>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════
if page=="Dashboard":
    st.markdown('<div class="gk-page-title">Dashboard</div><div class="gk-page-sub">Live Portfolio Overview</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not tickers:
        st.info("Add stocks from Manage Portfolio above to begin."); st.stop()

    c1,c2,c3,c4,c5=st.columns(5)
    card(c1,"Portfolio Value",f"${total_value:,.0f}",f"{'▲' if day_chg>=0 else '▼'} ${abs(day_chg):,.0f} today","pos" if day_chg>=0 else "neg")
    card(c2,"Total P&L",f"{pnl_pct:+.1f}%",f"${total_pnl:+,.0f}","pos" if total_pnl>=0 else "neg")
    card(c3,"Holdings",str(len(tickers)),f"{len(sectors_map)} sectors","gold")
    card(c4,"Best Today",best_t,f"+{changes.get(best_t,0):.2f}%","pos")
    card(c5,"Worst Today",worst_t,f"{changes.get(worst_t,0):+.2f}%","neg")

    st.markdown("<br>",unsafe_allow_html=True)
    left,right=st.columns([3,2])
    with left:
        st.markdown('<div class="gk-section">Live Holdings</div>', unsafe_allow_html=True)
        for sec,ts in sectors_map.items():
            color=SECTOR_COLORS.get(sec,"#c9a84c")
            st.markdown(f'<div style="color:{color};font-size:9px;letter-spacing:2px;text-transform:uppercase;margin:12px 0 5px 0">{sec}</div>', unsafe_allow_html=True)
            for t in ts:
                p=prices.get(t); chg=changes.get(t,0); sh=st.session_state.portfolio[t]["shares"]
                val=(p or 0)*sh; clr="#3d6b3a" if chg>=0 else "#b84c3a"; arr="▲" if chg>=0 else "▼"
                st.markdown(f"""<div class="gk-row">
                  <div><span style="font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:600">{t}</span>
                  <span style="color:#8a7560;font-size:11px;margin-left:8px">{sh:.2f} sh</span></div>
                  <div style="text-align:center;min-width:85px"><div style="font-size:14px;font-weight:500">{ps(p)}</div>
                  <div style="color:{clr};font-size:11px">{arr} {chg:+.2f}%</div></div>
                  <div style="text-align:right;min-width:75px"><div style="font-size:9px;color:#8a7560">VALUE</div>
                  <div style="font-size:13px;font-weight:500">${val:,.0f}</div></div>
                </div>""", unsafe_allow_html=True)
    with right:
        alloc={sec:sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in ts) for sec,ts in sectors_map.items()}
        if sum(alloc.values())>0:
            fig=go.Figure(go.Pie(labels=list(alloc.keys()),values=list(alloc.values()),hole=0.55,
                marker_colors=[SECTOR_COLORS.get(s,"#c9a84c") for s in alloc],
                textinfo="label+percent",textfont=dict(family="DM Mono",size=10)))
            fig.update_layout(**{**PLOT,"height":260,"showlegend":False,
                "annotations":[dict(text="ALLOC",x=0.5,y=0.5,font=dict(size=11,color="#8a7560"),showarrow=False)]})
            st.plotly_chart(fig,use_container_width=True)
        st.markdown('<div class="gk-section">Movers</div>', unsafe_allow_html=True)
        for t in sorted(tickers,key=lambda x:changes.get(x,0),reverse=True)[:8]:
            chg=changes.get(t,0); bc="#5c6b3a" if chg>=0 else "#b84c3a"; bw=min(abs(chg)*10,100)
            st.markdown(f"""<div style="display:flex;align-items:center;gap:10px;margin:4px 0">
              <span style="font-size:11px;width:44px;font-weight:500">{t}</span>
              <div style="flex:1;background:#ede4d3;border-radius:3px;height:4px">
                <div style="width:{bw}%;background:{bc};height:4px;border-radius:3px"></div></div>
              <span style="font-size:11px;color:{bc};width:54px;text-align:right">{chg:+.2f}%</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PAGE: PERFORMANCE
# ══════════════════════════════════════════════════════
elif page=="Performance":
    st.markdown('<div class="gk-page-title">Performance</div><div class="gk-page-sub">Returns & Comparative Analysis</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    sel=st.multiselect("Select holdings to chart",tickers,default=tickers[:min(8,len(tickers))],key="perf_sel")
    extra=st.text_input("Benchmark any ticker (SPY, QQQ, BTC-USD...)","",key="extra_perf").upper().strip()
    compare=[*sel,*([extra] if extra and extra not in sel else [])]
    if compare:
        ch=get_hist(tuple(compare),st.session_state.get("period","1y"))
        valid=[t for t in compare if not ch.empty and t in ch.columns]
        if valid:
            norm=ch[valid]/ch[valid].iloc[0]*100
            fig=go.Figure()
            for t in valid:
                c=SECTOR_COLORS.get(st.session_state.portfolio.get(t,{}).get("sector","Other"),"#c9a84c")
                fig.add_trace(go.Scatter(x=norm.index,y=norm[t],name=t,line=dict(color=c,width=2),
                    hovertemplate=f"<b>{t}</b> %{{y:.1f}}<extra></extra>"))
            fig.update_layout(**{**PLOT,"height":420,"yaxis_title":"Indexed (100=start)","hovermode":"x unified",
                "legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10))})
            st.plotly_chart(fig,use_container_width=True)
            rows=[]
            for t in valid:
                s=ch[t].dropna()
                if len(s)<2: continue
                dr=s.pct_change().dropna()
                rows.append({"Ticker":t,"Period":f"{(s.iloc[-1]/s.iloc[0]-1)*100:+.1f}%",
                    "1M":f"{(s.iloc[-1]/s.iloc[-min(21,len(s))]-1)*100:+.1f}%",
                    "3M":f"{(s.iloc[-1]/s.iloc[-min(63,len(s))]-1)*100:+.1f}%",
                    "Vol":f"{dr.std()*np.sqrt(252)*100:.1f}%","Price":ps(prices.get(t))})
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
# PAGE: QUANT ANALYSIS
# ══════════════════════════════════════════════════════
elif page=="Quant Analysis":
    st.markdown('<div class="gk-page-title">Quant Analysis</div><div class="gk-page-sub">Risk · Returns · Correlation</div>', unsafe_allow_html=True)
    st.markdown("""<div class="teach"><strong>📚 Guide</strong> — <strong>Sharpe</strong>: return/risk (>1 good) ·
    <strong>Beta</strong>: vs S&P500 sensitivity · <strong>Max DD</strong>: worst drawdown ·
    <strong>VaR 95%</strong>: worst daily loss 1-in-20 · <strong>Correlation</strong>: low = diversified</div>""", unsafe_allow_html=True)
    sel=st.multiselect("Select stocks",tickers,default=tickers[:min(10,len(tickers))],key="q_sel")
    extra=st.text_input("Add any ticker","",key="q_extra").upper().strip()
    ql=[*sel,*([extra] if extra and extra not in sel else [])]
    if ql:
        qh=get_hist(tuple(ql),"1y")
        v1y=[t for t in ql if not qh.empty and t in qh.columns]
        if v1y:
            dr=qh[v1y].pct_change().dropna()
            spy=get_hist(("SPY",),"1y")
            spyr=spy["SPY"].pct_change().dropna() if "SPY" in spy.columns else None
            rows=[]
            for t in v1y:
                r=dr[t].dropna()
                if len(r)<10: continue
                sharpe=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
                cum=(1+r).cumprod(); mdd=((cum-cum.cummax())/cum.cummax()).min()*100
                beta=None
                if spyr is not None:
                    idx=r.index.intersection(spyr.index)
                    if len(idx)>30: beta,*_=stats.linregress(spyr.loc[idx],r.loc[idx])
                rows.append({"Ticker":t,"Ann. Return":f"{r.mean()*252*100:+.1f}%",
                    "Ann. Vol":f"{r.std()*np.sqrt(252)*100:.1f}%","Sharpe":f"{sharpe:.2f}",
                    "Max DD":f"{mdd:.1f}%","Beta":f"{beta:.2f}" if beta is not None else "—",
                    "VaR 95%":f"{np.percentile(r,5)*100:.2f}%"})
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
            if len(v1y)>1:
                st.markdown('<div class="gk-section">Correlation Matrix</div>', unsafe_allow_html=True)
                corr=dr[v1y].corr()
                fig=go.Figure(go.Heatmap(z=corr.values,x=corr.columns,y=corr.index,
                    colorscale=[[0,"#b84c3a"],[0.5,"#ede4d3"],[1,"#5c6b3a"]],
                    zmin=-1,zmax=1,text=np.round(corr.values,2),texttemplate="%{text}",textfont=dict(size=9,family="DM Mono")))
                fig.update_layout(**{**PLOT,"height":380})
                st.plotly_chart(fig,use_container_width=True)
        st.markdown('<div class="gk-section">DuPont · Horizontal Analysis</div>', unsafe_allow_html=True)
        dp_t=st.selectbox("Stock for DuPont",ql,key="dp_sel")
        info=get_info(dp_t)
        roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets"); pm=info.get("profitMargins"); at=info.get("assetTurnover")
        lev=(roe/roa) if roe and roa and roa!=0 else None
        for col,(lbl,val) in zip(st.columns(5),[("ROE",fpct(roe)),("Net Margin",fpct(pm)),
            ("Asset Turnover",f"{at:.2f}x" if at else "—"),("ROA",fpct(roa)),
            ("Equity Multiplier",f"{lev:.2f}x" if lev else "—")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px">{val}</div></div>', unsafe_allow_html=True)
        if v1y:
            hrows=[]
            for t in v1y:
                s=qh[t].dropna(); row={"Ticker":t}
                for lbl,d in {"1W":5,"1M":21,"3M":63,"6M":126,"1Y":252}.items():
                    row[lbl]=f"{(s.iloc[-1]/s.iloc[-min(d,len(s))]-1)*100:+.1f}%" if len(s)>d else "—"
                hrows.append(row)
            st.dataframe(pd.DataFrame(hrows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
# PAGE: MONTE CARLO
# ══════════════════════════════════════════════════════
elif page=="Monte Carlo":
    st.markdown('<div class="gk-page-title">Monte Carlo</div><div class="gk-page-sub">Stress Testing & Probability Scenarios</div>', unsafe_allow_html=True)
    st.markdown("""<div class="teach"><strong>📚 Monte Carlo</strong> — Runs thousands of random future scenarios using historical volatility.
    Not a prediction — a probability range. <strong>Bear = 5th percentile · Bull = 95th percentile.</strong></div>""", unsafe_allow_html=True)
    mode=st.radio("Mode",["Full Portfolio","Selected Stocks"],horizontal=True,key="mc_mode")
    if mode=="Selected Stocks":
        mc_sel=st.multiselect("Select stocks",tickers,default=tickers[:min(5,len(tickers))],key="mc_sel")
        ex=st.text_input("Add any ticker","",key="mc_extra").upper().strip()
        mc_t=[*mc_sel,*([ex] if ex and ex not in mc_sel else [])]
    else: mc_t=tickers
    c1,c2,c3=st.columns(3)
    with c1: n_sim=st.select_slider("Simulations",[500,1000,2000,5000],value=1000)
    with c2: n_days=st.select_slider("Forecast Days",[30,60,90,180,252],value=252)
    with c3: run_mc=st.button("▶ RUN SIMULATION",use_container_width=True)
    if run_mc and mc_t:
        mch=get_hist(tuple(mc_t),"1y")
        vmc=[t for t in mc_t if not mch.empty and t in mch.columns]
        if vmc:
            with st.spinner("Running..."):
                dr_mc=mch[vmc].pct_change().dropna()
                if mode=="Full Portfolio":
                    pv={(t):(prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in vmc}
                    tv=sum(pv.values()); sv=total_value
                    w=np.array([pv[t]/tv if tv>0 else 1/len(vmc) for t in vmc])
                else: w=np.ones(len(vmc))/len(vmc); sv=10000
                port_r=dr_mc[vmc].values@w; mu,sigma=port_r.mean(),port_r.std()
                np.random.seed(42)
                sims=np.zeros((n_days,n_sim))
                for i in range(n_sim): sims[:,i]=sv*np.cumprod(1+np.random.normal(mu,sigma,n_days))
                finals=sims[-1,:]; pcts={k:np.percentile(finals,v) for k,v in {"p5":5,"p25":25,"p50":50,"p75":75,"p95":95}.items()}
                fig=go.Figure()
                for i in range(min(200,n_sim)):
                    fig.add_trace(go.Scatter(y=sims[:,i],mode="lines",line=dict(color="rgba(201,168,76,0.03)",width=1),showlegend=False,hoverinfo="skip"))
                for lbl,p,clr in [("Bull 95th",pcts["p95"],"#5c6b3a"),("Median",pcts["p50"],"#c9a84c"),("Bear 5th",pcts["p5"],"#b84c3a")]:
                    idx=np.argmin(np.abs(sims[-1,:]-p))
                    fig.add_trace(go.Scatter(y=sims[:,idx],mode="lines",name=f"{lbl}: ${p:,.0f}",line=dict(color=clr,width=2.5)))
                fig.update_layout(**{**PLOT,"height":420,"yaxis":dict(gridcolor="#d4c4a8",tickprefix="$",tickformat=",.0f"),"legend":dict(bgcolor="rgba(0,0,0,0)")})
                st.plotly_chart(fig,use_container_width=True)
                for col,(lbl,p,clr) in zip(st.columns(5),[("Bear 5%",pcts["p5"],"#b84c3a"),("25th",pcts["p25"],"#a0896a"),("Median",pcts["p50"],"#c9a84c"),("75th",pcts["p75"],"#5c6b3a"),("Bull 95%",pcts["p95"],"#3d6b3a")]):
                    chg=(p-sv)/sv*100 if sv>0 else 0
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:17px;color:{clr}">${p:,.0f}</div><div class="gk-sub" style="color:{clr}">{chg:+.1f}%</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# PAGE: IB MODELS
# ══════════════════════════════════════════════════════
elif page=="IB Models":
    st.markdown('<div class="gk-page-title">Investment Banking Models</div><div class="gk-page-sub">DCF · Comps · Precedent Transactions · LBO · Document Memo</div>', unsafe_allow_html=True)
    ic1,ic2=st.columns([2,3])
    with ic1: ib_port=st.selectbox("From portfolio",["— enter below —"]+tickers,key="ib_port")
    with ic2: ib_cust=st.text_input("Or any ticker","",placeholder="MSFT, TSLA...",key="ib_cust").upper().strip()
    ib_t=ib_cust if ib_cust else (ib_port if ib_port!="— enter below —" else (tickers[0] if tickers else ""))
    if not ib_t: st.info("Select or enter a company above."); st.stop()
    st.markdown(f'<div style="font-family:Cormorant Garamond,serif;font-size:18px;color:#3d2b10;margin:6px 0 14px 0">Analyzing: <strong style="color:#c9a84c">{ib_t}</strong></div>', unsafe_allow_html=True)
    info=get_info(ib_t)
    ib1,ib2,ib3,ib4,ib5,ib6=st.tabs(["DCF","COMPS","PRECEDENT TXN","LBO","RATIOS","📄 DOCUMENT MEMO"])

    with ib1:
        st.markdown("""<div class="teach"><strong>📚 DCF</strong> — A company is worth the sum of all future free cash flows discounted to today.
        <strong>WACC</strong> = cost of capital. Intrinsic value > price → potentially undervalued.</div>""", unsafe_allow_html=True)
        d1,d2,d3,d4=st.columns(4)
        with d1: wacc=st.number_input("WACC %",value=10.0,step=0.5,key="wacc")/100
        with d2: g5=st.number_input("5Y Rev Growth %",value=8.0,step=0.5,key="g5")/100
        with d3: tg=st.number_input("Terminal Growth %",value=2.5,step=0.5,key="tg")/100
        with d4: fcfm=st.number_input("FCF Margin %",value=15.0,step=1.0,key="fcfm")/100
        if st.button("◈ CALCULATE INTRINSIC VALUE",key="run_dcf"):
            rev=info.get("totalRevenue"); sh_out=info.get("sharesOutstanding")
            try: cur_p=yf.Ticker(ib_t).fast_info.last_price
            except: cur_p=None
            if rev and sh_out:
                fcfs=[]; r=rev
                for yr in range(1,6):
                    r*=(1+g5); fcf=r*fcfm; pv_fcf=fcf/(1+wacc)**yr
                    fcfs.append({"Year":f"Year {yr}","Revenue":fmv(r),"FCF":fmv(fcf),"PV FCF":fmv(pv_fcf),"_pv":pv_fcf})
                pv_term=(fcfs[-1]["_pv"]*(1+tg)/(wacc-tg))/(1+wacc)**5 if wacc>tg else 0
                total_pv=sum(f["_pv"] for f in fcfs)+pv_term; intrinsic=total_pv/sh_out
                for f in fcfs: del f["_pv"]
                st.dataframe(pd.DataFrame(fcfs),use_container_width=True,hide_index=True)
                mos=((intrinsic-(cur_p or 0))/intrinsic*100) if cur_p and intrinsic>0 else 0
                for col,(lbl,val) in zip(st.columns(4),[("PV Terminal",fmv(pv_term)),("Total Equity",fmv(total_pv)),("Intrinsic/Share",f"${intrinsic:.2f}"),("Margin of Safety",f"{mos:+.1f}%")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px">{val}</div></div>', unsafe_allow_html=True)
                if cur_p:
                    st.markdown(f'<div class="teach">Current <strong>{ps(cur_p)}</strong> vs intrinsic <strong>${intrinsic:.2f}</strong> → <strong>{"🟢 UNDERVALUED" if mos>15 else "🟡 FAIR" if mos>-10 else "🔴 OVERVALUED"}</strong></div>', unsafe_allow_html=True)
            else: st.warning("Revenue data unavailable.")

    with ib2:
        st.markdown("""<div class="teach"><strong>📚 Comps</strong> — Value by comparing to similar public companies using multiples like EV/EBITDA and P/E.</div>""", unsafe_allow_html=True)
        cin=st.text_input("Comparable tickers","NVDA,AMD,INTC,QCOM",key="comps_in")
        if st.button("◈ RUN COMPS",key="run_comps"):
            all_t=list(set([ib_t]+[x.strip().upper() for x in cin.split(",") if x.strip()]))
            rows=[]
            for t in all_t:
                i=get_info(t)
                if not i: continue
                rows.append({"Ticker":t,"Name":i.get("shortName","")[:20],"Mkt Cap":fmv(i.get("marketCap")),
                    "EV/EBITDA":f"{i.get('enterpriseToEbitda',0):.1f}x" if i.get("enterpriseToEbitda") else "—",
                    "P/E":f"{i.get('trailingPE',0):.1f}x" if i.get("trailingPE") else "—",
                    "Gross Margin":fpct(i.get("grossMargins")),"Net Margin":fpct(i.get("profitMargins")),"ROE":fpct(i.get("returnOnEquity"))})
            if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    with ib3:
        st.markdown("""<div class="teach"><strong>📚 Precedent Transactions</strong> — What did acquirers pay for similar companies? Includes control premium (20–40% above market).</div>""", unsafe_allow_html=True)
        p1,p2,p3=st.columns(3)
        with p1: lo=st.number_input("Low EV/EBITDA",value=10.0,step=0.5,key="lo_ev")
        with p2: hi=st.number_input("High EV/EBITDA",value=18.0,step=0.5,key="hi_ev")
        with p3: prem=st.slider("Control Premium %",0,50,25,key="prem")/100
        if st.button("◈ ESTIMATE VALUE",key="run_prec"):
            ebitda=info.get("ebitda"); sh_out=info.get("sharesOutstanding")
            try: cur_p=yf.Ticker(ib_t).fast_info.last_price
            except: cur_p=None
            if ebitda and sh_out:
                nd=info.get("totalDebt",0)-(info.get("totalCash",0) or 0)
                lo_pp=(ebitda*lo-nd)/sh_out*(1+prem); hi_pp=(ebitda*hi-nd)/sh_out*(1+prem)
                for col,(lbl,val) in zip(st.columns(4),[("Low EV",fmv(ebitda*lo)),("High EV",fmv(ebitda*hi)),("Low/Share",f"${lo_pp:.2f}"),("High/Share",f"${hi_pp:.2f}")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px">{val}</div></div>', unsafe_allow_html=True)
                if cur_p: st.markdown(f'<div class="teach">At <strong>{ps(cur_p)}</strong>, high-end deal implies <strong>{(hi_pp-cur_p)/cur_p*100:+.1f}% premium</strong></div>', unsafe_allow_html=True)
            else: st.warning("EBITDA unavailable.")

    with ib4:
        st.markdown("""<div class="teach"><strong>📚 LBO</strong> — PE buys using mostly debt, improves ops, sells in ~5 years. <strong>IRR target: 20%+</strong>. <strong>MOIC</strong> = money back multiple.</div>""", unsafe_allow_html=True)
        l1,l2,l3=st.columns(3)
        with l1: ent=st.number_input("Entry EV/EBITDA",value=12.0,step=0.5,key="lbo_ent"); dbt=st.number_input("Debt % EV",value=65.0,step=5.0,key="lbo_dbt")/100
        with l2: ext=st.number_input("Exit EV/EBITDA",value=14.0,step=0.5,key="lbo_ext"); eg=st.number_input("EBITDA Growth/yr %",value=10.0,step=1.0,key="lbo_g")/100
        with l3: hold=st.number_input("Hold (yrs)",value=5,min_value=1,max_value=10,step=1,key="lbo_hold")
        if st.button("◈ RUN LBO",key="run_lbo"):
            ebitda=info.get("ebitda")
            if ebitda:
                ev=ebitda*ent; debt=ev*dbt; eq=ev*(1-dbt)
                ex_ev=ebitda*(1+eg)**hold*ext; ex_eq=ex_ev-debt*(0.7**hold)
                moic=ex_eq/eq if eq>0 else 0; irr=(moic**(1/hold)-1)*100
                for col,(lbl,val) in zip(st.columns(4),[("Entry EV",fmv(ev)),("Exit EV",fmv(ex_ev)),("MOIC",f"{moic:.2f}x"),("IRR",f"{irr:.1f}%")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="teach">IRR of <strong>{irr:.1f}%</strong> {"✅ meets 20%+ PE target" if irr>=20 else "⚠️ below 20% target"}</div>', unsafe_allow_html=True)
            else: st.warning("EBITDA unavailable.")

    with ib5:
        for col,(lbl,val,tip) in zip(st.columns(4),[
            ("Debt/Equity",f"{info.get('debtToEquity',0)/100:.2f}x" if info.get("debtToEquity") else "—","<1x conservative"),
            ("Current Ratio",f"{info.get('currentRatio',0):.2f}x" if info.get("currentRatio") else "—",">1x healthy"),
            ("Quick Ratio",f"{info.get('quickRatio',0):.2f}x" if info.get("quickRatio") else "—",">1x good"),
            ("Interest Coverage",f"{info.get('interestCoverage',0):.1f}x" if info.get("interestCoverage") else "—",">3x safe")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px">{val}</div><div class="gk-sub" style="font-size:10px;color:#8a7560">{tip}</div></div>', unsafe_allow_html=True)
        for col,(lbl,val) in zip(st.columns(4),[("Gross Margin",fpct(info.get("grossMargins"))),("Net Margin",fpct(info.get("profitMargins"))),("ROE",fpct(info.get("returnOnEquity"))),("EV/EBITDA",f"{info.get('enterpriseToEbitda',0):.1f}x" if info.get("enterpriseToEbitda") else "—")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px">{val}</div></div>', unsafe_allow_html=True)

    with ib6:
        st.markdown("""<div class="teach"><strong>📚 Document Memo</strong> — Upload any financial document (10-K, earnings, balance sheet, investor deck).
        Gekko AI will read it and generate a professional IB memo with thesis, risks, and valuation perspective.</div>""", unsafe_allow_html=True)
        if not st.session_state.api_key:
            st.warning("Add your Anthropic API key in Manage Portfolio → AI Key & Settings to use this feature.")
        else:
            doc_up=st.file_uploader("Upload Document (PDF, CSV, Excel, TXT)",type=["pdf","csv","xlsx","xls","txt"],key="ib_doc")
            doc_ctx=""
            if doc_up:
                try:
                    if doc_up.name.endswith(".csv"): doc_ctx=f"CSV Data:\n{pd.read_csv(doc_up).to_string(max_rows=60)}"
                    elif doc_up.name.endswith((".xlsx",".xls")): doc_ctx=f"Excel Data:\n{pd.read_excel(doc_up).to_string(max_rows=60)}"
                    elif doc_up.name.endswith(".txt"): doc_ctx=f"Document:\n{doc_up.read().decode('utf-8',errors='ignore')[:8000]}"
                    elif doc_up.name.endswith(".pdf"):
                        doc_ctx=f"PDF: {doc_up.name}"
                        try:
                            import pdfplumber
                            with pdfplumber.open(doc_up) as pdf:
                                doc_ctx="PDF Content:\n"+"".join([p.extract_text() or "" for p in pdf.pages[:10]])[:8000]
                        except: pass
                    st.success(f"✓ Loaded: {doc_up.name}")
                except Exception as e: st.error(f"Could not read: {e}")
            mt=st.selectbox("Memo Type",["Full IB Memo","Executive Summary","Risk Analysis","Investment Thesis"],key="memo_type")
            if st.button("◈ GENERATE MEMO",key="gen_memo"):
                with st.spinner("Generating memo..."):
                    ctx=doc_ctx if doc_ctx else f"Analyze {ib_t} as an IB target using public knowledge."
                    prompt=f"""You are a senior Goldman Sachs banker writing a {mt}.
Company/Document: {ib_t}
{ctx[:6000]}
Write a professional structured memo with: Company Overview, Financial Highlights, Investment Thesis, Key Risks (3-5), Valuation Perspective, Recommendation. Be specific with numbers."""
                    st.session_state.ib_memo=ask_ai([{"role":"user","content":prompt}],
                        "You are a senior Goldman Sachs investment banker writing professional memos.",st.session_state.api_key)
            if st.session_state.ib_memo:
                st.markdown(f'<div class="chat-ai" style="max-width:100%;white-space:pre-wrap;margin-top:12px">{st.session_state.ib_memo}</div>', unsafe_allow_html=True)
                st.download_button("⬇ Download Memo",data=st.session_state.ib_memo,file_name=f"gekko_memo_{ib_t}.txt",mime="text/plain",key="dl_memo")

# ══════════════════════════════════════════════════════
# PAGE: FINANCIALS
# ══════════════════════════════════════════════════════
elif page=="Financials":
    st.markdown('<div class="gk-page-title">Financials</div><div class="gk-page-sub">Financial Statements · Upload Documents</div>', unsafe_allow_html=True)
    fc1,fc2=st.columns([2,3])
    with fc1: fp=st.selectbox("From portfolio",["— enter below —"]+tickers,key="fin_port")
    with fc2: fc=st.text_input("Or any ticker","",placeholder="AAPL, MSFT...",key="fin_cust").upper().strip()
    fin_t=fc if fc else (fp if fp!="— enter below —" else (tickers[0] if tickers else ""))
    if fin_t and st.button("◈ FETCH STATEMENTS",key="fetch_fins"):
        fins=get_fins(fin_t)
        ft1,ft2,ft3=st.tabs(["INCOME STATEMENT","BALANCE SHEET","CASH FLOW"])
        with ft1:
            if fins.get("income") is not None and not fins["income"].empty: st.dataframe(fins["income"],use_container_width=True)
        with ft2:
            if fins.get("balance") is not None and not fins["balance"].empty: st.dataframe(fins["balance"],use_container_width=True)
        with ft3:
            if fins.get("cashflow") is not None and not fins["cashflow"].empty: st.dataframe(fins["cashflow"],use_container_width=True)
    st.markdown('<div class="gk-section">Upload Your Own Document</div>', unsafe_allow_html=True)
    st.markdown("""<div class="teach"><strong>Source files from:</strong> SEC EDGAR (sec.gov), company investor relations, or Bloomberg exports.</div>""", unsafe_allow_html=True)
    up=st.file_uploader("CSV or Excel",type=["csv","xlsx","xls"],key="fin_upload")
    if up:
        try:
            df_up=pd.read_csv(up) if up.name.endswith(".csv") else pd.read_excel(up)
            st.dataframe(df_up,use_container_width=True)
            st.success(f"✓ {len(df_up)} rows × {len(df_up.columns)} columns")
        except Exception as e: st.error(f"Could not read: {e}")

# ══════════════════════════════════════════════════════
# PAGE: AI ADVISOR
# ══════════════════════════════════════════════════════
elif page=="AI Advisor":
    st.markdown('<div class="gk-page-title">AI Advisor</div><div class="gk-page-sub">Powered by Claude · Knows your portfolio · Teaches as it advises</div>', unsafe_allow_html=True)
    if not st.session_state.api_key:
        st.markdown("""<div class="teach"><strong>🔑 Activate AI Advisor</strong> — Go to <strong>Manage Portfolio → AI Key & Settings</strong> and add your Anthropic API key.<br>
        Get a free key at <strong>console.anthropic.com</strong> in 2 minutes.</div>""", unsafe_allow_html=True)
    else:
        quick_qs=["Analyze my portfolio risk","Which holding has best upside?","Am I well diversified?",
            "Explain Sharpe Ratio simply","Explain DCF in plain English","What is WACC?",
            "What's my riskiest position?","Build me a portfolio strategy","How do T-bills reduce risk?",
            "Explain beta vs volatility","What is a control premium?","Teach me semiconductor supply chain"]
        st.markdown('<div style="font-size:10px;letter-spacing:2px;color:#8a7560;text-transform:uppercase;margin-bottom:8px">Quick Questions</div>', unsafe_allow_html=True)
        for row_qs in [quick_qs[:4],quick_qs[4:8],quick_qs[8:]]:
            cols=st.columns(4)
            for i,q in enumerate(row_qs):
                with cols[i]:
                    if st.button(q,key=f"qq_{q[:20]}",use_container_width=True):
                        st.session_state.chat_history.append({"role":"user","content":q})
                        with st.spinner(""):
                            reply=ask_ai([{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history],
                                SYSTEM_PROMPT+f"\n\n{portfolio_ctx()}",st.session_state.api_key)
                        st.session_state.chat_history.append({"role":"assistant","content":reply}); st.rerun()
        st.markdown("<br>",unsafe_allow_html=True)
        if not st.session_state.chat_history:
            st.markdown("""<div class="chat-wrap" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
              <div style="font-family:'Cormorant Garamond',serif;font-size:42px;color:#c9a84c">🦎</div>
              <div style="font-size:13px;color:#8a7560;margin-top:12px;text-align:center;max-width:360px;line-height:1.8">
                Ask anything about your portfolio, financial concepts, or investment strategy.<br>
                <span style="color:#c9a84c">I know your holdings and I'll teach you as I advise.</span></div>
            </div>""", unsafe_allow_html=True)
        else:
            msgs="".join([f'<div class="chat-lbl" style="{"text-align:right" if m["role"]=="user" else ""}">{"You" if m["role"]=="user" else "🦎 Gekko AI"}</div><div class="{"chat-user" if m["role"]=="user" else "chat-ai"}">{m["content"]}</div>' for m in st.session_state.chat_history])
            st.markdown(f'<div class="chat-wrap">{msgs}</div>', unsafe_allow_html=True)
        ic,bc=st.columns([5,1])
        with ic: user_in=st.text_input("Ask Gekko anything...",placeholder="e.g. Should I add T-bills to balance my semiconductor exposure?",key="chat_in",label_visibility="collapsed")
        with bc: send=st.button("SEND ▶",use_container_width=True,key="send_btn")
        if send and user_in:
            st.session_state.chat_history.append({"role":"user","content":user_in})
            with st.spinner(""):
                reply=ask_ai([{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history],
                    SYSTEM_PROMPT+f"\n\n{portfolio_ctx()}",st.session_state.api_key)
            st.session_state.chat_history.append({"role":"assistant","content":reply}); st.rerun()
        if st.session_state.chat_history:
            if st.button("Clear conversation",key="clear_chat"): st.session_state.chat_history=[]; st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
