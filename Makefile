CC = clang
CFLAGS = -std=c99 -Wall -pedantic -fpic

# Target for phylib.o
phylib.o: phylib.c
	$(CC) $(CFLAGS) -c $< -o $@

# Target for libphylib.so
libphylib.so: phylib.o
	$(CC) -shared $< -o $@

# Target for phylib_wrap.c and phylib.py
phylib_wrap.c phylib.py: phylib.i phylib.o
	swig -python $<
	$(CC) $(CFLAGS) -c phylib_wrap.c -o phylib_wrap.o

# Target for _phylib.so
_phylib.so: phylib_wrap.o phylib.o
	$(CC) -shared $^ -o $@

# Target for cleaning up
clean:
	rm -f phylib_wrap.c phylib.py phylib_wrap.o phylib.o libphylib.so _phylib.so
