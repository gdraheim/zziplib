
pages = 64on32.htm configs.htm copying.htm developer.htm \
 download.htm faq.htm fseeko.htm functions.htm future.htm \
 history.htm memdisk.htm mmapped.htm notes.htm referentials.htm \
 sfx-make.htm zip-php.htm zzip-api.htm zzip-basics.htm \
 zzip-crypt.htm zzip-cryptoid.htm zzip-extio.htm zzip-extras.htm \
 zzip-file.htm zzip-index.htm zzip-parse.htm zzip-sdl-rwops.htm \
 zzip-xor.htm zzip-zip.htm

xx:
	test -d tmp.xx || mkdir tmp.xx
	for p in $(pages); do python3 docs/mdhtm.py docs/$$p > tmp.xx/$$p.xx1 ; done
	for p in $(pages); do python3 docs/md2dbk.py -r docs/$$p.md > tmp.xx/$$p.xx2 ; done

html2md.py:
	wget https://raw.githubusercontent.com/al3xandru/html2md/master/html2md.py
docsmd:
	for p in $(pages); do python html2md.py docs/$$p > docs/$$p.md ; done
