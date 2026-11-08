from datetime import datetime

from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments


def make_appointment(
    appointment_id: str,
    practitioner: Practitioner,
    status: AppointmentStatus,
    date_time: datetime,
) -> Appointment:
    patient = Patient("P1", "Alex Example")

    return Appointment(
        appointment_id,
        patient,
        practitioner,
        date_time,
        status,
    )


def test_selects_only_requested_practitioner():
    d1 = Practitioner("D1", "Taylor Example", "General practice")
    d2 = Practitioner("D2", "Jordan Example", "Cardiology")

    a1 = make_appointment(
        "A1",
        d1,
        AppointmentStatus.SCHEDULED,
        datetime(2026, 10, 1, 9, 0),
    )

    a2 = make_appointment(
        "A2",
        d2,
        AppointmentStatus.SCHEDULED,
        datetime(2026, 10, 1, 10, 0),
    )

    result = select_appointments([a1, a2], "D1")

    assert result == [a1]


def test_status_filter_and_all_statuses():
    d1 = Practitioner("D1", "Taylor Example", "General practice")

    scheduled = make_appointment(
        "A1",
        d1,
        AppointmentStatus.SCHEDULED,
        datetime(2026, 10, 1, 9, 0),
    )

    cancelled = make_appointment(
        "A2",
        d1,
        AppointmentStatus.CANCELLED,
        datetime(2026, 10, 1, 10, 0),
    )

    all_results = select_appointments([scheduled, cancelled], "D1")

    cancelled_results = select_appointments(
        [scheduled, cancelled],
        "D1",
        AppointmentStatus.CANCELLED,
    )

    assert all_results == [scheduled, cancelled]
    assert cancelled_results == [cancelled]


def test_sorting_uses_datetime_then_appointment_id():
    d1 = Practitioner("D1", "Taylor Example", "General practice")

    later = make_appointment(
        "A3",
        d1,
        AppointmentStatus.CANCELLED,
        datetime(2026, 10, 1, 10, 0),
    )

    same_time_b = make_appointment(
        "B2",
        d1,
        AppointmentStatus.CANCELLED,
        datetime(2026, 10, 1, 9, 0),
    )

    same_time_a = make_appointment(
        "A1",
        d1,
        AppointmentStatus.COMPLETED,
        datetime(2026, 10, 1, 9, 0),
    )

    source = [later, same_time_b, same_time_a]

    result = select_appointments(source, "D1")

    assert result == [same_time_a, same_time_b, later]


def test_query_does_not_mutate_source_list():
    d1 = Practitioner("D1", "Taylor Example", "General practice")

    a1 = make_appointment(
        "A1",
        d1,
        AppointmentStatus.SCHEDULED,
        datetime(2026, 10, 1, 9, 0),
    )

    a2 = make_appointment(
        "A2",
        d1,
        AppointmentStatus.CANCELLED,
        datetime(2026, 10, 1, 8, 0),
    )

    source = [a1, a2]
    before = list(source)

    result = select_appointments(source, "D1")

    assert source == before
    assert result is not source


def test_no_matches_returns_new_empty_list():
    d1 = Practitioner("D1", "Taylor Example", "General practice")

    source = []

    result = select_appointments(source, "D1")

    assert result == []
    assert result is not source


def test_named_sort_key_returns_datetime_and_id():
    d1 = Practitioner("D1", "Taylor Example", "General practice")

    appointment = make_appointment(
        "A5",
        d1,
        AppointmentStatus.SCHEDULED,
        datetime(2026, 10, 1, 11, 30),
    )

    assert appointment_sort_key(appointment) == (
        datetime(2026, 10, 1, 11, 30),
        "A5",
    )