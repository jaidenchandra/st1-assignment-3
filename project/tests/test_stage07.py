from datetime import datetime 

import pytest

from smartcare.domain import (
    Appointment, 
    AppointmentStatus, 
    Patient,
    Practitioner,
)

def test_cancelled_appointment_remains_cancelled():
    patient = Patient('P1', 'Test Patient')
    practitioner = Practitioner('PR1', 'Test Practitioner', 'GP')
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9),
    )

    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED

    with pytest.raises(ValueError):
        appointment.cancel()  

    assert appointment.status == AppointmentStatus.CANCELLED

def test_cancelled_appointment_remains_in_store():
    from smartcare.data_store import SmartCareDataStore

    store = SmartCareDataStore()
    patient = Patient('P2', 'Test Patient')
    practitioner = Practitioner('PR2', 'Test Practitioner', 'GP')

    store.add_patient(patient)
    store.add_practitioner(practitioner)

    appointment = Appointment(
        'A2',
        patient,
        practitioner,
        datetime(2026, 10, 1, 10),
    )

    store.add_appointment(appointment)
    appointment.cancel()

    found = store.find_appointment('A2')

    assert found is appointment
    assert found.status == AppointmentStatus.CANCELLED


def test_known_appointment_id_returns_correct_appointment():
    from smartcare.data_store import SmartCareDataStore
    from smartcare.services import AppointmentService

    store = SmartCareDataStore()
    patient = Patient("P3", "Test Patient")
    practitioner = Practitioner("PR3", "Test Practitioner", "GP")

    store.add_patient(patient)
    store.add_practitioner(practitioner)

    appointment = Appointment(
        "A3",
        patient,
        practitioner,
        datetime(2026, 11, 1, 12, 0),
    )
    store.add_appointment(appointment)

    service = AppointmentService(store)
    found = service.find_appointment("A3")

    assert found is appointment
    assert found.patient is patient
    assert found.practitioner is practitioner


def test_blank_appointment_id_is_rejected():
    with pytest.raises(ValueError):
        Appointment(
            "   ",
            Patient("P4", "Test Patient"),
            Practitioner("PR4", "Test Practitioner", "GP"),
            datetime(2026, 11, 1, 13, 0),
        )