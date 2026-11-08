
"""Tests for SmartCare Stage 6 service operations.

Covers FR-02 patient lookup, practitioner lookup supporting
FR-03, FR-06 appointment cancellation, and FR-07 retained history.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


@pytest.fixture
def setup_services():
    """Create a fresh store and registered participants."""
    store = SmartCareDataStore()

    patient_service = PatientService(store)
    practitioner_service = PractitionerService(store)
    appointment_service = AppointmentService(store)

    patient = patient_service.register_patient(
        "P1", "Alex Example"
    )

    practitioner = practitioner_service.register_practitioner(
        "D1", "Taylor Example", "General"
    )

    return (
        store,
        patient_service,
        practitioner_service,
        appointment_service,
        patient,
        practitioner,
    )


# --------------------------------------------------
# FR-02: Patient lookup
# --------------------------------------------------

def test_find_existing_patient(setup_services):
    """Patient lookup returns the original stored object."""
    (
        store,
        patient_service,
        _,
        _,
        patient,
        _,
    ) = setup_services

    result = patient_service.find_patient("P1")

    assert result is patient
    assert store.find_patient("P1") is patient


def test_find_patient_with_trimmed_id(setup_services):
    """Patient lookup accepts surrounding whitespace."""
    _, patient_service, _, _, patient, _ = setup_services

    assert patient_service.find_patient(" P1 ") is patient


def test_patient_id_is_case_sensitive(setup_services):
    """Patient lookup does not ignore case."""
    _, patient_service, _, _, _, _ = setup_services

    with pytest.raises(LookupError):
        patient_service.find_patient("p1")


def test_find_unknown_patient(setup_services):
    """Unknown patient IDs raise LookupError."""
    _, patient_service, _, _, _, _ = setup_services

    with pytest.raises(LookupError):
        patient_service.find_patient("UNKNOWN")


@pytest.mark.parametrize("invalid_id", ["", " ", "\t", None, 123])
def test_find_patient_invalid_id(setup_services, invalid_id):
    """Invalid patient IDs raise ValueError."""
    _, patient_service, _, _, _, _ = setup_services

    with pytest.raises(ValueError):
        patient_service.find_patient(invalid_id)


# --------------------------------------------------
# Practitioner lookup supporting FR-03
# --------------------------------------------------

def test_find_existing_practitioner(setup_services):
    """Practitioner lookup returns the stored object."""
    (
        store,
        _,
        practitioner_service,
        _,
        _,
        practitioner,
    ) = setup_services

    result = practitioner_service.find_practitioner("D1")

    assert result is practitioner
    assert store.find_practitioner("D1") is practitioner


def test_find_practitioner_with_trimmed_id(setup_services):
    """Practitioner lookup accepts surrounding whitespace."""
    _, _, service, _, _, practitioner = setup_services

    assert service.find_practitioner(" D1 ") is practitioner


def test_practitioner_id_is_case_sensitive(setup_services):
    """Practitioner lookup preserves case sensitivity."""
    _, _, service, _, _, _ = setup_services

    with pytest.raises(LookupError):
        service.find_practitioner("d1")


def test_find_unknown_practitioner(setup_services):
    """Unknown practitioner IDs raise LookupError."""
    _, _, service, _, _, _ = setup_services

    with pytest.raises(LookupError):
        service.find_practitioner("UNKNOWN")


@pytest.mark.parametrize("invalid_id", ["", " ", "\t", None, 123])
def test_find_practitioner_invalid_id(setup_services, invalid_id):
    """Invalid practitioner IDs raise ValueError."""
    _, _, service, _, _, _ = setup_services

    with pytest.raises(ValueError):
        service.find_practitioner(invalid_id)


# --------------------------------------------------
# FR-06 and FR-07: Appointment cancellation
# --------------------------------------------------

def test_cancel_scheduled_appointment(setup_services):
    """Cancelling a scheduled appointment changes its status."""
    (
        store,
        _,
        _,
        service,
        _,
        _,
    ) = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    result = service.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancelled_appointment_remains_stored(setup_services):
    """Cancelled appointments remain retrievable."""
    store, _, _, service, _, _ = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    service.cancel_appointment("A1")

    assert service.find_appointment("A1") is appointment
    assert store.list_appointments() == [appointment]
    assert appointment.status is AppointmentStatus.CANCELLED


def test_repeated_cancellation_rejected(setup_services):
    """A cancelled appointment cannot be cancelled twice."""
    _, _, _, service, _, _ = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert service.find_appointment("A1") is appointment


def test_cancel_unknown_appointment(setup_services):
    """Unknown appointment IDs raise LookupError."""
    _, _, _, service, _, _ = setup_services

    with pytest.raises(LookupError):
        service.cancel_appointment("UNKNOWN")


@pytest.mark.parametrize("invalid_id", ["", " ", "\t", None, 123])
def test_cancel_invalid_appointment_id(setup_services, invalid_id):
    """Invalid appointment IDs raise ValueError."""
    _, _, _, service, _, _ = setup_services

    with pytest.raises(ValueError):
        service.cancel_appointment(invalid_id)


def test_cancel_appointment_with_trimmed_id(setup_services):
    """Cancellation accepts surrounding whitespace."""
    _, _, _, service, _, _ = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    result = service.cancel_appointment(" A1 ")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancel_appointment_id_is_case_sensitive(setup_services):
    """Cancellation does not ignore ID case."""
    _, _, _, service, _, _ = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    with pytest.raises(LookupError):
        service.cancel_appointment("a1")

    assert appointment.status is AppointmentStatus.SCHEDULED


def test_failed_cancellation_preserves_appointment(setup_services):
    """An unsuccessful cancellation does not modify the record."""
    store, _, _, service, _, _ = setup_services

    appointment = service.book_appointment(
        "A1",
        "P1",
        "D1",
        datetime(2026, 10, 1, 9),
    )

    with pytest.raises(LookupError):
        service.cancel_appointment("MISSING")

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert service.find_appointment("A1") is appointment
    assert store.list_appointments() == [appointment]
