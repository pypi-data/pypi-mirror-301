#!/usr/bin/env python3
from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractclassmethod
from curses.ascii import ctrl, alt
from typing import Any, cast, List, Iterator, Optional, Union, TYPE_CHECKING, NoReturn

from pyre_extensions import none_throws

if TYPE_CHECKING:
    from keyslib.visitor import Visitor

from keyslib.exceptions import ParserError
from keyslib.types import KeywordType, ModifierType
from keyslib.scanner import Scanner, Token, TokenType
from keyslib.printer import Printer

# Current expression grammar:
# expression   -> key_sequence ;
# key_sequence -> combo ( "+" key_sequence )* ;
# combo        -> ( "(" mask ")" ) key ;
# mask         -> modifier ( "|" modifier )* ;
# modifier     -> CTRL | ALT | CMD | SHIFT ;
# key          -> primary | "<" keyword ">"
# keyword      -> LEFT | RIGHT | UP | DOWN... ;
# primary      -> NUMBER | LETTER ;
#
# Current statement grammar:
# program      -> bind* EOF ;
# bind         -> identifier "=" "'" expression ( "#" doctag ) "'" ;
# doctag       -> identifier ( docstring ) ;
# docstring    -> * EOL ;


class Expr(metaclass=ABCMeta):
    """Key expression base class.

    An expression represents any matched component of a key sequence returned
    by the Parser. It has associated code for parsing from Tokens returned by
    the Scanner and being formatted as a string sequence via the Printer, which
    are also used for hashing and comparison.

    Expressions can be instantiated either by value through keyword arguments:
    keys = KeySequence(
        combo=Combo(
            "(ctrl|shift|alt|cmd)b",
        ),
        key_sequence=KeySequence(
            combo=Combo("(ctrl)<left>"),
            key_sequence=KeySequence(combo=Combo("(cmd|alt)c")),
        ),
    )

    Or by passing in a single string representing the sequence:
    keys = KeySequence("(ctrl|shift|alt|cmd)b+(ctrl)<left>+(cmd|alt)c")

    combo = Combo("(ctrl|shift|alt|cmd)b")

    Similar to pathlib, expressions and strings can be mixed and matched:
    (Mask("ctrl") / "shift" / "alt" / "cmd") * Combo("b") == combo

    KeySequence("(ctrl|shift|alt|cmd)b") + "(ctrl)<left>" + "(cmd|alt)c" == keys
    """

    def __new__(cls, sequence: Optional[str] = None, *args: Any, **kwargs: Any) -> Expr:
        """Create a new instance of an expression.

        Given a sequence, this will call the expression class' from_str method
        to parse and return an instance. Otherwise, it will create it as normal
        and initialization will happen by keyword value in the expression's
        __init__.

        Args:
            sequence: Optional[str]. Text sequence to parse as an expression.

        Returns:
            expr: Expr. Expression instance.
        """

        if sequence is not None:
            # Parse provided string sequence as expression and return it
            return cls.from_str(sequence)
        else:
            # Return a fresh expression instance as normal
            return super().__new__(cls)

    @abstractclassmethod
    def from_str(cls, sequence: str) -> Expr:
        """Parse an Expression from a text sequence.

        Args:
            sequence: str. Text sequence to be parsed.

        Returns:
            parsed_expr: Expr. Parsed expression from sequence.
        """

        raise NotImplementedError()

    def to_str(self) -> str:
        """Return the text representation of this expression.

        This uses the Key Printer to convert the sequence for this Expr into
        text.

        Returns:
            text_expr: str. Text representation of this expression.
        """

        return Printer().accept(self)

    def __repr__(self) -> str:
        return self.to_str()

    def __hash__(self) -> int:
        return hash(self.to_str())

    def __eq__(self, other: Union[str, Expr]) -> bool:
        if isinstance(other, str):
            other = self.from_str(other)

        return self.to_str() == other.to_str()

    @abstractmethod
    def accept(self, visitor: Visitor) -> str: ...


