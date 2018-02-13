#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfrw

def hideImages(pdfPage) :
  XObject = pdfPage.Resources.XObject
  #    [/I1] {
  #      '/Name': '/I1',
  #      '/Type': '/XObject',
  #      '/Subtype': '/Image',
  #      '/Length': '18034',
  #      '/Width': '300',
  #      '/Height': '169',
  #      '/ColorSpace': '/DeviceRGB',
  #      '/BitsPerComponent': '8',
  #      '/Filter': ['/ASCII85Decode', '/DCTDecode'],
  #    }
  for key in XObject.keys():
    #print( key + " : " + str(type(XObject[key])) )
    if XObject[key].Type=="/XObject" and XObject[key].Subtype=="/Image" :
      print("hiding image[" + key + "] ...")
      XObject[key].Width = 1 ## !! good !!
      XObject[key].Height = 1

      #XObject[key].Length = 0 ## !! no effect !!
      #del XObject[key] ## !! OK, but error exists on this page, Acrobat may not display the page correctly !!
    #
  #
  return pdfPage
#

(scriptPath, filePath, outFilePath) = sys.argv

with open(filePath, 'rb') as f:
  bytes = f.read()
  pdfPages = pdfrw.PdfReader(fdata=bytes.decode('Latin-1')).pages

  pdfPages[0] = hideImages(pdfPages[0])

  writer = pdfrw.PdfWriter()
  for page in pdfPages: writer.addpage(page)
  writer.write(outFilePath)
#

print("Done.")

