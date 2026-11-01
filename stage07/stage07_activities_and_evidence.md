# Stage 7 Testing and Verification Record

Group/tutorial: [Thurs 2:30-4:30 Group 2]  Members/cohorts: [Musab, Saja, Jaiden, Yashmeen]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | [Register a patient with valid details and a unique ID] | [Attempt to register a patient using an existing ID] | [The valid patient is stored; the duplicate is rejected and the original record remains unchanged] |
| FR-05 Prevent practitioner conflict | [Book two appointments with the same practitioner at different times] | [Attempt to book two appointments with the same practioner at the exact same date and time] | [The first appointment is stored; the conflicting appointment is rejected] |
| FR-06 Cancel appointment | [Cancel a scheduled appointment] | [Attempt to cancel the same appointment a second time] | [The status changes to CANCELLED; repeated cancellation is rejected] |
| FR-07 Retain cancelled history | [Cancel an appointment and retrieve it by its ID] | [Attempt to retrieve a cancelled appointment using an unknown ID] | [The cancelled appointment remains retrievable with its details and CANCELLED status; the unknown ID is not found] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Weak/unclear]  Why: [It always passes, regardless of whether the required behaviour is correct. It does not check any result from the program]

`assert appointment is not None`
Judgement: [Weak/unclear]  Why: [It only checks that the appointment object exist. It does not verify the appointment's details, date, practitioner, or status. ]

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour]  Why: [It directly checks that cancelling the appointment changes its status to CANCELLED. Limits: it does not prove that the appointment's history is retained or that the repeated cancellation is rejected ]

`assert len(results) > 0`
Judgement: [Weak/unclear]  Why: [It only checks that the list isn't empty. It does not confirm that the correct appointment is present or that the results meet the requirements]

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour]  Why: [It checks that looking up A1 returns the exact same appointment object. This provides evidence that the appointment is retrievable, but it does not independently prove its status is CANCELLED]

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions. For each input/state, expected result and supporting contract: 

[Input/State: Blank patient ID -> e.g (" ", "Sam")
Expected result: Reject registration and do not store a patient -> ValueError
Supporting contract: required_text

Input/State: Patient name containing only spaces ("  ")
Expected result: Reject registration as name is blank after trimming whitespace -> ValueError
Supporting contract:required_text

Input/State: Same time practitioner bookings 
Expected result: Second booking rejected if first appointment is still SCHEDULED -> ValueError
Supporting contract:practitioner conflict and prevent exact date/time

Input/State: Cancelled appointment is retrieved using its ID 
Expected result: Return the appointment with its status still CANCELLED 
Supporting contract: retain cancelled appointment history 

Input/State: Attempt to cancel an already cancelled appointment
Expected result: ValueError; status stays CANCELLED 
Supporting contract: cancel allows only a SCHEDULED appointment 

Input/State: Attempt an invalid status transition -> cancelling a COMPLETED appointment
Expected result: ValueError -> leave appointment status unchanged 
Supporting contract: cancel only permits SCHEDULED -> CANCELLED]


### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [Only checks that an object exists, not that it contains the right information] | [Register a valid patient and verify the patient is stored with the correct ID and details] |
| 2 | [Only checks that an object is not None; it does not verify the required behaviour] | [Book an appointment and verify the correct patient, practitioner, date, and time are stored] |
| 3 | [assert True always passes, even if the software is incorrect] | [Attempt to book two appointments with the same practitioner at the same date and time, and verify the second booking is rejected] |
| 4 | [Assumes SMS notifications exist, although this feature is not specified in the requirements] | [Cancel a scheduled appointment and verify its status changes to CANCELLED] |
| 5 | [Assume SMS notifications exist instead of testing a supported requirement] | [Retrieve a cancelled appointment by its ID and verify its details and CANCELLED status are retained] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[100% code coverage means every line of code has been executed, but it does not guarantee the software works correctly. Tests may use weak assertions, miss boundary cases, or fail to check expected results. Good software verification requires testing requirements, correct behaviour, invalid inputs, and potential errors, not just executing every line of code.]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| [FR-01] | [AC-01.1] | [TEST-01] | [Positive] | [test_register_patient - tests/test_services.py] | [Valid patient is stored and can be retrieved with the correct details] | [Passed ] | [Supplied] |

| [FR-01] | [AC-01.2] | [TEST-02] | [Negative] | [test_duplicate_patient_id_rejected - tests/test_services.py] | [Duplicate registration is rejected and the original patient remains unchanged] | [Passed] | [Supplied] |

| [FR-01] | [Revision 2 contract: required text must not be blank] | [TEST-03] | [Boundary] | [test_required_fields — tests/test_starter.py] | [Invalid blank fields are rejected] | [Passed] | [Supplied] |

| [FR-03] | [Duplicate practitioner IDs must not overwrite exisiting records ] | [TEST-04] | [Negative] | [test_duplicate_practitioner_preserves_original — tests/test_starter.py] | [Duplicate registration is rejected and the original patient remains unchanged] | [Passed] | [Supplied] |

| [FR-04]| [Duplicate appointment IDs are rejected]| [TEST-05]| [Negative] | [test_duplicate_appointment_preserves_original — tests/test_starter.py]|[Duplicate booking is rejected and the original appointment remains unchanged]|[Passed]|[Supplied] |

| [FR-04]| [Both participants must be registered before booking]| [TEST-06]| [Negative] | [test_unregistered_participants_rejected — tests/test_starter.py]|[Booking with unregistered participants is rejected]|[Passed]|[Supplied] |

| [FR-05]| [Supporting contract: conflict]| [TEST-07]| [Positive and negative] | [test_conflict_rule_and_different_practitioner — tests/test_starter.py]|[Conflicting booking is rejected and the original appointment remains stored.]|[Passed]|[Supplied] |

| [FR-06]| [AC-05.1]| [TEST-08]|[Positive]|[test_domain_cancellation_and_guard — tests/test_starter.py]|[Appointment status changes from SCHEDULED to CANCELLED]|[Passed]|[Supplied] |

| [FR-06]| [AC-05.3]| [TEST-09]|[Negative]|[test_cancelled_appointment_remains_cancelled — tests/test_stage07.py]|[Repeated cancellation raises ValueError; status remains CANCELLED]|[Passed]|[Student-authored] |

| [FR-07]| [AC-05.2]| [TEST-10]|[Positive]|[test_cancelled_remains_in_store — tests/test_stage07.py]|[Cancelled appointment remains retrievable by ID with its details and status]|[Passed]|[Student-authored] |

| [FR-08]| [AC-06.1]| [TEST-11]|[Positive]|[test_known_appointment_id_returns_correct_appointment — tests/test_stage07.py]|[The correct appointment and associated patient and practitioner are returned]|[Passed]|[Student-authored] |

| [Revision 2 validation contract]| [Appointment IDs must contain nonblank text]| [TEST-12]|[Boundary]|[test_blank_appointment_id_is_rejected — tests/test_stage07.py]|[An appointment with a blank ID is rejected with ValueError]|[Passed]|[Student-authored] |

# Command: python3 -m pytest -v 
# Observed result: 12 tests passed
# Supplied tests: 8 in test/test_starter.py
# Student-authored tests: 4 in tets/test_stage07.py

## C Test Design
Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| [TEST-09] | [FR-06] | [AC-05.3] | [Negative] | [test_cancelled_appointment_remains_cancelled() checks that an appointment cannot be cancelled twice.] | [A second cancellation raises ValueError, and the status remains CANCELLED] | [Confirms repeated cancellation is rejected and does not change the appointment's final status] |
| [TEST-10] | [FR-07] | [AC-05.2] | [Positive] | [test_cancelled_remains_in_store() checks that a cancelled appointment remains in the data store] | [The same appointment can still be retrieved with status CANCELLED] | [Confirms cancellation preserves the appointment record rather than deleting it] |
| [TEST-11] | [FR-08] | [AC-06.1] | [Positive] | [test_known_appointment_id_returns_correct_appointment() checks appointment lookup using a valid ID] | [The correct appointment, patient and practitioner are returned] | [Adds evidence that lookup returns the correct record and its associated participants] |
| [TEST-12] | [Appointment ID validation] | [Revision 2 contract - appointment IDs must not be blank] | [Boundary] | [test_blank_appointment_id_is_rejected() checks an appointment ID containing only spaces] | [Creating the appointment raises ValueError] | [Adds evidence that whitespace-only appointment IDs are rejected, which is not covered by the supplied tests] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [TEST-09] | [Create an appointment and cancel it once] | [Attempt to cancel the appointment a second time] | [pytest.raises(ValueError) confirms the second cancellation is rejected; check that status remains CANCELLED] | [Proves repeated cancellation is rejected and does not change the appointment's status] |
| [TEST-10] | [Create an appointment, add it to the data store, and cancel it] | [Retrieve the appointment using its ID] | [The retrieved object is the same appointment, and its status is CANCELLED] | [Proves cancellation preserves the appointment record for retrieval] |
| [TEST-11] | [Register a patient and practitioner, create an appointment, and store it] | [Find the appointment using its known ID] | [The returned appointment has the expected ID, patient and practitioner] | [Proves lookup returns the correct appointment and its associated records] |
| [TEST-12] | [Prepare an appointment ID containing only spaces, with otherwise valid appointment data] | [Attempt to create the appointment] | [pytest.raises(ValueError) confirms the blank ID is rejected] | [Proves whitespace-only appointment IDs are invalid] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [TEST-D01] | [Reject a blank patient ID] | [tests/test_domain.py — test_blank_patient_id_is_rejected] | [Passed] |
| [TEST-D01] | [A newly created appointment starts with status SCHEDULED] | [tests/test_domain.py — test_new_appointment_starts_scheduled] | [Passed] |
| [TEST-D03] | [Cancelling a scheduled appointment changes its status to CANCELLED] | [tests/test_domain.py — test_cancel_changes_status] | [Passed] |
| [TEST-D04] | [Repeated cancellation is rejected] | [tests/test_domain.py — test_repeated_cancellation_is_rejected] | [Passed only if a test specifically checks this behaviour] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [TEST-01] | [Register a patient and book an appointment successfully] | [FR-01 / AC-01.1; FR-04 / AC-03.1] | [tests/test_starter.py — test_registration_and_booking] | [Passed - supplied test] |
| [TEST-02] | [Reject a duplicate patient ID without changing the original record] | [FR-01 / AC-01.2] | [tests/test_starter.py — test_duplicate_patient_preserves_original] | [Passed - supplied test] |
| [TEST-04] | [Reject a duplicate practitioner ID without changing the original record] | [FR-03] | [tests/test_starter.py — test_duplicate_practitioner_preserves_original] | [Passed — supplied test] |
| [TEST-05] | [Reject a duplicate appointment ID] | [FR-04] | [tests/test_starter.py — test_duplicate_appointment_preserves_original] | [Passed — supplied test] |
| [TEST-06] | [Reject booking when participants are not registered] | [FR-04 / AC-03.2] | [tests/test_starter.py — test_unregistered_participants_rejected] | [Passed — supplied test] |
| [TEST-07] | [Reject a same-practitioner, same-time conflict while allowing a different practitioner] | [FR-05 / AC-04.1 and AC-04.2] | [tests/test_starter.py — test_conflict_rule_and_different_practitioner] | [Passed — supplied test] |
| [TEST-10] | [Keep a cancelled appointment retrievable in the data store] | [FR-07 / AC-05.2] | [tests/test_stage07.py — test_cancelled_remains_in_store] | [Passed — student-authored test] |
| [TEST-11] | [Return the correct appointment for a known appointment ID] | [FR-08 / AC-06.1] | [tests/test_stage07.py — test_known_appointment_id_returns_correct_appointment] | [Passed — student-authored test] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [Patient validation] | [Patient ID is blank or contains only spaces ] | [Raise ValueError; no patient should be registered] | [TEST-03] |
| [Duplicate patient registration] | [Register a patient using an existing patient ID] | [Reject registration and preserve the original patient] | [TEST-02] |
| [Duplicate practitioner registration] | [Register a practitioner using an existing practitioner ID] | [Reject registration and preserve the original practitioner] | [TEST-04] |
| [Appointment ID validation] | [Appointment ID contains only spaces] | [Raise ValueError; appointment is not created] | [TEST-12] |
| [Appointment booking] | [Patient or practitioner is not registered] | [Reject booking; no appointment is stored] | [TEST-06] |
| [Practitioner conflict] | [Same practitioner has a scheduled appointment at the exact same date and time] | [Reject the conflicting booking and preserve the existing appointment] | [TEST-07] |
| [Repeated cancellation] | [Attempt to cancel an already cancelled appointment] | [Raise ValueError; status remains CANCELLED] | [TEST-09] |
| [Cancelled appointment history] | [Retrieve an appointment after cancellation] | [The original appointment remains retrievable with status CANCELLED] | [TEST-10] |


## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [FR-06: cancel appointment]
Acceptance criterion: [AC-05.1: cancelling a SCHEDULED appointment changes its status to CANCELLED]
Behaviour to test: [Cancelling a scheduled appointment updates its status correctly]
Human-first test idea/categories: [Positive test — create a valid appointment, cancel it, and assert that its status is CANCELLED. Negative test — attempt to cancel an already cancelled appointment and assert that ValueError is raised]
Prompt and purpose: [Ask GitHub Copilot to suggest a pytest test for AC-05.1 using the existing SmartCare domain classes. The test must use public methods, assert the exact status change, and avoid inventing business rules]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [Test that cancelling an appointment changes its status to CANCELLED]
- What it claims to verify: [The appointment status changes to CANCELELD after calling the cancel() method]
- Requirement trace: [Appointment cancellation requirement - verify that a scheduled appointment can be cancelled]
- Assertion quality: [The assertion directly compares the appointment status with AppointmentStatus.CANCELLED]
- Human critique: [The test creates valid patient, practitioner, and appointment objects, cancels the appointment, and checks the resulting status. It verifies the main cancellation outcome but does not test repeated cancellation]
- Decision: [Accept]
- Reason: [The test is relevant to the cancellation requirement, and its assertion checks the expected result]
- Final test reference if accepted/modified: [project/tests/test_domain.py — test_cancelled_appointment_changes_status_to_cancelled]
- Actual verification result: [Passed when executed using pytest]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [The test test_cancelled_appointment_changes_status_to_cancelled, generated by Copilot, looked convincing because it created an appointment, cancelled it and checked that the status became CANCELLED]
Why was it weak? [The test checked the final cancellation status but did not explicitly verify that the appointment started in the SCHEDULED state. Therefore, it did not fully demonstrate the transition from a scheduled appointment to a cancelled appointment]
How did you strengthen it? [I reviewed the test against the cancellation requirement and confirmed that its assertion checked the expected final status. The test passed when executed using pytest. To strengthen it further, an assertion could be added before cancellation to verify that the initial status is SCHEDULED]
Accepted / modified / rejected test decisions and evidence: [The Copilot-generated test was accepted and saved in project/tests/test_domain.py as test_cancelled_appointment_changes_status_to_cancelled. The test passed when executed using pytest. The decision and verification result are documented in Section H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [python -m pytest -v] | [project/] | [Not available - no Git repository] | [13] | [0] | [No test failures] | [All 13 tests passed] | [All 13 tests passed, indicating that the accumulated test suite passed in this run] |

# Full-suite result: 13 passed. The traceability matrix records selected tests relevant to the requirements

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [Although all 13 tests passed, the suite does not prove that every possible input and scenario works correctly. Further testing may be needed to identify remaining defects]
Coverage if used: [Not used. No code coverage measurement was performed]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [Invalid inputs and appointment cancellation edge cases may require further testing. These areas matter because errors could lead to incorrect records or unexpected behaviour. A high coverage percentage does not guarantee that tests check the correct outcomes or all business requirements]
Optional fixtures/parametrisation used and why, if any: [Not used. Each test uses its own test data. Fixtures or parametrisation could help reduce repeated setup and test multiple input scenarios]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [Stage 7 testing and regression checks] | [Not available] | [Not available] | [Not applicable] | [Ran the full pytest suite; all 13 tests passed] | [Regression run completed; Git review evidence unavailable] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [Musab] | [Worked on implementing and integrating patient, practitioner and appointment service functions, including lookup and cancellation] | [project/tests/test_domain.py; stage06_activities_and_evidence.md] |
| [Saja] | [Created a pytest test for appointment cancellation, reviewed Copilot's suggestion, documented the decision and ran the regression suite, with 13 tests passing] | [stage07/stage07_activities_and_evidence.md] |
| [Jaiden] | [Not completed; need to: Diagnose and fix data_store.py faults, add regression tests, refactor safely, and rerun tests before and after changes] | [stage08/stage08_activities_and_evidence.md] |
| [Yashmeen] | [Not completed; need to: Implement and test queries and console workflows, update the README, and review Copilot’s suggestions] | [stage09/stage09_activities_and_evidence.md] |

## N Formative Questions

1. What question does verification answer?
[Are we building the product correctly?]

2. What question does validation answer?
[Are we building the right product fit to the user's needs?]

3. What is a unit test?
[A test that checks one small part of a program independently]

4. What is a pytest fixture?
[Reusable setup code that provides test data or objects]

5. What is parametrisation in pytest?
[Running the same test with different input values]

6. What is regression testing?
[Retesting software to ensure changes have not been broken existing functionality]

7. What does code coverage tell us, and what does it not prove?
[It shows which code was executed during testing, but does not prove the code is correct]

8. What makes an assertion weak?
[It does not clearly check the required behaviour or expected result]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[To suggest tests that a developer reviews, improves, and verifies before accepting]

10. What is the Stage 7 engineering rule?
[Review and verify every test, retain evidence, and never claim a test passed until it was actually run]

## O Stage Completion

Tested Stage 7 main SHA: [Unavailable - no local Git repository was found]
Full-suite result: [Complete - python3 -m pytest -v returned 13 passed, 0 failed]
Unresolved defects and effect on baseline: [No test failure occured in rerecorded run. Unresolved defects have not been independetly confirmed]
Clean working tree and integration evidence: [Not verified as Git repository evidence is unavailable]
Stage 8 handover status: [complete; stage 8 work applicable]
All tutorial/formative responses and traceability/Copilot decisions complete: [Formative responses completed. Copilot test review and decision documented; confirm that all traceability entries are complete]
