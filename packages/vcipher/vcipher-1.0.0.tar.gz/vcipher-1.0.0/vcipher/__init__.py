## Vcipher (c) 2024 - Made by V / Lou du Poitou ##
##
# GitHub => https://github.com/Lou-du-Poitou/
# Python => https://pypi.org/user/lou_du_poitou/
# Git => https://github.com/Lou-du-Poitou/vcipher
##

# --- --- --- #

# MIT License

# Copyright (c) 2024 V / Lou du Poitou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# --- --- --- #

def _break_in_128_bits(data: bytes) -> list:
    padding = bytes(16-(len(data)%16))
    if len(padding) != 16: data += padding
    
    result = []
    for i in range(0, len(data)//16):
        bloc = data[i*16 : i*16 + 16]
        grid = [[], [], [], []]
        for i in range(0, 4):
            for x in range(0, 4):
                grid[i].append(bloc[i + x * 4])
        result.append(grid)
    return result

# --- --- --- #

def _restore_from_blocks(data: list) -> list:
    result = []
    for i in range(0, len(data)):
        for x in range(0, 4):
            for y in range(0, 4):
                result.append(data[i][y][x])
    return result

# --- --- --- #

def cipher(data: bytes, key: bytes) -> bytes:
    '''
    > Vcipher (c) 2024 - Made by V / Lou du Poitou
    
    > Use cipher(data: bytes, key: bytes)
    
    > The key length must be 128 bits
    '''
    
    if len(key) != 16: 
        raise ValueError("The key length must be 128 bits")
    
    data = _break_in_128_bits(data)
    
    for i in range(0, len(data)):
        key = key[1:] + key[:1]
        for x in range(0, 4):
            for y in range(0, 4):
                data[i][x][y] ^= key[x * 4 + y]
                
    result = _restore_from_blocks(data)
                
    return bytes(result)

# --- --- --- #

## Vcipher (c) 2024 - Made by V / Lou du Poitou ##