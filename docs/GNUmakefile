#! /usr/bin/gmake -f

BUILD ?= ../build

testmanpages: zzip_close zzip_closedir zzip_fopen zzip_fread zzip_fstat
zzip_close zzip_closedir zzip_fopen zzip_fread zzip_fstat: 
	man -M $(BUILD)/docs -P cat $@

-include Makefile
