import json,html,re
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Image,Table,TableStyle
from PIL import Image as PILImage
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
font_dir=Path(__file__).resolve().parent/'fonts'
pdfmetrics.registerFont(TTFont('StudySans',str(font_dir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('StudySans-Bold',str(font_dir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('StudySans',normal='StudySans',bold='StudySans-Bold',italic='StudySans',boldItalic='StudySans-Bold')
import content
root=Path(__file__).resolve().parent.parent; assets=root/'assets'
# The tracked question PDFs preserve the original nine-page upload by course.
styles=getSampleStyleSheet()
for style in styles.byName.values(): style.fontName='StudySans-Bold' if 'Heading' in style.name or style.name=='Title' else 'StudySans'
styles.add(ParagraphStyle(name='BodyStudy',fontName='StudySans',fontSize=10,leading=15,spaceAfter=9,textColor=colors.HexColor('#253a35')))
styles.add(ParagraphStyle(name='AnswerTitle',fontName='StudySans-Bold',fontSize=12,leading=16,spaceBefore=14,spaceAfter=8,textColor=colors.HexColor('#163d31'),keepWithNext=True))
styles.add(ParagraphStyle(name='SummaryStudy',parent=styles['BodyStudy'],backColor=colors.HexColor('#e8f3ed'),borderPadding=8,spaceBefore=5,spaceAfter=16))
def clean(s):
 return html.escape(s.replace('–','-').replace('—','-').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('Aurélien','Aurelien').replace('Géron','Geron').replace('COCOMO’s',"COCOMO's")).replace('\n','<br/>')
def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#d2e1d8'));canvas.line(42,38,553,38)
 canvas.setFont('StudySans',8);canvas.setFillColor(colors.HexColor('#53655e'));canvas.drawString(42,26,'SEMESTER ARCHIVE | Model study answers - not an official marking scheme');canvas.drawRightString(553,26,str(doc.page))
for c in content.courses:
 q=PdfWriter()
 source=PdfReader(assets/f"{c['id']}-questions.pdf") if max(c['pages'])<=9 else None
 for page_index,n in enumerate(c['pages']):
  if n<=9:q.add_page(source.pages[page_index])
  else:
   buf=BytesIO();PILImage.open(assets/f'page-{n}.jpg').convert('RGB').save(buf,format='PDF');buf.seek(0);q.append(PdfReader(buf))
 with open(assets/f"{c['id']}-questions.pdf",'wb') as f:q.write(f)
 story=[Paragraph(clean(c['title']),styles['Title']),Paragraph(clean(c['code']+' | Session '+c.get('session','2020-21')+' | '+c.get('exam','Final exam')),styles['Heading2']),Paragraph('Model study answers. Every listed option is addressed. Question titles are paraphrased; exact wording and original diagrams are in the source pages appended to this pack.',styles['BodyStudy'])]
 if c['note']:story.append(Paragraph(clean(c['note']),styles['SummaryStudy']))
 story += [Paragraph('Quick revision',styles['Heading1'])]
 for f in c['formula']:story.append(Paragraph(clean(f),styles['BodyStudy']))
 story.append(PageBreak())
 for item in c['items']:
  segment_start=len(story)
  story.append(Paragraph(clean(item['ref']+' | '+item['title']),styles['AnswerTitle']))
  parts=item['body'].split('\n');idx=0
  while idx<len(parts):
   if parts[idx].startswith('Activity | '):
    rows=[]
    while idx<len(parts) and ' | ' in parts[idx]:rows.append(parts[idx].split(' | '));idx+=1
    data=[[Paragraph(clean(cell),ParagraphStyle(name='cell',fontName='StudySans',fontSize=8,leading=11)) for cell in row] for row in rows]
    widths=[48,44,93,48,48,48,48,48] if len(rows[0])==8 else None
    table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f3ed')),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#bacdc0')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([table,Spacer(1,12)])
   else:story.append(Paragraph(clean(parts[idx]),styles['BodyStudy']));idx+=1
  if item.get('figure'):
   img=PILImage.open(assets/item['figure']); iw,ih=img.size;w=min(510,iw);h=w*ih/iw
   if h>500:w*=500/h;h=500
   story.append(Image(str(assets/item['figure']),width=w,height=h))
  for ref in item.get('sources',[]):story.append(Paragraph('Reading: '+clean(ref['title'])+' - '+'<link href="'+html.escape(ref['url'],quote=True)+'" color="#24614a">'+clean(ref['url'])+'</link>',styles['BodyStudy']))
  if c['id']=='ml' and item['ref']=='5(c)': story.append(Image(str(assets/'slope-derivative-gradient.png'),width=510,height=153))
  story.append(Paragraph('<b>Revision answer:</b> '+clean(item['final']),styles['SummaryStudy']))
  if len(item['body'])<1500 and not item.get('figure') and not (c['id']=='ml' and item['ref']=='5(c)'):
   group=story[segment_start:];del story[segment_start:];story.append(KeepTogether(group))
 story += [PageBreak(),Paragraph('Reference reading',styles['Heading1'])]
 for r in c['refs']:story.append(Paragraph(clean(r),styles['BodyStudy']))
 for r in c.get('materials',[]):story.append(Paragraph(clean(r['title']+' - '+r['url']),styles['BodyStudy']))
 story.append(Paragraph('These are supporting reading references, not claims that this paper or its answer key appears in those books. Course-specific terminology and source ambiguities are noted beside the affected answers.',styles['BodyStudy']))
 temp=root/f"{c['id']}-answers.tmp.pdf"
 SimpleDocTemplate(str(temp),pagesize=(595.276,841.89),rightMargin=42,leftMargin=42,topMargin=44,bottomMargin=55,title=c['title']+' - Model answers',author='Semester Study Archive').build(story,onFirstPage=footer,onLaterPages=footer)
 out=PdfWriter();out.append(str(temp));out.append(str(assets/f"{c['id']}-questions.pdf"))
 with open(assets/f"{c['id']}-study-pack.pdf",'wb') as f:out.write(f)
 temp.unlink()
 print(c['id'],len(out.pages),'pages')
