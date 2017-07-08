import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def group_list(my_list, chunk_size):
    return [my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)]

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)