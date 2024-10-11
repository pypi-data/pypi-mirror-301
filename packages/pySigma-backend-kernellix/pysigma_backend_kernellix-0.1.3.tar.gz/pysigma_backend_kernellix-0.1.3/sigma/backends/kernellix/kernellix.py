import re
import json
from typing import Iterable, ClassVar, Dict, List, Optional, Pattern, Tuple, Union, Any

from sigma.conversion.state import ConversionState
from sigma.rule import SigmaRule, SigmaRuleTag
from sigma.conversion.base import TextQueryBackend
from sigma.conversion.deferred import DeferredQueryExpression
from sigma.conditions import (
    ConditionItem,
    ConditionAND,
    ConditionOR,
    ConditionNOT,
    ConditionFieldEqualsValueExpression,
)
from sigma.types import SigmaCompareExpression, SigmaNull, SpecialChars, SigmaNumber
from sigma.data.mitre_attack import mitre_attack_tactics, mitre_attack_techniques

class kernellixBackend(TextQueryBackend):
    name : ClassVar[str] = "kernellix backend"
    formats : Dict[str, str] = {
        "default": "Plain kernellix queries",
        "siem_rule": "VQL Queries to used in data pipline"
        
    }
    # Does the backend requires that a processing pipeline is provided?
    requires_pipeline: ClassVar[bool] = True

    # Operator precedence: tuple of Condition{AND,OR,NOT} in order of precedence.
    # The backend generates grouping if required
    precedence: ClassVar[Tuple[ConditionItem, ConditionItem, ConditionItem]] = (
        ConditionNOT,
        ConditionOR,
        ConditionAND,
    )
    group_expression : ClassVar[str] = "({expr})"
    parenthesize : bool = True

    # Generated query tokens
    token_separator : str = " "    
    or_token : ClassVar[str] =  "or"  #"||"
    and_token : ClassVar[str] = "and" #"&&"
    not_token : ClassVar[str] = "not"
    eq_token : ClassVar[str] = "=="
    not_eq_token: ClassVar[str] = "!="
    field_quote : ClassVar[str] = "" 
    field_quote_pattern : ClassVar[Pattern] = re.compile("^w+$")
    field_quote_pattern_negation : ClassVar[bool] = False 

    ### Escaping
    field_escape_quote : ClassVar[bool] = False
    #field_escape_pattern : ClassVar[Pattern] = re.compile("s")

    ## Values
    str_quote       : ClassVar[str] = '"'     # string quoting character (added as escaping character)
    # wildcard_multi  : ClassVar[str] = "*"     # Character used as multi-character wildcard
    # wildcard_single : ClassVar[str] = "*"     # Character used as single-character wildcard
    bool_values     : ClassVar[Dict[bool, str]] = {   # Values to which boolean values are mapped.
        True: "true",
        False: "false",
    }

    retrieve_expression : str = "record.deepget"
    # String matching operators. if none is appropriate eq_token is used.
    startswith_expression : ClassVar[str] = 'record.deepget("{field}").startswith({value})'
    endswith_expression   : ClassVar[str] = 'record.deepget("{field}").endswith({value})'
    contains_expression   : ClassVar[str] = '{value} in record.deepget("{field}")'
    cmdeq_expression      : ClassVar[str] = 'record.deepget("{field}").cmdeq({value})'
    # wildcard_match_expression : ClassVar[str] = "{field} match {value}"







    #cidr_expression : ClassVar[Optional[str]] = None  
    # Numeric comparison operators
    compare_op_expression : ClassVar[str] = "{field}{operator}{value}" 
    # Mapping between CompareOperators elements and strings used as replacement for {operator} in compare_op_expression
    compare_operators : ClassVar[Dict[SigmaCompareExpression.CompareOperators, str]] = {
        SigmaCompareExpression.CompareOperators.LT  : "<",
        SigmaCompareExpression.CompareOperators.LTE : "<=",
        SigmaCompareExpression.CompareOperators.GT  : ">",
        SigmaCompareExpression.CompareOperators.GTE : ">=",
    }

    # Expression for comparing two event fields
    field_equals_field_expression : ClassVar[Optional[str]] = None 
    field_equals_field_escaping_quoting : Tuple[bool, bool] = (True, True)   

    # Null/None expressions
    field_null_expression : ClassVar[str] = "record.deepget({field}) is None" 

    # Field existence condition expressions.
    field_exists_expression : ClassVar[str] = "exists({field})"
    convert_or_as_in : ClassVar[bool] = False                     # Convert OR as in-expression
    convert_and_as_in : ClassVar[bool] = False                    # Convert AND as in-expression
    field_in_list_expression : ClassVar[str] = "{op}({field},({list}))"  # Expression for field in list of values as format string with placeholders {field}, {op} and {list}
    or_in_operator : ClassVar[str] = "includes"               # Operator used to convert OR into in-expressions. Must be set if convert_or_as_in is set
    and_in_operator : ClassVar[str] = "contains-all"    # Operator used to convert AND into in-expressions. Must be set if convert_and_as_in is set
    list_separator : ClassVar[str] = ", "               # List element separator

    # Value not bound to a field
    unbound_value_str_expression : ClassVar[str] = '"{value}"'
    unbound_value_num_expression : ClassVar[str] = '{value}'
    unbound_value_re_expression : ClassVar[str] = '_=~{value}'

    def finalize_query_default(
        self, rule: SigmaRule, query: str, index: int, state: ConversionState
    ) -> str:
        return f"{query}"

    def finalize_output_default(self, queries: List[str]) -> Any:
        return list(queries)

    def finalize_query_siem_rule(
        self, rule: SigmaRule, query: str, index: int, state: ConversionState
    ) -> str:
        """
        Generation of Kernellix Security Platform Detection Rules.
        """
        query = extract_string(query)
        siem_rule = f"""def detect(record):\n  return (\n    {query}\n  )"""
        siem_rule = siem_rule.replace(r'\n', '\n')
        siem_rule = siem_rule.replace(r'\"', '"').replace(r"\'", "'")

        #print (extract_string(query))

        return siem_rule
        
    def finalize_output_siem_rule(self, queries: List[Dict]) -> List[Dict]:
        return list(queries)
    
def extract_string(var):
    ret=var + ""
    idx=var.find("==")
    if idx==-1:
        return var
    
    #print(get_extract_func("hellow","world"))

    fdx=var[0:idx].rfind("(")
    sdx=var[0:idx].rfind(" ")

    if fdx!=-1 or sdx!=-1:
        if fdx>sdx:
            #print(var[0:fdx+1] + get_extract_func("record.deepget",str(var[fdx+1:idx])))
            return (var[0:fdx+1] + get_extract_func("record.deepget",str(var[fdx+1:idx])))+ " == "   + extract_string(var[idx+2:])
        #print(var[0:sdx+1] + get_extract_func("record.deepget",var[sdx+1:idx]))
        return (var[0:sdx+1] + get_extract_func("record.deepget",var[sdx+1:idx]))+ " == "  + extract_string(var[idx+2:])
    #print(var[:idx])
    return (get_extract_func("record.deepget",var[:idx])) + " == " + extract_string(var[idx+2:]) 

def get_extract_func(function_str,field_name):
    return(f'{function_str}("{field_name}")')
    