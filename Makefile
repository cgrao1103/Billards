# Makefile for C program with all warnings enabled

# Compiler
CC = gcc

# Compiler flags with all warnings
CFLAGS = -Wall -std=c99 -g

# Source files
SRCS = phylib.c A1test1.c

# Header files
HDRS = phylib.h

# Object files
OBJS = $(SRCS:.c=.o)

# Executable name
TARGET = A1test1

# Rule to build the executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Rule to build object files
%.o: %.c $(HDRS)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean rule
clean:
	rm -f $(OBJS) $(TARGET)
