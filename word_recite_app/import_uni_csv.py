import csv
from app import create_app, db
from app.models import Word

app = create_app()

csv_file = 'uni_words.csv'  # 确保这个 CSV 跟你脚本在同一个目录

with app.app_context():
    count = 0
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip()
            meaning = row['meaning'].strip()
            phonetic = (row.get('phonetic') or '').strip()


            # 防止重复单词
            if not Word.query.filter_by(word=word).first():
                new_word = Word(
                    word=word,
                    meaning=meaning,
                    phonetic=phonetic,
                    category='uni'
                )
                db.session.add(new_word)
                count += 1
    db.session.commit()
    print(f"已成功导入 {count} 个四级词汇")
