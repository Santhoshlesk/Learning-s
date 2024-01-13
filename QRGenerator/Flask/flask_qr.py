from flask import Flask, render_template, request, send_file
import os
import qrcode

app = Flask(__name__)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    text = request.form['text']
    images_directory = os.path.join(app.root_path, 'static', 'images')

    ensure_directory_exists(images_directory)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(images_directory, f'{text}.png')
    img.save(img_path)

    return send_file(img_path, mimetype='image/png', download_name=f'{text}.png')

if __name__ == '__main__':
    app.run(debug=True)
