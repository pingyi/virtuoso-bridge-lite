from __future__ import annotations

from virtuoso_bridge.virtuoso.schematic.ops import (
    schematic_create_net_expression,
    schematic_set_netset_property,
)


def test_schematic_create_net_expression_attaches_expression_to_net_wire() -> None:
    skill = schematic_create_net_expression(
        "VDD",
        "[@vdd:%:vdd!]",
        1.25,
        -0.5,
        justification="centerLeft",
        rotation="R90",
        font_style="stick",
        height=0.0625,
    )

    assert 'x~>net && x~>net~>name == "VDD"' in skill
    assert 'unless(rbWire error("wire for net not found"))' in skill
    assert (
        'schCreateNetExpression(cv "[@vdd:%:vdd!]" rbWire '
        '\'(1.250 -0.500) "centerLeft" "R90" "stick" 0.0625)'
    ) in skill


def test_schematic_create_net_expression_accepts_custom_cellview_expr() -> None:
    skill = schematic_create_net_expression(
        "VSS",
        "[@vss:%:gnd!]",
        0,
        0,
        cv_expr="targetCv",
    )

    assert "targetCv~>shapes" in skill
    assert 'schCreateNetExpression(targetCv "[@vss:%:gnd!]" rbWire' in skill


def test_schematic_set_netset_property_writes_inherited_override() -> None:
    skill = schematic_set_netset_property("XI0", "vdd", "VDD")

    assert 'x~>name == "XI0"' in skill
    assert 'unless(rbInst error("instance not found"))' in skill
    assert 'dbReplaceProp(rbInst "vdd" "netSet" "VDD")' in skill


def test_schematic_set_netset_property_escapes_string_literals() -> None:
    skill = schematic_set_netset_property('XI"0', "bulk\\net", 'VDD"TOP')

    assert 'x~>name == "XI\\"0"' in skill
    assert 'dbReplaceProp(rbInst "bulk\\\\net" "netSet" "VDD\\"TOP")' in skill
