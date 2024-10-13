from .parser import parse as parser_parse
from .peripherals import Keyboard, Screen
from .vm import VM


def run(src, *, keyboard=None, screen=None, parse=None):
    parse = parse or parser_parse
    vm = VM()
    vm.keyboard = keyboard or Keyboard()
    vm.screen = screen or Screen()
    vm.instructions = parse(src)
    vm.run()
