import streamlit as st
import replicate
import os

# 1. 讀取金鑰 (從你的 Streamlit Secrets)
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("請在 Secrets 設定中配置 REPLICATE_API_TOKEN")

# 網頁標題與介紹
st.set_page_config(page_title="AI 專輯封面生成器", page_icon="🎨")
st.title("🎨 AI 專輯封面生成器")
st.markdown("---")

# --- 第一部分：風格設定 ---
st.header("1. 風格設定")
style_files = st.file_uploader("上傳你喜歡的風格參考圖", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# --- 第二部分：專輯資訊 ---
st.header("2. 專輯資訊")
album_title = st.text_input("專輯名稱 (之後會印在封面上面)", placeholder="例如: Midnight City")
artist_name = st.text_input("歌手/團體名稱", placeholder="例如: The Dreamers")
genre = st.text_input("曲風", placeholder="例如: Lo-fi, Synthwave, Jazz")
description = st.text_area("專輯介紹 (想傳達的感覺)", placeholder="描述一下這張專輯的故事或畫面感...")

# --- 第三部分：素材 ---
st.header("3. 核心素材")
content_file = st.file_uploader("上傳你的核心視覺素材 (例如主唱照片或特定物件)", type=["png", "jpg", "jpeg"])

# --- 生成按鈕 ---
st.markdown("---")
if st.button("🚀 開始生成 Spotify 標準封面", use_container_width=True):
    if not style_files:
        st.warning("請至少上傳一張『風格參考圖』，讓 AI 知道你喜歡什麼感覺。")
    else:
        st.info("🎨 AI 正在分析風格並構圖，請稍候約 30-60 秒...")
        
        try:
            # 建立 Prompt
            prompt_text = f"Professional album cover art, {genre} style. {description}. High quality, artistic."
            
            # 呼叫 Replicate API (更換為更穩定的 FLUX 模型路徑)
            output = replicate.run(
                "black-forest-labs/flux-dev",
                input={
                    "prompt": prompt_text,
                    "image_prompt": style_files[0], # 這裡會參考你的風格圖
                    "aspect_ratio": "1:1",
                    "output_format": "jpg",
                    "guidance_scale": 3.5,
                    "num_inference_steps": 28
                }
            )
            
            if output:
                # 取得圖片的網址或數據
                # Replicate 的 FLUX 模型有時回傳清單，有時回傳單一物件
                image_url = output[0] if isinstance(output, list) else output

                # 顯示圖片
                st.image(image_url, caption=f"預覽：{album_title}", use_container_width=True)
                
                st.success("✅ 生成成功！這是一張符合 1:1 比例的底圖。")
                
                # 提供下載按鈕（直接連結到生成的圖片）
                st.markdown(f'[👉 點我開啟並儲存高解析度原圖]({image_url})')
                
                # 下載按鈕
                st.download_button(
                    label="💾 下載這張封面",
                    data=output[0],
                    file_name="album_cover_raw.jpg",
                    mime="image/jpeg"
                )

        except Exception as e:
            st.error(f"哎呀，出錯了：{e}")
