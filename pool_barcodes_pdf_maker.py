import os,sys
import csv
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas

if len(sys.argv) != 2:
	sys.stderr.write( "You put the csv file as the argument: python3 pool_barcodes_pdf_maker.py <csv-file>\n")
	sys.exit( 1 )

try:
	open( sys.argv[1] ).close()
except:
	sys.stderr.write( "ERROR: Failed to open data file.\n\n")
	sys.stderr.write( str( sys.exc_info()[1] ) + "\n" )
	sys.exit( 1 )

reader = csv.reader(open(sys.argv[1]))

result={}
for row in reader:
    if row:
        if row[2]=='?Bar Code Cassette2:09' or row[2]== '?Bar Code Cassette2:11' or row[2]== '?Bar Code Cassette3:04':
            pass
        else:
            key = row[0]
            if key in result:
                barcode.append(row[2])
                result[key]=barcode
            else:
                barcode=[row[2]]
                result[key] = barcode

pdf_file = os.path.splitext(sys.argv[1])[0] + ".pdf"
barcode_canvas = canvas.Canvas(pdf_file, pagesize=A4)
barcode_canvas.setLineWidth(.3)

#x coordinates
x_coords = []
x_start = .0
for i in range(4):
    x_coords.append(round(x_start, 4))
    x_start += 2.2

#y coordinates
y_coords = []
y_start = 10
for i in range(9):
    y_coords.append(round(y_start, 4))
    y_start -= 1.21

xy_coords = []
for x_coord in x_coords:
    for y_coord in y_coords:
        xy_coords.append((x_coord*inch , y_coord*inch))
c = 0
for pool in result:
    x = x_coords[0]*inch
    y = xy_coords[c][1]
    # Create the barcodes and sample_id text and draw them on the canvas
    barcode = code128.Code128(pool, barWidth=.02*inch, barHeight=.8*inch, humanReadable=True)
    barcode.drawOn(barcode_canvas, x, y)
    #the offset for the text will change automatically as x and y coordinates are
    #changed therefore the the following values do not need to be changed.
    i = 0
    c += 1
    width, height = A4
    for record in result[pool]:
        if i < 4:
            if c < (9 - 1):
                x_p = x_coords[i]*inch
                y_p = xy_coords[c][1]
                pool_barcode = code128.Code128(record, barWidth=.01*inch, barHeight=.6*inch, humanReadable=True)
                pool_barcode.drawOn(barcode_canvas, x_p, y_p)
                i += 1
            else:
                c = 0
                barcode_canvas.showPage()
                x_p = x_coords[i]*inch
                y_p = xy_coords[c][1]
                pool_barcode = code128.Code128(record, barWidth=.01*inch, barHeight=.6*inch, humanReadable=True)
                pool_barcode.drawOn(barcode_canvas, x_p, y_p)
                i += 1
        else:
            if c < (9 - 1):
                i = 0
                c += 1
                x_p = x_coords[i]*inch
                y_p = xy_coords[c][1]
                pool_barcode = code128.Code128(record, barWidth=.01*inch, barHeight=.6*inch, humanReadable=True)
                pool_barcode.drawOn(barcode_canvas, x_p, y_p)
                i += 1
            else:
                i = 0
                c = 0
                barcode_canvas.showPage()
                x_p = x_coords[i]*inch
                y_p = xy_coords[c][1]
                pool_barcode = code128.Code128(record, barWidth=.01*inch, barHeight=.6*inch, humanReadable=True)
                pool_barcode.drawOn(barcode_canvas, x_p, y_p)
                i += 1
    if c < (9 - 4):
        c += 1
        y_l = xy_coords[c][1]
        barcode_canvas.line(x_start ,y_l ,width,y_l)
        c += 1
    else:
        c = 0
        barcode_canvas.showPage()

barcode_canvas.save()
print("\n pdf file is made \n")
