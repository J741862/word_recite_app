from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, User, Word, CheckIn
from flask_login import login_user, logout_user, login_required, current_user
from app.sms import send_sms
from datetime import date
import requests

bp = Blueprint('main', __name__)

@bp.route('/')
def root():
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('用户名已存在！')
            return redirect(url_for('main.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录！')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if not user.interests:
                return redirect(url_for('main.survey'))
            return redirect(url_for('main.index'))
        flash('用户名或密码错误！')
        return redirect(url_for('main.login'))
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录。')
    return redirect(url_for('main.login'))

@bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        # store multiple selected categories
        cats = request.form.getlist('categories')
        current_user.interests = ','.join(cats)
        current_user.duration  = int(request.form['duration'])
        current_user.unit      = request.form['unit']
        current_user.reminder  = (request.form['reminder'] == 'yes')
        phone = request.form.get('phone','').strip()
        if current_user.reminder and phone:
            current_user.phone = phone
            send_sms(phone, '您已开启每日打卡提醒，我们会准时提醒您背单词！')
        db.session.commit()
        flash('问卷提交成功！')
        return redirect(url_for('main.index'))
    return render_template('survey.html')

@bp.route('/index')
@login_required
def index():
    raw = current_user.interests or ''
    cats = [c.strip() for c in raw.split(',') if c.strip()]
    return render_template('index.html', categories=cats)


def fetch_phonetic(word):
    try:
        resp = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if resp.status_code == 200:
            data = resp.json()[0]
            phonetic = data.get('phonetic') or next(
                (p['text'] for p in data.get('phonetics', []) if 'text' in p),
                ''
            )
            return phonetic
    except:
        pass
    return ''

@bp.route('/add_word', methods=['POST'])
@login_required
def add_word():
    w = request.form.get('word')
    m = request.form.get('meaning')
    c = request.form.get('category')
    if not all([w, m, c]):
        flash('单词、翻译和分类都不能为空！')
        return redirect(url_for('main.index'))
    if Word.query.filter_by(word=w).first():
        flash('该单词已存在！')
        return redirect(url_for('main.index'))
    phon = fetch_phonetic(w)
    db.session.add(Word(word=w, meaning=m, phonetic=phon, category=c))
    db.session.commit()
    flash('单词添加成功！')
    return redirect(url_for('main.index'))

@bp.route('/check_in', methods=['POST'])
@login_required
def check_in():
    today = date.today()
    if not CheckIn.query.filter_by(date=today).first():
        db.session.add(CheckIn(date=today))
        db.session.commit()
        flash('打卡成功！')
    else:
        flash('今天已经打卡了！')
    return redirect(url_for('main.index'))

@bp.route('/word_dictionary')
@login_required
def word_dictionary():
    # read the clicked‐category override if present
    single = request.args.get('category')

    if single:
        cats = [single]
    else:
        raw = current_user.interests or ''
        cats = [c.strip() for c in raw.split(',') if c.strip()]

    # Now this will only ever look for exact matches in cats
    query = Word.query.filter(Word.category.in_(cats))

    # exclude notebook
    notebook_ids = [w.id for w in current_user.notebook]
    if notebook_ids:
        query = query.filter(~Word.id.in_(notebook_ids))

    # paginate
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    pagination = query.order_by(Word.id) \
                      .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'word_dictionary.html',
        words      = pagination.items,
        pagination = pagination,
        category   = single
    )


@bp.route('/add_to_notebook/<int:word_id>', methods=['POST'])
@login_required
def add_to_notebook(word_id):
    word = Word.query.get_or_404(word_id)
    if word not in current_user.notebook:
        current_user.notebook.append(word)
        db.session.commit()
        flash(f'“{word.word}” 已添加到笔记本！')
    else:
        flash('该单词已在笔记本中！')
    return redirect(request.referrer or url_for('main.word_dictionary'))

@bp.route('/notebook')
@login_required
def notebook():
    return render_template('notebook.html', words=current_user.notebook)

@bp.route('/delete_word/<int:word_id>', methods=['POST'])
@login_required
def delete_word(word_id):
    w = Word.query.get_or_404(word_id)
    db.session.delete(w)
    db.session.commit()
    flash('单词已删除！')
    return redirect(url_for('main.word_dictionary'))

@bp.route('/add_to_library/<int:word_id>', methods=['POST'])
@login_required
def add_to_library(word_id):
    w = Word.query.get_or_404(word_id)
    if not Word.query.filter_by(word=w.word).first():
        db.session.add(Word(word=w.word, meaning=w.meaning, phonetic=w.phonetic, category=w.category))
        db.session.commit()
        flash('单词成功添加到词库！')
    else:
        flash('该单词已在词库中！')
    return redirect(url_for('main.word_dictionary'))
