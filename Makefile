# Makefile for C program with all warnings enabled

# Compiler
CC = clang
CFLAGS = -std=c99 -Wall -pedantic
LDFLAGS = -L. -lphylib -lm

all: libphylib.so 

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fpic -c $< -o $@

libphylib.so: phylib.o
	$(CC) -shared -o $@ $<

A1test1: A1test1.c phylib.h libphylib.so
	$(CC) $(CFLAGS) $< $(LDFLAGS) -o $@

clean:
	rm -f *.o *.so