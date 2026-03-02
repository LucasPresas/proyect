from flask import Blueprint, request, jsonify, redirect
from scraper import robust_scraper_multi
from database import fetch_all, fetch_one

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/player_api.php')
def xtream_api():
    username = request.args.get('username')
    password = request.args.get('password')
    action = request.args.get('action')

    user = fetch_one('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    if not user: return jsonify({"user_info": {"auth": 0}})

    if not action:
        return jsonify({"user_info": {"auth": 1, "status": "Active", "exp_date": "1772443263"}})

    if action == "get_live_categories":
        return jsonify(fetch_all('SELECT id as category_id, name as category_name FROM categories'))

    if action == "get_live_streams":
        return jsonify(fetch_all('SELECT id as stream_id, name, category_id FROM streams'))
    
    return jsonify({})

# RUTA CORREGIDA: Sin espacio en <u_user>
@api_bp.route('/live/<u_user>/<p_pass>/<int:stream_id>.m3u8')
def live_proxy(u_user, p_pass, stream_id):
    user = fetch_one('SELECT * FROM users WHERE username=? AND password=?', (u_user, p_pass))
    if not user: return "Auth Fail", 403
    
    stream = fetch_one('SELECT * FROM streams WHERE id=?', (stream_id,))
    if not stream: return "Not Found", 404
    
    urls = robust_scraper_multi(stream['target_url'])
    if urls: return redirect(urls[0])
    return "No Signal", 404