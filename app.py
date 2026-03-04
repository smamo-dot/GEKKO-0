import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import requests
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Gekko Finance",
    page_icon="🦎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&display=swap');
:root {
    --cream:#faf6ef;--cream2:#f3ede2;--cream3:#ede4d3;
    --gold:#c9a84c;--gold2:#e8c97a;--gold3:#7a5c1e;
    --olive:#5c6b3a;--brown:#6b4f2e;--brown2:#3d2b10;
    --text:#2c1f0e;--muted:#8a7560;--border:#d4c4a8;
    --pos:#3d6b3a;--neg:#b84c3a;--surface:#f7f0e4;
    --sapp:#1a3a6b;--sapp2:#2a5298;--sapp3:#4a90d9;
}
html,body,[class*="css"]{font-family:'DM Mono',monospace;background:var(--cream);color:var(--text);}
.stApp{background:var(--cream);background-image:radial-gradient(ellipse at 15% 0%,rgba(201,168,76,0.09) 0%,transparent 55%),radial-gradient(ellipse at 85% 100%,rgba(26,58,107,0.06) 0%,transparent 55%);}
[data-testid="stSidebar"]{background:var(--brown2)!important;border-right:1px solid rgba(201,168,76,0.2)!important;}
[data-testid="stSidebar"] *{color:#f3ede2!important;}
[data-testid="stSidebar"] input{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(201,168,76,0.25)!important;color:#f3ede2!important;border-radius:6px!important;font-family:'DM Mono',monospace!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(201,168,76,0.25)!important;border-radius:6px!important;}
[data-testid="stSidebar"] .stButton>button{background:var(--gold)!important;color:var(--brown2)!important;border:none!important;border-radius:6px!important;font-size:11px!important;letter-spacing:1px!important;font-weight:600!important;width:100%!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--gold2)!important;}
.stButton>button{background:transparent;border:1px solid var(--gold);color:var(--gold3);border-radius:6px;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1px;transition:all 0.2s;padding:8px 20px;}
.stButton>button:hover{background:var(--gold);color:var(--brown2);}
.stTabs [data-baseweb="tab-list"]{background:var(--cream2);border-radius:8px;padding:4px;border:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent;color:var(--muted);border-radius:6px;font-family:'DM Mono',monospace;font-size:11px;letter-spacing:1px;}
.stTabs [aria-selected="true"]{background:var(--gold)!important;color:var(--brown2)!important;font-weight:500;}
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:var(--surface)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;font-size:13px!important;}
.stSelectbox>div>div{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;}
.gk-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px 22px;position:relative;overflow:hidden;margin-bottom:8px;}
.gk-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--sapp3),transparent);}
.gk-label{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.gk-value{font-family:'Cormorant Garamond',serif;font-size:30px;font-weight:600;color:var(--text);line-height:1;}
.gk-sub{font-size:12px;margin-top:5px;}
.pos{color:var(--pos)!important;}.neg{color:var(--neg)!important;}.gold{color:var(--gold)!important;}
.gk-section{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--gold3);padding-bottom:8px;border-bottom:1px solid var(--border);margin:20px 0 14px 0;}
.gk-row{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px 18px;margin:4px 0;display:flex;align-items:center;justify-content:space-between;transition:border-color 0.2s;}
.gk-row:hover{border-color:var(--gold);}
.teach{background:rgba(201,168,76,0.07);border-left:3px solid var(--gold);border-radius:0 10px 10px 0;padding:14px 18px;margin:12px 0;font-size:12px;line-height:1.85;color:var(--brown);}
.teach strong{color:var(--gold3);}
.chat-wrap{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px;height:480px;overflow-y:auto;margin-bottom:12px;}
.chat-user{background:linear-gradient(135deg,var(--gold),var(--gold2));color:var(--brown2);border-radius:14px 14px 2px 14px;padding:12px 16px;margin:8px 0 8px auto;max-width:75%;font-size:13px;line-height:1.6;width:fit-content;}
.chat-ai{background:var(--cream2);border:1px solid var(--border);border-left:3px solid var(--sapp3);border-radius:0 14px 14px 14px;padding:14px 18px;margin:8px auto 8px 0;max-width:92%;font-size:13px;line-height:1.85;}
.chat-label{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:3px;}
.gk-title{font-family:'Cormorant Garamond',serif;font-size:52px;font-weight:300;letter-spacing:-2px;color:var(--brown2);line-height:1;}
.gk-title em{color:var(--gold);font-style:italic;}
#MainMenu,footer,header{visibility:hidden;}
hr{border-color:var(--border);}
.stDataFrame{border:1px solid var(--border);border-radius:10px;overflow:hidden;}
details{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:8px!important;margin-bottom:6px!important;}
summary{font-family:'DM Mono',monospace!important;font-size:12px!important;padding:10px 14px!important;}
</style>
""", unsafe_allow_html=True)

# ── Session State — starts empty for every new user ───────────────────────────
if "portfolio"     not in st.session_state: st.session_state.portfolio     = {}
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "api_key"       not in st.session_state: st.session_state.api_key       = ""
if "watchlist"     not in st.session_state: st.session_state.watchlist     = []
if "ib_memo"       not in st.session_state: st.session_state.ib_memo       = ""

SECTOR_OPTIONS = [
    "Semiconductor Equipment","Semiconductor Materials","Chip Components",
    "Battery Materials","Critical Metals","ETF / Index","Fixed Income",
    "Technology","Healthcare","Energy","Financials","Consumer","Industrial","Other"
]
SECTOR_COLORS = {
    "Semiconductor Equipment":"#c9a84c","Semiconductor Materials":"#5c6b3a",
    "Chip Components":"#6b4f2e","Battery Materials":"#8a9e5a","Critical Metals":"#a0896a",
    "ETF / Index":"#2a5298","Fixed Income":"#4a90d9","Technology":"#7a5c1e",
    "Healthcare":"#6b3a3a","Energy":"#6b5a2e","Financials":"#3a506b",
    "Consumer":"#506b3a","Industrial":"#4a4a6b","Other":"#8a7560",
}
PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(243,237,226,0.5)",
    font=dict(family="DM Mono",color="#8a7560",size=11),
    xaxis=dict(gridcolor="#d4c4a8",zeroline=False),
    yaxis=dict(gridcolor="#d4c4a8",zeroline=False),
    margin=dict(t=30,b=30,l=10,r=10),
    colorway=["#c9a84c","#5c6b3a","#6b4f2e","#8a9e5a","#2a5298","#e8c97a","#b84c3a","#4a90d9"],
)
SYSTEM_PROMPT = """You are Sapphire, an elite AI financial advisor and teacher built into a portfolio management platform.
You have full access to the user's real portfolio data. You combine Wall Street sharpness with professor-level clarity.
Rules:
1. Give accurate, sharp financial advice
2. ALWAYS explain jargon in plain language — users are learning
3. Reference actual portfolio data when relevant
4. Use **bold** for key terms and numbers
5. Be direct, warm, occasionally witty — be the mentor they need"""

# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_prices(tickers_tuple):
    prices,changes = {},{}
    for t in tickers_tuple:
        try:
            fi=yf.Ticker(t).fast_info
            prices[t]=fi.last_price
            prev=fi.previous_close
            changes[t]=((fi.last_price-prev)/prev*100) if prev else 0
        except: prices[t]=None; changes[t]=0
    return prices,changes

@st.cache_data(ttl=300)
def get_hist(tickers_tuple,period="1y"):
    if not tickers_tuple: return pd.DataFrame()
    try:
        raw=yf.download(list(tickers_tuple),period=period,auto_adjust=True,progress=False)
        close=raw["Close"] if isinstance(raw.columns,pd.MultiIndex) else raw
        return close.dropna(how="all")
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_info(ticker):
    try: return yf.Ticker(ticker).info
    except: return {}

@st.cache_data(ttl=3600)
def get_fins(ticker):
    try:
        tk=yf.Ticker(ticker)
        return {"income":tk.financials,"balance":tk.balance_sheet,"cashflow":tk.cashflow}
    except: return {}

def ps(p): return f"${p:,.2f}" if p else "N/A"
def fmv(v,d=1):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    if abs(v)>=1e12: return f"${v/1e12:.{d}f}T"
    if abs(v)>=1e9:  return f"${v/1e9:.{d}f}B"
    if abs(v)>=1e6:  return f"${v/1e6:.{d}f}M"
    return f"${v:,.{d}f}"
def fpct(v):
    if v is None or (isinstance(v,float) and np.isnan(v)): return "—"
    return f"{v*100:.1f}%"

def ask_ai(messages,system,api_key):
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1500,"system":system,"messages":messages},
            timeout=45)
        return r.json()["content"][0]["text"] if r.status_code==200 else f"Error {r.status_code}: {r.text[:200]}"
    except Exception as e: return f"Connection error: {e}"

def portfolio_ctx():
    p=st.session_state.portfolio
    if not p: return "No holdings yet."
    try:
        prices,changes=get_prices(tuple(p.keys()))
        lines=["Current Portfolio:"]
        for t,d in p.items():
            val=(prices.get(t) or 0)*d["shares"]
            lines.append(f"  {t} | {d['sector']} | {d['shares']:.4f} sh | {ps(prices.get(t))} | {changes.get(t,0):+.2f}% | ${val:,.0f}")
        return "\n".join(lines)
    except: return "Portfolio data unavailable."

def export_portfolio_csv():
    p=st.session_state.portfolio
    if not p: return None
    rows=[]
    try:
        prices,changes=get_prices(tuple(p.keys()))
        for t,d in p.items():
            pr=prices.get(t)
            rows.append({"Ticker":t,"Sector":d["sector"],"Shares":d["shares"],
                "Avg Cost":d["avg_cost"],"Current Price":pr or 0,
                "Value":(pr or 0)*d["shares"],"Day Change %":f"{changes.get(t,0):+.2f}%"})
    except:
        for t,d in p.items():
            rows.append({"Ticker":t,"Sector":d["sector"],"Shares":d["shares"],"Avg Cost":d["avg_cost"]})
    df=pd.DataFrame(rows)
    buf=io.BytesIO()
    df.to_excel(buf,index=False,engine="openpyxl")
    return buf.getvalue()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 10px 0">
        <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:600;color:#e8c97a">🦎 Gekko</div>
        <div style="font-size:9px;letter-spacing:3px;color:rgba(243,237,226,0.3);text-transform:uppercase;margin-top:2px">Finance Intelligence</div>
    </div>
    <hr style="border-color:rgba(201,168,76,0.15);margin:8px 0 12px 0">
    """, unsafe_allow_html=True)

    with st.expander("🔑 AI Advisor Key"):
        st.markdown('<div style="font-size:10px;color:rgba(243,237,226,0.4);margin-bottom:6px">Get free key → console.anthropic.com</div>', unsafe_allow_html=True)
        key_in=st.text_input("API Key",value=st.session_state.api_key,type="password",placeholder="sk-ant-...",key="key_input")
        if st.button("SAVE KEY",key="save_key_btn"):
            st.session_state.api_key=key_in; st.success("✓ Saved!")

    # Add single stock
    with st.expander("➕ Add Single Stock"):
        nt=st.text_input("Ticker",placeholder="SPY, BND, AAPL...",key="nt").upper().strip()
        ns=st.selectbox("Sector",SECTOR_OPTIONS,key="ns")
        nsh=st.number_input("Shares",min_value=0.0,value=1.0,step=0.1,key="nsh",format="%.4f")
        nco=st.number_input("Avg Cost / Share ($)",min_value=0.0,value=0.0,step=0.01,key="nco",format="%.2f")
        if st.button("ADD ➕",key="add_btn"):
            if nt:
                st.session_state.portfolio[nt]={"sector":ns,"shares":nsh,"avg_cost":nco}
                st.success(f"✓ {nt}"); st.rerun()
            else: st.error("Enter a ticker")

    # Bulk add
    with st.expander("📋 Bulk Add Stocks"):
        st.markdown('<div style="font-size:10px;color:rgba(243,237,226,0.4);margin-bottom:6px">One ticker per line or comma separated. Adds with 0 shares — edit after.</div>', unsafe_allow_html=True)
        bulk_in=st.text_area("Tickers",placeholder="ASML\nAMAT\nLRCX\nor: ASML, AMAT, LRCX",key="bulk_in",height=100)
        bulk_sector=st.selectbox("Sector for all",SECTOR_OPTIONS,key="bulk_sec")
        if st.button("BULK ADD ➕",key="bulk_btn"):
            raw_tickers=[x.strip().upper() for x in bulk_in.replace(",","\n").split("\n") if x.strip()]
            added=0
            for t in raw_tickers:
                if t not in st.session_state.portfolio:
                    st.session_state.portfolio[t]={"sector":bulk_sector,"shares":0.0,"avg_cost":0.0}
                    added+=1
            st.success(f"✓ Added {added} stocks"); st.rerun()

    # Edit/Remove
    with st.expander("✏️ Edit / Remove"):
        if st.session_state.portfolio:
            et=st.selectbox("Stock",list(st.session_state.portfolio.keys()),key="et")
            cur=st.session_state.portfolio[et]
            esh=st.number_input("Shares",value=float(cur["shares"]),step=0.1,key="esh",format="%.4f")
            eco=st.number_input("Avg Cost ($)",value=float(cur["avg_cost"]),step=0.01,key="eco",format="%.2f")
            es=st.selectbox("Sector",SECTOR_OPTIONS,index=SECTOR_OPTIONS.index(cur["sector"]) if cur["sector"] in SECTOR_OPTIONS else 0,key="es")
            c1,c2=st.columns(2)
            with c1:
                if st.button("SAVE ✓",key="save_e",use_container_width=True):
                    st.session_state.portfolio[et].update({"shares":esh,"avg_cost":eco,"sector":es})
                    st.success("✓"); st.rerun()
            with c2:
                if st.button("REMOVE 🗑",key="rem_e",use_container_width=True):
                    del st.session_state.portfolio[et]; st.rerun()
        else:
            st.markdown('<div style="font-size:11px;color:rgba(243,237,226,0.4)">No holdings yet</div>', unsafe_allow_html=True)

    # Clear all
    with st.expander("⚠️ Clear Portfolio"):
        st.markdown('<div style="font-size:10px;color:rgba(243,237,226,0.4);margin-bottom:6px">This removes all holdings</div>', unsafe_allow_html=True)
        if st.button("CLEAR ALL",key="clear_all"):
            st.session_state.portfolio={}; st.rerun()

    st.markdown('<hr style="border-color:rgba(201,168,76,0.15);margin:12px 0 10px 0">', unsafe_allow_html=True)

    # Holdings list
    sectors_map={}
    for t,d in st.session_state.portfolio.items():
        sectors_map.setdefault(d["sector"],[]).append(t)

    if sectors_map:
        st.markdown('<div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(232,201,122,0.5);margin-bottom:8px">Holdings</div>', unsafe_allow_html=True)
        for sec,ts in sectors_map.items():
            color=SECTOR_COLORS.get(sec,"#c9a84c")
            st.markdown(f'<div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{color};margin:10px 0 4px 0">{sec}</div>', unsafe_allow_html=True)
            for t in ts:
                sh=st.session_state.portfolio[t]["shares"]
                st.markdown(f'<div style="font-size:11px;color:rgba(243,237,226,0.45);padding-left:8px;margin:2px 0">→ {t} <span style="color:rgba(243,237,226,0.22)">({sh:.2f} sh)</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:11px;color:rgba(243,237,226,0.3);text-align:center;padding:20px 0">Add stocks to begin</div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-color:rgba(201,168,76,0.15);margin:12px 0 10px 0">', unsafe_allow_html=True)
    period=st.select_slider("Chart Period",["1mo","3mo","6mo","1y","2y","5y"],value="1y")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:24px">
  <div>
    <div class="gk-title">Gekko <em>Finance</em></div>
    <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#8a7560;margin-top:6px">
      Portfolio · Quant · Investment Banking · AI Advisor
    </div>
  </div>
  <div style="font-family:'Cormorant Garamond',serif;font-size:13px;color:#8a7560;text-align:right;padding-bottom:6px">
    "The most valuable commodity I know of is information."<br>
    <span style="color:#c9a84c">— Gordon Gekko</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
