# 와석초 3D 배치도

2026학년도 와석초등학교 교실배치도를 3D로 보여주는 웹페이지입니다.

- **외관 보기**: 드론 사진을 참고한 건물 외관과 운동장
- **교실 배치도**: 층별 교실, 층 선택, 교실 검색
- **외관 겹쳐 보기**: 투명한 외관 안에 교실 배치를 함께 표시
- **길찾기**: 출발지에서 도착지까지 단계별 안내, 따라가기 모드
- **비상대피로**: 교실별 대피 경로 (공식 경로를 받기 전까지는 가장 가까운 출구로 안내하는 임시 경로)

## 폴더 구성

| 경로 | 내용 |
| --- | --- |
| `index.html` | 배포되는 페이지 (`tools/build.py`로 생성, 직접 고치지 않기) |
| `src/template.html` | 페이지 원본 (화면, 3D 모델, 길찾기 코드) |
| `data/rooms.json` | 층별 실 위치와 이름 (배치도 PDF에서 추출) |
| `tools/extract_rooms.py` | 배치도 PDF에서 칸과 이름을 뽑아 `data/groups.json` 생성 |
| `tools/merge_rooms.py` | 칸을 실 단위로 정리해 `data/rooms.json` 생성 |
| `tools/build.py` | 템플릿과 데이터를 합쳐 `index.html` 생성 |

## 수정하는 방법

1. `src/template.html` 또는 `data/rooms.json`을 고칩니다.
2. `python tools/build.py`로 `index.html`을 다시 만듭니다.
3. 커밋하고 푸시하면 GitHub Pages에 자동으로 반영됩니다 (1~2분 소요).

### 새 학년도 배치도로 바꿀 때

배치도 PDF는 저장소에 올리지 않습니다. PDF 경로를 넣어 실행하세요.

```bash
pip install pymupdf
python tools/extract_rooms.py "배치도.pdf"
python tools/merge_rooms.py
python tools/build.py
```

PDF의 칸 구성이 바뀌면 `tools/extract_rooms.py`의 층 구분 좌표(`bands`, `anc`)와 `tools/merge_rooms.py`의 이름 보정 규칙을 맞춰야 할 수 있습니다.

### 비상대피로 넣기

`src/template.html`에서 `const EVAC={};`를 찾아 반별 경로를 적습니다. 지나갈 계단과 나갈 출구 이름을 순서대로 넣으면 됩니다.

```js
const EVAC={
  '5-3':['계단3','현관③'],
  '6-2':['계단1','현관①'],
};
```

출구 이름은 같은 파일의 `EXITS` 목록에 있습니다.
