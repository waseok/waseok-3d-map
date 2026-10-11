"""src/template.html 에 data/rooms.json 을 넣어 index.html(배포용 페이지)을 만듭니다.

사용법 (저장소 폴더에서):
    python tools/build.py
"""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template = (root / "src" / "template.html").read_text(encoding="utf-8")
rooms = (root / "data" / "rooms.json").read_text(encoding="utf-8")

page = (
    '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    "<style>body{margin:0}</style>\n</head>\n<body>\n"
    + template.replace("__DATA__", rooms)
    + "\n</body>\n</html>\n"
)
(root / "index.html").write_text(page, encoding="utf-8")
print("index.html 생성 완료")
