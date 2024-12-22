from moviepy.editor import VideoFileClip, AudioFileClip
from playsound import playsound
from googletrans import Translator
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from gtts import gTTS
import transformers
import torch
from moviepy.video.fx.all import speedx  # Sửa đúng cách nhập thư viện speedx
import boto3
from deep_translator import GoogleTranslator

def get_video_name(video_file="Input Video/10_10_6.mp4" ):
    """
    Lấy tên của tệp video từ đường dẫn của nó.

    Tham số:
    - video_file (str): Đường dẫn đầy đủ đến tệp video.

    Trả về:
    - str: Tên tệp video không có đường dẫn thư mục.
    """
    # Lấy tên video
    video_name = os.path.basename(video_file)
    return video_file, video_name

# Hàm chuyển đổi MP3 thành WAV
def convert_mp3_to_wav(mp3_path):
    """Chuyển đổi tệp MP3 sang định dạng WAV."""
    wav_path = mp3_path.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")
    return wav_path

# Hàm nhận diện giọng nói trong tệp âm thanh
def transcribe_audio(path):
    """Chuyển âm thanh thành văn bản sử dụng API Google Web Speech."""
    try:
        # Sử dụng tệp âm thanh làm nguồn âm thanh
        with sr.AudioFile(path) as source:
            # Ghi âm từ tệp
            audio_listened = r.record(source)
            # Thử chuyển âm thanh thành văn bản qua API nhận diện giọng nói của Google
            text = r.recognize_google(audio_listened)
        return text
    except sr.UnknownValueError:
        # Xử lý khi không thể nhận diện được giọng nói
        print(f"Google Speech Recognition không thể hiểu âm thanh từ {path}.")
        return ""
    except sr.RequestError as e:
        # Xử lý lỗi kết nối API
        print(f"Không thể yêu cầu kết quả từ dịch vụ Google Speech Recognition; {e}")
        return ""

# Hàm chia tệp âm thanh thành các đoạn nhỏ dựa trên khoảng lặng và áp dụng nhận diện giọng nói
def get_large_audio_transcription_on_silence(path):
    """
    Chia tệp âm thanh lớn thành các đoạn nhỏ
    và áp dụng nhận diện giọng nói trên mỗi đoạn.
    """
    # Kiểm tra xem tệp có định dạng MP3 và chuyển sang WAV nếu cần thiết
    if path.endswith(".mp3"):
        print(f"Đang chuyển {path} thành định dạng WAV...")
        path = convert_mp3_to_wav(path)

    try:
        # Mở tệp âm thanh bằng pydub
        sound = AudioSegment.from_wav(path)
    except Exception as e:
        print(f"Lỗi khi mở tệp âm thanh: {e}")
        return ""

    # Chia âm thanh nơi có lặng từ 500 mili giây trở lên và lấy các đoạn
    chunks = split_on_silence(
        sound,
        # Chiều dài tối thiểu của lặng sẽ được sử dụng để phát hiện điểm chia (500ms)
        min_silence_len=500,
        # Ngưỡng lặng (điều chỉnh dựa trên âm lượng của tệp âm thanh)
        silence_thresh=audio_clip.dBFS - 14,
        # Thêm 500ms lặng ở đầu và cuối mỗi đoạn
        keep_silence=500,
    )

    folder_name = "audio-chunks"
    # Tạo thư mục lưu các đoạn âm thanh nếu thư mục chưa tồn tại
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    # Xử lý mỗi đoạn âm thanh
    for i, audio_chunk in enumerate(chunks, start=1):
        # Xuất đoạn âm thanh và lưu vào thư mục `folder_name`
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # Nhận diện văn bản từ đoạn âm thanh
        print(f"Đang xử lý đoạn {i}...")
        text = transcribe_audio(chunk_filename)

        if text:
            # Viết hoa chữ cái đầu tiên và thêm dấu chấm ở cuối
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text

    # Trả về văn bản đã được chuyển ngữ
    return whole_text

def translate_to_vietnamese(text):
    translator = GoogleTranslator(source='auto', target='vi')
    translation = translator.translate(text)
    return translation

def convert_text_to_audio(text, language='vi', output_filename='Output Video/audio/vietnamese_audio.mp3'):
    """
    Chuyển văn bản thành tệp âm thanh bằng tiếng Việt và lưu nó.

    Tham số:
    - text (str): Văn bản cần chuyển thành âm thanh.
    - language (str): Mã ngôn ngữ cho tiếng Việt (mặc định là 'vi').
    - output_filename (str): Tên tệp âm thanh đầu ra.

    Trả về:
    - str: Đường dẫn đến tệp âm thanh đã lưu.
    """
    try:
        # Chuyển văn bản thành âm thanh
        tts = gTTS(text=text, lang=language, slow=False)
        # Lưu tệp âm thanh
        tts.save(output_filename)
        print(f"Đã lưu âm thanh với tên {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Lỗi khi chuyển văn bản thành âm thanh: {e}")
        return None
    

