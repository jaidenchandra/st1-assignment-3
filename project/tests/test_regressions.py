from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_f8_01_conflict_rejection_preserves_store():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    service = AppointmentService(store)

    patients.register_patient("P1", "Synthetic Patient")
    practitioners.register_practitioner("D1", "Practitioner One", "GP")
    practitioners.register_practitioner("D2", "Practitioner Two", "GP")

    when = datetime(2026, 10, 1, 9)
    first = service.book_appointment("A1", "P1", "D1", when)
    before = store.list_appointments()

    with pytest.raises(ValueError):
        service.book_appointment("A2", "P1", "D1", when)

    assert store.list_appointments() == before
    assert store.find_appointment("A1") is first
    assert store.find_appointment("A2") is None
    assert first.status == AppointmentStatus.SCHEDULED

    other = service.book_appointment("A3", "P1", "D2", when)

    assert other.practitioner.practitioner_id == "D2"
    assert store.find_appointment("A3") is other
    assert store.list_appointments() == [first, other]


def test_f8_02_cancelled_history_and_guard_preserve_store():
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    service = AppointmentService(store)

    patients.register_patient("P1", "Synthetic Patient")
    practitioners.register_practitioner("D1", "Practitioner One", "GP")

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    assert service.cancel_appointment("A1") is appointment
    assert appointment.status == AppointmentStatus.CANCELLED
    assert store.list_appointments() == [appointment]
    assert store.find_appointment("A1") is appointment
    assert service.find_appointment("A1") is appointment

    before = store.list_appointments()
    original_fields = (
        appointment.appointment_id,
        appointment.patient,
        appointment.practitioner,
        appointment.date_time,
        appointment.status,
    )

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert store.list_appointments() == before
    assert store.find_appointment("A1") is appointment
    assert service.find_appointment("A1") is appointment
    assert (
        appointment.appointment_id,
        appointment.patient,
        appointment.practitioner,
        appointment.date_time,
        appointment.status,
    ) == original_fields