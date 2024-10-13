from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal

import pyparsing as pp

from configcalc.typing import Number


@dataclass
class Formatter:
    formatter: Callable[[str | Number], Number]
    parser: Callable[[], pp.ParserElement]


def decimal_parser() -> pp.ParserElement:
    def convert_to_decimal(token: pp.ParseResults) -> Decimal:
        return Decimal(str(token[0]))

    int_part = pp.Opt(pp.one_of("- +")) + pp.Word(pp.nums)
    mantissa = int_part + pp.Opt("." + pp.Opt(pp.Word(pp.nums)))
    exponent_part = pp.Opt(
        pp.one_of("e E") + pp.Opt(pp.one_of("- +")) + pp.Word(pp.nums)
    )
    number = pp.Combine(mantissa + exponent_part)
    number.set_parse_action(convert_to_decimal)
    return number


def regular_number_parser() -> pp.ParserElement:
    return pp.common.number


number_formatters = {
    "decimal": Formatter(formatter=Decimal, parser=decimal_parser),
    "float": Formatter(formatter=float, parser=regular_number_parser),
}


def var_name_parser() -> pp.ParserElement:
    dict_like_key = pp.Suppress(".") + pp.common.identifier
    list_like_index = pp.Suppress("[") + pp.common.integer + pp.Suppress("]")
    subvar_element = dict_like_key ^ list_like_index
    return pp.Group(pp.common.identifier + subvar_element[...], aslist=True)


def operator_operand_expr(
    number_parser: Callable[[], pp.ParserElement],
) -> pp.ParserElement:
    operator_operand = pp.Forward()
    number = number_parser()
    var_name = var_name_parser()
    function_struct = (
        pp.common.identifier + pp.Suppress("(") + operator_operand + pp.Suppress(")")
    )

    operand = function_struct | number | var_name
    operator_operand <<= pp.infix_notation(
        operand,
        [
            ("-", 1, pp.OpAssoc.RIGHT),
            ("^", 2, pp.OpAssoc.LEFT),
            (pp.one_of("* /"), 2, pp.OpAssoc.LEFT),
            (pp.one_of("+ -"), 2, pp.OpAssoc.LEFT),
        ],
    )
    return operator_operand


def build_operand_parser(
    number_parser: Callable[[], pp.ParserElement],
) -> pp.ParserElement:
    operator_operand = operator_operand_expr(number_parser)
    return pp.Suppress("=") + operator_operand