def add_audio_to_video(video, output_audio, output_video):
    """
    Thêm âm thanh vào tệp video.
    
    Tham số:
    - video_file (str): Đường dẫn đến tệp video gốc.
    - audio_file (str): Đường dẫn đến tệp âm thanh (định dạng MP3).
    - output_video (str): Đường dẫn để lưu video với âm thanh đã thêm.
    """
    # Tải tệp video và âm thanh
    audio = AudioFileClip(output_audio)
    
    # Gán âm thanh cho video
    final_video = video.set_audio(audio)
    
    # Lưu video kết quả
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

def match_audio_length(video_duration, audio_file, output_audio_file):
    """
    Điều chỉnh tốc độ âm thanh sao cho độ dài của nó khớp với độ dài video.

    Tham số:
    - video_duration (float): Thời gian của video.
    - audio_file (str): Đường dẫn đến tệp âm thanh.
    - output_audio_file (str): Đường dẫn để lưu âm thanh đã điều chỉnh.
    """
    # Tải tệp âm thanh
    audio_clip = AudioFileClip(audio_file)

    # Kiểm tra xem âm thanh đã được tải đúng chưa
    if audio_clip is None:
        print("Lỗi khi tải tệp âm thanh. Vui lòng kiểm tra đường dẫn và định dạng tệp.")
        return

    audio_duration = audio_clip.duration  # Thời gian âm thanh tính bằng giây

    print(f"Thời gian âm thanh gốc: {audio_duration:.2f} giây")
    print(f"Thời gian video mục tiêu: {video_duration:.2f} giây")

    # Tính toán yếu tố tốc độ để khớp độ dài âm thanh với video
    speed_factor = audio_duration / video_duration 

    # Điều chỉnh tốc độ âm thanh để khớp với độ dài video
    adjusted_audio_clip = audio_clip.fx(speedx, speed_factor)

    # Xuất âm thanh đã điều chỉnh ra tệp đầu ra
    adjusted_audio_clip.write_audiofile(output_audio_file)

    # Đóng âm thanh để giải phóng tài nguyên
    audio_clip.close()
    adjusted_audio_clip.close()

    print(f"Âm thanh đã điều chỉnh được lưu tại: {output_audio_file}")

def extract_audio_from_video(video_file):
    """
    Trích xuất âm thanh từ tệp video và trả về dưới dạng AudioSegment.
    """
    video_clip = VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video_clip.audio.write_audiofile(audio_file)
    video_clip.close()
    return AudioSegment.from_wav(audio_file)

# Hàm nhận diện giọng nói từ đoạn âm thanh
def transcribe_audio(chunk_filename):
    """
    Nhận diện giọng nói từ tệp âm thanh sử dụng thư viện nhận diện giọng nói.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(chunk_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print(f"Không thể hiểu âm thanh trong {chunk_filename}.")
            return ""
        except sr.RequestError as e:
            print(f"Không thể yêu cầu kết quả từ dịch vụ Google Speech Recognition; {e}")
            return ""

# Hàm chia âm thanh lớn thành các đoạn nhỏ và áp dụng nhận diện giọng nói
def get_large_audio_transcription_on_silence(audio_clip):
    """
    Chia âm thanh lớn thành các đoạn nhỏ và áp dụng nhận diện giọng nói trên mỗi đoạn.
    """
    try:
        # Sử dụng audio_clip trực tiếp, giả sử đây là một AudioSegment hợp lệ
        sound = audio_clip
    except Exception as e:
        print(f"Lỗi khi mở tệp âm thanh: {e}")
        return ""

    # Chia âm thanh tại các điểm có lặng 500ms trở lên và lấy các đoạn
    chunks = split_on_silence(
        sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14,
        keep_silence=500,
    )

    folder_name = "audio-chunks"
    # Tạo thư mục để lưu các đoạn âm thanh nếu chưa tồn tại
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    # Xử lý mỗi đoạn âm thanh
    for i, audio_chunk in enumerate(chunks, start=1):
        # Xuất đoạn âm thanh và lưu vào thư mục `folder_name`
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # Nhận diện văn bản từ đoạn âm thanh
        print(f"Đang xử lý đoạn {i}...")
        text = transcribe_audio(chunk_filename)

        if text:
            # Viết hoa chữ cái đầu tiên và thêm dấu chấm ở cuối
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text

    # Trả về văn bản đã chuyển ngữ
    return whole_text

# Hàm chuyển văn bản thành âm thanh sử dụng Polly của Amazon
def convert_text_to_audio_polly(text, output_filename, voice_id='Vy'):
    """
    Chuyển văn bản thành âm thanh bằng Polly của Amazon.

    Tham số:
    - text (str): Văn bản cần chuyển thành âm thanh.
    - output_filename (str): Đường dẫn để lưu âm thanh đầu ra.
    - voice_id (str): ID giọng nói, mặc định là Vy.
    """
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id
    )
    
    with open(output_filename, 'wb') as file:
        file.write(response['AudioStream'].read())

    return output_filename
