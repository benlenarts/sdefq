"""Parse SDEF XML into model objects."""

import xml.etree.ElementTree as ET
from typing import List, Optional

from .models import (
    Class,
    Command,
    Dictionary,
    Element,
    EnumValue,
    Enumeration,
    Parameter,
    Property,
    Suite,
)


def parse_xml(xml_bytes: bytes, app_name: str = "", app_path: str = "") -> Dictionary:
    """Parse raw SDEF XML bytes into a Dictionary model."""
    root = ET.fromstring(xml_bytes)
    suites = [_parse_suite(el) for el in root.findall("suite")]
    return Dictionary(app_name=app_name, app_path=app_path, suites=suites)


def _parse_suite(el: ET.Element) -> Suite:
    commands = [_parse_command(c) for c in el.findall("command")]
    classes = [_parse_class(c) for c in el.findall("class")]
    # class-extension elements become Class with is_extension=True
    for ext in el.findall("class-extension"):
        classes.append(_parse_class_extension(ext))
    enumerations = [_parse_enumeration(e) for e in el.findall("enumeration")]
    return Suite(
        name=el.get("name", ""),
        code=el.get("code", ""),
        description=el.get("description", ""),
        commands=commands,
        classes=classes,
        enumerations=enumerations,
    )


def _parse_command(el: ET.Element) -> Command:
    # Direct parameter
    dp_el = el.find("direct-parameter")
    direct_parameter = None  # type: Optional[Parameter]
    if dp_el is not None:
        direct_parameter = Parameter(
            name="direct parameter",
            type=dp_el.get("type", dp_el.get("description", "")),
            description=dp_el.get("description", ""),
            optional=dp_el.get("optional", "no") == "yes",
        )

    # Named parameters
    parameters = []  # type: List[Parameter]
    for p in el.findall("parameter"):
        parameters.append(Parameter(
            name=p.get("name", ""),
            type=p.get("type", ""),
            description=p.get("description", ""),
            optional=p.get("optional", "no") == "yes",
        ))

    # Result
    result_el = el.find("result")
    result_type = None  # type: Optional[str]
    result_description = ""
    if result_el is not None:
        result_type = result_el.get("type", "")
        result_description = result_el.get("description", "")

    return Command(
        name=el.get("name", ""),
        code=el.get("code", ""),
        description=el.get("description", ""),
        direct_parameter=direct_parameter,
        parameters=parameters,
        result_type=result_type,
        result_description=result_description,
    )


def _parse_class(el: ET.Element) -> Class:
    properties = [_parse_property(p) for p in el.findall("property")]
    elements = [
        Element(type=e.get("type", ""), access=e.get("access", ""))
        for e in el.findall("element")
    ]
    responds_to = [r.get("command", "") for r in el.findall("responds-to")]
    return Class(
        name=el.get("name", ""),
        code=el.get("code", ""),
        description=el.get("description", ""),
        inherits=el.get("inherits"),
        plural=el.get("plural", ""),
        properties=properties,
        elements=elements,
        responds_to=responds_to,
        is_extension=False,
        extends=None,
    )


def _parse_class_extension(el: ET.Element) -> Class:
    properties = [_parse_property(p) for p in el.findall("property")]
    elements = [
        Element(type=e.get("type", ""), access=e.get("access", ""))
        for e in el.findall("element")
    ]
    responds_to = [r.get("command", "") for r in el.findall("responds-to")]
    extends = el.get("extends", "")
    return Class(
        name=extends,
        code=el.get("code", ""),
        description=el.get("description", ""),
        inherits=None,
        plural="",
        properties=properties,
        elements=elements,
        responds_to=responds_to,
        is_extension=True,
        extends=extends,
    )


def _parse_property(el: ET.Element) -> Property:
    access = el.get("access", "rw")
    return Property(
        name=el.get("name", ""),
        type=el.get("type", ""),
        access=access,
        description=el.get("description", ""),
    )


def _parse_enumeration(el: ET.Element) -> Enumeration:
    values = []  # type: List[EnumValue]
    for v in el.findall("enumerator"):
        values.append(EnumValue(
            name=v.get("name", ""),
            code=v.get("code", ""),
            description=v.get("description", ""),
        ))
    return Enumeration(
        name=el.get("name", ""),
        code=el.get("code", ""),
        values=values,
    )
