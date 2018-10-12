import string


class Lexer:
    def __init__(self, code):
        self.code = code
        self.state = self._state_none
        self.acc = ""

    def process(self):
        return [self.parse(line) for line in self.code.splitlines() if line.strip() and not line.strip().startswith(";")]

    def parse(self, line):
        line = line.strip()
        cmd, *args = line.split(None, 1)

        #print(cmd, args)
        if args:
            args = self.parse_args(args[0])
        else:
            if cmd.endswith(":"):
                args = [cmd[:-1]]
                cmd = "label"
            elif cmd not in ('ret', 'end'):
                raise RuntimeError

        print(cmd, args)
        return cmd, tuple(args)

    def parse_args(self, args):
        self.state = self._state_none

        def generator():
            for c in args:
                if self.state:
                    #print(c, self.state.__name__)
                    yield self.state(c)
            if self.acc:
                yield self.acc

        return [token for token in generator() if token or type(token) is int]

    def _state_none(self, c):
        self.acc = ""

        if c == ";":
            self.state = None
            return

        if c == "'":
            self.state = self._state_string
            self.acc = c
            return

        if c in string.ascii_letters:
            self.state = self._state_label
            self.acc = c
            return

        if c in string.digits:
            self.state = self._state_num
            self.acc = c
            return

    def _state_label(self, c):
        if c == ",":
            pass
        elif c in string.ascii_letters or c in string.digits or c in string.punctuation:
            self.acc += c
            return

        self.state = self._state_none
        return self.acc

    def _state_string(self, c):
        self.acc += c
        if c == "'":
            self.state = self._state_none
            return self.acc

    def _state_num(self, c):
        if c in string.digits:
            self.acc += c
            return

        self.state = self._state_none
        return int(self.acc)


program_fibonacci = '''
mov   a, 8            ; value
mov   b, 0            ; next
mov   c, 0            ; counter
mov   d, 0            ; first
mov   e, 1            ; second
call  proc_fib
call  print
end
; comment
proc_fib:
    cmp   c, 2
    jl    func_0
    mov   b, d
    add   b, e
    mov   d, e
    mov   e, b
    inc   c
    cmp   c, a
    jle   proc_fib
    ret

func_0:
    mov   b, c
    inc   c
    jmp   proc_fib

print:
    msg   'Term ', a, ' of Fibonacci series is: ', b        ; output text
    ret
'''


Lexer(program_fibonacci).process()