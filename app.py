import myfitnesspal
from datetime import date
import streamlit as st

# 1. 登入設定 (請在實際運行時替換為你的帳號密碼)
# 建議使用 Streamlit 的 secrets 管理密碼以保安全
USER_ID = "你的MFP帳號"
PASSWORD = "你的MFP密碼"

def get_mfp_data():
    try:
        client = myfitnesspal.Client(USER_ID, PASSWORD)
        day = client.get_date(date.today())
        return day
    except Exception as e:
        st.error(f"連線 MFP 失敗: {e}")
        return None

st.title("🔥 體態巔峰管理系統 (MFP 同步版)")

# --- 2. 獲取並顯示營養數據 ---
day_data = get_mfp_data()

if day_data:
    totals = day_data.totals
    # MFP 資料庫通常包含: calories, carbohydrates, fat, protein, sugar
    protein = totals.get('protein', 0)
    carbs = totals.get('carbohydrates', 0)
    sugar = totals.get('sugar', 0)
    calories = totals.get('calories', 0)

    st.subheader(f"📅 今日營養摘要 ({date.today()})")
    col1, col2, col3 = st.columns(3)
    col1.metric("蛋白質", f"{protein}g")
    col2.metric("總碳水", f"{carbs}g")
    col3.metric("糖攝取", f"{sugar}g")

    # --- 3. 針對糖量的即時控管 ---
    if sugar > 25:
        st.error(f"⚠️ 警告：今日糖量已達 {sugar}g！這會導致胖胖臉與腹部脂肪囤積，請停止攝取精緻糖。")
    else:
        st.success(f"✅ 今日控糖表現優秀！目前糖量：{sugar}g")

# --- 4. 針對肌力與心肺的專業建議 ---
st.divider()
st.header("🏋️ 專屬運動建議")

if sugar > 30:
    st.warning("👉偵測到糖分偏高：強烈建議今日增加 **30分鐘高強度心肺 (HIIT)** 來消耗掉血糖，避免轉化為腹部脂肪。")
else:
    st.info("👉狀態良好：今日適合進行 **大重量肌力訓練**（深蹲、硬舉），增加肌肉量來提升基礎代謝。")

# --- 5. 體重與進度追蹤 ---
weight = st.number_input("今日體重 (kg)", step=0.1)
if st.button("記錄數據並分析"):
    st.write(f"當前體重：{weight}kg。目標：遠離人生巔峰，邁向精實線條！")
