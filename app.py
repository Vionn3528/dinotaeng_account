import streamlit as st
import pandas as pd

# 頁面基本設定
st.set_page_config(
    page_title="盲盒收納整理",
    page_icon="🧸",
    layout="centered"
)

# 標題與溫馨小語
st.markdown("🧸 **盲盒收藏與收納整理**")
st.markdown("把每一隻可愛的小寶貝照顧好，讓盲盒們陪你過得舒適又自在～ Marshmallow ✨")
st.markdown("---")

# 側邊欄：新增/記錄盲盒項目
st.sidebar.header("📦 新增或記錄盲盒")

# 狀態選擇
item_status = st.sidebar.radio(
    "記錄類型", 
    ["已收藏入櫃", "尋找新主人 (售出/交換)", "待補齊/許願"]
)

item_name = st.sidebar.text_input("盲盒名稱 / 系列")
item_category = st.sidebar.selectbox(
    "角色系列", 
    ["Dinotaeng", "Miffy", "Sanrio (三麗鷗)", "其他盲盒系列"]
)
item_price = st.sidebar.number_input("入手金額 / 預估價值 (元)", min_value=0, value=300, step=50)

# 初始化記錄資料庫 (簡單用 Session 儲存)
if 'blind_box_data' not in st.session_state:
    st.session_state.blind_box_data = pd.DataFrame(columns=[
        "狀態", "名稱", "系列", "金額"
    ])

if st.sidebar.button("確認新增"):
    if item_name.strip() == "":
        st.sidebar.warning("請輸入盲盒名稱喔！")
    else:
        new_data = pd.DataFrame({
            "狀態": [item_status],
            "名稱": [item_name],
            "系列": [item_category],
            "金額": [item_price]
        })
        st.session_state.blind_box_data = pd.concat(
            [st.session_state.blind_box_data, new_data], 
            ignore_index=True
        )
        st.sidebar.success("成功加入收納清單！")

# 主畫面：顯示統計與整體清單
col1, col2 = st.columns(2)

total_items = len(st.session_state.blind_box_data)
total_value = st.session_state.blind_box_data["金額"].sum() if total_items > 0 else 0

with col1:
    st.metric(label="🧸 收藏總數", value=f"{total_items} 個")

with col2:
    st.metric(label="💰 總花費/收藏價值", value=f"${total_value:,}")

st.markdown("---")

# 搜尋功能區塊
st.subheader("🔍 搜尋盲盒")
search_keyword = st.text_input("輸入關鍵字搜尋名稱（例如：Bobo、庫洛米...）", "")

st.subheader("📋 盲盒收藏分類檢視")

if total_items > 0:
    df = st.session_state.blind_box_data
    
    # 如果有輸入關鍵字，就進行篩選
    if search_keyword.strip() != "":
        df = df[df["名稱"].str.contains(search_keyword, case=False, na=False)]
        st.info(f"✨ 包含關鍵字「{search_keyword}」的搜尋結果共 {len(df)} 筆")

    # 建立分類頁籤 (Tabs)
    categories = ["全部顯示", "Dinotaeng", "Miffy", "Sanrio (三麗鷗)", "其他盲盒系列"]
    tabs = st.tabs(categories)
    
    # 全部顯示 (或搜尋過後的結果)
    with tabs[0]:
        st.markdown("### 🌟 列表總覽")
        if len(df) > 0:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("沒有找到符合條件的盲盒喔！")
        
    # 各個分類分頁
    for i, cat in enumerate(categories[1:], start=1):
        with tabs[i]:
            st.markdown(f"### 🧸 {cat} 系列專區")
            # 結合分類與搜尋條件
            filtered_df = df[df["系列"] == cat]
            if len(filtered_df) > 0:
                st.dataframe(filtered_df, use_container_width=True)
                cat_total = filtered_df["金額"].sum()
                st.info(f"✨ {cat} 系列目前顯示 {len(filtered_df)} 個，總價值：${cat_total:,}")
            else:
                st.info(f"此系列目前沒有符合的盲盒記錄。")

    st.markdown("---")
    # 清空按鈕
    if st.button("清空所有記錄"):
        st.session_state.blind_box_data = pd.DataFrame(columns=["狀態", "名稱", "系列", "金額"])
        st.rerun()
else:
    st.info("目前還沒有記錄盲盒喔！趕快從側邊欄新增你的第一隻小可愛吧 ✨")
