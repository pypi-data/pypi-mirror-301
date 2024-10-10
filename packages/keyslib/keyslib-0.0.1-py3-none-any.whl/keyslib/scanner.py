#!/usr/bin/env python3
from enum import auto, IntEnum
from dataclasses import dataclass
from typing import List, Optional, Union

from keyslib.types import ModifierType, KeywordType


class TokenType(IntEnum):
    """Scanner token types.

    These correspond to the various tokens that the scanner can return from a
    given source text sequence.
    """

    UNKNOWN = 0

    # End of sequence
    EOF = auto()

    # Plus for delineating key sequences
    # + -> PLUS
    PLUS = auto()

    # Pipe for combining modifiers
    # | -> PIPE
    PIPE = auto()

    # <> symbols, for denoting of a keyword key
    # <left> for left arrow
    LESS_THAN = auto()
    GREATER_THAN = auto()

    # Parenthesis, for grouping modifiers
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    # Modifiers, expressed within () symbols
    # (ctrl) -> LEFT_PAREN, MODIFIER(ModifierType.CTRL), RIGHT_PAREN
    MODIFIER = auto()

    # Keywords, expressed within <> symbols
    # <left> -> LESS_THAN, KEYWORD(KeyWordType.LEFT), GREATER_THAN
    KEYWORD = auto()

    # "Primary" key
    # b -> PRIMARY("b")
    PRIMARY = auto()

    # Doctag, which is a hash (#) symbol at the end of a key sequence, followed
    # by an optional group name (#editor)
    DOCTAG = auto()

    # Docstring, which is any additional metadata after a hash (#) on a key sequence
    # b # Press the b key -> PRIMARY("b"), DOCSTRING(" Press the b key")
    DOCSTRING = auto()


# TODO: I could probably Token into a typed subclass, but it isn't used past
# scanning so it's probably not really necessary.
TokenValue = Union[str, KeywordType, ModifierType]


@dataclass(frozen=True)
class Token:
    """A token from the Scanner, representing a portion of the scanned text.

    Public Attributes:
        type: TokenType. The type of the token value scanned.
        value: Optional[TokenValue]. The parsed value for this token, if any.
    """

    type: TokenType
    value: Optional[TokenValue] = None


