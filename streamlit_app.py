import streamlit as st
import replicate # 這是連接 AI 繪圖的插件

# 網頁標題
st.title("🎨 AI 專輯封面生成器")
st.subheader("為你的音樂打造專屬視覺")

# 第一部分：餵風格 (Style)
st.header("1. 風格設定")
style_files = st.file_uploader("上傳你喜歡的風格參考圖", accept_multiple_files=True)

# 第二部分：輸入內容 (Context)
st.header("2. 專輯資訊")
genre = st.text_input("曲風 (例如: Lo-fi, Synthwave, Jazz)")
description = st.text_area("專輯介紹 (想傳達的感覺或故事)")

# 第三部分：素材與規格 (Specs)
st.header("3. 素材與輸出規格")
content_file = st.file_uploader("上傳你的核心視覺素材 (可選)")
size = st.selectbox("輸出尺寸", ["3000 x 3000 (Spotify 標準)", "1024 x 1024"])

# 按鈕：開始生成
if st.button("開始生成封面"):
    st.info("AI 正在解析風格並作畫中，請稍候...")
    # 這裡未來會接上 Replicate API 的呼叫
    st.success("生成完成！(目前為原型演示)")
