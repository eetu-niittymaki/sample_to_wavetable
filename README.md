# sample_to_wavetable

A small script I wrote to make it easier to create new samples for an arduino based drum machine.
Cuts down .wav files to 2048 samples in length and downsamples them to mono, 
uses ffmpeg to generate signed 8bit .raw files from the .wav files. Finally it creates wavetables to .c header files.
