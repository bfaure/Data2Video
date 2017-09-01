from PIL import Image
import binascii

from bitstring import BitArray

# for creating gifs
import imageio

import os,sys

four_k = (3840,2160)
HD = (1920,1080)

# encoding...
# 0 is black pixel, white is 1

# writes a gif in parent_folder made up of all it's sorted .png files
def make_gif(parent_folder,fname):
	items = os.listdir(parent_folder)
	png_filenames = []
	for elem in items:
		if elem.find(".png")!=-1:
			png_filenames.append(elem)

	sorted_png = []
	while True:
		lowest = 10000000
		lowest_idx = -1
		for p in png_filenames:
			val = int(p.split("-")[1].split(".")[0])
			if lowest_idx==-1 or val<lowest:
				lowest = val
				lowest_idx = png_filenames.index(p)
		sorted_png.append(png_filenames[lowest_idx])
		del png_filenames[lowest_idx]
		if len(png_filenames)==0: break
	png_filenames = sorted_png

	with imageio.get_writer(fname+".gif", mode='I',duration=0.1) as writer:
		for filename in png_filenames:
			image = imageio.imread(parent_folder+"/"+filename)
			writer.append_data(image)
	return fname+".gif"

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

# writes out the bits as binary to a file
def bits_2_file(bits,fname):
	f = open(fname,'wb')
	idx=0
	inc=8
	while True:
		char = ''.join(bits[idx:idx+inc])
		f.write(chr(int(char,2)))
		idx+=inc
		if idx>=len(bits): break
	f.close()
	print "bits_2_file: Wrote %d bits to %s" % (len(bits),fname)

# returns a list of bits in the file
def file_2_bits(fname):
	bits = []
	f = open(fname, "rb")
	try:
	    byte = f.read(1)
	    while byte != "":
	        cur_bits = bin(ord(byte))[2:]
	        while len(cur_bits)<8:
	        	cur_bits = "0"+cur_bits
	        for b in cur_bits:
	        	bits.append(b)
	       	byte = f.read(1)
	finally:
	    f.close()
	'''
	first_char = ''.join(bits[:8])
	n = int(first_char,2)
	print binascii.unhexlify('%x' % n)
	'''
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
	fname_bitstr = bin(int(binascii.hexlify(fname), 16))
	
	print "add_header: fname_bitstr length %d" % len(fname_bitstr)

	# extra 2 bytes (16 bits) before header tells how long header is (in bits)
	fname_bitstr_length_bitstr = "{0:b}".format(len(fname_bitstr)-2)

	while len(fname_bitstr_length_bitstr)<16:
		fname_bitstr_length_bitstr = "0"+fname_bitstr_length_bitstr

	# length header to tell how long the rest of the header is, as
	# well as the header itself
	fname_headers = fname_bitstr_length_bitstr+fname_bitstr[2:]

	# converting the string header to a list
	header_list = []
	for char in fname_headers:
		header_list.append(char)

	# secondary header after filename to tell how many bits the payload is
	# length of secondary header is 64 bits to allow for massive payload sizes
	payload_length_header = "{0:b}".format(len(bits))

	print "bits in payload: %d" % len(bits)

	while len(payload_length_header)<64:
		payload_length_header = "0"+payload_length_header

	# append the secondary header to the main header
	for char in payload_length_header:
		header_list.append(char)

	total_header_length = len(header_list)

	# append the original bits onto the header and return
	header_list.extend(bits)
	#print "add_header: Added %d length header, total bits: %d" % (len(total_header),len(header_list))

	#print "add_header: total_header: %s" % ''.join(header_list[:total_header_length])
	return header_list

# takes in the bits, decodes the header into a filename.
# returns the filename, as well as the rest of the bits 
# after the header section
def decode_header(bits):

	# helper function, converts a binary string (eg. '10101') to ASCII characters
	def decode_binary_string(s):
	    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

	#print ''.join(bits[:100])

	# first 16 bits store the length of the filename (in bits)
	fname_length_binstr = ''.join(bits[:16])

	# converting filename length to integer
	fname_length = int(fname_length_binstr,2)
	print "decode_header: fname_length: %d" % fname_length

	# next fname_length bits are the ASCII filename
	fname_binstr = ''.join(bits[16:16+fname_length])
	fname_binstr = "0"+fname_binstr

	#print "fname binary %s" % fname_binstr
	
	# convert the fname bitstring to ASCII
	fname = decode_binary_string(fname_binstr)
	print "decode_header: fname: %s"%fname

	#n = int(rest_of_header,2)
	#fname = binascii.unhexlify('%x' % n)

	# now need to decode the size of the payload
	payload_length_binstr = ''.join(bits[16+fname_length:16+fname_length+64])

	# convert the payload length to integer
	payload_length = int(payload_length_binstr,2)
	print "decode_header: payload_length: %d" % payload_length

	#print "decoder_header: total_header: %s" % ''.join(bits[:16+fname_length+64])

	#print "decode_header: Found %d length header, " % (fname_length)
	return fname,bits[16+fname_length+64:16+fname_length+64+payload_length]

def test_bit_similarity(bits1,bits2):

	f = open("bits.txt","w")
	for b1 in bits1:
		f.write(b1)
	f.write("\n")
	for b2 in bits2:
		f.write(b2)
	f.write("\n")
	f.close()

	if len(bits1)!=len(bits2):
		print "Bit lengths are not the same!"
		return
	for b1,b2 in zip(bits1,bits2):
		if b1!=b2:
			print "Bits are not the same!"
			return
	print "Bits are identical"

# - provided a source file, encodes it into a .gif video
# - all .png's created in the process are held in the /temp directory
def encode(src,res=four_k):
	bits 	= file_2_bits(src)
	bits 	= add_header(bits,src.split("/")[-1])
	pixels 	= bits_2_pixels(bits)

	# get the total number of pixels in a single image
	pixels_per_image = res[0]*res[1]

	# get the number of images required to hold entire file
	num_imgs = int(len(pixels)/pixels_per_image)+1

	# filename without any path specifiers
	name_clean = src.split("/")[-1]

	# create each of the png's
	for i in range(num_imgs):
		cur_temp_name = "temp/"+name_clean+"-"+str(i)+".png"
		cur_start_idx = i*pixels_per_image
		cur_span = min(pixels_per_image, len(pixels)-cur_start_idx)
		cur_pixels = pixels[cur_start_idx:cur_start_idx+cur_span]
		pixels_2_png(cur_pixels,cur_temp_name)
		if cur_span<pixels_per_image: break

	# create gif from png sequence
	gif_name = make_gif("temp",name_clean)
	return gif_name


def main():
	encode("data/test.jpg")


	'''
	src_f 		= "data/test.jpg"
	src_f_cln 	= "test.jpg"
	img_f 		= "data/image.png"


	#print "Converting file to bits..."
	test_f_bits = file_2_bits(src_f)
	orig_bits = test_f_bits

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

	test_bit_similarity(orig_bits,bits)

	bits_2_file(bits,src_f.split(".")[0]+"-copy."+src_f_cln.split(".")[1])

	#bitstr = ''.join(bits)
	'''

if __name__ == '__main__':
	main()