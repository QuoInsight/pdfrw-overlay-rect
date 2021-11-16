
## [ https://github.com/kosta93/Create_invoices_python ]
## [ https://www.youtube.com/watch?v=wcekVN4lVe8 ]

import openpyxl
def readInvoiceData(xlsFilePath, sheetName):
  wb = openpyxl.load_workbook(xlsFilePath, data_only=True) ## [default]data_only=False ==> cell.value==formula!!
  ws = wb.get_sheet_by_name(sheetName)
  data = []
  firstRow = True
  for row in ws.rows:
    #print(row[0].value)
    if firstRow :
      firstRow = False
      continue
    #
    data.append({
      'invoice_number'  : str(row[0].value),
      'customer'        : str(row[2].value),
      'description'     : str(row[3].value),
      'amount_excl_vat' : row[4].value,
      'vat'             : row[5].value,
      'total_amount'    : row[6].value,
      'invoice_date'    : str(row[7].value),
      'due_date'        : str(row[8].value)
    })

    #    for cell in row:
    #      ## https://openpyxl.readthedocs.io/en/stable/api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell
    #      print("[" + cell.column + str(cell.row) + "] " + str(cell.value))
    #      ## the value that you get when opening a Workbook with data_only=True
    #      ## is "the value stored the last time Excel read the sheet". 
    #      ## openpyxl does not and will not calculate the result of a formula at runtime
    #      ## There are libraries out there like pycel which purport to do this.
    #    #

  #

  ##ws.cell(row=2, column=1).value = "inv#1";  wb.save(xlsFilePath);  ## if data_only=True this will replaced all formulas with values only

  wb.close()
  return data
#

import PIL
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
import reportlab.pdfgen.canvas
def create_invoice(invData):
  #convert the font so it is compatible
  reportlab.pdfbase.pdfmetrics.registerFont(
    reportlab.pdfbase.ttfonts.TTFont('Arial','Arial.ttf')
  )

  #import company's logo
  im = PIL.Image.open('invoice_logo.jpg')
  width, height = im.size
  ratio=width/height;  image_width=400;  image_height=int(image_width/ratio)

  #Page information
  page_width = 2156;  page_height = 3050

  #Invoice variables
  invData["company_name"] ='The best company in the world'
  payment_terms = 'x'
  contact_info = 'x'
  margin = 100
  month_year = 'August 2019'

  #Creating a pdf file and setting a naming convention
  c = reportlab.pdfgen.canvas.Canvas(invData["invoice_number"] + '_' + invData["customer"] +'.pdf')
  c.setPageSize((page_width, page_height))

  #Drawing the image
  c.drawInlineImage(
    "invoice_logo.jpg",
    page_width - image_width - margin,  page_height - image_height - margin,
    image_width, image_height
  )

  #Invoice information
  c.setFont('Arial',80)
  text = 'INVOICE'
  text_width = reportlab.pdfbase.pdfmetrics.stringWidth(text,'Arial',80)
  c.drawString((page_width-text_width)/2, page_height - image_height - margin, text)
  y = page_height - image_height - margin*4
  x = 2*margin
  x2 = x + 550

  c.setFont('Arial',45);  text_heigth = 45;  line_spacing = (text_heigth*1.1) * 1.0
  c.drawString(x,y, 'Issued by: ');      c.drawString(x2,y, invData["company_name"])
  y -= line_spacing
  c.drawString(x,y, 'Issued to: ');      c.drawString(x2,y, invData["customer"])
  y -= line_spacing
  c.drawString(x,y, 'Invoice number: '); c.drawString(x2,y, invData["invoice_number"])
  y -= line_spacing
  c.drawString(x,y, 'Invoice date: ');   c.drawString(x2,y, invData["invoice_date"])
  y -= line_spacing
  c.drawString(x,y, 'Due date: ');       c.drawString(x2,y, invData["due_date"])
  y -= line_spacing *2
  c.drawString(x,y, 'Invoice issued for performed '+ invData["description"] + ' for ' + month_year)
  y -= line_spacing *2
  c.drawString(x,y, 'Amount excluding VAT: ');  c.drawString(x2,y, 'EUR ' + str(invData["amount_excl_vat"]))
  y -= line_spacing
  c.drawString(x,y, 'Value added tax: ');  c.drawString(x2,y, 'EUR ' + str(invData["vat"]))
  y-= line_spacing
  c.drawString(x,y, 'Total amount: ');  c.drawString(x2,y,'EUR ' + str(invData["total_amount"]))
  y -= line_spacing*3
  c.drawString(x,y, 'If paid within 10 days, 2% of discount is granted.')
  y -= line_spacing
  c.drawString(x,y, 'Bank account number: 1234 ABCD 4567 EFGH')
  y -= line_spacing
  c.drawString(x,y, 'In case of any questions, contact info@thebestcompany.com')

  #Saving the pdf file
  c.save()
#


## main() ##############################################################

for invData in readInvoiceData('invoice_data.xlsx', 'invoices') : 
  print(str(invData["invoice_number"]))
  create_invoice(invData)
#

quit()


