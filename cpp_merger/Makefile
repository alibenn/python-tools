CC = g++
CFLAGS = -c -Wall `root-config --cflags` -g 
LDFLAGS=`root-config --glibs`
EXECUTABLE=merger
SOURCES=merger.cpp
OBJECTS=$(SOURCES:.cpp=.o)
all: $(SOURCES) $(EXECUTABLE)
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@
.cpp.o:
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm ./*~ ./*.o ./merger
