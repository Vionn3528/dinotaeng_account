import streamlit as pd_streamlit
import pandas as pd

# 頁面基本設定
pd_streamlit.set_page_config(
    page_title="盲盒收納整理",
    page_icon="🧸",
    layout="centered"
)

# 標題與溫馨小語
pd_streamlit.markdown("🧸 **盲盒收藏與收納整理**")
pd_streamlit.markdown("把每一隻可愛的小寶貝照顧好，讓盲盒們陪你過得舒適又自在～ Marshmallow ✨")
pd_streamlit.markdown("---")

# 側邊欄：新增/記錄盲盒項目
pd_streamlit.sidebar.header("📦 新增或記錄盲盒")

# 狀態選擇
item_status = pd_streamlit.sidebar.radio(
    "記錄類型", 
    ["已收藏入櫃", "尋找新主人 (售出/交換)", "待補齊/許願"]
)

item_name = pd_streamlit.sidebar.text_input("盲盒名稱 / 系列")
item_category = pd_streamlit.sidebar.selectbox(
    "角色系列", 
    ["Dinotaeng", "Miffy", "Sanrio (三麗鷗)", "其他盲盒系列"]
)
item_price = pd_streamlit.sidebar.number_input("入手金額 / 預估價值 (元)", min_value=0, value=300, step=50)

# 初始化記錄資料庫 (簡單用 Session 儲存)
if 'blind_box_data' not in pd_streamlit.session_state:
    pd_streamlit.session_state.blind_box_data = pd.DataFrame(columns=[
        "狀態", "名稱", "系列", "金額"
    ])

if pd_streamlit.sidebar.button("確認新增"):
    new_data = pd.DataFrame({
        "狀態": [item_status],
        "名稱": [item_name],
        "系列": [item_category],
        "金額": [item_price]
    })
    pd_streamlit.session_state.blind_box_data = pd.concat(
        [pd_streamlit.session_state.blind_box_data, new_data], 
        ignore_index=True
    )
    pd_streamlit.sidebar.success("成功加入收納清單！")

# 主畫面：顯示統計與清單
col1, col2 = pd_streamlit.columns(2)

total_items = len(pd_streamlit.session_state.blind_box_data)
total_value = pd_streamlit.session_state.blind_box_data["金額"].sum() if total_items > 0 else 0

with col1:
    pd_streamlit.metric(label="🧸 收藏總數", value=f"{total_items} 個")

with col2:
    pd_streamlit.metric(label="💰 總花費/收藏價值", value=f"${total_value:,}")

pd_streamlit.markdown("---")
pd_streamlit.subheader("📋 目前的盲盒收藏清單")

if total_items > 0:
    pd_streamlit.dataframe(pd_streamlit.session_state.blind_box_data, use_container_width=True)
    
    # 清空按鈕
    if pd_streamlit.button("清空所有記錄"):
        pd_streamlit.session_state.blind_box_data = pd.DataFrame(columns=["狀態", "名稱", "系列", "金額"])
        pd_streamlit.experimental_rerun()
else  :
    pd_streamlit.info("目前還沒有記錄盲盒喔！趕快從側邊欄新增你的第一隻小可愛吧 ✨")
