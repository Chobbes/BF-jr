"""
  Copyright (C) 2013 Calvin Beck

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation files
  (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge,
  publish, distribute, sublicense, and/or sell copies of the Software,
  and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
  ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

"""

import sys


if len(sys.argv) != 3:
    # Display usage information if the number of arguments is incorrect.
    print("python3 bftomips.py input.bf output.s")
    exit(-1)

# Fetch the Brainfuck program as a string.
bf_file = open(sys.argv[1])
bf_string = bf_file.read()
bf_file.close()

jump_stack = [] # Stack to keep track of the addresses for jumps
translation = [] # List of translated instructions.


for i, character in enumerate(bf_string):
    if character == '+':
        translation += ["addi $r1 $r1 1"]
    elif character == '-':
        translation += ["addi $r1 $r1 -1"]
    elif character == '.':
        translation += ["disp $r1 0"]
    elif character == '>':
        translation += ["sw $r1 0($r0)", "addi $r0 $r0 1", "lw $r1 0($r0)"]
    elif character == '<':
        translation += ["sw $r1 0($r0)", "addi $r0 $r0 -1", "lw $r1 0($r0)"]
    elif character == '[':
        jump_stack += [len(translation)] # Jump to next instruction

        # Need to find the closing bracket
        other_brackets = 0
        offset = 0
        found_matching = False
        for char in bf_string[i:]:
            if char == '>' or char == '<':
                offset += 3
            else:
                offset += 1

            if char == '[':
                other_brackets += 1
            elif char == ']':
                if other_brackets:
                    other_brackets -= 1
                else:
                    found_matching = True
                    break

        if found_matching:
            translation += ["beq $r1 $r2 " + str(offset)]
        else:
            print("Unmatched parenthesis!")
            exit(-1)
    elif character == ']':
        try:
            address = jump_stack.pop()
        except:
            print("Unmatched parenthesis!")
            exit(-1)

        translation += ["j " + str(address)]
        
final_translation = "\n".join(translation) + "\n"

output_file = open(sys.argv[2], "w")
output_file.write(final_translation)
output_file.close()
