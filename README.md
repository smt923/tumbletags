# tumbletags
Scrape a Tumblr blog and save tags found within posts to a csv file. Should work with any blog where the archive is accessable at `/archive`

## Usage
Run with no arguments and `-h` for a list of flags.

Basic usage:

```
python tumbletags.py http://tumblrblog.tumblr.com
```
This will save the output to a csv file with the blog's url as the filename.

## Requirements
Beautifulsoup is required:
```
pip3 install beautifulsoup4
```