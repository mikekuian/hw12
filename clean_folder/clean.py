import os
import shutil
import sys
import PIL

# Функція для транслітерації та нормалізації імен файлів
def normalize(name):
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'iu', 'я': 'ia',
    }
    normalized_name = ""
    for char in name:
        if char.lower() in translit_map:
            normalized_name += translit_map[char.lower()]
        elif char.isalpha() or char.isdigit():
            normalized_name += char
        else:
            normalized_name += '_'
    return normalized_name


# Функція для сортування та обробки папок
def clean_folder(folder_path):
    image_ext = ('jpeg', 'jpg', 'png', 'svg')
    video_ext = ('avi', 'mp4', 'mov', 'mkv')
    document_ext = ('doc', 'docx', 'txt', 'pdf', 'djvu','xlsx', 'pptx', 'tex', 'djvu')
    audio_ext = ('mp3', 'ogg', 'wav', 'amr')
    archive_ext = ('zip', 'gz', 'tar')

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_extension = file.split('.')[-1].lower()
            normalized_file_name = normalize(file.split('.')[0]) + '.' + file_extension

            if file_extension in image_ext:
                target_folder = 'images'
            elif file_extension in video_ext:
                target_folder = 'video'
            elif file_extension in document_ext:
                target_folder = 'documents'
            elif file_extension in audio_ext:
                target_folder = 'audio'
            elif file_extension in archive_ext:
                target_folder = 'archives'
                archive_subfolder = os.path.splitext(normalized_file_name)[0]
                archive_subfolder_path = os.path.join(target_folder, archive_subfolder)
                os.makedirs(archive_subfolder_path, exist_ok=True)
                try:
                    shutil.unpack_archive(os.path.join(root, file), archive_subfolder_path)
                except:
                    pass
                continue
            else:
                target_folder = 'unknown'

            target_folder_path = os.path.join(folder_path, target_folder)
            os.makedirs(target_folder_path, exist_ok=True)
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_folder_path, normalized_file_name)
            shutil.move(source_file_path, target_file_path)

        for dir in dirs:
            if dir not in ('archives', 'video', 'audio', 'documents', 'images'):
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass


def main():
    folder_path = input("Enter the folder path: ")
    clean_folder(folder_path)


if __name__ == "__main__":
    main()
