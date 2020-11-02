import os,sys
import csv
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas

def write_barcode(barcode_label, canvas, x, y, size):
	if barcode_label.startswith("?"):
		canvas.drawString((x + .37 * inch), (y - .15 * inch), "Lesefehler!")

	else:
	    barcode = code128.Code128(barcode_label, barWidth=size[0]*inch, barHeight=size[1]*inch, humanReadable=True)
	    barcode.drawOn(canvas, x, y)

def write_pdf(input_csv, output_pdf, columns = 4, rows = 9):

	reader = csv.reader(open(sys.argv[1]))

	result={}
	for row in reader:
		if row:
			key = row[0]

			if key in result:
				barcode.append(row[2])
				result[key] = barcode
			else:
				barcode=[row[2]]
				result[key] = barcode


	barcode_canvas = canvas.Canvas(output_pdf, pagesize=A4)
	barcode_canvas.setLineWidth(.3)
	#x coordinates
	x_coords = []
	x_start = .0
	for i in range(columns):
		x_coords.append(round(x_start, 4))
		x_start += 2.2

		#y coordinates
		y_coords = []
		y_start = 10
		for i in range(rows):
			y_coords.append(round(y_start, 4))
			y_start -= 1.21

	xy_coords = []
	for x_coord in x_coords:
		for y_coord in y_coords:
			xy_coords.append((x_coord*inch , y_coord*inch))

	width, height = A4
	c = 0

	for pool in result:
		x = x_coords[0]*inch
		y = xy_coords[c][1]
		# Create the barcodes and sample_id text and draw them on the canvas
		#the offset for the text will change automatically as x and y coordinates are
		#changed therefore the the following values do not need to be changed.
		i = 0
		write_barcode(pool, barcode_canvas, x, y, [0.02, 0.8])
		c += 1
		for record in result[pool]:
			if i < columns:
				if c >= (rows - 1):
					c = 0
					barcode_canvas.showPage()
			else:
				if c < (rows - 1):
					c += 1
				else:
					c = 0
				i = 0
			x_p = x_coords[i]*inch
			y_p = xy_coords[c][1]
			write_barcode(record, barcode_canvas, x_p, y_p, [0.01, 0.6])
			i += 1

		if c < (rows - 4):
			c += 1
			y_l = xy_coords[c][1]
			barcode_canvas.line(x_start ,y_l ,width,y_l)
			c += 1
		else:
			c = 0
			barcode_canvas.showPage()

	barcode_canvas.save()
	print("\n pdf file is made \n")

def main():
	if len(sys.argv) != 2:
		sys.stderr.write( "You should put the csv file as the argument: python3 pool_barcodes_pdf_maker.py <csv-file>\n")
		sys.exit( 1 )

	try:
		open( sys.argv[1] ).close()
	except:
		sys.stderr.write( "ERROR: Failed to open data file.\n\n")
		sys.stderr.write( str( sys.exc_info()[1] ) + "\n" )
		sys.exit( 1 )

	pdf_file = os.path.splitext(sys.argv[1])[0] + ".pdf"
	write_pdf(sys.argv[1], pdf_file)

if __name__ == "__main__":
	main()
