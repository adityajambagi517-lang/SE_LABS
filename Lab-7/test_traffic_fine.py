from hypothesis import given, strategies as st
from traffic_fine import (
    parse_ticket_id,
    total_fines,
    speed_excess
)


@given(st.one_of(st.text(), st.none()))
def test_parse_ticket_id_no_crash(ticket_id):
    parse_ticket_id(ticket_id)


@given(st.one_of(st.text(), st.none()))
def test_total_fines_no_crash(amounts):
    total_fines(amounts)


@given(st.one_of(st.text(), st.none()))
def test_speed_excess_no_crash(reading):
    speed_excess(reading)
