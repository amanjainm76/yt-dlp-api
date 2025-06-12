from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/get-formats', methods=['POST'])
def get_formats():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'noplaylist': True,
        'extract_flat': False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        for f in info.get('formats', []):
            if f.get('url') and f.get('ext') in ['mp4', 'm4a', 'webm', 'mp3']:
                is_audio = 'audio' in f.get('format', '').lower() or f.get('vcodec') == 'none'
                label = f"{f.get('ext').upper()} - {'Audio' if is_audio else 'Video'} - {f.get('format_note') or f.get('abr') or f.get('acodec') or f.get('vcodec')}"
                formats.append({
                    'url': f['url'],
                    'label': label.strip()
                })

        return jsonify({
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'formats': formats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "🎉 yt-dlp API is up and running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
