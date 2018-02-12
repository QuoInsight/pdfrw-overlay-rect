import io
import sys
import pdfrw
import reportlab.pdfgen.canvas

def overlayCanvas2Pdf(canvasBuffer, underneath, inFilePath) :
  canvasBuffer.seek(0)
  pdfOverlay = pdfrw.PdfReader(canvasBuffer)
  overlayPage = pdfrw.PageMerge().add(pdfOverlay.pages[0])[0]
  pdfInput = pdfrw.PdfReader(inFilePath)
  for page in pdfInput.pages :
    pdfrw.PageMerge(page).add(overlayPage, prepend=underneath).render()
  #
  return pdfInput
#

def coverUpRectAreaOnPDF(filePath, x, y, width, height) :
  with io.BytesIO() as dataBuffer :
    c = reportlab.pdfgen.canvas.Canvas(
      dataBuffer, pagesize=(x+width, y+height)
    )
    c.setFillColorRGB(1, 1, 1) ## r, g, b ==> 0.000 -- 1.000
    c.rect(x, y, width, height, 0, 1) ## canvas.rect(x, y, width, height, stroke=1, fill=0)
    c.showPage() ## end of current page
    c.save() ## end of document
    pdfOutput = overlayCanvas2Pdf(dataBuffer, underneath=False, inFilePath=filePath)
  #
  return pdfOutput
#

########################################################################

(scriptPath, filePath, x, y, w, h) = sys.argv
outFilePath = filePath[0:filePath.rfind(".")] + ".overlaid.pdf"

pdfOutput = coverUpRectAreaOnPDF(filePath, int(x), int(y), int(w), int(h)) ## (x, y, width, height, stroke=1, fill=0)
pdfrw.PdfWriter(outFilePath, trailer=pdfOutput).write()

print(outFilePath)
