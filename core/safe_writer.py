import os, base64

class SafeWriter:
    @staticmethod
    def write_file_b64(filepath, b64_content):
        try:
            os.magedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(b64_content))
            return True
        except Exception as e:
            print(f'SafeWriter Error: {e}')
            return False

    @staticmethod
    def atomic_write(filepath, content):
        temp_path = filepath + '.tmp'
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.replace(temp_path, filepath)
            return True
        except Exception as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            return False