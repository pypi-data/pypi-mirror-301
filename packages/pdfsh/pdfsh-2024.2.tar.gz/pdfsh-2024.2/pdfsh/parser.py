# Copyright (C) 2024 Mete Balci
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# pdfsh: a minimal shell to investigate PDF files
# Copyright (C) 2024 Mete Balci
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
import re

from .tokens import *
from .tokenizer import Tokenizer
from .objects import *

logger = logging.getLogger(__name__)

integer_re = re.compile(r"^[\+\-]?[0-9]+$")
real1_re = re.compile(r"^[\+\-]?[0-9]*\.[0-9]+$")
real2_re = re.compile(r"^[\+\-]?[0-9]+\.[0-9]*$")

LF = 0x0A
CR = 0x0D

def is_integer(v):
    assert isinstance(v, str)
    return integer_re.match(v) is not None

def is_real(v):
    assert isinstance(v, str)
    return (real1_re.match(v) is not None) or (real2_re.match(v) is not None)

# parser for PDF data in buffer
class Parser:

    def __init__(self, buffer):
        self.buffer = buffer
        self.tokenizer = Tokenizer(self.buffer)

    def size(self):
        return len(self.buffer)

    def next_line(self):
        start = self.tell()
        end = start
        pos = start
        while pos < len(self.buffer):
            ch = self.buffer[pos]
            if pos > 0 and ch == ord('%'):
                break
            end = pos
            pos = pos + 1
            # LF is EOL
            if (ch == LF):
                break
            # CR is EOL
            elif ch == CR:
                # CR LF is EOL, it is important to advance position +1
                if pos < len(self.buffer) and self.buffer[pos] == LF:
                    pos = pos + 1
                break
        self.seek(pos)
        line = self.buffer[start:end]
        logger.debug('line=%s 0x%s' % (line.decode('ascii', 'replace'),
                                       line[0:32].hex() if len(line) > 32 else line.hex()))
        return line

    def seek_to_start_of_line(self):
        pos = self.tell()
        # if already at pos=0, cannot move back
        if pos == 0:
            return

        # if on EOL marker, move back to last char to find the end of line
        if self.buffer[pos] == LF or self.buffer[pos] == CR:
            while pos >= 0:
                if self.buffer[pos] == LF or self.buffer[pos] == CR:
                    pos = pos - 1

                else:
                    break

        # move back to CR or LF to find the start of the line
        while pos >= 0:
            if self.buffer[pos] == CR or self.buffer[pos] == LF:
                self.seek(pos + 1)
                return

            else:
                pos = pos - 1

        self.seek(0)

    def reset(self):
        self.seek(0)

    def tell(self):
        return self.tokenizer.tell()

    def seek(self, pos):
        self.tokenizer.seek(pos)

    def next(self):
        token = self.tokenizer.next()
        if isinstance(token, TokenLiteral):
            v = token.as_bytes().decode('ascii', 'replace')
            if v == 'true':
                return PdfBoolean(True)
            elif v == 'false':
                return PdfBoolean(False)
            elif v == 'null':
                return PdfNull()
            else:
                if is_integer(v):
                    logger.debug('v: %s' % v)
                    rollback_pos = self.tell()
                    object_number = int(v)
                    v2 = self.tokenizer.next()
                    logger.debug('v2: %s' % v2)
                    if (v2 is not None and
                        isinstance(v2, TokenLiteral) and
                        is_integer(v2.as_bytes().decode('ascii', 'replace'))):
                        generation_number = int(v2.as_ascii())
                        v3 = self.tokenizer.next()
                        logger.debug('v3: %s' % v3)
                        if (v3 is not None and
                            isinstance(v3, TokenLiteral)):
                            if (v3.as_bytes() == b'R'):
                                return PdfIndirectReference(object_number,
                                                            generation_number)
                            elif (v3.as_bytes() == b'obj'):
                                value = self.next()
                                stream_dictionary = None
                                stream_data = None
                                if isinstance(value, PdfDictionary):
                                    token = self.tokenizer.next()
                                    if isinstance(token, TokenLiteral):
                                        if token.as_bytes() == b'stream':
                                            logger.debug('found stream')
                                            stream_dictionary = value
                                            assert PdfName('Length') in stream_dictionary, 'stream dictionary does not have Length'
                                            # read stream data directly
                                            stream_length = stream_dictionary[PdfName('Length')].p
                                            logger.debug('stream_length: %d' % stream_length)
                                            stream_data = self.buffer[self.tell():self.tell() + stream_length]
                                            # advance
                                            self.seek(self.tell() + stream_length)
                                            token = self.tokenizer.next()
                                            assert isinstance(token, TokenLiteral)
                                            assert token.as_bytes() == b'endstream', 'stream does not end with endstream'
                                            token = self.tokenizer.next()
                                            assert isinstance(token, TokenLiteral)
                                            assert token.as_bytes() == b'endobj', 'stream does not end with endobj'
                                            return PdfIndirectObject(object_number,
                                                                     generation_number,
                                                                     PdfStream(stream_dictionary,
                                                                               stream_data))
                                return PdfIndirectObject(object_number,
                                                         generation_number,
                                                         value)
                    self.seek(rollback_pos)
                    return PdfIntegerNumber(int(v))
                elif is_real(v):
                    try:
                        return PdfRealNumber(float(v))
                    except ValueError:
                        raise PossibleBugException('not a real number? %s' % v)
                else:
                    assert False, 'not implemented'
        elif isinstance(token, TokenLiteralStringStart):
            string = self.tokenizer.next()
            assert isinstance(string, TokenLiteral), string
            end = self.tokenizer.next()
            assert isinstance(end, TokenLiteralStringEnd), end
            return PdfLiteralString(string.as_bytes())
        elif isinstance(token, TokenHexStringStart):
            string = self.tokenizer.next()
            assert isinstance(string, TokenLiteral), string
            end = self.tokenizer.next()
            assert isinstance(end, TokenHexStringEnd), end
            return PdfHexadecimalString(string.as_bytes())
        elif isinstance(token, TokenSolidus):
            token = self.tokenizer.next()
            return PdfName(token.as_bytes())
        elif isinstance(token, TokenArrayStart):
            logger.debug('PdfArray')
            array = PdfArray()
            while True:
                rollback_pos = self.tell()
                token = self.tokenizer.next()
                if isinstance(token, TokenArrayEnd):
                    return array
                else:
                    # rollback because entry or initial part of it is already read
                    self.seek(rollback_pos)
                    entry = self.next()
                    logger.debug('entry: %s' % entry)
                    array.append(entry)
        elif isinstance(token, TokenDictionaryStart):
            logger.debug('PdfDictionary')
            dictionary = PdfDictionary()
            while True:
                rollback_pos = self.tell()
                token = self.tokenizer.next()
                if isinstance(token, TokenDictionaryEnd):
                    logger.debug('PdfDictionary len=%d' % len(dictionary))
                    return dictionary
                else:
                    assert isinstance(token, TokenSolidus)
                    # rollback because solidus is already read
                    self.seek(rollback_pos)
                    entry_key = self.next()
                    assert isinstance(entry_key, PdfName), entry_key

                    entry_value = self.next()
                    assert isinstance(entry_key, PdfObject), entry_value

                    if (isinstance(entry_value, PdfArray) or
                        isinstance(entry_value, PdfDictionary)):
                        logger.debug('%s -> entry_value_type: %s' % (entry_key,
                                                                     entry_value.__class__.__name__))
                    else:
                        logger.debug('%s -> entry_value: %s' % (entry_key,
                                                                entry_value))

                    if (entry_key == PdfName(b'Type') or
                        entry_key == PdfName(b'Subtype')):
                        if not isinstance(entry_value, PdfName):
                            raise PdfConformanceException('The value of Type and Subtype entries in a dictionary should be a Name')

                    # "A dictionary entry whose value is null
                    # shall be treated the same as if the entry does not exist"
                    # ISO 32000-2 7.3.7
                    if not isinstance(entry_value, PdfNull):
                        dictionary[entry_key] = entry_value
