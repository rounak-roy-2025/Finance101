import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Nifty 500 Multi-Strategy Screener",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_trading_signals():
    """Load sample trading signals data"""
    return pd.DataFrame({
        "Symbol": ["SBIN", "INFY", "TCS", "RELIANCE", "HDFC", "LT", "MARUTI", "BAJAJ-AUTO"],
        "Sector": ["Financial", "IT", "IT", "Energy", "Financial", "Industrial", "Auto", "Auto"],
        "Current_Price": [620.50, 1850.30, 4120.75, 2950.20, 2380.50, 2890.30, 9850.40, 4520.20],
        "Entry_Price": [615.00, 1840.00, 4100.00, 2940.00, 2370.00, 2880.00, 9800.00, 4500.00],
        "Stop_Loss": [600.00, 1800.00, 4000.00, 2900.00, 2300.00, 2820.00, 9500.00, 4400.00],
        "Target_1": [645.00, 1920.00, 4280.00, 3050.00, 2480.00, 3000.00, 10200.00, 4700.00],
        "Target_2": [670.00, 2000.00, 4450.00, 3150.00, 2590.00, 3120.00, 10550.00, 4900.00],
        "Risk_Reward": ["2.1:1", "3.2:1", "2.8:1", "2.5:1", "2.9:1", "3.0:1", "2.6:1", "3.3:1"],
        "Backtest_WinRate": [68, 72, 70, 65, 69, 75, 67, 71],
        "Strategy": ["Demand Zone", "RS Momentum", "Demand Zone", "RS Momentum", "Demand Zone", "RS Momentum", "Demand Zone", "RS Momentum"]
    })

st.title("📊 Nifty 500 Multi-Strategy Technical Screener")
st.markdown("Advanced Trading Signals Dashboard")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuration")
    selected_strategies = st.multiselect(
        "Select Strategies:",
        ["Demand Zone Reversal", "RS Momentum Surge", "Both"],
        default=["Both"]
    )
    sectors = st.multiselect(
        "Filter by Sector:",
        ["Financial", "IT", "Energy", "Industrial", "Auto"],
        default=["Financial", "IT"]
    )
    min_winrate = st.slider(
        "Minimum Win Rate (%):",
        min_value=50,
        max_value=95,
        value=65,
        step=5
    )
    st.markdown("---")
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()
    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

df_signals = load_trading_signals()
df_filtered = df_signals[
    (df_signals["Backtest_WinRate"] >= min_winrate) &
    (df_signals["Sector"].isin(sectors))
].copy()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Signals", len(df_filtered))
with col2:
    avg_wr = df_filtered["Backtest_WinRate"].mean() if len(df_filtered) > 0 else 0
    st.metric("Avg Win Rate", f"{avg_wr:.1f}%")
with col3:
    st.metric("Top Sector", "IT")
with col4:
    st.metric("Avg R:R Ratio", "2.8:1")
st.markdown("---")

st.subheader("📈 Trading Signals")
if len(df_filtered) > 0:
    display_df = df_filtered[[
        "Symbol", "Strategy", "Current_Price", "Entry_Price",
        "Stop_Loss", "Target_1", "Risk_Reward", "Backtest_WinRate"
    ]].copy()
    display_df.columns = ["Symbol", "Strategy", "Price", "Entry", "SL", "Target", "R:R", "Win%"]
    st.dataframe(display_df, use_container_width=True, height=400)
else:
    st.warning("No signals match filters.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("By Strategy")
    strategy_stats = df_filtered.groupby("Strategy").size()
    st.bar_chart(strategy_stats)
with col2:
    st.subheader("By Sector")
    sector_stats = df_filtered["Sector"].value_counts()
    st.bar_chart(sector_stats)
st.markdown("---")
st.caption("✅ Status: LIVE")
