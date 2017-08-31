
from PIL import Image

import binascii

import struct

four_k = (3840,2160)
HD = (1920,1080)

# encoding...
# 0 is black pixel, white is 1

# provided a list of pixels, writes it out as an image
# with the specified resolution
def pixels_2_png(pixels,reso=four_k,fname="image.png"):
	img = Image.new('RGB',reso)
	img.putdata(pixels)
	img.save(fname)
	print "Saved to %s" % fname

# provided a filename, reads the png and returns a list of pixels
def png_2_pixels(fname="image.png"):
	im = Image.open(fname)
	pixel_list = []
	pixels = im.load()
	width,height = im.size
	for row in range(height):
		for col in range(width):
			pixel_list.append(pixels[col,row])
	return pixel_list

# returns a list of bits in the file
def file_2_bits(fname):
	# allows iteration over the bits (0 or 1) in a file
	def bit_reader(fname):
	    bytes = (ord(b) for b in fname.read())
	    for b in bytes:
	        for i in xrange(8):
	            yield (b >> i) & 1
	bits = []
	for b in bit_reader(open(fname,'r')):
		bits.append(b)
	return bits

# converts a list of 0/1 bits to pixels
def bits_2_pixels(bits):
	pixels=[]
	for b in bits:
		if b==0:
			pixels.append((0,0,0))
		else:
			pixels.append((255,255,255))
	return pixels 

# converts opposite of bits_2_pixels
def pixels_2_bits(pixels):
	bits = []
	for p in pixels:
		if p==(0,0,0):
			bits.append('0')
		else:
			bits.append('1')
	return bits

# adds the file name header to the list of bits
def add_header(bits,fname):
	# filename encoded as ascii --> binary
	header_bits = bin(int(binascii.hexlify(fname), 16))
	
	# extra 2 bytes (16 bits) before header tells how long header is (in bits)
	length_header = "{0:b}".format(len(header_bits))

	while len(length_header)<16:
		length_header = "0"+length_header

	# length header to tell how long the rest of the header is, as
	# well as the header itself
	total_header = length_header+header_bits[2:]

	# converting the string header to a list
	header_list = []
	for char in total_header:
		header_list.append(char)

	# append the original bits onto the header and return
	header_list.extend(bits)
	return header_list

# takes in the bits, decodes the header into a filename.
# returns the filename, as well as the rest of the bits 
# after the header section
def decode_header(bits):
	header_length_binstr = ''.join(bits[:16])
	header_length = int(header_length_binstr,2)
	
	rest_of_header = ''.join(bits[16:16+header_length])
	n = int(rest_of_header,2)
	fname = binascii.unhexlify('%x' % n)

	return fname,bits[16+header_length:]

def main():

	test_f = "data/test.txt"

	print "Converting file to bits..."
	test_f_bits = file_2_bits(test_f)

	print "Adding header to bits..."
	test_f_bits = add_header(test_f_bits,test_f.split("/")[1])

	print "Converting bits to pixels..."
	pixels = bits_2_pixels(test_f_bits)

	print "Writing out pixels to image..."
	pixels_2_png(pixels)

	print "Reading pixels from png..."
	pixels = png_2_pixels("image.png")

	print "Converting pixels to bits..."
	bits = pixels_2_bits(pixels)

	print "Decoding bit header..."
	fname,bits = decode_header(bits)

	print "Recovered filename: %s" % fname 

	#bitstr = ''.join(bits)


if __name__ == '__main__':
	main()