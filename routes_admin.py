from flask import Blueprint, render_template, request, redirect, url_for
from database import fetch_all, fetch_one, execute_query
from scraper import robust_scraper_multi

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/')
def index():
    streams = fetch_all('SELECT * FROM streams')
    return render_template('index.html', streams=streams)

@admin_bp.route('/admin_users')
def admin_users():
    users = fetch_all('SELECT * FROM users')
    return render_template('admin_users.html', users=users)

@admin_bp.route('/add_stream', methods=['POST'])
def add_stream():
    execute_query('INSERT INTO streams (name, target_url, category_id) VALUES (?, ?, 1)', 
                  (request.form['name'], request.form['url']))
    return redirect(url_for('admin_bp.index'))

@admin_bp.route('/add_user', methods=['POST'])
def add_user():
    execute_query('INSERT INTO users (username, password) VALUES (?, ?)', 
                  (request.form['username'], request.form['password']))
    return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/watch/<int:id>')
def watch(id):
    stream = fetch_one('SELECT * FROM streams WHERE id=?', (id,))
    if not stream: return "Canal no encontrado", 404
    urls = robust_scraper_multi(stream['target_url'])
    return render_template('player.html', urls=urls, name=stream['name'])