from dspeech import STT

# 初始化模型
stt_handler = STT(model_name="paraformer-zh", vad_model="fsmn-vad", punc_model="ct-punc", emo_model="emotion2vec_plus_large")

# 加载音频文件
audio_file = "tests/output.wav"

# 语音转文字
transcribed_text = stt_handler.transcribe_file(audio_file)
print("语音转文字结果:", transcribed_text)

# 标点符号恢复
punctuated_text = stt_handler.punc_result(transcribed_text)
print("标点符号恢复结果:", punctuated_text)

# 情感分类
emotion = stt_handler.emo_classify(audio_file,start=0,end=5)
print("情感分类结果:", emotion)

# 语音活动检测
vad_segments = stt_handler.vad_file(audio_file,start=0,end=5)
print("语音活动检测结果:", vad_segments)
