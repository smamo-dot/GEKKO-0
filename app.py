import streamlit as st

st.set_page_config(
    page_title="Gekko — Finance Intelligence",
    page_icon="🦎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --cream:   #faf6ef;
    --cream2:  #f3ede2;
    --cream3:  #ede4d3;
    --gold:    #c9a84c;
    --gold2:   #e8c97a;
    --gold3:   #7a5c1e;
    --olive:   #5c6b3a;
    --brown:   #6b4f2e;
    --brown2:  #3d2b10;
    --text:    #2c1f0e;
    --muted:   #8a7560;
    --border:  #d4c4a8;
    --pos:     #3d6b3a;
    --neg:     #b84c3a;
    --surface: #f7f0e4;
}

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background: var(--cream);
    color: var(--text);
}
.stApp {
    background: var(--cream);
    background-image:
        radial-gradient(ellipse at 15% 0%, rgba(201,168,76,0.1) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 100%, rgba(92,107,58,0.07) 0%, transparent 55%);
}

/* Sidebar */
[data-testid="stSidebar"] { background: var(--brown2) !important; border-right: 1px solid rgba(201,168,76,0.25); }
[data-testid="stSidebar"] * { color: #f3ede2 !important; }
[data-testid="stSidebar"] .stTextInput>div>div>input,
[data-testid="stSidebar"] .stNumberInput>div>div>input,
[data-testid="stSidebar"] .stSelectbox>div>div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    color: #f3ede2 !important; border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stSidebar"] .stButton>button {
    background: var(--gold) !important; color: var(--brown2) !important;
    border: none !important; border-radius: 6px; font-size: 11px; letter-spacing: 1px; font-weight: 500;
}
[data-testid="stSidebar"] .stButton>button:hover { background: var(--gold2) !important; }

/* Buttons */
.stButton>button {
    background: transparent; border: 1px solid var(--gold); color: var(--gold3);
    border-radius: 6px; font-family: 'DM Mono', monospace; font-size: 11px;
    letter-spacing: 1px; transition: all 0.2s; padding: 8px 20px;
}
.stButton>button:hover { background: var(--gold); color: var(--brown2); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--cream2); border-radius: 8px; padding: 4px;
    gap: 2px; border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--muted); border-radius: 6px;
    font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: 1px; padding: 8px 14px;
}
.stTabs [aria-selected="true"] { background: var(--gold) !important; color: var(--brown2) !important; font-weight: 500; }

/* Inputs */
.stTextInput>div>div>input, .stNumberInput>div>div>input,
.stSelectbox>div>div, .stTextArea>div>div>textarea {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    color: var(--text) !important; border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important; font-size: 13px !important;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: var(--gold) !important; box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

/* Cards */
.gk-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px 24px; position: relative; overflow: hidden;
}
.gk-card::after {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--gold), transparent);
}
.gk-label { font-size:10px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-bottom:8px; }
.gk-value { font-family:'Cormorant Garamond',serif; font-size:34px; font-weight:600; color:var(--text); line-height:1; }
.gk-sub { font-size:12px; margin-top:6px; }
.pos { color: var(--pos); } .neg { color: var(--neg); } .gold { color: var(--gold); }

/* Section headers */
.gk-section {
    font-size:10px; letter-spacing:3px; text-transform:uppercase; color:var(--gold3);
    padding-bottom:10px; border-bottom:1px solid var(--border); margin:24px 0 16px 0;
}

/* Stock rows */
.gk-row {
    background: var(--surface); border: 1px solid var(--border); border-radius:10px;
    padding:14px 20px; margin:5px 0; display:flex; align-items:center;
    justify-content:space-between; transition: border-color 0.2s;
}
.gk-row:hover { border-color: var(--gold); }

/* Chat */
.chat-wrap {
    background: var(--surface); border: 1px solid var(--border); border-radius:14px;
    padding: 20px; min-height: 420px; max-height: 520px; overflow-y: auto;
    margin-bottom: 12px;
}
.chat-user {
    background: var(--gold); color: var(--brown2); border-radius:14px 14px 2px 14px;
    padding:12px 16px; margin:10px 0 10px auto; max-width:75%;
    font-size:13px; line-height:1.6; width:fit-content;
}
.chat-ai {
    background: var(--cream2); border:1px solid var(--border); border-radius:14px 14px 14px 2px;
    padding:14px 18px; margin:10px auto 10px 0; max-width:88%;
    font-size:13px; line-height:1.8; color: var(--text);
}
.chat-ai strong { color: var(--gold3); }
.chat-name-user { font-size:9px; letter-spacing:2px; color:var(--brown); text-align:right; margin-bottom:4px; text-transform:uppercase; }
.chat-name-ai { font-size:9px; letter-spacing:2px; color:var(--gold); margin-bottom:4px; text-transform:uppercase; }
.chat-empty {
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    height:300px; color:var(--muted);
}

/* Teach bubble */
.teach-bubble {
    background: rgba(201,168,76,0.08); border:1px solid rgba(201,168,76,0.3);
    border-radius:10px; padding:14px 18px; margin:12px 0; font-size:12px;
    line-height:1.7; color:var(--brown);
}
.teach-bubble strong { color:var(--gold3); }

/* Title */
.gk-title { font-family:'Cormorant Garamond',serif; font-size:56px; font-weight:300; letter-spacing:-2px; color:var(--brown2); line-height:1; }
.gk-title em { color:var(--gold); font-style:italic; }

/* File uploader */
[data-testid="stFileUploader"] {
    background:var(--surface); border:2px dashed var(--border); border-radius:12px; padding:16px;
}

/* Dataframe */
.stDataFrame { border:1px solid var(--border); border-radius:10px; overflow:hidden; }

/* Hide branding */
#MainMenu, footer, header { visibility:hidden; }
hr { border-color:var(--border); }

/* Expander */
details { background:var(--surface); border:1px solid var(--border) !important; border-radius:8px !important; }
summary { font-family:'DM Mono',monospace; font-size:12px; color:var(--text); padding:12px !important; }

