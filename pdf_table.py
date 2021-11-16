
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
import reportlab.pdfgen.canvas
import reportlab.platypus
#import reportlab.lib

#convert the font so it is compatible
reportlab.pdfbase.pdfmetrics.registerFont(
  reportlab.pdfbase.ttfonts.TTFont('Arial','Arial.ttf')
)

#Page information ## A4 /* 595pt;842pt | 21cm;29.7cm | 8.3in;11.7in; */
page_width = 595;  page_height = 842;  margin = 10; lineHeight = 24;

#Creating a pdf file and setting a naming convention
c = reportlab.pdfgen.canvas.Canvas("B:\\test.pdf")
c.setPageSize((page_width, page_height))

#Invoice information
fontHeight = 24
c.setFont('Arial',fontHeight)
text = 'Page Title'
text_width = reportlab.pdfbase.pdfmetrics.stringWidth(text,'Arial',fontHeight)
c.drawString((page_width-text_width)/2, page_height-fontHeight, text)
y = page_height - margin - fontHeight - lineHeight
x = margin

data = [
  ['0,0', '1,0', '2,0'],
  ['0,1', '1,1', '2,1'],
  ['0,2', '1,2', '2,2'],
]
cellWidth = cellHeight = 36
t = reportlab.platypus.Table(data, cellWidth, cellHeight) ## cell width & height
# [ https://www.reportlab.com/docs/reportlab-userguide.pdf ]
# [ https://www.blog.pythonlibrary.org/2010/09/21/reportlab-tables-creating-tables-in-pdfs-with-python/ ]
# (x,y) ==> 0:first; -1:last;
# The positive system starts at (0,0) at the top left corner
# and increments numbers as you go down and to the right.
# The negative system starts at [-1][-1] at the lower right corner
# and decreases (larger negatives) as you go up and to the left.
t.setStyle(reportlab.platypus.TableStyle([
  ('GRID',          (0,0),(-1,-1),  1, 'BLACK'), ##  GRID is the equivalent of applying both BOX and INNERGRID
  ('LEFTPADDING',   (0,0),(-1,-1),  6),
  ('RIGHTPADDING',  (0,0),(-1,-1),  6),
  ('TOPADDING',     (0,0),(-1,-1),  6),
  ('BOTTOMPADDING', (0,0),(-1,-1),  9),
  ('FONTSIZE',      (0,0),(-1,-1),  16),
  ('TEXTFONT',      (0,0),(-1,-1),  'Arial'),
  ('TEXTCOLOR',     (0,0),(-1,-1),  'GREEN'),
  ('BACKGROUND',    (0,0),(-1,-1),  'WHITE'),
  ('ALIGN',         (0,0),(-1,-1),  'CENTER'),
  ('VALIGN',        (0,0),(-1,-1),  'MIDDLE'),

  ('TEXTCOLOR', (0,0),(0,0), 'RED'),
  ('TEXTCOLOR', (-1,-1),(-1,-1), 'YELLOW'),
  ('ALIGN',     (0,1),(0,1), 'LEFT'),
  ('VALIGN',    (1,1),(-1,-1), 'TOP'),
  ('VALIGN',    (0,2),(0,2), 'BOTTOM'),
  ('ALIGN',     (0,2),(0,2), 'RIGHT'),
]))
t.wrapOn(c, 0, 0)
y = y - cellHeight*len(data)
t.drawOn(c, x, y)

#Saving the pdf file
c.save()

quit()


