import streamlit as st
import pandas as pd
from datetime import datetime

# 頁面基本設定
st.set_page_config(
    page_title="盲盒收納整理",
    page_icon="🧸",
    layout="centered"
)

# 初始化記錄資料庫 (包含建立日期與刪除選取欄位)
if 'blind_box_data' not in st.session_state:
    st.session_state.blind_box_data = pd.DataFrame(columns=[
        "選擇", "建立日期", "狀態", "名稱", "系列", "金額"
    ])

# 側邊欄：自訂介面名稱與新增項目
st.sidebar.header("⚙️ 介面與設定")
custom_title = st.sidebar.text_input("自訂網頁標題", "🧸 盲盒收藏與收納整理")

# 標題與溫馨小語
st.markdown(f"**{custom_title}**")
st.markdown("把每一隻可愛的小寶貝照顧好，讓盲盒們陪你過得舒適又自在～ Marshmallow ✨")
st.markdown("---")

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
item_date = datetime.now().strftime("%Y-%m-%d")

if st.sidebar.button("確認新增"):
    if item_name.strip() == "":
        st.sidebar.warning("請輸入盲盒名稱喔！")
    else:
        new_row = pd.DataFrame({
            "選擇": [False],
            "建立日期": [item_date],
            "狀態": [item_status],
            "名稱": [item_name],
            "系列": [item_category],
            "金額": [item_price]
        })
        st.session_state.blind_box_data = pd.concat(
            [st.session_state.blind_box_data, new_row], 
            ignore_index=True
        )
        st.sidebar.success("成功加入收納清單！")
        st.rerun()

# 主畫面：顯示統計與整體清單
total_items = len(st.session_state.blind_box_data)
total_value = st.session_state.blind_box_data["金額"].sum() if total_items > 0 else 0

col1, col2 = st.columns(2)
with col1:
    st.metric(label="🧸 收藏總數", value=f"{total_items} 個")
with col2:
    st.metric(label="💰 總花費/收藏價值", value=f"${total_value:,}")

st.markdown("---")

# 搜尋功能區塊
st.subheader("🔍 搜尋盲盒")
search_keyword = st.text_input("輸入關鍵字搜尋名稱（例如：Bobo、庫洛米...）", "")

st.subheader("📋 盲盒收藏分類與編輯檢視")

if total_items > 0:
    df = st.session_state.blind_box_data
    
    # 建立分類頁籤 (Tabs)
    categories = ["全部顯示", "Dinotaeng", "Miffy", "Sanrio (三麗鷗)", "其他盲盒系列"]
    tabs = st.tabs(categories)
    
    # 用來處理編輯或刪除的容器
    with st.form("edit_delete_form"):
        # 顯示全部或過濾後的結果
        if search_keyword.strip() != "":
            display_df = df[df["名稱"].str.contains(search_keyword, case=False, na=False)]
            st.info(f"✨ 包含關鍵字「{search_keyword}」的搜尋結果共 {len(display_df)} 筆")
        else:
            display_df = df

        # 全部顯示分頁
        with tabs[0]:
            st.markdown("### 🌟 列表總覽（支援表格內直接修改文字）")
            # 使用 data_editor 讓使用者可以直接在表格內修改名稱、金額或勾選刪除
            edited_df = st.data_editor(
                df, 
                use_container_width=True, 
                key="main_data_editor",
                num_rows="dynamic"
            )
            # 即時同步編輯後的資料
            st.session_state.blind_box_data = edited_df

        # 各個分類分頁
        for i, cat in enumerate(categories[1:], start=1):
            with tabs[i]:
                st.markdown(f"### 🧸 {cat} 系列專區")
                filtered_df = df[df["系列"] == cat]
                if len(filtered_df) > 0:
                    st.dataframe(filtered_df, use_container_width=True)
                    cat_total = filtered_df["金額"].sum()
                    st.info(f"✨ {cat} 系列共 {len(filtered_df)} 個，總價值：${cat_total:,}")
                else:
                    st.info(f"此系列目前沒有符合的盲盒記錄。")

        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            delete_selected = st.form_submit_button("🗑️ 刪除勾選的項目")
        with col_btn2:
            clear_all = st.form_submit_button("⚠️ 清空所有記錄")

        if delete_selected:
            # 過濾掉「選擇」為 True 的列
            st.session_state.blind_box_data = st.session_state.blind_box_data[
                st.session_state.blind_box_data["選擇"] != True
            ]
            st.success("已成功刪除勾選的項目！")
            st.rerun()

        if clear_all:
            st.session_state.blind_box_data = pd.DataFrame(columns=[
                "選擇", "建立日期", "狀態", "名稱", "系列", "金額"
            ])
            st.success("已清空所有記錄！")
            st.rerun()
else:
    st.info("目前還沒有記錄盲盒喔！趕快從側邊欄新增你的第一隻小可愛吧 ✨")
