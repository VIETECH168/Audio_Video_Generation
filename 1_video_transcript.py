import os
from moviepy.editor import VideoFileClip, AudioFileClip
from function import extract_audio_from_video, get_large_audio_transcription_on_silence, translate_to_vietnamese, get_video_name

# Định nghĩa đường dẫn tới thư mục "Input Video"
input_folder = 'Input Video/'

if __name__ == "__main__":
    # Kiểm tra xem thư mục có tồn tại hay không
    if not os.path.exists(input_folder):
        print(f"Thư mục '{input_folder}' không tồn tại!")  # In ra thông báo nếu thư mục không có
    else:
        # Lặp qua tất cả các tệp trong thư mục
        for filename in os.listdir(input_folder):
            if filename.endswith(('.mp4', '.avi', '.mov')):  # Kiểm tra xem tệp có phải là video với các phần mở rộng hỗ trợ không
                # Xây dựng đường dẫn đầy đủ tới tệp video
                video_path = os.path.join(input_folder, filename)

                # Lấy tên video và tệp video
                video_file, video_name = get_video_name(video_file=video_path)  # Lấy thông tin video

                # Định dạng lại đường dẫn tệp video đầu ra, thêm "_edited" vào tên video
                output_video = f"Output Video/{video_name[:-4]}_edited.mp4"  # Xóa phần mở rộng .mp4 và thêm _edited
                
                # Tải tệp video bằng MoviePy
                video_clip = VideoFileClip(video_file)
                video_duration = video_clip.duration  # Lấy thời lượng video

                # Trích xuất âm thanh từ tệp video
                audio_clip = extract_audio_from_video(video_file)

                # Chuyển đổi âm thanh thành văn bản 
                transcribed_text = get_large_audio_transcription_on_silence(audio_clip)
                print("Văn bản đã chuyển ngữ:", transcribed_text)  # In ra văn bản đã chuyển ngữ

                # Dịch văn bản đã chuyển ngữ sang tiếng Việt
                vietnamese_translation = translate_to_vietnamese(transcribed_text)
                print(vietnamese_translation)  # In ra bản dịch tiếng Việt

                # Lưu bản ghi âm tiếng Anh vào một tệp văn bản
                with open(f'Output Video/transcript/{video_name[:-4]}_english.txt', 'w', encoding='utf-8') as file:
                    file.write(transcribed_text)  # Ghi văn bản tiếng Anh đã chuyển ngữ vào tệp

                # Lưu bản dịch tiếng Việt vào một tệp văn bản
                with open(f'Output Video/transcript/{video_name[:-4]}_vietnamese.txt', 'w', encoding='utf-8') as file:
                    file.write(vietnamese_translation)  # Ghi bản dịch tiếng Việt vào tệp
