from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

def test_blank_patient_id_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        Patient(' ', 'Test Patient')

def test_cancelled_appointment_changes_status_to_cancelled():
    patient = Patient('P1', 'Test Patient')
    practitioner = Practitioner('PR1', 'Test Practitioner', 'GP')
    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )
    
    assert appointment.status == AppointmentStatus.SCHEDULED
    appointment.cancel()

    assert appointment.status == AppointmentStatus.CANCELLED