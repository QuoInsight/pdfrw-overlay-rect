import xhtml2pdf.pisa

with open("template.html", encoding='ascii', errors='ignore') as f: html = f.read()
print(html)

xhtml2pdf.pisa.showLogging()

with open("B:\\test.pdf", "w+b") as f1:
  status = xhtml2pdf.pisa.CreatePDF(html, dest=f1)
  ## !! not supporting <LINK REL=stylesheet HREF="template.css" TYPE="text/css"/>
  print( str(status.err) )
#
quit()

#----------------------------------------------------------------------#

import weasyprint.HTML 
## packages: webencodings, tinycss2, cssselect2, cairocffi, defusedxml, CairoSVG, Pyphen, html5lib, weasyprint
## cairosvg.exe is installed in 'C:\BigData\Python34\Scripts', consider adding this directory to PATH
## error: cairo = dlopen(ffi, 'cairo', 'cairo-2', 'cairo-gobject-2')
## pip install --upgrade pycairo --> error: Microsoft Visual C++ 10.0 is required

with open("template.html") as f: html = f.read()
print(html)

weasyprint.HTML(string=html).write_pdf(
    "template.out.pdf", stylesheets=["template.css",]
)
