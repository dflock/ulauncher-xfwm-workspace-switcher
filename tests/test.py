# -*- coding: UTF-8 -*-

wmlist = [
  '0  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Personal: Email',
  '1  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Personal: Jobs',
  '2  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Notes',
  '3  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Todo',
  '4  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Finances',
  '5  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: duncanlock.net',
  '6  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Personal: D&D',
  '7  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  PHEMI: Code',
  '8  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  PHEMI: Email & Slack',
  '9  - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  PHEMI: Cloud',
  '10 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  PHEMI: Docs & AsciiDoc',
  '11 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: Home Dashboard',
  '12 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: LanguageTool',
  '13 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: Gemini',
  '14 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: lite-xl',
  '15 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: Standard eBooks',
  '16 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: NAS & Storage',
  '17 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Project: Processing',
  '18 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Personal: Retro Hardware',
  '19 * DG: 5760x1080  VP: 0,0  WA: 0,0 5760x1080  Prokect: ulauncher',
  '20 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  [emp    ty]',
  '21 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  [empty]',
  '22 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  [empty]',
  '23 - DG: 5760x1080  VP: N/A  WA: 0,0 5760x1080  Music',
  '0  - DG: N/A  VP: N/A  WA: N/A  ~',
  '1  * DG: N/A  VP: N/A  WA: N/A  ~',
  '2  - DG: N/A  VP: N/A  WA: N/A  ➋ ·web·🌏',
  '3  - DG: N/A  VP: N/A  WA: N/A  ➐ ·foo',
  '4  - DG: N/A  VP: N/A  WA: N/A  ➎ ·media·♫'
]

def get_desktop_name(line):
  parts = line.split('  ')
  # print(parts)
  # print(len(parts))
  # geom = line.find('WA: N/A') == -1
  # print(geom)
  print(parts[-1])
  # print

def get_desktop_name2(tmp):
  import re
  id = tmp.split()[0]
  name = ''
  m = re.search('^.*WA: (N/A|.,. \d+x\d+) *', tmp)
  if m and m.span():
      name = tmp[m.span()[1]:]

  print([id, name])

for l in wmlist:
  get_desktop_name2(l)