"""Checks for the SmartCare foundation and completed service workflows."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation() -> tuple[
    SmartCareDataStore,
    Patient,
    Practitioner,
    AppointmentService,
]:
    """Create fresh registered participants and services for a supplied check."""
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    return (data_store, patient, practitioner, AppointmentService(data_store))


def test_required_fields() -> None:
    """Verify required fields."""
    with pytest.raises(ValueError):
        Patient(' ', 'Alex Example')
    with pytest.raises(ValueError):
        Practitioner('D1', 'Taylor Example', '')


def test_registration_and_booking() -> None:
    """Verify registration and booking."""
    data_store, patient, practitioner, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )
    assert appointment_service.find_appointment('A1') is appointment
    assert appointment.patient is patient and appointment.practitioner is practitioner
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


def test_duplicate_patient_preserves_original() -> None:
    """Verify duplicate patient preserves original."""
    data_store, patient, _, _ = foundation()
    with pytest.raises(ValueError):
        PatientService(data_store).register_patient('P1', 'Replacement')
    assert data_store.find_patient('P1') is patient
    assert patient.name == 'Alex Example'


def test_duplicate_practitioner_preserves_original() -> None:
    """Verify duplicate practitioner preserves original."""
    data_store, _, practitioner, _ = foundation()
    with pytest.raises(ValueError):
        PractitionerService(data_store).register_practitioner('D1', 'Replacement', 'Other')
    assert data_store.find_practitioner('D1') is practitioner
    assert practitioner.name == 'Taylor Example'


def test_duplicate_appointment_preserves_original() -> None:
    """Verify duplicate appointment preserves original."""
    data_store, _, _, appointment_service = foundation()
    original = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            'A1', 'P1', 'D1', datetime(2026, 10, 1, 10)
        )
    assert data_store.list_appointments() == [original]
    assert original.date_time == datetime(2026, 10, 1, 9)


def test_unregistered_participants_rejected() -> None:
    """Verify unregistered participants rejected."""
    data_store, patient, practitioner, appointment_service = foundation()
    with pytest.raises(LookupError):
        appointment_service.book_appointment(
            'A1', 'missing', 'D1', datetime(2026, 10, 1, 9)
        )
    impostor = Patient('P1', 'Unregistered')
    with pytest.raises(ValueError):
