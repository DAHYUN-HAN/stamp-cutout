# -*- coding: utf-8 -*-
"""build_template.html + 배경.jpg  ->  index.html (독립 실행 문서)

아티팩트로 게시할 때는 클로드가 doctype/head/뷰포트를 씌워주지만,
GitHub Pages는 파일을 그대로 내보내므로 여기서 직접 완성된 문서를 만든다.
"""
import base64, glob, hashlib, io, os, shutil

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="사진 한 장을 우표 모양으로 오려내 위·아래 두 폭 이미지로 만듭니다.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="stamp">
<meta property="og:title" content="stamp">
<meta property="og:description" content="사진 한 장을 우표 모양으로 오려냅니다.">
<meta property="og:url" content="https://dahyun-han.github.io/stamp-cutout/">
<meta property="og:image" content="https://dahyun-han.github.io/stamp-cutout/__OG__">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="사진에서 우표 모양을 오려낸 결과 예시">
<meta name="twitter:card" content="summary_large_image">
<style>
  :root{color-scheme:light dark}
  html,body{margin:0;padding:0}
  img{max-width:100%}
  [hidden]{display:none!important}
</style>
"""

# 링크 미리보기 이미지는 내용이 바뀌면 파일 이름도 바뀌게 한다.
# 카카오톡 등은 og 이미지를 주소 기준으로 캐시해서, 이름이 같으면 예전 그림을 계속 쓴다.
h = hashlib.sha256(open('og.jpg', 'rb').read()).hexdigest()[:8]
og_name = 'og-%s.jpg' % h
for stale in glob.glob('og-*.jpg'):
    if stale != og_name:
        os.remove(stale)
if not os.path.exists(og_name):
    shutil.copyfile('og.jpg', og_name)

tpl = io.open('build_template.html', encoding='utf-8').read()
split = '</style>\n\n<div class="app">'
assert tpl.count(split) == 1, '템플릿 head/body 경계를 찾지 못함'
head, body = tpl.split(split)

doc = (HEAD + head + '</style>\n</head>\n<body>\n<div class="app">' + body
       + '\n</body>\n</html>\n')
doc = doc.replace('__OG__', og_name)
doc = doc.replace('__BG_B64__', base64.b64encode(open('배경.jpg', 'rb').read()).decode())
assert '__BG_B64__' not in doc and '__OG__' not in doc and 'viewport' in doc

io.open('index.html', 'w', encoding='utf-8', newline='\n').write(doc)
print('index.html', os.path.getsize('index.html'), 'bytes')
print('미리보기 이미지', og_name)