class Primary(Expr):
    """A primary key expression.

    A primary key is any key that is a single unicode character and is otherwise
    unreserved by other expressions. For all other key types, Keyword is used.

    Primary(value="b") == "b"
    Prinary(",") == ","

    Args:
        sequence: Optional[str]. Text representation of the primary.
        value: Optional[str]. The character represented by this primary expression.
    """

    def __init__(
        self, sequence: Optional[str] = None, *, value: Optional[str] = None
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.value: str = none_throws(value)

    @classmethod
    def from_str(cls, sequence: str) -> Primary:
        return Parser.parse_primary(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_primary(self)

    def unicode(self) -> int:
        """Get the unicode code point for this character as an integer.

        Returns:
            code_point: int. Unicode code point for this character.
        """

        return ord(self.value)


class Keyword(Expr):
    """A keyword expression.

    A keyword is any "named" key that cannot be represented easily with
    a single alphanumeric character. These are represented by the KeywordType enum,
    and are enclosed in <> symbols to distinguish them from primary keys.

    Keyword("<left>") == "<left>"
    Keyword(value=KeywordType.UP) == "<up>"

    Args:
        sequence: Optional[str]. Text representation of keyword.
        value: Optional[KeywordType]. The keyword represented by this expression,
            when instantiated by-value.

    Public Attributes:
        value: KeywordType. The keyword type represented by this expression.
    """

    def __init__(
        self, sequence: Optional[str] = None, *, value: Optional[KeywordType] = None
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.value: KeywordType = none_throws(value)

    @classmethod
    def from_str(cls, sequence: str) -> Keyword:
        return Parser.parse_keyword(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_keyword(self)

    def unicode(self) -> int:
        # Print hex codes:
        # import sys
        # import tty
        # tty.setcbreak(sys.stdin)
        # while True:
        #     print(ord(hex(sys.stdin.read(1))))

        match self.value:
            # Single character ASCII sequences
            case KeywordType.SPACE:
                return 0x20
            case KeywordType.BACKSPACE:
                return 0x08
            case KeywordType.TAB:
                return 0x09
            case KeywordType.DELETE:
                return 0x7F
            case KeywordType.ENTER:
                return 0x0A
            case KeywordType.ESCAPE:
                return 0x1B
            case KeywordType.QUOTE:
                return 0x22
            case KeywordType.HASH:
                return 0x23
            case _:
                raise ValueError(f"Unsupported unicode keyword: {self.value.name}")


class Key(Expr):
    """A key expression.

    A key expression is a container which can hold either a primary key or a
    keyword:

    Key("b") == "b"
    Key(value=Keyword(value="<left>")) == "<left>"

    Args:
        sequence: Optional[str]. Text representation of keyword.
        value: Optional[KeywordType]. The keyword represented by this expression,
            when instantiated by-value.

    Public Attributes:
        value: KeywordType. The keyword type represented by this expression.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        value: Optional[Union[Primary, Keyword]] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.value: Union[Primary, Keyword] = none_throws(value)

    @classmethod
    def from_str(cls, sequence: str) -> Key:
        return Parser.parse_key(sequence)

    def accept(self, visitor: Visitor) -> str:
        return self.value.accept(visitor)

    def __rmul__(self, mask: Union[str, Mask]) -> Combo:
        if not isinstance(mask, Mask):
            mask = Mask.from_str(mask)

        return Combo(key=self, mask=mask)

    def unicode(self) -> int:
        return self.value.unicode()


class Modifier(Expr):
    """A modifier expression.

    A modifier is any named key that modifies other keys in an expression:

    Modifier("ctrl") == "ctrl"
    Modifier(value=ModifierType.ALT) == "alt"

    Modifiers are used in Mask expressions to generate key Combos.

    Args:
        sequence: Optional[str]. Text representation of modifier.
        value: Optional[ModifierType]. The modifier represented by this expression,
            when instantiated by-value.

    Public Attributes:
        value: ModifierType. The modifier type represented by this expression.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        value: Optional[ModifierType] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.value: ModifierType = none_throws(value)

    @classmethod
    def from_str(cls, sequence: str) -> Modifier:
        return Parser.parse_modifier(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_modifier(self)


class Mask(Expr):
    """A mask expression.

    A mask is a combination of modifier keys which modify a key expression:

    Mask("ctrl|alt") == "ctrl|alt"
    Mask(
        modifier=Modifier(
            value=ModifierType.CMD
        ),
        mask=Mask(modifier=Modifier(value=ModifierType.SHIFT)),
    ) == "cmd|shift"

    Masks can be combined with other Masks or strings via division, similar to
    pathlib:

    Mask("ctrl") / "alt" / "shift" == "ctrl|alt|shift"

    Args:
        sequence: Optional[str]. Text representation of mask.
        modifier: Optional[Modifier]. The modifier for this mask, when instantiated
            by-value.
        mask: Optional[Mask]. Any additional Masks representing additional modifiers.

    Public Attributes:
        modifier: Modifier. The modifier for this mask.
        mask: Optional[Mask]. Any additional Masks representing additional modifiers.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        modifier: Optional[Modifier] = None,
        mask: Optional[Mask] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.modifier: Modifier = none_throws(modifier)
        self.mask = mask

    @classmethod
    def from_str(cls, sequence: str) -> Mask:
        return Parser.parse_mask(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_mask(self)

    def __iter__(self) -> Iterator[Modifier]:
        yield self.modifier

        if self.mask:
            yield from self.mask

    def __truediv__(self, mask: Union[str, Mask]) -> Mask:
        if not isinstance(mask, Mask):
            mask = Mask.from_str(mask)

        if self.mask is not None:
            return Mask(modifier=self.modifier, mask=self.mask / mask)
        else:
            return Mask(modifier=self.modifier, mask=mask)

    # TODO: Move this into the unicode formatter instead
    def unicode_mask(self, code_point: int) -> int:
        for modifier in self:
            match modifier.value:
                case ModifierType.CTRL:
                    code_point = ctrl(code_point)
                case ModifierType.ALT:
                    code_point = alt(code_point)
                case ModifierType.SHIFT:
                    # TODO: The SHIFT modifier needs to be handled contextually
                    # since it would be ord(<previous char>.toupper())
                    raise NotImplementedError("SHIFT modifier not implemented")
                case _:
                    raise ValueError(
                        f"Unable to apply mask for modifier type: {modifier}"
                    )

        return code_point


class Combo(Expr):
    """A combo expression.

    A combo is any key expression with an optional mask applied:

    Combo("(ctrl|alt)b") == "(ctrl|alt)b"
    Combo(
        key=Key(value=Keyword(value=KeywordType.LEFT)),
        mask=Mask(modifier=Modifier(value=ModifierType.SHIFT)),
    ) == "(shift)<left>"

    Masks can be applied to Keys to yield Combos via right multiplication:
    (Mask("ctrl") / "alt") * Key("b") == Combo("(ctrl|alt)b")

    They can also be applied to Combos to overwrite any existing mask:
    (Mask("ctrl") / "alt") * Combo("(cmd)b") == Combo("(ctrl|alt)b")

    Args:
        sequence: Optional[str]. Text representation of mask.
        key: Optional[Key]. The key for this Combo, when instantiated by-value.
        mask: Optional[Mask]. The mask for this Combo, if any.

    Public Attributes:
        key: Key. The key for this Combo.
        mask: Optional[Mask]. The mask for this Combo, if any.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        key: Optional[Key] = None,
        mask: Optional[Mask] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.key: Key = none_throws(key)
        self.mask = mask

    @classmethod
    def from_str(cls, sequence: str) -> Combo:
        return Parser.parse_combo(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_combo(self)

    def __rmul__(self, mask: Union[str, Mask]) -> Combo:
        if not isinstance(mask, Mask):
            mask = Mask.from_str(mask)

        return Combo(key=self.key, mask=mask)

    def unicode(self) -> int:
        code_point = self.key.unicode()

        if self.mask:
            code_point = self.mask.unicode_mask(code_point)

        return code_point


class KeySequence(Expr):
    """A key sequence expression.

    A key sequence represents one or more key combos:

    KeySequence("(ctrl|alt)c+b") == "(ctrl|alt)c+b"
    KeySequence(
        combo=Combo(
            key=Key(value=Primary("b")),
            mask=Mask(modifier=Modifier(value=ModifierType.CTRL)),
        ),
        key_sequence=KeySequence(
            combo=Combo(key=Key(value=Primary("c"))),
        ),
    ) = "(ctrl)b+c"

    Key sequences can be added together:
    KeySequence("(ctrl)b") + "c" == "(ctrl)b+c"

    Key sequences can also have doctags for additional metadata:
    KeySequence("(ctrl)b") + "c #editor Create window" == "(ctrl)b+c # Create window"

    Args:
        sequence: Optional[str]. Text representation of key sequence.
        combo: Optional[Combo]. The combo for this key sequence, when instantiated
            by-value.
        key_sequence: Optional[KeySequence]. Additional key sequence, if any.
        doctag: Optional[Doctag]. A doctag attached to this key sequence,
            if any.

    Public Attributes:
        combo: Combo. The combo for this key sequence.
        key_sequence: Optional[KeySequence]. Additional key sequence, if any.
        doctag: Optional[Doctag]. A docstring attached to this key sequence,
            if any.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        combo: Optional[Combo] = None,
        key_sequence: Optional[KeySequence] = None,
        doctag: Optional[Doctag] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.combo: Combo = none_throws(combo)
        self.key_sequence = key_sequence

        # TODO: This works for now, but it does mean that the docstring is
        # unnecessarily nested within the sequence.
        self.doctag = doctag

    @classmethod
    def from_str(cls, sequence: str) -> KeySequence:
        return Parser.parse_key_sequence(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_key_sequence(self)

    def __iter__(self) -> Iterator[KeySequence]:
        yield self

        if self.key_sequence:
            yield from self.key_sequence

    def __add__(self, key_sequence: Union[str, KeySequence]) -> KeySequence:
        if not isinstance(key_sequence, KeySequence):
            key_sequence = KeySequence.from_str(key_sequence)

        if self.key_sequence is not None:
            return KeySequence(
                combo=self.combo, key_sequence=self.key_sequence + key_sequence
            )
        else:
            return KeySequence(combo=self.combo, key_sequence=key_sequence)

    def unicode(self) -> Iterator[int]:
        for key_sequence in self:
            yield key_sequence.combo.unicode()

    @property
    def doc(self) -> Optional[Doctag]:
        # TODO: See __init__
        return list(self)[-1].doctag


class Doctag(Expr):
    """A doctag expression.

    A doctag represents the beginning of any additional metadata about a key
    sequence. It consists of a # (<hash>) symbol, an optional group name, and an
    optional Docstring, which describes the key sequence:

    Doctag("#window Create window") == "# Create window"
    Doctag(group="window", docstring=Docstring(description="Create window"))
        == "# Create window"

    If no group is provided, the command will be assigned the default group.

    Args:
        sequence: Optional[str]. Text representation of doctag.
        group: Optional[str]. Group this key sequence belongs to, this is the
            "default" group if not provided.
        docstring: Optional[Docstring]. Docstring for this doctag, if any.

    Public Attributes:
        group: str. Group this key sequence belongs to.
        docstring: Optional[Docstring]. Docstring for this doctag, if any.
    """

    DEFAULT_GROUP: str = "default"

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        group: Optional[str] = None,
        docstring: Optional[Docstring] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.group: str = group if group else Doctag.DEFAULT_GROUP
        self.docstring: Optional[Docstring] = docstring

    @classmethod
    def from_str(cls, sequence: str) -> Doctag:
        return Parser.parse_doctag(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_doctag(self)


class Docstring(Expr):
    """A docstring expression.

    A docstring is a short description of a key sequence. Currently this is just
    a description, which represents all matched characters after a doctag in
    a key sequence:

    Docstring("# Create window") == "# Create window"
    Docstring(description="Create window") == "# Create window"

    Args:
        sequence: Optional[str]. Text representation of docstring.
        description: Optional[str]. Docstring description, when instantiated by-value.

    Public Attributes:
        description: str. Docstring description.
    """

    def __init__(
        self,
        sequence: Optional[str] = None,
        *,
        description: Optional[str] = None,
    ) -> None:
        if sequence is not None:
            # Expression was initialized by text sequence.
            return

        self.description: str = none_throws(description)

    @classmethod
    def from_str(cls, sequence: str) -> Docstring:
        return Parser.parse_docstring(sequence)

    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_docstring(self)


class Parser:
    """Key parser class.

    This class processes a set of Tokens provided by the Scanner and generates
    key sequence expression(s) and their components.

    Args:
        tokens: List[Token]. Tokens to process, typically generated from the Scanner
            against a sequence text.

    Public Attributes:
        current: int. Current token index of the key parser.
    """

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    @property
    def at_end(self) -> bool:
        """Check if Parser's current position is at the end of the token list (EOF).

        Returns:
            at_end: bool. Whether or not the Parser has reached the end of the
                sequence.
        """

        return self.peek().type is TokenType.EOF

    def advance(self) -> Token:
        """Retrieve the token at the Parser's current position, then advance it.

        Returns:
            token: Token. Token at the Parser's position prior to advancement.
        """

        token = self.tokens[self.current]
        if not self.at_end:
            self.current += 1

        return token

    def peek(self) -> Token:
        """Return the token at the current index without consuming it.

        Returns:
            current_token: Token. Token at the current index.
        """

        return self.tokens[self.current]

    def check(self, ttype: TokenType) -> bool:
        """Check if the current Token is of a given type.

        Args:
            ttype: TokenType. Token type to check current token against.

        Returns:
            is_type: bool. Whether or not the Parser's current token matches the
                given type.
        """

        if self.at_end:
            return False

        return self.peek().type is ttype

    def match(self, *args: TokenType) -> bool:
        """Check if current token is a given type and advance.

        If the token does not match the given types, the Parser will not advance.

        Args:
            *ttype: TokenType. Token type(s) to check for.

        Returns:
            is_match: bool. Whether or not the Parser's current token matches
                any of the given ttypes.
        """

        for ttype in args:
            if self.check(ttype):
                self.advance()
                return True

        return False

    def consume(self, ttype: TokenType, error_message: str) -> Token:
        """Ensure the current token is of a given type, and consume it.

        Args:
            ttype: TokenType. Token type to check for.
            error_message: str. Error message if no match.

        Returns:
            token: Token. The consumed token of the provided ttype.

        Raises:
            ValueError: If the Parser's current token is not of the provided ttype.
        """

        if self.check(ttype):
            return self.advance()

        raise ValueError(error_message)

    def expression(self) -> Expr:
        return self.key_sequence()

    def doctag(self) -> Doctag:
        # Consume doctag as group
        # TODO: Maybe consider allowing multiple key-value doctags ie:
        # #editor #debug:true #hidden:true -> {"group": "editor", "debug": True
        #    "hidden": True}
        doctag = self.consume(TokenType.DOCTAG, "Doctag expected")
        group = cast(str, doctag.value)

        if self.check(TokenType.DOCSTRING):
            # Parse docstring for this doctag
            docstring = self.docstring()
        else:
            docstring = None

        # Remove leading spaces after # (<hash>) and parse the rest as the
        # docstring description
        return Doctag(group=group, docstring=docstring)

    def docstring(self) -> Docstring:
        docstring = self.consume(TokenType.DOCSTRING, "Docstring expected")

        # Remove leading spaces after # (<hash>) and parse the rest as the
        # docstring description
        return Docstring(description=cast(str, docstring.value))

    def key_sequence(self) -> KeySequence:
        combo = self.combo()

        if self.match(TokenType.PLUS):
            sequence = self.key_sequence()
            expr = KeySequence(combo=combo, key_sequence=sequence)
        else:
            expr = KeySequence(combo=combo, key_sequence=None)

        if self.check(TokenType.DOCTAG):
            # Parse provided doctag for this sequence
            expr.doctag = self.doctag()

        return expr

    def combo(self) -> Combo:
        if self.match(TokenType.LEFT_PAREN):
            mask = self.mask()
            self.consume(TokenType.RIGHT_PAREN, ") expected")
        else:
            mask = None

        key = self.key()

        return Combo(key=key, mask=mask)

    def mask(self) -> Mask:
        left = self.modifier()

        if self.match(TokenType.PIPE):
            right = self.mask()
            expr = Mask(modifier=left, mask=right)
        else:
            expr = Mask(modifier=left, mask=None)

        return expr

    def modifier(self) -> Modifier:
        mod_token = self.consume(TokenType.MODIFIER, "modifier expected")

        return Modifier(value=cast(ModifierType, mod_token.value))

    def key(self) -> Key:
        if self.check(TokenType.LESS_THAN):
            keyword = self.keyword()

            return Key(value=keyword)
        else:
            primary = self.primary()

            return Key(value=primary)

    def keyword(self) -> Keyword:
        self.consume(TokenType.LESS_THAN, "< expected")
        keyword_token = self.consume(TokenType.KEYWORD, "keyword expected")
        self.consume(TokenType.GREATER_THAN, "> expected")

        return Keyword(value=cast(KeywordType, keyword_token.value))

    def primary(self) -> Primary:
        primary = self.consume(TokenType.PRIMARY, "primary key expected")

        return Primary(value=cast(str, primary.value))

    @staticmethod
    def _handle_error(sequence: str, exception: Exception) -> NoReturn:
        raise ParserError(f"Error parsing sequence '{sequence}': {str(exception)}")

    @staticmethod
    def parse_doctag(sequence: str) -> Doctag:
        try:
            return Parser(Scanner.scan(sequence)).doctag()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_docstring(sequence: str) -> Docstring:
        try:
            return Parser(Scanner.scan(sequence)).docstring()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_key_sequence(sequence: str) -> KeySequence:
        try:
            return Parser(Scanner.scan(sequence)).key_sequence()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_combo(sequence: str) -> Combo:
        try:
            return Parser(Scanner.scan(sequence)).combo()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_mask(sequence: str) -> Mask:
        try:
            return Parser(Scanner.scan(sequence)).mask()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_modifier(sequence: str) -> Modifier:
        try:
            return Parser(Scanner.scan(sequence)).modifier()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_key(sequence: str) -> Key:
        try:
            return Parser(Scanner.scan(sequence)).key()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_keyword(sequence: str) -> Keyword:
        try:
            return Parser(Scanner.scan(sequence)).keyword()
        except Exception as e:
            Parser._handle_error(sequence, e)

    @staticmethod
    def parse_primary(sequence: str) -> Primary:
        try:
            return Parser(Scanner.scan(sequence)).primary()
        except Exception as e:
            Parser._handle_error(sequence, e)
