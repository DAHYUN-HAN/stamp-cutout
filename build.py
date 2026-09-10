# -*- coding: utf-8 -*-
"""build_template.html + 배경.jpg  ->  index.html (독립 실행 문서)

아티팩트로 게시할 때는 클로드가 doctype/head/뷰포트를 씌워주지만,
GitHub Pages는 파일을 그대로 내보내므로 여기서 직접 완성된 문서를 만든다.
"""
import base64, io, os

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="사진 한 장을 우표 모양으로 오려내 위·아래 두 폭 이미지로 만듭니다.">
<style>
  :root{color-scheme:light dark}
  html,body{margin:0;padding:0}
  img{max-width:100%}
  [hidden]{display:none!important}
</style>
"""

tpl = io.open('build_template.html', encoding='utf-8').read()
split = '</style>\n\n<div class="app">'
assert tpl.count(split) == 1, '템플릿 head/body 경계를 찾지 못함'
head, body = tpl.split(split)

doc = (HEAD + head + '</style>\n</head>\n<body>\n<div class="app">' + body
       + '\n</body>\n</html>\n')
doc = doc.replace('__BG_B64__', base64.b64encode(open('배경.jpg', 'rb').read()).decode())
assert '__BG_B64__' not in doc and 'viewport' in doc

io.open('index.html', 'w', encoding='utf-8', newline='\n').write(doc)
print('index.html', os.path.getsize('index.html'), 'bytes')
