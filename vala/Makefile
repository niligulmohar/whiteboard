
SOURCES = src/whiteboards.vala
NAME = Whiteboard-0.1
LIBRARY = lib$(NAME).so
GIR = $(NAME).gir
TYPELIB = $(NAME).typelib

all: $(LIBRARY) $(TYPELIB)

$(LIBRARY): $(SOURCES)
	valac --pkg=gio-2.0 --pkg=gee-0.8 --library=whiteboard -X -fPIC -X -shared --gir=$(GIR) -o $@ $^

$(TYPELIB): $(LIBRARY)
	g-ir-compiler --shared-library=$< --output=$@ $(GIR)

clean:
	@rm $(LIBRARY) $(GIR) $(TYPELIB)

.PHONY: all clean
