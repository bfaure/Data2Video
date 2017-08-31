
from PIL import Image

import binascii

four_k = (3840,2160)
HD = (1920,1080)

# encoding...
# 0 is black pixel, white is 1

# 
def write_png(pixels,reso=four_k,fname="image.png"):
	img = Image.new('RGB',reso)
	img.putdata(pixels)
	img.save(fname)

# returns a list of bits in the file
def read_file_bits(fname):

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
			bits.append(0)
		else:
			bits.append(1)
	return bits

# adds the file name header to the list of bits
def add_header(bits,fname):
	# header is always 300 characters (2400 bits at 8 bits/character)
	header_bits = bin(int(binascii.hexlify(fname), 16))
	print header_bits



def main():

	fname = "test.txt"
	add_header([],fname)
	return


	pixels = [(0,0,0),(255,255,255),(0,0,0),(255,255,255),
			(0,0,0),(255,255,255),(0,0,0),(255,255,255),(0,0,0),
			(255,255,255),(0,0,0),(255,255,255),(0,0,0)]

	write_png(pixels)


if __name__ == '__main__':
	main()