# Compiler and flags
CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -shared -llzma

HARDNESTED_DIR = .

# Source files
HARDNESTED_SOURCES = $(HARDNESTED_DIR)/pm3/ui.c $(HARDNESTED_DIR)/pm3/util.c \
                     $(HARDNESTED_DIR)/cmdhfmfhard.c $(HARDNESTED_DIR)/library.c \
                     $(HARDNESTED_DIR)/pm3/commonutil.c $(HARDNESTED_DIR)/crapto1.c \
                     $(HARDNESTED_DIR)/bucketsort.c $(HARDNESTED_DIR)/crypto1.c \
                     $(HARDNESTED_DIR)/hardnested/hardnested_bf_core.c \
                     $(HARDNESTED_DIR)/hardnested/hardnested_bruteforce.c \
                     $(HARDNESTED_DIR)/hardnested/hardnested_bitarray_core.c \
                     $(HARDNESTED_DIR)/hardnested/tables.c \
                     $(HARDNESTED_DIR)/pm3/util_posix.c

# Object files
HARDNESTED_OBJECTS = $(HARDNESTED_SOURCES:.c=.o)

# Dependency files
HARDNESTED_DEPS = $(HARDNESTED_SOURCES:.c=.d)

# Targets
all: hardnested.so

hardnested.so: $(HARDNESTED_OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(HARDNESTED_OBJECTS) $(HARDNESTED_DEPS) hardnested.so

.PHONY: all clean

# Include dependencies
-include $(HARDNESTED_OBJECTS:.o=.d)

# Generate dependencies
%.d: %.c
	@$(CC) -MM $(CFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$
