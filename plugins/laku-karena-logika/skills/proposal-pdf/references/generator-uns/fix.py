import re
titles={'penawaran.html':'VEN-PolicyLab-2026-016','lampiran.html':'VEN-PolicyLab-2026-016-Lampiran-Estimasi','sla.html':'VEN-PolicyLab-2026-016-Service-Agreement'}
for f,t in titles.items():
    s=open(f).read()
    s=s.replace('Delivery Point (DP)','Delivery Point (selanjutnya disebut Poin)')
    s=re.sub(r'(?<![A-Za-z])DP(?![A-Za-z])','Poin',s)
    s=re.sub(r'<title>.*?</title>',f'<title>{t}</title>',s)
    open(f,'w').write(s)
    print(f, len(re.findall(r'\bDP\b',s)), s.count('Poin'), s.count('GitLab'))
