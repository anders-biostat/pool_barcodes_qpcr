import os, sys, math
import csv
from collections import defaultdict
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas


# Grid positions (for a grid of 9 rows, 4 columns, on A4 paper):
gridpos_x = [ 1*cm + 5*i*cm for i in range(4) ]
gridpos_y = [ A4[1] - 4*cm - 3*i*cm for i in range(9) ]

# Check that they fit on page
assert min( gridpos_x ) > 0
assert min( gridpos_y ) > 0
assert max( gridpos_x ) < A4[0]
assert max( gridpos_y ) < A4[1]


def write_barcode( canvas, code, gridrow, gridcol, height ):

	if code.startswith( "?" ):
		canvas.drawString( gridpos_x[ gridcol ] + 1*cm, gridpos_y[ gridrow ] + 0.3*height, "Lesefehler" )
	else:
	    barcode = code128.Code128( code, barWidth = .03*cm, barHeight=height, humanReadable=True )
	    barcode.drawOn( canvas, gridpos_x[ gridcol ], gridpos_y[ gridrow ]  )


def write_header( canvas, text ):

	canvas.drawString( 1*cm, A4[1] - 1*cm, text )


def write_pdf( input_csv, output_pdf ):

	data = defaultdict( list )
	with open( input_csv ) as f:
		for record in csv.reader( f ):
			pool = record[0]
			sample = record[2]
			data[ pool ].append( sample )


	barcode_canvas = canvas.Canvas(output_pdf, pagesize=A4)
	barcode_canvas.setLineWidth(.3)
	page_number = 1
	write_header( barcode_canvas, "Page %d for '%s'" % ( page_number, input_csv, ) )

	grid_row = 0
	grid_col = 0

	for pool in data:

		samples = data[pool]

		# How many rows do we need?
		rows_needed = math.ceil( len(samples) / len( gridpos_y ) ) + 1

		# Enough space for that, or do we need a new page?
		if grid_row + rows_needed >= len(gridpos_y):

			if grid_row == 0:  # Starting a new page would be pointless if the current page is empty
				sys.stderr.write( "Too many samples in pool %s to fit on page!" % pool )
				sys.exit( 1 )

			barcode_canvas.showPage()  # Start a new page
			page_number += 1
			write_header( barcode_canvas, "Page %d for '%s'" % ( page_number, input_csv, ) )
			grid_row = 0

		if grid_row != 0:
			# We didn't start a new page, so let's make a line (one row higher)
			line_ypos = .3*gridpos_y[ grid_row-2 ] + .7*gridpos_y[ grid_row-1 ]
			barcode_canvas.line( 1*cm , line_ypos , A4[0] - 1*cm, line_ypos )

		# Print pool bar code:
		write_barcode( barcode_canvas, pool, grid_row, grid_col, 2*cm )
		grid_row += 1

		grid_col = 0
		for sample in samples:

			# new row needed?
			if grid_col >= len( gridpos_x ):
				grid_col = 0
				grid_row += 1
				assert grid_row < len( gridpos_y )

			write_barcode( barcode_canvas, sample, grid_row, grid_col, 1.5*cm )

			grid_col += 1

		# Start new row
		grid_row += 2
		grid_col = 0

	barcode_canvas.save()
	print("Written file", output_pdf )


def main():

	if len( sys.argv ) != 2:
		sys.stderr.write( "Usage: python pool_barcodes_pdf_maker.py <csv-file-from-Janus>\n")
		sys.exit( 1 )

	try:
		open( sys.argv[1] ).close()
	except:
		sys.stderr.write( "ERROR: Failed to open data file %s.\n" % sys.argv[1] )
		sys.stderr.write( str( sys.exc_info()[1] ) + "\n" )
		sys.exit( 1 )

	pdf_file = os.path.splitext( sys.argv[1] )[0] + ".pdf"
	write_pdf( sys.argv[1], pdf_file )

if __name__ == "__main__":
	main()
