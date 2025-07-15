from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Falta el parámetro de búsqueda'}), 400

    search_opts = {
        'quiet': True,
        'skip_download': True,
        'format': 'bestaudio',
        'default_search': 'ytsearch10',
        'extract_flat': False,
        'noplaylist': True
    }

    results = []

    with YoutubeDL(search_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            for entry in info['entries']:
                audio_url = entry['url']
                title = entry.get('title', 'Sin título')
                results.append({
                    'title': title,
                    'url': audio_url
                })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
