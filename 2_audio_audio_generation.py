import os
from function import convert_text_to_audio, get_video_name, add_audio_to_video
from moviepy.editor import VideoFileClip

if __name__ == "__main__":
    # Lấy đường dẫn và tên video từ file đầu vào
    video_file, video_name = get_video_name(video_file="Input Video/Self-Healing Metal Shocks Scientists in Experiment.mp4")
    
    # Tải video clip
    video_clip = VideoFileClip(video_file)

    # Lấy tên file video (chỉ tên file, không bao gồm đường dẫn)
    video_name = os.path.basename(video_file)
    
    # Đọc nội dung bản dịch tiếng Việt từ file transcript
    transcript_path = f'Output Video/transcript/{video_name[:-4]}_vietnamese.txt'
    with open(transcript_path, 'r', encoding='utf-8') as file:
        vietnamese_translation = file.read()
    
    # Tạo đường dẫn cho file âm thanh đầu ra
    audio_output = f'Output Video/audio/{video_name[:-4]}_audio.mp3'
    
    # Chuyển đổi nội dung văn bản tiếng Việt thành file âm thanh
    output_audio = convert_text_to_audio(vietnamese_translation, language='vi', output_filename=audio_output)

    # Tạo đường dẫn cho file video đầu ra
    output_video = f"Output Video/{video_name[:-4]}_edited.mp4"
    
    # Thêm âm thanh đã tạo vào video
    add_audio_to_video(video_clip, output_audio, output_video)

    # Thông báo hoàn thành
    print(f"Video đã được xử lý và lưu tại: {output_video}")
