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
    """Create fresh registered participants and services for a supplied
    check.
    """
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(
        data_store,
    ).register_practitioner('D1', 'Taylor Example', 'General')
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
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
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
        PractitionerService(
            data_store,
        ).register_practitioner('D1', 'Replacement', 'Other')
    assert data_store.find_practitioner('D1') is practitioner
    assert practitioner.name == 'Taylor Example'


def test_patient_lookup_returns_registered_patient() -> None:
    """Verify patient lookup returns the stored object and rejects invalid IDs.
    """
    data_store, patient, _, _ = foundation()
    service = PatientService(data_store)
    assert service.find_patient('P1') is patient
    with pytest.raises(LookupError):
        service.find_patient('missing')
    with pytest.raises(ValueError):
        service.find_patient(' ')


def test_practitioner_lookup_returns_registered_practitioner() -> None:
    """Verify practitioner lookup returns the stored object and rejects
    invalid IDs.
    """
    data_store, _, practitioner, _ = foundation()
    service = PractitionerService(data_store)
    assert service.find_practitioner('D1') is practitioner
    with pytest.raises(LookupError):
        service.find_practitioner('missing')
    with pytest.raises(ValueError):
        service.find_practitioner(' ')


def test_duplicate_appointment_preserves_original() -> None:
    """Verify duplicate appointment preserves original."""
    data_store, _, _, appointment_service = foundation()
    original = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    with pytest.raises(ValueError):
        appointment_service.book_appointment(
            'A1',
            'P1',
            'D1',
            datetime(2026, 10, 1, 10),
        )
    assert data_store.list_appointments() == [original]
    assert original.date_time == datetime(2026, 10, 1, 9)


def test_unregistered_participants_rejected() -> None:
    """Verify unregistered participants rejected."""
    data_store, patient, practitioner, appointment_service = foundation()
    with pytest.raises(LookupError):
        appointment_service.book_appointment(
            'A1',
            'missing',
            'D1',
            datetime(2026, 10, 1, 9),
        )
    impostor = Patient('P1', 'Unregistered')
    with pytest.raises(ValueError):
        data_store.add_appointment(
            Appointment('A2', impostor, practitioner, datetime(2026, 10, 1, 9)),
        )
    assert data_store.list_appointments() == []


def test_conflict_rule_and_different_practitioner() -> None:
    """Verify conflict rule and different practitioner."""
    data_store, _, _, appointment_service = foundation()
    PractitionerService(
        data_store,
    ).register_practitioner('D2', 'Morgan Example', 'General')
    when = datetime(2026, 10, 1, 9)
    appointment_service.book_appointment('A1', 'P1', 'D1', when)
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert appointment_service.book_appointment(
        'A3',
        'P1',
        'D2',
        when,
    ).practitioner.practitioner_id == 'D2'


def test_service_cancellation_and_guard() -> None:
    """Verify service cancellation, retention and invalid transition guard."""
    data_store, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    assert appointment_service.cancel_appointment('A1') is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED
    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('missing')
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(' ')
