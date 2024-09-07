import streamlit as st
from openai import OpenAI
import os

# OpenAI 클라이언트 초기화
openai_api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=openai_api_key)

# Streamlit 앱 레이아웃
st.title("AI 이미지 생성기")
st.write("텍스트 프롬프트를 입력하고 AI 이미지를 생성하세요.")

# 텍스트 입력
prompt = st.text_input("프롬프트를 입력하세요:")

# 이미지 크기 선택 메뉴 추가
size_options = {
    "256x256 (Small)": "256x256",
    "512x512 (Medium)": "512x512",
    "1024x1024 (Large)": "1024x1024"
}
selected_size = st.selectbox("이미지 크기 선택:", list(size_options.keys()))
image_size = size_options[selected_size]  # 선택된 크기에 따라 크기 값 설정

# 이미지 스타일 선택 메뉴 추가
style_options = {
    "스케치": "sketch style",
    "수채화": "watercolor style",
    "사진 화법": "photo style"
}
selected_style = st.selectbox("이미지 스타일 선택:", list(style_options.keys()))
image_style = style_options[selected_style]  # 선택된 스타일에 따른 스타일 값 설정

# "이미지 생성" 버튼
if st.button("이미지 생성"):
    if prompt:
        try:
            # 프롬프트에 스타일을 추가하여 최종 프롬프트 생성
            final_prompt = f"{prompt}, {image_style}"

            kwargs = {
                "prompt": final_prompt,
                "n": 2,  # 이미지 2개 생성
                "size": image_size  # 사용자가 선택한 크기를 적용
            }

            # OpenAI API를 사용하여 이미지 생성
            response = client.images.generate(**kwargs)

            # 응답에서 이미지 URL 추출
            image_urls = [image.url for image in response.data]

            # 생성된 이미지 표시
            for i, image_url in enumerate(image_urls):
                st.image(image_url, caption=f"생성된 이미지 {i+1}: {selected_style}", use_column_width=True)

        except Exception as e:
            st.error(f"이미지 생성 중 오류 발생: {e}")
    else:
        st.warning("이미지를 생성하려면 프롬프트를 입력하세요.")
