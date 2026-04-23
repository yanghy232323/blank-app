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
import os

# 從 Secrets 中讀取你的 API Token
replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]
os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

if st.button("開始生成封面"):
    if not style_files:
        st.error("請先上傳至少一張風格參考圖！")
    else:
        st.info("🎨 正在捕捉風格並生成封面，請稍候約 30 秒...")
        
        try:
            # 1. 準備提示詞 (Prompt)
            final_prompt = f"An album cover, {genre} style, {description}, high quality, digital art"
            
            # 2. 呼叫 Replicate API
            # 我們使用 FLUX 搭配 IP-Adapter 來實現你的「餵風格」需求
            output = replicate.run(
                "lucataco/flux-dev-ip-adapter:81896898d933757303f27a6962f3a8b417c805eb319983ed81d4590458117765",
                input={
                    "prompt": final_prompt,
                    "image": style_files[0], # 使用你上傳的第一張風格圖
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "guidance_scale": 3.5
                }
            )

            # 3. 顯示結果
            if output:
                st.image(output[0], caption="AI 生成的初步封面", use_column_width=True)
                st.success("生成成功！")
                
                # 提供下載按鈕
                st.download_button("下載封面圖片", output[0], file_name="album_cover.webp")
                
        except Exception as e:
            st.error(f"發生錯誤：{e}")
