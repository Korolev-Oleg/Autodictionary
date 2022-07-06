from db.models import Word

lines = []
for word in Word.select():
    lines.append(
        f'english\trussian\t{word.heading}\t{word.translation}\n'
    )

with open('data/words.txt', 'w', encoding='utf8') as f:
    f.writelines(lines)
