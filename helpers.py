import os

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def group_list(my_list, chunk_size):
    return [my_list[i:i + chunk_size] for i in range(0, len(my_list), chunk_size)]

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def format_date(date):
	return date.strftime("%B %d, %Y")

def format_date_hour(time):
	return time.strftime('%l:%M%p on %b %d, %Y')

def upload_file(file, file_path):
    if file and allowed_file(file.filename):
        ensure_dir(file_path)
        file.save(file_path)
        print("FILE PATH IS: "+file_path)