tickers=list(st.session_state.portfolio.keys())
if not tickers:
    st.markdown("""
    <div style="text-align:center;padding:80px 40px;background:var(--surface);border:1px solid var(--border);border-radius:16px;margin-top:20px">
      <div style="font-family:'Cormorant Garamond',serif;font-size:56px;color:#c9a84c">💎</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:28px;color:#3d2b10;margin-top:12px">Welcome to Gekko</div>
      <div style="font-size:12px;color:#8a7560;margin-top:8px;line-height:1.8">
        Add stocks, ETFs, or fixed income to your portfolio using the sidebar.<br>
        You can add single tickers or bulk-paste an entire list at once.<br>
        <strong style="color:#c9a84c">Try adding: SPY, QQQ, BND, ASML, NVDA</strong>
      </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Fetch data ────────────────────────────────────────────────────────────────
with st.spinner(""):
    prices,changes=get_prices(tuple(tickers))
    hist  =get_hist(tuple(tickers),period)
    hist1y=get_hist(tuple(tickers),"1y")

total_value=sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in tickers)
total_cost =sum(
    st.session_state.portfolio[t]["avg_cost"]*st.session_state.portfolio[t]["shares"]
    if st.session_state.portfolio[t]["avg_cost"]>0
    else (prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]
    for t in tickers)
total_pnl=total_value-total_cost
pnl_pct=(total_pnl/total_cost*100) if total_cost>0 else 0
day_chg=sum((prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]*(changes.get(t,0)/100) for t in tickers)
best_t=max(tickers,key=lambda x:changes.get(x,0))

# ── KPI Row ───────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5=st.columns(5)
for col,lbl,val,sub,cls in [
    (c1,"Portfolio Value", f"${total_value:,.0f}", f"{'▲' if day_chg>=0 else '▼'} ${abs(day_chg):,.0f} today","pos" if day_chg>=0 else "neg"),
    (c2,"Total P&L",       f"{pnl_pct:+.1f}%",    f"${total_pnl:+,.0f}","pos" if total_pnl>=0 else "neg"),
    (c3,"Holdings",        str(len(tickers)),       f"{len(sectors_map)} sectors","gold"),
    (c4,"Best Today",      best_t,                 f"+{changes.get(best_t,0):.2f}%","pos"),
    (c5,"Worst Today",     min(tickers,key=lambda x:changes.get(x,0)),
                           f"{changes.get(min(tickers,key=lambda x:changes.get(x,0)),0):+.2f}%","neg"),
]:
    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value">{val}</div><div class="gk-sub {cls}">{sub}</div></div>', unsafe_allow_html=True)

# Download button row
dl_col,_=st.columns([2,8])
with dl_col:
    xlsx_data=export_portfolio_csv()
    if xlsx_data:
        st.download_button("⬇ Download Portfolio",data=xlsx_data,file_name="gekko_portfolio.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="dl_port")

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs([
    "💎 DASHBOARD","📈 PERFORMANCE","🧮 QUANT",
    "🎲 MONTE CARLO","🏦 IB MODELS","📁 FINANCIALS","🤖 AI ADVISOR"
])

# ══════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════
with tab1:
    left,right=st.columns([3,2])
    with left:
        st.markdown('<div class="gk-section">Live Holdings</div>', unsafe_allow_html=True)
        for sec,ts in sectors_map.items():
            color=SECTOR_COLORS.get(sec,"#c9a84c")
            st.markdown(f'<div style="color:{color};font-size:9px;letter-spacing:2px;text-transform:uppercase;margin:14px 0 6px 0">{sec}</div>', unsafe_allow_html=True)
            for t in ts:
                p=prices.get(t); chg=changes.get(t,0)
                sh=st.session_state.portfolio[t]["shares"]
                val=(p or 0)*sh; clr="#3d6b3a" if chg>=0 else "#b84c3a"
                arr="▲" if chg>=0 else "▼"; pstr=ps(p)
                st.markdown(f"""
                <div class="gk-row">
                  <div><span style="font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:600">{t}</span>
                  <span style="color:#8a7560;font-size:11px;margin-left:8px">{sh:.4f} sh</span></div>
                  <div style="text-align:center;min-width:90px">
                    <div style="font-size:15px;font-weight:500">{pstr}</div>
                    <div style="color:{clr};font-size:11px">{arr} {chg:+.2f}%</div>
                  </div>
                  <div style="text-align:right;min-width:80px">
                    <div style="font-size:10px;color:#8a7560">VALUE</div>
                    <div style="font-size:14px;font-weight:500">${val:,.0f}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="gk-section">Allocation</div>', unsafe_allow_html=True)
        alloc={}
        for t in tickers:
            sec=st.session_state.portfolio[t]["sector"]
            alloc[sec]=alloc.get(sec,0)+(prices.get(t) or 0)*st.session_state.portfolio[t]["shares"]
        if sum(alloc.values())>0:
            fig=go.Figure(go.Pie(
                labels=list(alloc.keys()),values=list(alloc.values()),hole=0.55,
                marker_colors=[SECTOR_COLORS.get(s,"#c9a84c") for s in alloc],
                textinfo="label+percent",textfont=dict(family="DM Mono",size=10)))
            fig.update_layout(**{**PLOT,"height":270,"showlegend":False,
                "annotations":[dict(text="ALLOC",x=0.5,y=0.5,font=dict(size=11,color="#8a7560"),showarrow=False)]})
            st.plotly_chart(fig,use_container_width=True)
        st.markdown('<div class="gk-section">Today\'s Movers</div>', unsafe_allow_html=True)
        for t in sorted(tickers,key=lambda x:changes.get(x,0),reverse=True)[:10]:
            chg=changes.get(t,0); bc="#5c6b3a" if chg>=0 else "#b84c3a"; bw=min(abs(chg)*10,100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:5px 0">
              <span style="font-size:11px;width:46px;font-weight:500;color:#2c1f0e">{t}</span>
              <div style="flex:1;background:#ede4d3;border-radius:3px;height:5px">
                <div style="width:{bw}%;background:{bc};height:5px;border-radius:3px"></div>
              </div>
              <span style="font-size:11px;color:{bc};width:58px;text-align:right">{chg:+.2f}%</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 2 — PERFORMANCE
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="gk-section">Select Stocks to Compare</div>', unsafe_allow_html=True)
    sel_perf=st.multiselect("Choose tickers to display",tickers,default=tickers[:min(8,len(tickers))],key="perf_sel")

    # Also allow adding any ticker for comparison (not just portfolio)
    extra_t=st.text_input("Compare with any ticker (e.g. SPY, QQQ, BTC-USD)","",key="extra_perf").upper().strip()

    compare_list=sel_perf.copy()
    if extra_t and extra_t not in compare_list:
        compare_list.append(extra_t)

    if compare_list:
        comp_hist=get_hist(tuple(compare_list),period)
        valid=[t for t in compare_list if not comp_hist.empty and t in comp_hist.columns]
        if valid:
            norm=comp_hist[valid]/comp_hist[valid].iloc[0]*100
            fig=go.Figure()
            for t in valid:
                color=SECTOR_COLORS.get(st.session_state.portfolio.get(t,{}).get("sector","Other"),"#c9a84c")
                fig.add_trace(go.Scatter(x=norm.index,y=norm[t],name=t,
                    line=dict(color=color,width=2),
                    hovertemplate=f"<b>{t}</b> %{{y:.1f}}<extra></extra>"))
            fig.update_layout(**{**PLOT,"height":420,"yaxis_title":"Indexed (100=start)",
                "hovermode":"x unified","legend":dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10))})
            st.plotly_chart(fig,use_container_width=True)
            rows=[]
            for t in valid:
                s=comp_hist[t].dropna()
                if len(s)<2: continue
                dr=s.pct_change().dropna()
                rows.append({"Ticker":t,
                    "Sector":st.session_state.portfolio.get(t,{}).get("sector","—"),
                    "Period Return":f"{(s.iloc[-1]/s.iloc[0]-1)*100:+.1f}%",
                    "1M":f"{(s.iloc[-1]/s.iloc[-min(21,len(s))]-1)*100:+.1f}%",
                    "3M":f"{(s.iloc[-1]/s.iloc[-min(63,len(s))]-1)*100:+.1f}%",
                    "Volatility":f"{dr.std()*np.sqrt(252)*100:.1f}%",
                    "Price":ps(prices.get(t) if t in tickers else None)})
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
# TAB 3 — QUANT
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="teach">
    <strong>📚 Quant Guide</strong> — <strong>Sharpe Ratio</strong>: return per unit of risk (>1 good, >2 excellent) ·
    <strong>Beta</strong>: sensitivity vs S&P 500 (1.2 = 20% more volatile) ·
    <strong>Max Drawdown</strong>: worst peak-to-trough loss ·
    <strong>VaR 95%</strong>: worst expected daily loss on a bad day (1 in 20) ·
    <strong>Correlation</strong>: how stocks move together (low = good diversification)
    </div>""", unsafe_allow_html=True)

    quant_sel=st.multiselect("Select stocks to analyze",tickers,default=tickers[:min(10,len(tickers))],key="quant_sel")
    extra_q=st.text_input("Add any ticker for quant analysis","",key="extra_q").upper().strip()
    quant_list=quant_sel.copy()
    if extra_q and extra_q not in quant_list: quant_list.append(extra_q)

    if quant_list:
        q_hist=get_hist(tuple(quant_list),"1y")
        valid1y=[t for t in quant_list if not q_hist.empty and t in q_hist.columns]
        if valid1y:
            dr=q_hist[valid1y].pct_change().dropna()
            spy=get_hist(("SPY",),"1y")
            spyr=spy["SPY"].pct_change().dropna() if "SPY" in spy.columns else None
            rows=[]
            for t in valid1y:
                r=dr[t].dropna()
                if len(r)<10: continue
                ann_r=r.mean()*252*100; ann_v=r.std()*np.sqrt(252)*100
                sharpe=r.mean()/r.std()*np.sqrt(252) if r.std()>0 else 0
                cum=(1+r).cumprod(); mdd=((cum-cum.cummax())/cum.cummax()).min()*100
                beta=None
                if spyr is not None:
                    idx=r.index.intersection(spyr.index)
                    if len(idx)>30: beta,*_=stats.linregress(spyr.loc[idx],r.loc[idx])
                rows.append({"Ticker":t,"Ann. Return":f"{ann_r:+.1f}%","Ann. Vol":f"{ann_v:.1f}%",
                    "Sharpe":f"{sharpe:.2f}","Max DD":f"{mdd:.1f}%",
                    "Beta":f"{beta:.2f}" if beta is not None else "—",
                    "VaR 95%":f"{np.percentile(r,5)*100:.2f}%"})
            st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

            if len(valid1y)>1:
                st.markdown('<div class="gk-section">Correlation Matrix</div>', unsafe_allow_html=True)
                corr=dr[valid1y].corr()
                fig=go.Figure(go.Heatmap(
                    z=corr.values,x=corr.columns,y=corr.index,
                    colorscale=[[0,"#b84c3a"],[0.5,"#ede4d3"],[1,"#5c6b3a"]],
                    zmin=-1,zmax=1,text=np.round(corr.values,2),
                    texttemplate="%{text}",textfont=dict(size=9,family="DM Mono")))
                fig.update_layout(**{**PLOT,"height":400})
                st.plotly_chart(fig,use_container_width=True)

        st.markdown('<div class="gk-section">DuPont Analysis</div>', unsafe_allow_html=True)
        dp_t=st.selectbox("Stock for DuPont",quant_list,key="dp_sel")
        info=get_info(dp_t)
        roe=info.get("returnOnEquity"); roa=info.get("returnOnAssets")
        pm=info.get("profitMargins");   at=info.get("assetTurnover")
        lev=(roe/roa) if roe and roa and roa!=0 else None
        for col,(lbl,val) in zip(st.columns(5),[
            ("ROE",fpct(roe)),("Net Margin",fpct(pm)),
            ("Asset Turnover",f"{at:.2f}x" if at else "—"),
            ("ROA",fpct(roa)),("Equity Multiplier",f"{lev:.2f}x" if lev else "—")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="gk-section">Horizontal Analysis</div>', unsafe_allow_html=True)
        hrows=[]
        if valid1y:
            for t in valid1y:
                s=q_hist[t].dropna(); row={"Ticker":t}
                for lbl,d in {"1W":5,"1M":21,"3M":63,"6M":126,"1Y":252}.items():
                    row[lbl]=f"{(s.iloc[-1]/s.iloc[-min(d,len(s))]-1)*100:+.1f}%" if len(s)>d else "—"
                hrows.append(row)
            st.dataframe(pd.DataFrame(hrows),use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
# TAB 4 — MONTE CARLO
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown("""<div class="teach">
    <strong>📚 Monte Carlo Simulation</strong> — Runs thousands of random future scenarios using historical volatility.
    Not a prediction — a probability range. <strong>Bear = 5th percentile · Bull = 95th percentile.</strong>
    You can simulate your full portfolio OR select specific stocks to stress test separately.
    </div>""", unsafe_allow_html=True)

    mc_mode=st.radio("Simulation Mode",["Full Portfolio","Selected Stocks"],horizontal=True,key="mc_mode")
    if mc_mode=="Selected Stocks":
        mc_sel=st.multiselect("Select stocks to simulate",tickers,default=tickers[:min(5,len(tickers))],key="mc_sel")
        extra_mc=st.text_input("Add any ticker to simulation","",key="extra_mc").upper().strip()
        mc_tickers=mc_sel.copy()
        if extra_mc and extra_mc not in mc_tickers: mc_tickers.append(extra_mc)
    else:
        mc_tickers=tickers

    mc1,mc2,mc3=st.columns(3)
    with mc1: n_sim=st.select_slider("Simulations",[500,1000,2000,5000],value=1000)
    with mc2: n_days=st.select_slider("Forecast Days",[30,60,90,180,252],value=252)
    with mc3: run_mc=st.button("▶  RUN SIMULATION",use_container_width=True,key="run_mc_btn")

    if run_mc and mc_tickers:
        mc_hist=get_hist(tuple(mc_tickers),"1y")
        valid_mc=[t for t in mc_tickers if not mc_hist.empty and t in mc_hist.columns]
        if valid_mc:
            with st.spinner("Running simulations..."):
                dr_mc=mc_hist[valid_mc].pct_change().dropna()
                if mc_mode=="Full Portfolio":
                    pv={t:(prices.get(t) or 0)*st.session_state.portfolio[t]["shares"] for t in valid_mc}
                    tv=sum(pv.values()); start_val=total_value
                    w=np.array([pv[t]/tv if tv>0 else 1/len(valid_mc) for t in valid_mc])
                else:
                    w=np.ones(len(valid_mc))/len(valid_mc); start_val=10000
                port_r=dr_mc[valid_mc].values@w
                mu,sigma=port_r.mean(),port_r.std()
                np.random.seed(42)
                sims=np.zeros((n_days,n_sim))
                for i in range(n_sim):
                    sims[:,i]=start_val*np.cumprod(1+np.random.normal(mu,sigma,n_days))
                finals=sims[-1,:]
                pcts={k:np.percentile(finals,v) for k,v in {"p5":5,"p25":25,"p50":50,"p75":75,"p95":95}.items()}
                fig=go.Figure()
                for i in range(min(200,n_sim)):
                    fig.add_trace(go.Scatter(y=sims[:,i],mode="lines",
                        line=dict(color="rgba(201,168,76,0.03)",width=1),showlegend=False,hoverinfo="skip"))
                for lbl,p,clr in [("Bull 95th",pcts["p95"],"#5c6b3a"),("Median",pcts["p50"],"#c9a84c"),("Bear 5th",pcts["p5"],"#b84c3a")]:
                    idx=np.argmin(np.abs(sims[-1,:]-p))
                    fig.add_trace(go.Scatter(y=sims[:,idx],mode="lines",name=f"{lbl}: ${p:,.0f}",line=dict(color=clr,width=2.5)))
                fig.update_layout(**{**PLOT,"height":420,
                    "yaxis":dict(gridcolor="#d4c4a8",tickprefix="$",tickformat=",.0f"),
                    "legend":dict(bgcolor="rgba(0,0,0,0)")})
                st.plotly_chart(fig,use_container_width=True)
                for col,(lbl,p,clr) in zip(st.columns(5),[
                    ("Bear 5%",pcts["p5"],"#b84c3a"),("25th",pcts["p25"],"#a0896a"),
                    ("Median",pcts["p50"],"#c9a84c"),("75th",pcts["p75"],"#5c6b3a"),
                    ("Bull 95%",pcts["p95"],"#3d6b3a")]):
                    chg=(p-start_val)/start_val*100 if start_val>0 else 0
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:18px;color:{clr}">${p:,.0f}</div><div class="gk-sub" style="color:{clr}">{chg:+.1f}%</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:60px;color:#8a7560"><div style="font-family:Cormorant Garamond,serif;font-size:44px;color:#c9a84c">◈</div><div style="font-size:11px;letter-spacing:2px;margin-top:12px">Configure above and click RUN SIMULATION</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAB 5 — IB MODELS
# ══════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="gk-section">Select or Enter Any Company to Analyze</div>', unsafe_allow_html=True)
    ib_col1,ib_col2=st.columns([2,3])
    with ib_col1:
        ib_from_portfolio=st.selectbox("From portfolio",["— type below —"]+tickers,key="ib_port_sel")
    with ib_col2:
        ib_custom=st.text_input("Or enter any ticker","",placeholder="MSFT, TSLA, 0700.HK...",key="ib_custom").upper().strip()
    ib_ticker=(ib_custom if ib_custom else (ib_from_portfolio if ib_from_portfolio!="— type below —" else (tickers[0] if tickers else "")))

    if not ib_ticker:
        st.info("Select a company above to begin IB analysis."); st.stop()

    st.markdown(f'<div style="font-family:Cormorant Garamond,serif;font-size:20px;color:#3d2b10;margin:8px 0 16px 0">Analyzing: <strong style="color:#c9a84c">{ib_ticker}</strong></div>', unsafe_allow_html=True)

    ib1,ib2,ib3,ib4,ib5,ib6=st.tabs(["DCF","COMPS","PRECEDENT TXN","LBO","RATIOS","📄 DOCUMENT MEMO"])

    with ib1:
        st.markdown("""<div class="teach"><strong>📚 DCF</strong> — A company is worth the sum of all future cash flows discounted to today.
        <strong>WACC</strong> = cost of capital. <strong>Intrinsic value > price</strong> → potentially undervalued.</div>""", unsafe_allow_html=True)
        info=get_info(ib_ticker)
        d1,d2,d3,d4=st.columns(4)
        with d1: wacc=st.number_input("WACC (%)",value=10.0,step=0.5,key="wacc")/100
        with d2: g5=st.number_input("5Y Rev Growth (%)",value=8.0,step=0.5,key="g5")/100
        with d3: tg=st.number_input("Terminal Growth (%)",value=2.5,step=0.5,key="tg")/100
        with d4: fcf_m=st.number_input("FCF Margin (%)",value=15.0,step=1.0,key="fcfm")/100
        if st.button("◈ CALCULATE INTRINSIC VALUE",key="run_dcf"):
            rev=info.get("totalRevenue"); sh_out=info.get("sharesOutstanding"); cur_p=prices.get(ib_ticker)
            if not cur_p:
                try: cur_p=yf.Ticker(ib_ticker).fast_info.last_price
                except: cur_p=None
            if rev and sh_out:
                fcfs=[]; r=rev
                for yr in range(1,6):
                    r*=(1+g5); fcf=r*fcf_m; pv_fcf=fcf/(1+wacc)**yr
                    fcfs.append({"Year":f"Year {yr}","Revenue":fmv(r),"FCF":fmv(fcf),"PV of FCF":fmv(pv_fcf),"_pv":pv_fcf})
                pv_term=(fcfs[-1]["_pv"]*(1+tg)/(wacc-tg))/(1+wacc)**5 if wacc>tg else 0
                total_pv=sum(f["_pv"] for f in fcfs)+pv_term
                intrinsic=total_pv/sh_out
                for f in fcfs: del f["_pv"]
                st.dataframe(pd.DataFrame(fcfs),use_container_width=True,hide_index=True)
                mos=((intrinsic-(cur_p or 0))/intrinsic*100) if cur_p and intrinsic>0 else 0
                for col,(lbl,val) in zip(st.columns(4),[
                    ("PV Terminal Value",fmv(pv_term)),("Total Equity Value",fmv(total_pv)),
                    ("Intrinsic Value/Share",f"${intrinsic:.2f}"),
                    ("Margin of Safety",f"{mos:+.1f}%")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)
                if cur_p:
                    status="🟢 UNDERVALUED" if mos>15 else "🟡 FAIRLY VALUED" if mos>-10 else "🔴 OVERVALUED"
                    st.markdown(f'<div class="teach">Current <strong>{ps(cur_p)}</strong> vs intrinsic <strong>${intrinsic:.2f}</strong> → <strong>{status}</strong> ({mos:+.1f}% margin of safety)</div>', unsafe_allow_html=True)
            else: st.warning("Revenue data unavailable — try a major US ticker.")

    with ib2:
        st.markdown("""<div class="teach"><strong>📚 Comps</strong> — Value by comparing to similar public companies using multiples.
        If peers trade at 15x EBITDA and your stock at 10x — either cheap or there's a reason.</div>""", unsafe_allow_html=True)
        comps_in=st.text_input("Comparable Tickers","NVDA,AMD,INTC,QCOM",key="comps_in")
        if st.button("◈ RUN COMPS",key="run_comps"):
            all_t=list(set([ib_ticker]+[x.strip().upper() for x in comps_in.split(",") if x.strip()]))
            rows=[]
            for t in all_t:
                i=get_info(t)
                if not i: continue
                rows.append({"Ticker":t,"Name":i.get("shortName","")[:22],
                    "Mkt Cap":fmv(i.get("marketCap")),
                    "EV/EBITDA":f"{i.get('enterpriseToEbitda',0):.1f}x" if i.get("enterpriseToEbitda") else "—",
                    "EV/Rev":f"{i.get('enterpriseToRevenue',0):.1f}x" if i.get("enterpriseToRevenue") else "—",
                    "P/E":f"{i.get('trailingPE',0):.1f}x" if i.get("trailingPE") else "—",
                    "Gross Margin":fpct(i.get("grossMargins")),
                    "Net Margin":fpct(i.get("profitMargins")),
                    "ROE":fpct(i.get("returnOnEquity"))})
            if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    with ib3:
        st.markdown("""<div class="teach"><strong>📚 Precedent Transactions</strong> — What did acquirers pay for similar companies?
        Includes control premium (20–40% above market). Upper bound of what a buyer would pay.</div>""", unsafe_allow_html=True)
        info=get_info(ib_ticker)
        p1,p2,p3=st.columns(3)
        with p1: lo=st.number_input("Low EV/EBITDA",value=10.0,step=0.5,key="lo_ev")
        with p2: hi=st.number_input("High EV/EBITDA",value=18.0,step=0.5,key="hi_ev")
        with p3: prem=st.slider("Control Premium %",0,50,25,key="prem")/100
        if st.button("◈ ESTIMATE TRANSACTION VALUE",key="run_prec"):
            ebitda=info.get("ebitda"); sh_out=info.get("sharesOutstanding")
            cur_p=prices.get(ib_ticker)
            if not cur_p:
                try: cur_p=yf.Ticker(ib_ticker).fast_info.last_price
                except: cur_p=None
            if ebitda and sh_out:
                net_debt=info.get("totalDebt",0)-(info.get("totalCash",0) or 0)
                lo_pp=(ebitda*lo-net_debt)/sh_out*(1+prem)
                hi_pp=(ebitda*hi-net_debt)/sh_out*(1+prem)
                for col,(lbl,val) in zip(st.columns(4),[
                    ("Low EV",fmv(ebitda*lo)),("High EV",fmv(ebitda*hi)),
                    ("Low Price/Share",f"${lo_pp:.2f}"),("High Price/Share",f"${hi_pp:.2f}")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)
                if cur_p: st.markdown(f'<div class="teach">At <strong>{ps(cur_p)}</strong>, high-end deal implies <strong>{(hi_pp-cur_p)/cur_p*100:+.1f}% premium</strong></div>', unsafe_allow_html=True)
            else: st.warning("EBITDA data unavailable.")

    with ib4:
        st.markdown("""<div class="teach"><strong>📚 LBO</strong> — PE firm buys using mostly debt, improves ops, sells in 5 years.
        <strong>IRR</strong> target: 20%+. <strong>MOIC</strong> = how many times your money back (2.5x = good).</div>""", unsafe_allow_html=True)
        info=get_info(ib_ticker)
        l1,l2,l3=st.columns(3)
        with l1:
            ent_ev=st.number_input("Entry EV/EBITDA",value=12.0,step=0.5,key="lbo_ent")
            dbt_pct=st.number_input("Debt % of EV",value=65.0,step=5.0,key="lbo_dbt")/100
        with l2:
            ext_ev=st.number_input("Exit EV/EBITDA",value=14.0,step=0.5,key="lbo_ext")
            ebitda_g=st.number_input("EBITDA Growth/yr %",value=10.0,step=1.0,key="lbo_g")/100
        with l3:
            hold=st.number_input("Hold Period (yrs)",value=5,min_value=1,max_value=10,step=1,key="lbo_hold")
        if st.button("◈ RUN LBO",key="run_lbo"):
            ebitda=info.get("ebitda")
            if ebitda:
                ent_ev_v=ebitda*ent_ev; debt=ent_ev_v*dbt_pct; equity=ent_ev_v*(1-dbt_pct)
                exit_ebitda=ebitda*(1+ebitda_g)**hold
                exit_ev_v=exit_ebitda*ext_ev
                rem_debt=debt*(0.7**hold)
                exit_eq=exit_ev_v-rem_debt
                moic=exit_eq/equity if equity>0 else 0
                irr=(moic**(1/hold)-1)*100
                for col,(lbl,val) in zip(st.columns(4),[
                    ("Entry EV",fmv(ent_ev_v)),("Exit EV",fmv(exit_ev_v)),
                    ("MOIC",f"{moic:.2f}x"),("IRR",f"{irr:.1f}%")]):
                    col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:22px">{val}</div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="teach">Equity check <strong>{fmv(equity)}</strong> on <strong>{fmv(ent_ev_v)}</strong> EV → IRR <strong>{irr:.1f}%</strong> {"✅ meets 20%+ PE target" if irr>=20 else "⚠️ below 20% target"}</div>', unsafe_allow_html=True)
            else: st.warning("EBITDA unavailable.")

    with ib5:
        info=get_info(ib_ticker)
        st.markdown('<div class="gk-section">Leverage Ratios</div>', unsafe_allow_html=True)
        de=info.get("debtToEquity"); cr=info.get("currentRatio"); qr=info.get("quickRatio"); ic=info.get("interestCoverage")
        for col,(lbl,val,tip) in zip(st.columns(4),[
            ("Debt/Equity",f"{de/100:.2f}x" if de else "—","<1x conservative · >3x aggressive"),
            ("Current Ratio",f"{cr:.2f}x" if cr else "—",">1x = covers short-term debt"),
            ("Quick Ratio",f"{qr:.2f}x" if qr else "—",">1x = healthy liquidity"),
            ("Interest Coverage",f"{ic:.1f}x" if ic else "—",">3x = comfortably covers interest")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div><div class="gk-sub" style="font-size:10px;color:#8a7560">{tip}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="gk-section">Performance Ratios</div>', unsafe_allow_html=True)
        for col,(lbl,val) in zip(st.columns(4),[
            ("Gross Margin",fpct(info.get("grossMargins"))),
            ("Operating Margin",fpct(info.get("operatingMargins"))),
            ("Net Margin",fpct(info.get("profitMargins"))),
            ("ROE",fpct(info.get("returnOnEquity")))]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)
        for col,(lbl,val) in zip(st.columns(4),[
            ("ROA",fpct(info.get("returnOnAssets"))),
            ("Revenue",fmv(info.get("totalRevenue"))),
            ("EV/EBITDA",f"{info.get('enterpriseToEbitda',0):.1f}x" if info.get("enterpriseToEbitda") else "—"),
            ("P/E",f"{info.get('trailingPE',0):.1f}x" if info.get("trailingPE") else "—")]):
            col.markdown(f'<div class="gk-card"><div class="gk-label">{lbl}</div><div class="gk-value" style="font-size:20px">{val}</div></div>', unsafe_allow_html=True)

    with ib6:
        st.markdown("""<div class="teach">
        <strong>📚 Document Memo Generator</strong> — Upload any financial document: annual report, 10-K, earnings transcript,
        investor presentation, or balance sheet. Gekko AI will read it, identify the company,
        and generate a professional Investment Banking memo with key findings, risks, and opportunities.
        </div>""", unsafe_allow_html=True)

        if not st.session_state.api_key:
            st.warning("Add your Anthropic API key in the sidebar to use the Document Memo feature.")
        else:
            uploaded_doc=st.file_uploader("Upload Financial Document (PDF, CSV, Excel, TXT)",
                type=["pdf","csv","xlsx","xls","txt"],key="ib_doc_upload")
            doc_context=""
            if uploaded_doc:
                try:
                    if uploaded_doc.name.endswith(".csv"):
                        df_doc=pd.read_csv(uploaded_doc)
                        doc_context=f"Document type: CSV/Spreadsheet\n{df_doc.to_string(max_rows=50)}"
                    elif uploaded_doc.name.endswith((".xlsx",".xls")):
                        df_doc=pd.read_excel(uploaded_doc)
                        doc_context=f"Document type: Excel Spreadsheet\n{df_doc.to_string(max_rows=50)}"
                    elif uploaded_doc.name.endswith(".txt"):
                        doc_context=f"Document type: Text File\n{uploaded_doc.read().decode('utf-8',errors='ignore')[:8000]}"
                    elif uploaded_doc.name.endswith(".pdf"):
                        doc_context=f"Document: {uploaded_doc.name} (PDF uploaded — analyze based on filename and any text content)"
                        try:
                            import pdfplumber
                            with pdfplumber.open(uploaded_doc) as pdf:
                                text="".join([p.extract_text() or "" for p in pdf.pages[:10]])
                            doc_context=f"PDF Document Content:\n{text[:8000]}"
                        except:
                            pass
                    st.success(f"✓ Document loaded: {uploaded_doc.name}")
                except Exception as e:
                    st.error(f"Could not read document: {e}")

            memo_type=st.selectbox("Memo Type",["Full IB Memo","Executive Summary","Risk Analysis","Investment Thesis","Comparable Analysis Notes"],key="memo_type")

            if st.button("◈ GENERATE MEMO",key="gen_memo") and (doc_context or ib_ticker):
                with st.spinner("Generating memo..."):
                    context=doc_context if doc_context else f"Analyze {ib_ticker} as an investment banking target."
                    memo_prompt=f"""You are a senior investment banker at Goldman Sachs writing a {memo_type}.
                    
Analyze the following document/company and produce a professional, structured IB memo.

Include:
1. **Company Overview** — Who is this company, what do they do, key metrics
2. **Financial Highlights** — Revenue, margins, growth, key ratios from the document
3. **Investment Thesis** — Bull case for investing or acquiring
4. **Key Risks** — Top 3-5 risks to the thesis
5. **Valuation Perspective** — Rough valuation range based on available data
6. **Recommendation** — Buy / Hold / Avoid with rationale

Document/Company: {ib_ticker}
{context[:6000]}

Write in professional IB style. Be specific with numbers where available."""
                    memo=ask_ai([{"role":"user","content":memo_prompt}],
                        "You are a senior Goldman Sachs investment banker producing professional memos.",
                        st.session_state.api_key)
                    st.session_state.ib_memo=memo

            if st.session_state.ib_memo:
                st.markdown('<div class="gk-section">Generated Memo</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-ai" style="max-width:100%;white-space:pre-wrap">{st.session_state.ib_memo}</div>', unsafe_allow_html=True)
                st.download_button("⬇ Download Memo",data=st.session_state.ib_memo,
                    file_name=f"gekko_memo_{ib_ticker}.txt",mime="text/plain",key="dl_memo")

# ══════════════════════════════════════════════════════
# TAB 6 — FINANCIALS
# ══════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="gk-section">Financial Statements</div>', unsafe_allow_html=True)
    fin_col1,fin_col2=st.columns([2,3])
    with fin_col1:
        fin_from_port=st.selectbox("From portfolio",["— type below —"]+tickers,key="fin_port")
    with fin_col2:
        fin_custom=st.text_input("Or any ticker","",placeholder="AAPL, MSFT...",key="fin_custom").upper().strip()
    fin_t=fin_custom if fin_custom else (fin_from_port if fin_from_port!="— type below —" else (tickers[0] if tickers else ""))

    if fin_t and st.button("◈ FETCH FINANCIALS",key="fetch_fins"):
        fins=get_fins(fin_t)
        if fins:
            ft1,ft2,ft3=st.tabs(["INCOME STATEMENT","BALANCE SHEET","CASH FLOW"])
            with ft1:
                if fins.get("income") is not None and not fins["income"].empty:
                    st.dataframe(fins["income"],use_container_width=True)
            with ft2:
                if fins.get("balance") is not None and not fins["balance"].empty:
                    st.dataframe(fins["balance"],use_container_width=True)
            with ft3:
                if fins.get("cashflow") is not None and not fins["cashflow"].empty:
                    st.dataframe(fins["cashflow"],use_container_width=True)

    st.markdown('<div class="gk-section">Upload Your Own Document</div>', unsafe_allow_html=True)
    st.markdown("""<div class="teach"><strong>📚 Source files from</strong> SEC EDGAR (sec.gov), company investor relations pages, or Bloomberg exports.</div>""", unsafe_allow_html=True)
    up=st.file_uploader("CSV or Excel",type=["csv","xlsx","xls"],key="fin_upload")
    if up:
        try:
            df_up=pd.read_csv(up) if up.name.endswith(".csv") else pd.read_excel(up)
            st.dataframe(df_up,use_container_width=True)
            st.success(f"✓ {len(df_up)} rows × {len(df_up.columns)} columns")
        except Exception as e: st.error(f"Could not read: {e}")

# ══════════════════════════════════════════════════════
# TAB 7 — AI ADVISOR
# ══════════════════════════════════════════════════════
with tab7:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px;padding:20px;background:var(--surface);border:1px solid var(--border);border-radius:14px;border-left:3px solid var(--sapp3)">
      <div style="font-size:36px">💎</div>
      <div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;color:#3d2b10">Gekko AI Advisor</div>
        <div style="font-size:10px;letter-spacing:2px;color:#8a7560;text-transform:uppercase;margin-top:2px">Powered by Claude · Knows your portfolio · Teaches as it advises</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.markdown("""<div class="teach">
        <strong>🔑 Activate AI Advisor</strong> — Add your Anthropic API key in the sidebar.<br>
        Get a free key at <strong>console.anthropic.com</strong> in 2 minutes.<br>
        Once active: ask about your portfolio, get stock analysis, learn IB concepts, build investment strategy.
        </div>""", unsafe_allow_html=True)
    else:
        quick_qs=["Analyze my portfolio risk","Which holding has best upside?","Am I well diversified?",
            "Explain Sharpe Ratio simply","Explain DCF in plain English","What is WACC?",
            "What's my riskiest position?","Build me a portfolio strategy","Explain beta vs volatility",
            "What is a good Sharpe ratio?","How do T-bills fit in a portfolio?","Explain correlation in investing"]
        st.markdown('<div style="font-size:10px;letter-spacing:2px;color:#8a7560;text-transform:uppercase;margin-bottom:10px">Quick Questions</div>', unsafe_allow_html=True)
        cols_q=st.columns(4)
        for i,q in enumerate(quick_qs):
            with cols_q[i%4]:
                if st.button(q,key=f"qq_{i}",use_container_width=True):
                    st.session_state.chat_history.append({"role":"user","content":q})
                    ctx=portfolio_ctx()
                    with st.spinner(""):
                        reply=ask_ai([{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history],
                            SYSTEM_PROMPT+f"\n\n{ctx}",st.session_state.api_key)
                    st.session_state.chat_history.append({"role":"assistant","content":reply})
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-wrap" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
              <div style="font-family:'Cormorant Garamond',serif;font-size:42px;color:#c9a84c">💎</div>
              <div style="font-size:13px;color:#8a7560;margin-top:12px;text-align:center;max-width:360px;line-height:1.8">
                Ask me anything about your portfolio, financial concepts, or investment strategy.<br>
                <span style="color:#c9a84c">I know your holdings and I'll teach you as I advise.</span>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            msgs_html=""
            for m in st.session_state.chat_history:
                if m["role"]=="user":
                    msgs_html+=f'<div class="chat-label" style="text-align:right">You</div><div class="chat-user">{m["content"]}</div>'
                else:
                    msgs_html+=f'<div class="chat-label">🦎 Gekko</div><div class="chat-ai">{m["content"]}</div>'
            st.markdown(f'<div class="chat-wrap">{msgs_html}</div>', unsafe_allow_html=True)

        inp_col,btn_col=st.columns([5,1])
        with inp_col:
            user_in=st.text_input("Ask Gekko anything...",
                placeholder="e.g. Should I add T-bills to balance my semiconductor exposure?",
                key="chat_in",label_visibility="collapsed")
        with btn_col:
            send=st.button("SEND ▶",use_container_width=True,key="send_btn")

        if send and user_in:
            st.session_state.chat_history.append({"role":"user","content":user_in})
            ctx=portfolio_ctx()
            with st.spinner(""):
                reply=ask_ai([{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history],
                    SYSTEM_PROMPT+f"\n\n{ctx}",st.session_state.api_key)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        cl1,cl2=st.columns([2,8])
        with cl1:
            if st.session_state.chat_history:
                if st.button("Clear conversation",key="clear_chat"):
                    st.session_state.chat_history=[]; st.rerun()
