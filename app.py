import pandas as pd
import streamlit as st

# 設定網頁標題與寬度
st.set_page_config(
    page_title="Dinotaeng 的溫馨記帳本 🦘", page_icon="🦘", layout="centered"
)

# 初始化 Session State (儲存記帳資料)
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["日期", "類型", "分類", "金額", "備忘"]
    )

# 頁面標題
st.title("🦘 Dinotaeng 的溫馨記帳本")
st.write("把每一筆花費照顧好，讓 BoBo 陪你過得舒適又自在～ Marshmallow✨")
st.markdown("---")

# --- 側邊欄：新增記帳 ---
st.sidebar.header("✨ 記一筆新帳")

with st.sidebar.form("expense_form", clear_on_submit=True):
    t_date = st.date_input("日期")
    t_type = st.radio("類型", ["支出 💸", "收入 💰"], horizontal=True)

    # 依照類型動態調整分類
    if "支出" in t_type:
        categories = ["飲食 🍔", "交通 🚇", "生活用品 🧴", "盲盒與周邊 🧸", "其他 📌"]
    else:
        categories = ["薪資 💼", "二手出清 📦", "其他 🏷️"]

    t_category = st.selectbox("分類", categories)
    t_amount = st.number_input("金額 (元)", min_value=1, step=10, value=100)
    t_memo = st.text_input("備忘 / 說明 (選填)")

    submit_btn = st.form_submit_button("送出紀錄 🍃")

    if submit_btn:
        new_data = pd.DataFrame(
            [
                {
                    "日期": t_date,
                    "類型": t_type,
                    "分類": t_category,
                    "金額": t_amount,
                    "備忘": t_memo if t_memo else "-",
                }
            ]
        )
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, new_data], ignore_index=True
        )
        st.sidebar.success("成功新增一筆紀錄！🎉")

# --- 主畫面：財務概況與明細 ---

df = st.session_state.transactions

if not df.empty:
    # 計算總收入、總支出、結餘
    total_income = df[df["類型"] == "收入 💰"]["金額"].sum()
    total_expense = df[df["類型"] == "支出 💸"]["金額"].sum()
    balance = total_income - total_expense

    # 顯示指標卡片
    col1, col2, col3 = st.columns(3)
    col1.metric("總收入 💰", f"${total_income:,.0f}")
    col2.metric("總支出 💸", f"${total_expense:,.0f}")
    col3.metric("目前結餘 🌿", f"${balance:,.0f}")

    st.markdown("---")

    # 帳目明細表
    st.subheader("📜 近期記帳明細")

    # 排序：依照日期由新到舊
    df_display = df.sort_values(by="日期", ascending=False).reset_index(
        drop=True
    )
    st.dataframe(df_display, use_container_width=True)

    # 刪除紀錄功能
    if not df.empty:
        st.markdown("### 🗑️ 管理紀錄")
        delete_idx = st.selectbox(
            "選擇要刪除的紀錄編號",
            options=df_display.index,
            format_func=lambda x: f"#{x} - {df_display.loc[x, '日期']} | {df_display.loc[x, '類型']} | {df_display.loc[x, '分類']} | ${df_display.loc[x, '金額']}",
        )
        if st.button("刪除此筆紀錄"):
            # 找到原本 df 中的正確索引並刪除
            original_idx = df.sort_values(
                by="日期", ascending=False
            ).index[delete_idx]
            st.session_state.transactions = (
                st.session_state.transactions.drop(original_idx)
                .reset_index(drop=True)
            )
            st.success("已刪除該筆紀錄！")
            st.rerun()

    # 分類支出統計
    st.markdown("---")
    st.subheader("📊 支出分類佔比")
    expense_df = df[df["類型"] == "支出 💸"]
    if not expense_df.empty:
        expense_by_cat = expense_df.groupby("分類")["金額"].sum()
        st.bar_chart(expense_by_cat)
    else:
        st.info("目前還沒有支出紀錄，BoBo 覺得非常棒呢！✨")

else:
    st.info("👋 目前還沒有任何記帳資料，請從左側欄位新增第一筆紀錄吧！")
    st.markdown(
        "> *「就像吃棉花糖一樣甜美，把每一筆帳目都記好，生活就會軟綿綿很安心～」*"
    )
