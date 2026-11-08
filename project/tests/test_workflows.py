from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_services():
    store = SmartCareDataStore()

    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient_service.register_patient("P1", "Alex Example")

    practitioner_service.register_practitioner(
        "D1",
        "Taylor Example",
        "General practice",
    )

    practitioner_service.register_practitioner(
        "D2",
        "Jordan Example",
        "Cardiology",
    )

    return appointment_service


def test_list_practitioner_appointments_returns_correct_practitioner():
    appointments = make_services()

    a1 = appointments.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9, 0),
    )

    appointments.book_appointment(
        "A2",
        "P1",
        "D2",
        datetime(2026, 10, 1, 9, 0),
    )

    result = appointments.list_practitioner_appointments("D1")

    assert result == [a1]


def test_known_practitioner_with_no_matches_returns_empty_list():
    appointments = make_services()

    result = appointments.list_practitioner_appointments("D1")

    assert result == []


def test_unknown_practitioner_raises_lookup_error():
    appointments = make_services()

    with pytest.raises(LookupError):
        appointments.list_practitioner_appointments("D999")


def test_blank_practitioner_id_raises_value_error():
    appointments = make_services()

    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments("   ")


def test_invalid_status_raises_value_error():
    appointments = make_services()

    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments(
            "D1",
            "scheduled",
        )


def test_default_status_includes_cancelled_appointments():
    appointments = make_services()

    appointment = appointments.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9, 0),
    )

    appointments.cancel_appointment("A1")

    result = appointments.list_practitioner_appointments("D1")

    assert result == [appointment]
    assert result[0].status is AppointmentStatus.CANCELLED