/* Slider */
.stSlider>div>div>div>div { background:var(--gold) !important; }
</style>
""", unsafe_allow_html=True)

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import requests, json, datetime, io
import warnings
warnings.filterwarnings('ignore')

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(243,237,226,0.5)",
    font=dict(family="DM Mono", color="#8a7560", size=11),
    xaxis=dict(gridcolor="#d4c4a8", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="#d4c4a8", showgrid=True, zeroline=False),
    margin=dict(t=30,b=30,l=10,r=10),
    colorway=["#c9a84c","#5c6b3a","#6b4f2e","#8a9e5a","#3d2b10","#e8c97a","#b84c3a","#a0896a"],
)

DEFAULT_SECTORS = {
    "Semiconductor Equipment": {"tickers":["ASML","AMAT","LRCX","KLAC"],"color":"#c9a84c"},
    "Semiconductor Materials":  {"tickers":["ENTG","APD","LIN"],"color":"#5c6b3a"},
    "Chip Components":          {"tickers":["ADI","TXN","MRVL","AVGO"],"color":"#6b4f2e"},
    "Battery Materials":        {"tickers":["ALB","SQM"],"color":"#8a9e5a"},
    "Critical Metals":          {"tickers":["BHP"],"color":"#a0896a"},
}

# Session state
for key, default in [
    ("portfolio", {t:{"sector":s,"shares":0.0,"avg_cost":0.0} for s,d in DEFAULT_SECTORS.items() for t in d["tickers"]}),
    ("chat_history", []),
    ("api_key", ""),
    ("chat_context", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Data helpers ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_prices(tickers):
    prices,changes = {},{}
    for t in tickers:
        try:
            fi=yf.Ticker(t).fast_info
            prices[t]=fi.last_price
            prev=fi.previous_close
            changes[t]=((fi.last_price-prev)/prev*100) if prev else 0
        except: prices[t]=None; changes[t]=0
    return prices,changes

@st.cache_data(ttl=300)
def get_hist(tickers, period="1y"):
    if not tickers: return pd.DataFrame()
    try:
        raw=yf.download(tickers,period=period,auto_adjust=True,progress=False)
        close=raw["Close"] if isinstance(raw.columns,pd.MultiIndex) else raw
        return close.dropna(how="all")
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_info(ticker):
    try: return yf.Ticker(ticker).info
    except: return {}

@st.cache_data(ttl=3600)
def get_financials(ticker):
    try:
        tk=yf.Ticker(ticker)
        return {"income":tk.financials,"balance":tk.balance_sheet,"cashflow":tk.cashflow,"info":tk.info}
    except: return {}

def fmv(v, prefix="$", decimals=1):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    if abs(v)>=1e12: return f"{prefix}{v/1e12:.{decimals}f}T"
    if abs(v)>=1e9:  return f"{prefix}{v/1e9:.{decimals}f}B"
    if abs(v)>=1e6:  return f"{prefix}{v/1e6:.{decimals}f}M"
    return f"{prefix}{v:,.{decimals}f}"

def fpct(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    return f"{v*100:.1f}%"

# ── AI Chat helper ────────────────────────────────────────────────────────────
def ask_claude(messages, system_prompt, api_key):
    headers = {"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"}
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": messages
    }
    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
        else:
            return f"API error {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return f"Connection error: {str(e)}"

def build_portfolio_context():
    tickers = list(st.session_state.portfolio.keys())
    if not tickers: return "No portfolio holdings yet."
    try:
        prices,changes = get_prices(tickers)
        lines = ["Current Portfolio Holdings:"]
        for t,d in st.session_state.portfolio.items():
            p = prices.get(t); chg = changes.get(t,0)
            val = (p or 0)*d["shares"]
            lines.append(f"  {t} | Sector: {d['sector']} | Shares: {d['shares']} | Price: ${p:,.2f} if p else N/A | Day Change: {chg:+.2f}% | Value: ${val:,.0f}")
        return "\n".join(lines)
    except:
        return "Portfolio data temporarily unavailable."

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 16px 0">
        <div style="font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:600;color:#e8c97a;letter-spacing:-0.5px">🦎 Gekko</div>
        <div style="font-size:9px;letter-spacing:3px;color:rgba(243,237,226,0.4);text-transform:uppercase;margin-top:2px">Finance Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    with st.expander("🔑 AI Advisor Key"):
        st.markdown('<div style="font-size:11px;color:rgba(243,237,226,0.5);margin-bottom:8px">Get yours at console.anthropic.com</div>', unsafe_allow_html=True)
        k = st.text_input("Anthropic API Key", value=st.session_state.api_key, type="password", placeholder="sk-ant-...")
        if k != st.session_state.api_key:
            st.session_state.api_key = k
            st.success("✓ Key saved")

    with st.expander("➕ Add Stock"):
        nt = st.text_input("Ticker Symbol", placeholder="NVDA").upper().strip()
        ns = st.selectbox("Sector", list(DEFAULT_SECTORS.keys())+["Other"], key="new_sector")
        nsh = st.number_input("Shares", min_value=0.0, value=0.0, step=0.1, key="new_shares")
        nc = st.number_input("Avg Cost ($)", min_value=0.0, value=0.0, step=0.01, key="new_cost")
        if st.button("ADD STOCK", use_container_width=True):
            if nt:
                st.session_state.portfolio[nt] = {"sector":ns,"shares":nsh,"avg_cost":nc}
                st.success(f"✓ {nt} added"); st.rerun()

    with st.expander("✏️ Edit / Remove"):
        if st.session_state.portfolio:
            et = st.selectbox("Stock", list(st.session_state.portfolio.keys()), key="edit_t")
            cur = st.session_state.portfolio[et]
            esh = st.number_input("Shares", value=float(cur["shares"]), step=0.1, key="esh")
            eco = st.number_input("Avg Cost", value=float(cur["avg_cost"]), step=0.01, key="eco")
            c1,c2 = st.columns(2)
            with c1:
                if st.button("SAVE",use_container_width=True,key="save_b"):
                    st.session_state.portfolio[et].update({"shares":esh,"avg_cost":eco}); st.rerun()
            with c2:
                if st.button("REMOVE",use_container_width=True,key="rem_b"):
                    del st.session_state.portfolio[et]; st.rerun()

    st.markdown("---")
    sectors_map = {}
    for t,d in st.session_state.portfolio.items():
        sectors_map.setdefault(d["sector"],[]).append(t)
    for sec,ts in sectors_map.items():
        color = DEFAULT_SECTORS.get(sec,{}).get("color","#c9a84c")
        st.markdown(f'<div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{color};margin:12px 0 4px 0">{sec}</div>', unsafe_allow_html=True)
        for t in ts:
            sh = st.session_state.portfolio[t]["shares"]
            st.markdown(f'<div style="font-size:11px;color:rgba(243,237,226,0.55);padding-left:8px">→ {t} <span style="color:rgba(243,237,226,0.25)">({sh:.1f} sh)</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    period = st.select_slider("Chart Period",["1mo","3mo","6mo","1y","2y"],value="1y")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:28px">
    <div>
        <div class="gk-title">Gekko <em>Finance</em></div>
        <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#8a7560;margin-top:6px">
            Portfolio · Quant · Investment Banking · AI Advisor
        </div>
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:13px;color:#8a7560;text-align:right;padding-bottom:8px">
        "Greed, for lack of a better word, is good."<br>
        <span style="color:#c9a84c">— Gordon Gekko</span>
    </div>
</div>
""", unsafe_allow_html=True)