# (ctrl|shift)<left>+c
# [LEFT_PAREN, MODIFIER(CTRL), PIPE, MODIFIER(SHIFT), RIGHT_PAREN, LESS THAN,
#  KEYWORD(LEFT), GREATER_THAN, PLUS, PRIMARY("c"), EOF]
class Scanner:
    """Key Scanner class.

    This class scans a given source text and returns a list of tokens, to be
    used by the Parser to generate a KeySequence.

    Args:
        sequence: str. Key sequence in text format.

    Public Attributes:
        length: int. Length of the input sequence.
        start: int. Start index of the current scan pass. This is updated to the
            current position after every scanned Token.
        current: int. Current index of the scan pass. The range from start:current
            will represent a matched Token at the end of a scan pass.
        tokens: List[Token]. All scanned tokens.
    """

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence
        self.length: int = len(self.sequence)
        self.start = 0
        self.current = 0
        self.tokens: List[Token] = []

    @staticmethod
    def scan(sequence: str) -> List[Token]:
        """Scan a key sequence.

        Given a text key sequence, this will return a scanned list of all matched
        tokens, to be used by the Parser to generate a KeySequence.

        Args:
            sequence: str. Text key sequence.

        Returns:
            tokens: List[Token]. All Tokens matched from the text.
        """

        return Scanner(sequence).scan_tokens()

    @property
    def at_end(self) -> bool:
        """Check if Scanner's current position is at the end of the sequence.

        Returns:
            at_end: bool. Whether or not the Scanner has reached the end of the
                sequence.
        """

        return self.current >= self.length

    def advance(self) -> str:
        """Retrieve the char at the Scanner's current position, then advance it.

        Returns:
            char: str. Character at Scanner's position prior to advancement.
        """

        char = self.sequence[self.current]
        self.current += 1

        return char

    def peek(self) -> str:
        """Return the char at the current index without consuming it.

        Returns:
            current_char: str. Char at the current index.
        """

        if self.at_end:
            # End of file, return NUL
            return "\0"

        return self.sequence[self.current]

    def add_token(self, type: TokenType, value: Optional[TokenValue] = None) -> None:
        """Add a matched token.

        Args:
            type: TokenType. The type of the token value scanned.
            value: Optional[TokenValue]. The parsed value for this token, if any.
        """

        self.tokens.append(Token(type=type, value=value))

    def scan_token(self) -> None:
        """Scan the remaining text for a Token.

        This is called at the start of a scan and after all token matches, until
        the end of the text is reached, adding a matched Token after each pass.
        """

        char = self.advance()
        match char:
            # Single character tokens
            case "+":
                self.add_token(TokenType.PLUS)
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "<":
                self.add_token(TokenType.LESS_THAN)
            case ">":
                self.add_token(TokenType.GREATER_THAN)
            case "|":
                self.add_token(TokenType.PIPE)
            case "#":
                # Scan in a doctag
                self.doctag()
            case _:
                # Ignored characters
                # Whitespace
                if char.isspace():
                    pass
                elif char.isalnum():
                    # Scan an alphanumeric char(s) or identifier
                    self.identifier()
                else:
                    # Add any other otherwise unrecognized chars as Primary tokens,
                    # which can be handled directly
                    self.add_token(TokenType.PRIMARY, char)

    def doctag(self) -> None:
        """Scan and match a doctag.

        A doctag represents the beginning of any additional metadata about a key
        sequence. It consists of a # (<hash>) symbol, an optional group name, and an
        optional Docstring, which describes the key sequence.
        """

        # #foo_123-bar Describe the command
        while self.peek().isalnum() or self.peek() in ("_", "-"):
            self.advance()

        # Doctag("foo_123-bar")
        doctag = self.sequence[self.start + 1 : self.current]
        self.add_token(TokenType.DOCTAG, doctag)

        # Anything the scanner stopped on that isn't a space is an unexpected
        # char in the doctag
        if not self.peek().isspace():
            raise ValueError(f"Unexpected character in doctag: {self.peek()}")

        # Skip whitespace
        while self.peek().isspace():
            self.advance()

        # Reset scan index
        # TODO: This should probably be split out of the docstring logic somehow,
        # it feels like too much parsing being done in the Scanner
        self.start = self.current

        self.docstring()

    def docstring(self) -> None:
        """Scan and match a docstring.

        A docstring is a short description of a key sequence. Currently this is just
        a description, which represents all matched characters after a doctag in
        a key sequence.
        """

        # Consume everything until the end of the line
        while not self.at_end:
            self.advance()

        # Trim leading and trailing whitespace, collect the rest
        docstring = self.sequence[self.start : self.current]
        self.add_token(TokenType.DOCSTRING, docstring.strip())

    def identifier(self) -> None:
        """Scan and match an alphanumeric "identifier".

        An identifier can either be a multi-character alphabetical keyword/modifier
        or a single alphanumeric character.

        Raises:
            ValueError: If more than one alphanumeric character was matched, and
                the matched text did not match any known identifier. Multi-character
                sequences must use plus separators ie f+o+o.
        """

        # Advance scanner to consume all alphanumeric chars, ie "ctrl" or "f1"
        while self.peek().isalnum():
            self.advance()

        # Retrieve substring of scanned alphabetical chars
        text = self.sequence[self.start : self.current]
        if modifier := getattr(ModifierType, text.upper(), None):
            # Add matched modifier token for this string
            # ie "ctrl" -> ModifierType.CTRL
            self.add_token(TokenType.MODIFIER, modifier)
        elif keyword := getattr(KeywordType, text.upper(), None):
            # Add matched keyword token for this string
            # ie "left" -> KeywordType.LEFT
            self.add_token(TokenType.KEYWORD, keyword)
        elif len(text) > 1:
            # A multiple character alphanumeric that does not match any identifier
            raise ValueError(f"Unknown multi-character identifier: {text}")
        else:
            # Single character alphanumeric token
            self.add_token(TokenType.PRIMARY, text)

    def scan_tokens(self) -> List[Token]:
        """Scan the input sequence and return all matched tokens.

        Returns:
            tokens: List[Token]. All matched tokens from the sequence.
        """

        while not self.at_end:
            # Scan and match tokens until the end of the sequence
            self.start = self.current
            self.scan_token()

        # Add end of signal token
        self.add_token(TokenType.EOF)

        # Return all matched tokens added from the input sequence
        return self.tokens
