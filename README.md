# Data2Video
Algorithms to convert arbitrary binary data into video and vice versa.

## Status

Currently we have the following pipeline; we take an arbitrary input file...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/source_file.PNG)

which is read as raw binary. To the beginning of this binary we append the following three header sections...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/headers.PNG)

The first of which is a constant 16 bits. This section denotes the number of bits in the following section, the "Filename" section, in binary numerical form. Thus, our maximum filename size is 65,535 bits, or 8,192 characters.

Inside the filename section we have the full text of the filename, encoded in binary format. Recall, this section is of variable length, as specified in the first section.

The third section, "Payload Length", functions similar to the "Filename Length" and specifies the number of bits in the original file. Payload length is of length 64 bits, meaning our maximum encoded filesize is 2^64-1 bits. Once again, this section is responsible for reporting the length of the next section, the "Payload" which is the original arbitrary input file.

With this entire binary string in hand, we now iterate over each bit, converting 0's to (0,0,0) and 1's to (255,255,255). At the end of this step, we now have another list of the same length as the number of bits, but containing instead, pixels which are either black (to signify '0'), or white (to signify '1'). We then create a new .png image with these pixels. The following is the .png representation of our original file...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/converted.png)

As of now, we are using a default 4K image size (3840 x 2160). This allows for a maximum size of 8,294,400 bits to be represented per frame, or approximately 1 MB. 

The reverse of this process is used to decode the contents of the image, simply put; we recover the bits of the .png image by converting all pixels to bits, then recover the length of the filename by reading the first 16 bits, then recover the original filename, then recover the length of the payload (original file) by reading the 64 bits of the "Payload Length" section.

## Issues

When converting back from .png to our original file, we are able to recover the ASCII filename and the length of the payload but the payload itself seems corrupted. Even though the bits we encode are identical to the bits we recover, the output file encoding seems inaccurate. For example, this is the decoded file for the example process above (Alice in Wonderland)...

![Alt text](https://github.com/bfaure/Data2Video/blob/master/resources/problems.PNG)

## Future Improvements

Allow for individual files to span across multiple .png images, to allow for files larger than 1MB to be represented. Once this is complete, the .png images will be strung together using the .gif wrapper to create videos of arbitrary length. Hesitate to use .mp4 wrapper because the compression may cause bits to be lost in translation. To combat the compression issues of .jpg and .mp4, increase the demarkation size for a single bit. For example, now we are encoding a single bit as a 1x1 pixel, which may be lost to compression. Instead, encoded each bit as an nxn square, making it less likely compression will remove the entity. 

# Overall Idea

Youtube allows for 128 GB uploads, and nearly infinite uploads total. If users could encode their data as videos, they would have an easy way of backing up whatever content they wish. A 60fps 4K video has the ability to store a lot of data, if the encoding process we use is sufficient.

