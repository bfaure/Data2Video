# Overall Idea

Youtube allows for 128 GB uploads, and nearly infinite uploads total, free of cost. If users could encode their data as videos, they would have an easy way of backing up whatever content they wish. A 60fps 4K video has the ability to store a lot of data, if the encoding process we use is sufficient.

Our process thus far only supports .gif output, which is not acceptable as a data format on Youtube. To route around this issue, Imgur can be used as the data sink, which also tmk has no cap on upload size / count.

# Example

We wish to encode the .mp3 audio file found under the /data directory into a .gif video. The song, viewable [here](https://drive.google.com/open?id=0BxJe_Ggl7BIgUmdCWk1ZY05SSWc), is "Paris" by LASERS.

We call the encode() function, passing the path to the .mp3 as the only parameter. This will convert the .mp3 into a list of pixels, either being (0,0,0) or (255,255,255), representing "0" and "1" in binary, respectively. The function will then produce a series of 4K .png images (stored in the /temp directory), which are strung together to create the final .gif video. For our input .mp3, the following is the .gif output.

![Alt text](https://github.com/bfaure/Data2Video/blob/master/test.mp3.gif)

Consisting of 9 4K .png's, at 10 frames per second. To increase the data bitrate, we can either increase the .png resolution or increase the framerate. Note that there is a minor header section we append to the bits before converting them into pixels, see the Encoding Process section for more info. 

To convert the .gif back into it's original file (in this case 'test.mp3'), it's as simple as calling decode(), passing the path to the gif as the parameter. This will split the .gif back into it's constituent .png images and reverse the encoding process to recover the original file, saving it with the same name as the original, but with -recovered appended to the end.

# Encoding / Decoding Process

Currently we have the following pipeline; we take an arbitrary input file (data/test.txt)...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/source_file.PNG)

and read it in as raw binary. To the beginning of this binary we append the following three header sections...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/headers.PNG)

The first of which is a constant 16 bits. This section denotes the number of bits in the following section, the "Filename" section, in binary numerical form. Thus, our maximum filename size is 65,535 bits, or 8,192 characters.

Inside the filename section we have the full text of the filename, encoded in binary format. Recall, this section is of variable length, as specified in the first section.

The third section, "Payload Length", functions similar to the "Filename Length" and specifies the number of bits in the original file. Payload length is of length 64 bits, meaning our maximum encoded filesize is 2^64-1 bits. Once again, this section is responsible for reporting the length of the next section, the "Payload" which is the original arbitrary input file.

With this entire binary string in hand, we now iterate over each bit, converting 0's to (0,0,0) and 1's to (255,255,255). At the end of this step, we now have another list of the same length as the number of bits, but containing instead, pixels which are either black (to signify '0'), or white (to signify '1'). We then create a new .png image with these pixels. The following is the .png representation of our original file...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/converted.png)

As of now, we are using a default 4K image size (3840 x 2160). This allows for a maximum size of 8,294,400 bits to be represented per frame, or approximately 1 MB. 

The reverse of this process is used to decode the contents of the image, simply put; we recover the bits of the .png image by converting all pixels to bits, then recover the length of the filename by reading the first 16 bits, then recover the original filename, then recover the length of the payload (original file) by reading the 64 bits of the "Payload Length" section.

## Future Improvements

Find a suitable video wrapper format to convert the .gif videos into. Hesitate to use .mp4 because the compression may cause bits to be lost in translation. To combat the compression issues of .jpg and .mp4, increase the demarkation size for a single bit. For example, now we are encoding a single bit as a 1x1 pixel, which may be lost to compression. Instead, encoded each bit as an nxn square, making it less likely compression will remove the entity. 

## Dependencies
* Python 2.7
* PIL Library
* bitstring Library
* imageio Library
* shutil Library


