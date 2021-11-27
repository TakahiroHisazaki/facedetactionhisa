import streamlit as st
import requests
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

st.title('表情認識アプリ')
st.header('概要')
st.write('こちらは人物の顔画像を読み込んで年齢推定や感情推定ができるアプリです。画像内の顔を分析するAIを搭載したAzure Face APIを利用しています。リンクは下記です。')
st.markdown('<a href="https://azure.microsoft.com/ja-jp/services/cognitive-services/face/">Azure Face API</a>', unsafe_allow_html=True)


subscription_key = '9e8317968d3d4dff826add79d0c52512'
assert subscription_key

face_api_url = 'https://20211126facedetection.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an imag'e...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #binary data取得 

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    draw = ImageDraw.Draw(img)
    textsize = 18 # 描画するテキストの大きさ
    font = ImageFont.truetype("arial.ttf", size=textsize)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        textage = result['faceAttributes']['age']
        textemotion = result['faceAttributes']['emotion']
        draw.rectangle([(rect['left'], rect['top']),(rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=5)
        draw.text((rect['left']-70, rect['top']-10),'age='+str(textage), font=font, fill='red', spacing=1, align='left')
        draw.text((rect['left']+rect['width']+2, rect['top']-10),'anger='+str(textemotion['anger'])+'\ncontempt='+str(textemotion['contempt'])+'\ndisgust='+str(textemotion['disgust'])+'\nfear='+str(textemotion['fear'])+'\nhappiness='+str(textemotion['happiness'])+'\nneutral='+str(textemotion['neutral'])+'\nsadness='+str(textemotion['sadness'])+'\nsurprise='+str(textemotion['surprise']), font=font, fill='blue', spacing=1, align='left')

    st.image(img, caption='Uploaded Image.', use_column_width = True)