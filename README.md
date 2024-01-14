# image-tokenizer

## Purpose

Given a picture containing text in an unknown characterset, identify 
the individual characters and convert them to a latin character set
for use in cryptanalysis.

This tool is intended for use in solving puzzles with novel character
sets as an alternative to manually transcribing images.

## Limitations

* Assumes left to right, top to bottom
* Assumes that lines are separated by pure whitespace
* Assumes that characters are separated by pure whitespace
* Will not work with any kind of cursive
* Colors hardcoded

## Future improvements

* Image similarity, not just exact match
* Alternative reading direction
* Overlapping characters
* Command line params: file name, background color
* Parse based on foreground, not background color in case of variable background

## Setup

```sh
sudo apt install python3 python3-pip && pip3 install numpy imageio
```