tickers = list(st.session_state.portfolio.keys())
if not tickers:
    st.info("Add stocks from the sidebar to begin."); st.stop()

with st.spinner(""):
    prices, changes = get_prices(tickers)
    hist = get_hist(tickers, period)
    hist_1y = get_hist(tickers, "1y")

total_value = sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in tickers)
total_cost  = sum(
    st.session_state.portfolio[t]["avg_cost"]*st.session_state.portfolio[t]["shares"]
    if st.session_state.portfolio[t]["avg_cost"]>0
    else (prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]
    for t in tickers
)
total_pnl = total_value - total_cost
pnl_pct = (total_pnl/total_cost*100) if total_cost>0 else 0
day_chg = sum((prices.get(t,0) or 0)*st.session_state.portfolio[t]["shares"]*(changes.get(t,0)/100) for t in tickers)

k1,k2,k3,k4 = st.columns(4)
best_t = max(tickers,key=lambda t:changes.get(t,0)) if tickers else "—"
for col,(lbl,val,sub,cls) in zip([k1,k2,k3,k4],[
    ("Portfolio Value",f"${total_value:,.0f}",f"{'▲' if day_chg>=0 else '▼'} ${abs(day_chg):,.0f} today","pos" if day_chg>=0 else "neg"),
    ("Total P&L",f"{'+'if total_pnl>=0 else ''}{pnl_pct:.1f}%",f"${total_pnl:+,.0f}","pos" if total_pnl>=0 else "neg"),
    ("Holdings",str(len(tickers)),f"{len(sectors_map)} sectors","gold"),
    ("Best Today",best_t,f"+{changes.get(best_t,0):.2f}%","pos"),
]):
    col.markdown(f"""
    <div class="gk-card">
        <div class="gk-label">{lbl}</div>
        <div class="gk-value">{val}</div>
        <div class="gk-sub {cls}">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
    "◈ DASHBOARD","📈 PERFORMANCE","🧮 QUANT","🎲 MONTE CARLO",
    "🏦 IB MODELS","📁 FINANCIALS","🤖 AI ADVISOR"
])

# ══════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([3,2])
    with col_l:
        st.markdown('<div class="gk-section">Live Holdings</div>', unsafe_allow_html=True)
        for sec,ts in sectors_map.items():
            color = DEFAULT_SECTORS.get(sec,{}).get("color","#c9a84c")
            st.markdown(f'<div style="color:{color};font-size:9px;letter-spacing:2px;text-transform:uppercase;margin:16px 0 6px 0">{sec}</div>', unsafe_allow_html=True)
            for t in ts:
                p=prices.get(t); chg=changes.get(t,0)
                shares=st.session_state.portfolio[t]["shares"]
                val=(p or 0)*shares
                clr="#3d6b3a" if chg>=0 else "#b84c3a"
                arr="▲" if chg>=0 else "▼"
                st.markdown(f"""
                <div class="gk-row">
                    <div>
                        <span style="font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600">{t}</span>
                        <span style="color:#8a7560;font-size:11px;margin-left:8px">{shares:.1f} sh</span>
                    </div>
                    <div style="text-align:center">
                        <div style="font-size:16px;font-weight:500">${p:,.2f if p else "N/A"}</div>
                        <div style="color:{clr};font-size:11px">{arr} {chg:+.2f}%</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:10px;color:#8a7560">VALUE</div>
                        <div style="font-size:15px;font-weight:500">${val:,.0f}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="gk-section">Sector Allocation</div>', unsafe_allow_html=True)
        alloc={}
        for t in tickers:
            sec=st.session_state.portfolio[t]["sector"]
            alloc[sec]=alloc.get(sec,0)+(prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]
        colors=[DEFAULT_SECTORS.get(s,{}).get("color","#c9a84c") for s in alloc]
        fig=go.Figure(go.Pie(
            labels=list(alloc.keys()),values=list(alloc.values()),
            hole=0.55,marker_colors=colors,
            textinfo="label+percent",textfont=dict(family="DM Mono",size=10),
        ))
        fig.update_layout(**{**PLOT,"height":280,"showlegend":False,
            "annotations":[dict(text="ALLOC",x=0.5,y=0.5,font=dict(size=11,color="#8a7560"),showarrow=False)]})
        st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="gk-section">Today\'s Movers</div>', unsafe_allow_html=True)
        for t in sorted(tickers,key=lambda x:changes.get(x,0),reverse=True)[:8]:
            chg=changes.get(t,0)
            bc="#5c6b3a" if chg>=0 else "#b84c3a"
            bw=min(abs(chg)*10,100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:6px 0">
                <span style="font-size:11px;width:46px;font-weight:500">{t}</span>
                <div style="flex:1;background:#ede4d3;border-radius:3px;height:6px">
                    <div style="width:{bw}%;background:{bc};height:6px;border-radius:3px"></div>
                </div>
                <span style="font-size:11px;color:{bc};width:58px;text-align:right">{chg:+.2f}%</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB 2 — PERFORMANCE
# ══════════════════════════════════════════════════
with tab2:
    valid=[t for t in tickers if not hist.empty and t in hist.columns]
    if valid:
        norm=hist[valid]/hist[valid].iloc[0]*100
        fig=go.Figure()
        for t in valid:
            color=DEFAULT_SECTORS.get(st.session_state.portfolio[t]["sector"],{}).get("color","#c9a84c")
            fig.add_trace(go.Scatter(x=norm.index,y=norm[t],name=t,
                line=dict(color=color,width=2),
                hovertemplate=f"<b>{t}</b> %{{y:.1f}}<extra></extra>"))
        fig.update_layout(**{**PLOT,"height":420,"yaxis_title":"Indexed (100=start)","hovermode":"x unified",
            "legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10))})
        st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="gk-section">Returns Summary</div>', unsafe_allow_html=True)
        rows=[]
        for t in valid:
            s=hist[t].dropna()
            if len(s)<2: continue
            dr=s.pct_change().dropna()
            rows.append({"Ticker":t,"Sector":st.session_state.portfolio[t]["sector"],
                "Period Return":f"{(s.iloc[-1]/s.iloc[0]-1)*100:+.1f}%",
                "1M":f"{(s.iloc[-1]/s.iloc[-min(21,len(s))]-1)*100:+.1f}%",
                "3M":f"{(s.iloc[-1]/s.iloc[-min(63,len(s))]-1)*100:+.1f}%",
                "Volatility":f"{dr.std()*np.sqrt(252)*100:.1f}%",
                "Price":f"${prices.get(t,0):,.2f}" if prices.get(t) else "N/A"})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════
# TAB 3 — QUANT
# ══════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="teach-bubble">
        <strong>📚 What is Quant Analysis?</strong><br>
        Quantitative analysis uses math and statistics to evaluate investments. 
        <strong>Sharpe Ratio</strong> measures return per unit of risk (higher = better, above 1.0 is good). 
        <strong>Beta</strong> measures how much a stock moves relative to the market (beta of 1.2 = moves 20% more than market). 
        <strong>Max Drawdown</strong> is the worst peak-to-trough drop. <strong>VaR</strong> = Value at Risk, the worst expected daily loss 95% of the time.
    </div>
    """, unsafe_allow_html=True)

    valid1y=[t for t in tickers if not hist_1y.empty and t in hist_1y.columns]
    if valid1y:
        dr=hist_1y[valid1y].pct_change().dropna()
        spy=get_hist(["SPY"],"1y")
        spy_r=spy["SPY"].pct_change().dropna() if "SPY" in spy.columns else None

        rows=[]
        for t in valid1y:
            r=dr[t].dropna()
            if len(r)<10: continue
            ann_r=r.mean()*252*100; ann_v=r.std()*np.sqrt(252)*100
            sharpe=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
            cum=(1+r).cumprod(); mdd=((cum-cum.cummax())/cum.cummax()).min()*100
            beta=None
            if spy_r is not None:
                idx=r.index.intersection(spy_r.index)
                if len(idx)>30: beta,_,_,_,_=stats.linregress(spy_r.loc[idx],r.loc[idx])
            var95=np.percentile(r,5)*100
            rows.append({"Ticker":t,"Ann. Return":f"{ann_r:+.1f}%","Ann. Vol":f"{ann_v:.1f}%",
                "Sharpe":f"{sharpe:.2f}","Max DD":f"{mdd:.1f}%",
                "Beta":f"{beta:.2f}" if beta else "—","VaR 95%":f"{var95:.2f}%"})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

        if len(valid1y)>1:
            st.markdown('<div class="gk-section">Correlation Matrix</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="teach-bubble">
                <strong>📚 Correlation Matrix</strong> — Shows how stocks move together. 
                <strong>1.0</strong> = move in perfect sync. <strong>-1.0</strong> = move in opposite directions. 
                <strong>0</strong> = no relationship. For diversification, you WANT low correlation between holdings.
            </div>""", unsafe_allow_html=True)
            corr=dr[valid1y].corr()
            fig=go.Figure(go.Heatmap(
                z=corr.values,x=corr.columns,y=corr.index,
                colorscale=[[0,"#b84c3a"],[0.5,"#ede4d3"],[1,"#5c6b3a"]],
                zmin=-1,zmax=1,text=np.round(corr.values,2),
                texttemplate="%{text}",textfont=dict(size=9,family="DM Mono")))
            fig.update_layout(**{**PLOT,"height":380})
            st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="gk-section">DuPont Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 DuPont Pyramid</strong> — Breaks down Return on Equity (ROE) into 3 drivers: 
            <strong>Net Margin</strong> (how much profit per dollar of sales) × 
            <strong>Asset Turnover</strong> (how efficiently assets generate sales) × 
            <strong>Equity Multiplier</strong> (financial leverage). Understanding which driver is powering ROE reveals the quality of returns.
        </div>""", unsafe_allow_html=True)
        dp_t=st.selectbox("Stock for DuPont",valid1y,key="dp_sel")
        info=get_info(dp_t)
        roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets")
        pm=info.get("profitMargins"); at=info.get("assetTurnover")
        lev=(roe/roa) if roe and roa and roa!=0 else None
        cols=st.columns(5)
        for col,(lbl,val) in zip(cols,[("ROE",fpct(roe)),("Net Margin",fpct(pm)),
            ("Asset Turnover",f"{at:.2f}x" if at else "—"),("ROA",fpct(roa)),
            ("Equity Multiplier",f"{lev:.2f}x" if lev else "—")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px">{val}</div></div>',unsafe_allow_html=True)

        st.markdown('<div class="gk-section">Horizontal Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 Horizontal Analysis</strong> — Tracks how stock price has changed over different time horizons. 
            This helps identify momentum and trend direction. A stock up 40% over 1Y but down 5% in 1M may be losing momentum.
        </div>""", unsafe_allow_html=True)
        hrows=[]
        for t in valid1y:
            s=hist_1y[t].dropna(); row={"Ticker":t}
            for lbl,d in {"1W":5,"1M":21,"3M":63,"6M":126,"1Y":252}.items():
                row[lbl]=f"{(s.iloc[-1]/s.iloc[-min(d,len(s))]-1)*100:+.1f}%" if len(s)>d else "—"
            hrows.append(row)
        st.dataframe(pd.DataFrame(hrows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════
# TAB 4 — MONTE CARLO
# ══════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="teach-bubble">
        <strong>📚 Monte Carlo Simulation</strong> — Runs thousands of possible future scenarios for your portfolio 
        using historical volatility and returns. It's like asking "if history repeated itself in random ways, 
        what range of outcomes would I get?" The result gives you a probability distribution — 
        not a prediction, but a range of realistic possibilities with their likelihoods.
    </div>""", unsafe_allow_html=True)

    mc1,mc2,mc3=st.columns(3)
    with mc1: n_sim=st.select_slider("Simulations",[500,1000,2000,5000],value=1000)
    with mc2: n_days=st.select_slider("Forecast Days",[30,60,90,180,252],value=252)
    with mc3: run_mc=st.button("▶ RUN SIMULATION",use_container_width=True)

    valid1y_mc=[t for t in tickers if not hist_1y.empty and t in hist_1y.columns]
    if run_mc and valid1y_mc:
        with st.spinner("Running simulations..."):
            dr_mc=hist_1y[valid1y_mc].pct_change().dropna()
            pv={t:(prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in valid1y_mc}
            tv=sum(pv.values())
            w=np.array([pv[t]/tv if tv>0 else 1/len(valid1y_mc) for t in valid1y_mc])
            port_r=dr_mc[valid1y_mc].values@w
            mu,sigma=port_r.mean(),port_r.std()

            np.random.seed(42)
            sims=np.zeros((n_days,n_sim))
            for i in range(n_sim):
                sims[:,i]=total_value*np.cumprod(1+np.random.normal(mu,sigma,n_days))

            finals=sims[-1,:]
            pcts={k:np.percentile(finals,v) for k,v in {"p5":5,"p25":25,"p50":50,"p75":75,"p95":95}.items()}

            fig=go.Figure()
            for i in range(min(150,n_sim)):
                fig.add_trace(go.Scatter(y=sims[:,i],mode="lines",
                    line=dict(color="rgba(201,168,76,0.04)",width=1),showlegend=False,hoverinfo="skip"))
            for lbl,p,clr in [("Bull 95th",pcts["p95"],"#5c6b3a"),("Median",pcts["p50"],"#c9a84c"),("Bear 5th",pcts["p5"],"#b84c3a")]:
                idx=np.argmin(np.abs(sims[-1,:]-p))
                fig.add_trace(go.Scatter(y=sims[:,idx],mode="lines",name=f"{lbl}: ${p:,.0f}",line=dict(color=clr,width=2.5)))
            fig.update_layout(**{**PLOT,"height":420,
                "yaxis":dict(gridcolor="#d4c4a8",tickprefix="$",tickformat=",.0f"),
                "legend":dict(bgcolor="rgba(0,0,0,0)")})
            st.plotly_chart(fig,use_container_width=True)

            cols5=st.columns(5)
            for col,(lbl,p,clr) in zip(cols5,[
                ("Bear (5%)",pcts["p5"],"#b84c3a"),("25th",pcts["p25"],"#a0896a"),
                ("Median",pcts["p50"],"#c9a84c"),("75th",pcts["p75"],"#5c6b3a"),("Bull (95%)",pcts["p95"],"#3d6b3a")]):
                chg=(p-total_value)/total_value*100 if total_value>0 else 0
                col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px;color:{clr}">${p:,.0f}</div><div class="gk-sub" style="color:{clr}">{chg:+.1f}%</div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB 5 — IB MODELS
# ══════════════════════════════════════════════════
with tab5:
    ib_t=st.selectbox("Select Company for Analysis",tickers,key="ib_sel")
    ib1,ib2,ib3,ib4,ib5=st.tabs(["DCF MODEL","COMPS ANALYSIS","PRECEDENT TXN","LBO MODEL","RATIO ANALYSIS"])

    with ib1:
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 DCF — Discounted Cash Flow</strong><br>
            The DCF is the gold standard of intrinsic valuation. The idea: a company is worth the sum of all its 
            future cash flows, discounted back to today's dollars. <strong>WACC</strong> = your discount rate (cost of capital). 
            <strong>Terminal Growth Rate</strong> = how fast cash flows grow forever after year 5. 
            If intrinsic value > current price → potentially undervalued.
        </div>""", unsafe_allow_html=True)

        info=get_info(ib_t)
        dc1,dc2,dc3,dc4=st.columns(4)
        with dc1: wacc=st.number_input("WACC (%)",value=10.0,step=0.5,key="wacc")/100
        with dc2: g5=st.number_input("5Y Revenue Growth (%)",value=8.0,step=0.5,key="g5")/100
        with dc3: tg=st.number_input("Terminal Growth (%)",value=2.5,step=0.5,key="tg")/100
        with dc4: fcf_margin=st.number_input("FCF Margin (%)",value=15.0,step=1.0,key="fcfm")/100

        if st.button("◈ CALCULATE INTRINSIC VALUE",key="run_dcf"):
            rev=info.get("totalRevenue"); shares_out=info.get("sharesOutstanding"); cur_p=prices.get(ib_t)
            if rev and shares_out:
                fcfs=[]; r=rev
                for yr in range(1,6):
                    r*=(1+g5); fcf=r*fcf_margin; pv_fcf=fcf/(1+wacc)**yr
                    fcfs.append({"Year":f"Year {yr}","Revenue":fmv(r),"FCF":fmv(fcf),"PV of FCF":fmv(pv_fcf),"_pv":pv_fcf})
                tv_fcf=fcfs[-1]["_pv"]*(1+tg)
                terminal=tv_fcf/(wacc-tg) if wacc>tg else 0
                pv_term=terminal/(1+wacc)**5
                total_pv_dcf=sum(r["_pv"] for r in fcfs)+pv_term
                intrinsic=total_pv_dcf/shares_out
                for r in fcfs: del r["_pv"]
                st.dataframe(pd.DataFrame(fcfs),use_container_width=True,hide_index=True)
                v1,v2,v3,v4=st.columns(4)
                mos=((intrinsic-(cur_p or 0))/intrinsic*100) if cur_p and intrinsic>0 else 0
                for col,(lbl,val,cls) in zip([v1,v2,v3,v4],[
                    ("PV Terminal Value",fmv(pv_term),"gold"),
                    ("Total Intrinsic Value",fmv(total_pv_dcf),"gold"),
                    ("Intrinsic Value / Share",f"${intrinsic:.2f}","gold"),
                    ("Margin of Safety",f"{mos:+.1f}%","pos" if mos>0 else "neg"),
                ]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px" class="{cls}">{val}</div></div>',unsafe_allow_html=True)
            else:
                st.warning("Could not fetch revenue data for this ticker.")

    with ib2:
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 Comparable Company Analysis (Comps)</strong><br>
            Valuing a company by comparing it to similar public companies using multiples like 
            <strong>EV/EBITDA</strong>, <strong>P/E</strong>, and <strong>EV/Revenue</strong>. 
            If peers trade at 15x EBITDA and your target trades at 10x, it might be undervalued — or there's a reason for the discount.
        </div>""", unsafe_allow_html=True)

        comps_input=st.text_input("Enter comparable tickers (comma separated)","NVDA,AMD,INTC,QCOM",key="comps_in")
        if st.button("◈ RUN COMPS",key="run_comps"):
            comp_tickers=[x.strip().upper() for x in comps_input.split(",") if x.strip()]
            all_t=list(set([ib_t]+comp_tickers))
            rows=[]
            for t in all_t:
                i=get_info(t)
                if not i: continue
                rows.append({
                    "Ticker":t,"Name":i.get("shortName","")[:25],
                    "Mkt Cap":fmv(i.get("marketCap")),
                    "EV/EBITDA":f"{i.get('enterpriseToEbitda',0):.1f}x" if i.get("enterpriseToEbitda") else "—",
                    "EV/Rev":f"{i.get('enterpriseToRevenue',0):.1f}x" if i.get("enterpriseToRevenue") else "—",
                    "P/E":f"{i.get('trailingPE',0):.1f}x" if i.get("trailingPE") else "—",
                    "P/S":f"{i.get('priceToSalesTrailing12Months',0):.1f}x" if i.get("priceToSalesTrailing12Months") else "—",
                    "Gross Margin":fpct(i.get("grossMargins")),
                    "Net Margin":fpct(i.get("profitMargins")),
                    "ROE":fpct(i.get("returnOnEquity")),
                })
            if rows:
                df=pd.DataFrame(rows)
                st.dataframe(df,use_container_width=True,hide_index=True)

    with ib3:
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 Precedent Transaction Analysis</strong><br>
            Looks at what acquirers paid for similar companies in past M&A deals. 
            These multiples typically include a <strong>control premium</strong> (20-40% above market price) 
            so they tend to be higher than comps. Useful for estimating acquisition value.
        </div>""", unsafe_allow_html=True)
        st.info("Enter deal data manually or use the auto-fetch below.")
        info=get_info(ib_t)
        ebitda=info.get("ebitda"); rev=info.get("totalRevenue")
        p1,p2=st.columns(2)
        with p1: low_ev_ebitda=st.number_input("Low EV/EBITDA Multiple",value=10.0,step=0.5,key="low_ev")
        with p2: high_ev_ebitda=st.number_input("High EV/EBITDA Multiple",value=18.0,step=0.5,key="high_ev")
        prem=st.slider("Control Premium (%)",0,50,25,key="prem")/100
        if st.button("◈ ESTIMATE TRANSACTION VALUE",key="run_prec"):
            shares_out=info.get("sharesOutstanding"); cur_p=prices.get(ib_t)
            if ebitda and shares_out:
                low_ev=ebitda*low_ev_ebitda; high_ev=ebitda*high_ev_ebitda
                net_debt=info.get("totalDebt",0)-(info.get("totalCash",0) or 0)
                low_eq=low_ev-net_debt; high_eq=high_ev-net_debt
                low_pp=low_eq/shares_out*(1+prem); high_pp=high_eq/shares_out*(1+prem)
                c1,c2,c3,c4=st.columns(4)
                for col,(lbl,val) in zip([c1,c2,c3,c4],[
                    ("Low Transaction Value",fmv(low_ev)),("High Transaction Value",fmv(high_ev)),
                    ("Low Price / Share",f"${low_pp:.2f}"),("High Price / Share",f"${high_pp:.2f}"),
                ]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>',unsafe_allow_html=True)
                if cur_p:
                    premium_paid=(high_pp-cur_p)/cur_p*100
                    st.markdown(f'<div class="teach-bubble">At current price of <strong>${cur_p:,.2f}</strong>, the high-end transaction value implies a premium of <strong>{premium_paid:+.1f}%</strong></div>',unsafe_allow_html=True)

    with ib4:
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 LBO — Leveraged Buyout Model</strong><br>
            A private equity firm buys a company using mostly debt (~60-70%), hoping to improve operations 
            and sell it in 5 years for a profit. The key metric is <strong>IRR (Internal Rate of Return)</strong> — 
            PE firms typically target 20%+ IRR. <strong>MOIC</strong> = Multiple on Invested Capital (how many times your money back).
        </div>""", unsafe_allow_html=True)

        info=get_info(ib_t)
        l1,l2,l3=st.columns(3)
        with l1:
            entry_ev_ebitda=st.number_input("Entry EV/EBITDA",value=12.0,step=0.5,key="lbo_entry")
            debt_pct=st.number_input("Debt % of EV",value=65.0,step=5.0,key="lbo_debt")/100
        with l2:
            exit_ev_ebitda=st.number_input("Exit EV/EBITDA",value=14.0,step=0.5,key="lbo_exit")
            ebitda_growth=st.number_input("Annual EBITDA Growth (%)",value=10.0,step=1.0,key="lbo_g")/100
        with l3:
            hold_years=st.number_input("Hold Period (Years)",value=5,min_value=1,max_value=10,step=1,key="lbo_yrs")
            int_rate=st.number_input("Interest Rate (%)",value=7.0,step=0.5,key="lbo_rate")/100

        if st.button("◈ RUN LBO MODEL",key="run_lbo"):
            ebitda=info.get("ebitda")
            if ebitda:
                entry_ev=ebitda*entry_ev_ebitda
                debt=entry_ev*debt_pct; equity=entry_ev*(1-debt_pct)
                exit_ebitda=ebitda*(1+ebitda_growth)**hold_years
                exit_ev=exit_ebitda*exit_ev_ebitda
                remaining_debt=debt*(0.7**hold_years)
                exit_equity=exit_ev-remaining_debt
                moic=exit_equity/equity if equity>0 else 0
                irr=(moic**(1/hold_years)-1)*100

                r1,r2,r3,r4=st.columns(4)
                for col,(lbl,val,cls) in zip([r1,r2,r3,r4],[
                    ("Entry EV",fmv(entry_ev),"gold"),("Exit EV",fmv(exit_ev),"gold"),
                    ("MOIC",f"{moic:.2f}x","pos" if moic>=2 else "neg"),
                    ("IRR",f"{irr:.1f}%","pos" if irr>=20 else "neg"),
                ]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:24px">{val}</div></div>',unsafe_allow_html=True)

                st.markdown(f"""
                <div class="teach-bubble">
                    Entry equity check of <strong>{fmv(equity)}</strong> on <strong>{fmv(entry_ev)}</strong> EV 
                    ({debt_pct*100:.0f}% debt). After {hold_years} years of {ebitda_growth*100:.0f}% EBITDA growth, 
                    exit at {exit_ev_ebitda}x for <strong>{fmv(exit_ev)}</strong>. 
                    IRR of <strong>{irr:.1f}%</strong> {'✅ meets PE target (20%+)' if irr>=20 else '⚠️ below typical PE target of 20%'}.
                </div>""", unsafe_allow_html=True)

    with ib5:
        st.markdown("""
        <div class="teach-bubble">
            <strong>📚 Financial Ratios</strong><br>
            <strong>Leverage Ratios</strong> measure how much debt a company has relative to earnings or equity.
            <strong>Performance Ratios</strong> measure how efficiently a company converts resources into profit.
            These are the core numbers every investment banker looks at first.
        </div>""", unsafe_allow_html=True)

        info=get_info(ib_t)
        st.markdown('<div class="gk-section">Leverage Ratios</div>', unsafe_allow_html=True)
        l1,l2,l3,l4=st.columns(4)
        de=info.get("debtToEquity"); cr=info.get("currentRatio"); qr=info.get("quickRatio")
        ic=info.get("ebitda",0)/(info.get("totalDebt",1) or 1)*info.get("interestCoverage",0) if info.get("ebitda") else None
        for col,(lbl,val,tip) in zip([l1,l2,l3,l4],[
            ("Debt/Equity",f"{de/100:.2f}x" if de else "—","<1x is conservative, >3x is aggressive"),
            ("Current Ratio",f"{cr:.2f}x" if cr else "—",">1x means can cover short-term debt"),
            ("Quick Ratio",f"{qr:.2f}x" if qr else "—",">1x is healthy liquidity"),
            ("Interest Coverage",f"{info.get('interestCoverage',0):.1f}x" if info.get("interestCoverage") else "—",">3x means comfortably covers interest"),
        ]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px">{val}</div><div class="gk-sub" style="color:#8a7560;font-size:10px">{tip}</div></div>',unsafe_allow_html=True)

        st.markdown('<div class="gk-section">Performance Ratios</div>', unsafe_allow_html=True)
        p1,p2,p3,p4=st.columns(4)
        for col,(lbl,val) in zip([p1,p2,p3,p4],[
            ("Gross Margin",fpct(info.get("grossMargins"))),
            ("Operating Margin",fpct(info.get("operatingMargins"))),
            ("Net Margin",fpct(info.get("profitMargins"))),
            ("Return on Equity",fpct(info.get("returnOnEquity"))),
        ]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px">{val}</div></div>',unsafe_allow_html=True)

        p5,p6,p7,p8=st.columns(4)
        for col,(lbl,val) in zip([p5,p6,p7,p8],[
            ("Return on Assets",fpct(info.get("returnOnAssets"))),
            ("Revenue",fmv(info.get("totalRevenue"))),
            ("EV/EBITDA",f"{info.get('enterpriseToEbitda',0):.1f}x" if info.get("enterpriseToEbitda") else "—"),
            ("P/E Ratio",f"{info.get('trailingPE',0):.1f}x" if info.get("trailingPE") else "—"),
        ]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px">{val}</div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# TAB 6 — FINANCIALS UPLOAD
# ══════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="gk-section">Auto-Fetch Financial Statements</div>', unsafe_allow_html=True)
    fin_t=st.selectbox("Select Ticker",tickers,key="fin_sel")
    if st.button("◈ FETCH FINANCIALS",key="fetch_fins"):
        fins=get_financials(fin_t)
        if fins:
            ft1,ft2,ft3=st.tabs(["INCOME STATEMENT","BALANCE SHEET","CASH FLOW"])
            with ft1:
                if fins.get("income") is not None and not fins["income"].empty:
                    st.dataframe(fins["income"].applymap(lambda x: fmv(x) if isinstance(x,(int,float)) else x),use_container_width=True)
            with ft2:
                if fins.get("balance") is not None and not fins["balance"].empty:
                    st.dataframe(fins["balance"].applymap(lambda x: fmv(x) if isinstance(x,(int,float)) else x),use_container_width=True)
            with ft3:
                if fins.get("cashflow") is not None and not fins["cashflow"].empty:
                    st.dataframe(fins["cashflow"].applymap(lambda x: fmv(x) if isinstance(x,(int,float)) else x),use_container_width=True)

    st.markdown('<div class="gk-section">Upload Your Own Financials (CSV / Excel)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="teach-bubble">
        <strong>📚 How to use this</strong> — Upload a company's balance sheet, income statement, or 10-K data 
        as CSV or Excel. Gekko will display and analyze it. You can get these files from 
        SEC EDGAR (sec.gov), company investor relations pages, or export from Bloomberg/FactSet.
    </div>""", unsafe_allow_html=True)
    uploaded=st.file_uploader("Drop CSV or Excel file here",type=["csv","xlsx","xls"])
    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df_up=pd.read_csv(uploaded)
            else:
                df_up=pd.read_excel(uploaded)
            st.dataframe(df_up,use_container_width=True)
            st.success(f"✓ Loaded {len(df_up)} rows × {len(df_up.columns)} columns")
        except Exception as e:
            st.error(f"Could not read file: {e}")

# ══════════════════════════════════════════════════
# TAB 7 — AI ADVISOR (INTERACTIVE CHAT)
# ══════════════════════════════════════════════════
with tab7:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
        <div style="font-family:'Cormorant Garamond',serif;font-size:28px;color:#c9a84c">🤖</div>
        <div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;color:#3d2b10">Gekko AI Advisor</div>
            <div style="font-size:10px;letter-spacing:2px;color:#8a7560;text-transform:uppercase">Powered by Claude · Knows your portfolio · Teaches as it advises</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.markdown("""
        <div class="teach-bubble">
            <strong>🔑 Add your Anthropic API key in the sidebar to activate the AI Advisor.</strong><br>
            Get a free key at <strong>console.anthropic.com</strong> — it takes 2 minutes. 
            Once added, you can ask me anything about your portfolio, get explanations of financial concepts, 
            request analysis of specific stocks, or have me walk you through IB models.
        </div>""", unsafe_allow_html=True)
    else:
        # Quick prompts
        st.markdown('<div style="font-size:10px;letter-spacing:2px;color:#8a7560;text-transform:uppercase;margin-bottom:8px">Quick Questions</div>', unsafe_allow_html=True)
        quick_cols=st.columns(4)
        quick_prompts=[
            "Analyze my portfolio risk",
            "Which holding has best upside?",
            "Explain Sharpe Ratio to me",
            "What is WACC and why does it matter?",
            "Am I well diversified?",
            "Explain DCF in simple terms",
            "What's a good entry strategy?",
            "Teach me about semiconductor supply chain",
        ]
        for i,col in enumerate(quick_cols):
            if col.button(quick_prompts[i],key=f"qp_{i}",use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":quick_prompts[i]})
                ctx=build_portfolio_context()
                system=f"""You are Gekko, an elite financial advisor and teacher inside a portfolio management app. 
You have full access to the user's portfolio data below. You combine the sharp analytical mind of Gordon Gekko 
with the teaching instincts of a great professor. Your job is to:
1. Give sharp, accurate financial advice
2. TEACH the user what things mean in plain language — they are learning
3. Be direct, smart, and occasionally witty
4. Reference their actual portfolio data when relevant
5. Format responses clearly with bold headers when helpful

User's Portfolio:
{ctx}

Always explain financial jargon when you use it. The user is a smart 24-year-old economics student learning investment."""
                msgs=[{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history]
                with st.spinner("Thinking..."):
                    reply=ask_claude(msgs,system,st.session_state.api_key)
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Chat display
        chat_container=st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="chat-wrap">
                    <div class="chat-empty">
                        <div style="font-family:'Cormorant Garamond',serif;font-size:36px;color:#c9a84c">◈</div>
                        <div style="font-size:13px;margin-top:12px;text-align:center;max-width:300px;line-height:1.7">
                            Ask me anything about your portfolio, financial concepts, or investment strategy.<br>
                            <span style="color:#c9a84c">I know your holdings and I'll teach you as I advise.</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                msgs_html="".join([
                    f'<div class="chat-name-{"user" if m["role"]=="user" else "ai"}">{"You" if m["role"]=="user" else "◈ Gekko AI"}</div><div class="chat-{"user" if m["role"]=="user" else "ai"}">{m["content"]}</div>'
                    for m in st.session_state.chat_history
                ])
                st.markdown(f'<div class="chat-wrap">{msgs_html}</div>', unsafe_allow_html=True)

        # Input area
        inp_col, btn_col = st.columns([5,1])
        with inp_col:
            user_input=st.text_input("Ask Gekko anything...",placeholder="e.g. What does my portfolio's Sharpe ratio tell me?",key="chat_input",label_visibility="collapsed")
        with btn_col:
            send=st.button("SEND ▶",use_container_width=True,key="send_btn")

        if (send or user_input) and user_input and st.session_state.api_key:
            st.session_state.chat_history.append({"role":"user","content":user_input})
            ctx=build_portfolio_context()
            system=f"""You are Gekko, an elite financial advisor and teacher inside a portfolio management app. 
You have full access to the user's portfolio data below. You combine the sharp analytical mind of Gordon Gekko 
with the teaching instincts of a great professor. Your job is to:
1. Give sharp, accurate financial advice
2. TEACH the user what things mean in plain language — they are learning
3. Be direct, smart, and occasionally witty  
4. Reference their actual portfolio data when relevant
5. Format responses clearly with bold for key terms

User's Portfolio:
{ctx}

Always explain financial jargon when you use it. The user is a smart 24-year-old economics student who is 
learning investments while building this platform. Be the mentor they need."""
            msgs_api=[{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history]
            with st.spinner("Gekko is thinking..."):
                reply=ask_claude(msgs_api,system,st.session_state.api_key)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        # Clear chat
        if st.session_state.chat_history:
            if st.button("Clear conversation",key="clear_chat"):
                st.session_state.chat_history=[]; st.rerun()
