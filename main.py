
from PIL import Image

import binascii

import struct

four_k = (3840,2160)
HD = (1920,1080)

# encoding...
# 0 is black pixel, white is 1

# provided a list of pixels, writes it out as an image
# with the specified resolution
def pixels_2_png(pixels,fname,reso=four_k):
	img = Image.new('RGB',reso)
	img.putdata(pixels)
	img.save(fname)
	#print pixels[:16]
	print "pixels_2_png: Saved to %d pixels to %s" % (len(pixels),fname)

# provided a filename, reads the png and returns a list of pixels
def png_2_pixels(fname):
	im = Image.open(fname)
	pixel_list = []
	pixels = im.load()
	width,height = im.size
	for row in range(height):
		for col in range(width):
			pixel_list.append(pixels[col,row])
	print "png_2_pixels: Read %d pixels from %s" % (len(pixel_list),fname)
	#pixels_2_png(pixel_list,"test2.png")
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
	print "file_2_bits: Read %d bits from %s" % (len(bits),fname)
	return bits

# converts a list of 0/1 bits to pixels
def bits_2_pixels(bits):
	pixels=[]
	for b in bits:
		if b=='0':
			pixels.append((0,0,0))
		else:
			pixels.append((255,255,255))
	print "bits_2_pixels: Converted %d bits to %d pixels" % (len(bits),len(pixels))
	return pixels 

# converts opposite of bits_2_pixels
def pixels_2_bits(pixels):
	#print pixels[:16]
	bits = []
	for p in pixels:
		if p==(0,0,0):
			bits.append('0')
		else:
			bits.append('1')
	print "pixels_2_bits: Converted %d pixels to %d bits" % (len(pixels),len(bits))
	return bits

# adds the file name header to the list of bits
def add_header(bits,fname):
	# filename encoded as ascii --> binary
	header_bits = bin(int(binascii.hexlify(fname), 16))
	
	# extra 2 bytes (16 bits) before header tells how long header is (in bits)
	length_header = "{0:b}".format(len(header_bits))

	print "header_length: %s" % len(header_bits)

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
	print "add_header: Added %d length header, total bits: %d" % (len(total_header),len(header_list))
	#print header_list[:16]
	return header_list

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

# takes in the bits, decodes the header into a filename.
# returns the filename, as well as the rest of the bits 
# after the header section
def decode_header(bits):
	header_length_binstr = ''.join(bits[:16])
	#print header_length_binstr
	header_length = int(header_length_binstr,2)
	print "header_length: %d" % header_length

	rest_of_header = ''.join(bits[16:16+header_length])
	rest_of_header = "0"+rest_of_header
	print rest_of_header
	fname = decode_binary_string(rest_of_header)
	#n = int(rest_of_header,2)
	#fname = binascii.unhexlify('%x' % n)

	print "decode_header: Found %d length header, " % (header_length)
	return fname,bits[16+header_length:]

def main():

	src_f 		= "data/b.txt"
	src_f_cln 	= "b.txt"
	img_f 		= "data/image.png"


	#print "Converting file to bits..."
	test_f_bits = file_2_bits(src_f)

	#print "Adding header to bits..."
	test_f_bits = add_header(test_f_bits,src_f_cln)

	#print "Converting bits to pixels..."
	pixels = bits_2_pixels(test_f_bits)

	#print "Writing out pixels to image..."
	pixels_2_png(pixels,img_f)


	#print "Reading pixels from png..."
	pixels = png_2_pixels(img_f)

	#print "Converting pixels to bits..."
	bits = pixels_2_bits(pixels)

	#print "Decoding bit header..."
	fname,bits = decode_header(bits)

	print "Recovered filename: %s" % fname 

	#bitstr = ''.join(bits)


if __name__ == '__main__':
	main()