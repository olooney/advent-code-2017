

def turing(tape, cursor, state):
    if cursor < 0 or cursor > len(tape):
        raise ValueError("cursor left tape.")

    if state == 'A':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'B')
        if tape[cursor] == 1:
              tape[cursor] = 1
              cursor -=1
              return (cursor, 'E')
    elif state == 'B':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'C')
        if tape[cursor] == 1:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'F')
    elif state == 'C':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor -=1
              return (cursor, 'D')
        if tape[cursor] == 1:
              tape[cursor] = 0
              cursor += 1
              return (cursor, 'B')
    elif state == 'D':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'E')
        if tape[cursor] == 1:
              tape[cursor] = 0
              cursor -=1
              return (cursor, 'C')
    elif state == 'E':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor -=1
              return (cursor, 'A')
        if tape[cursor] == 1:
              tape[cursor] = 0
              cursor += 1
              return (cursor, 'D')
    elif state == 'F':
        if tape[cursor] == 0:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'A')
        if tape[cursor] == 1:
              tape[cursor] = 1
              cursor += 1
              return (cursor, 'C')

tape = [0]*1000000
cursor = len(tape)//2
#Begin in state A.
state = 'A'

#Perform a diagnostic checksum after 12459852 steps.
for _ in range(12459852):
    cursor, state = turing(tape, cursor, state)

print(sum(tape))
