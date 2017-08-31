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

