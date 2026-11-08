# Stage 9 activities and evidence

Common UG and PG record.

**Group:** Thursday 2:30-4:30 Group 2

**Members and responsibilities:**
U3321093 – implemented Stage 9 appointment queries, practitioner appointment listing, interactive console integration, query/workflow tests, manual verification and regression testing.


**Stage 8 integrated SHA:** 3f24502d16277ec256e51cdc96ce123d9861c2fd

**Stage 8 verification command:** `python -m pytest -q`
**Working directory:** `project/`
**Actual result:** 16 passed in 0.01s

---

## A. Tutorial activities

### A1 Session state classification

| Information            | Required session/domain or transient state? | Requirement or reason                                                                                    |
| ---------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Patient identity       | Required session/domain state               | Patients must remain available during the session for lookup and appointment booking.                    |
| Appointment history    | Required session/domain state               | Appointments must remain available after booking and cancellation so history is retained.                |
| Temporary menu choice  | Transient state                             | The menu choice is only needed to decide which console action to run.                                    |
| Practitioner specialty | Required session/domain state               | Specialty is part of the registered Practitioner object and remains available during the session.        |
| Debug print output     | Transient state                             | Debug/display output is not part of stored SmartCare data.                                               |
| Appointment status     | Required session/domain state               | Status is required to distinguish scheduled, cancelled and completed appointments and support filtering. |

**What is intentionally lost on exit?**

All registered patients, practitioners and appointments are intentionally lost when the program exits because SmartCare uses session-only in-memory storage. Stage 9 does not add persistence.

---

### A2 Interface and domain data plan

| Function or component  | Explicit inputs and types                                                                      | Outputs                         | Responsibility and validation                                                                                                     | Domain source / existing constraint                        |
| ---------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `appointment_sort_key` | `appointment: Appointment`                                                                     | `tuple[datetime, str]`          | Returns the appointment date/time and ID ordering key. No I/O or mutation.                                                        | Existing `Appointment.date_time` and `appointment_id`.     |
| `select_appointments`  | `appointments: list[Appointment]`, `practitioner_id: str`, `status: AppointmentStatus \| None` | New `list[Appointment]`         | Filters by practitioner, optionally filters by status and sorts without mutating the source list.                                 |                                                            |
| Service listing        | `practitioner_id: str`, `status: AppointmentStatus \| None`                                    | New ordered `list[Appointment]` | Validates the practitioner, validates status, gets appointments from the store and delegates filtering/sorting to the pure query. | Shared SmartCareDataStore and registered practitioner IDs. |
| Console                | User-entered menu choice and text values                                                       | Printed results/errors          | Reads user input, converts values, calls services and handles expected errors while keeping the session running.                  | Existing service contracts, parser and status enum.        |

**Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts:**

Patient ID and name belong to the `Patient` domain object. Practitioner ID, name and specialty belong to the `Practitioner` domain object. Each Appointment stores its appointment ID, references to the actual registered Patient and Practitioner objects, date/time and AppointmentStatus. Stage 9 reuses these existing objects rather than creating replacement participants.

---

### A3 Responsibility violations

| Conceptual case                  | Violation                              | Correct boundary and reason                                                                                                                        |
| -------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Appointment.cancel` reads input | Domain object performing console I/O   | The console should read the appointment ID. The service retrieves the appointment and the domain method only performs the cancellation transition. |
| Service prints/reads the menu    | Service performing user-interface work | `console.py` should own input/output. Services should coordinate domain and store operations.                                                      |
| Query sorts its source in place  | Mutates the supplied collection        | The query should use `sorted(...)` and return a new list so the source list is unchanged.                                                          |
| Store prints `Appointment saved` | Store performing presentation work     | The store should manage collections only. The console should print user-facing messages.                                                           |

---

### A4 Sorting comparison

`appointments.sort(key=appointment_sort_key)` changes the original list in place and returns `None`.

`result = sorted(appointments, key=appointment_sort_key)` leaves the original source list unchanged and returns a separate sorted list.

A meaningful mutation check is:

```python
before = list(source)
result = select_appointments(source, "D1")

assert source == before
assert result is not source
```

The named key returns:

```python
(appointment.date_time, appointment.appointment_id)
```

Therefore date/time is the primary sort value and appointment ID breaks ties when appointments have the same time.

The key is passed to sorting using:

```python
sorted(selected, key=appointment_sort_key)
```

---

### A5 Exit question

Cancellation changes an appointment's status to `CANCELLED`; it does not delete the appointment.

The cancelled appointment should still be retrievable during the same session and should appear when listing all statuses or cancelled appointments. It should not appear in a `SCHEDULED`-only filter.

Because cancelled appointments remain in the store, appointment history is preserved during the session. All data is still intentionally lost once the program exits.

---

## B. Human design and contracts

| Requirement                  | Input / session data               | Operation and responsible component           | Expected result or error                                                             | Test / evidence                            |
| ---------------------------- | ---------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------ |
| QRY-01                       | Appointment list + practitioner ID | `select_appointments` filters by practitioner | Only requested practitioner's appointments returned                                  | `test_selects_only_requested_practitioner` |
| QRY-02                       | Appointment list + optional status | Query filters only when status is supplied    | `None` includes all statuses; enum includes matching status; no matches returns `[]` | Query tests                                |
| QRY-03                       | Matching appointments              | `appointment_sort_key` + `sorted`             | Ordered by date/time then appointment ID                                             | Sorting test                               |
| FP-01                        | Same explicit arguments            | Pure query                                    | Repeated calls give equivalent results and no side effects                           | Query tests + code inspection              |
| FP-02                        | Empty/sorted/unsorted source list  | `sorted(...)`                                 | New list returned; source unchanged                                                  | Non-mutation tests                         |
| FP-03                        | Appointment object                 | `appointment_sort_key`                        | Returns `(date_time, appointment_id)`                                                | Direct key test                            |
| Service known practitioner   | Registered practitioner ID         | AppointmentService validates and queries      | Matching ordered list or new empty list                                              | Workflow tests                             |
| Service unknown practitioner | Valid but unregistered ID          | Service/store validation                      | `LookupError`                                                                        | Workflow test                              |
| Service invalid ID           | Blank/invalid ID                   | Existing validation                           | `ValueError`                                                                         | Workflow test                              |
| Service invalid status       | Non-enum status                    | Service validates status                      | `ValueError`                                                                         | Workflow test                              |
| UI-01                        | Valid interactive session inputs   | Console dispatches to services                | Registration, booking, cancellation, lookup and listing work in one shared session   | Manual console test                        |
| UI-02                        | Invalid choice/date/status/IDs     | Console catches expected errors               | Error displayed and menu continues                                                   | Manual console test                        |

**Empty versus unknown versus invalid:**

A registered practitioner with no matching appointments returns a new empty list. A valid-format but unregistered practitioner ID raises `LookupError`. A blank or invalid practitioner ID, or an invalid non-enum status, raises `ValueError`.

**Enum conversion:**

The console converts user-entered text such as `scheduled`, `cancelled` and `completed` into the corresponding `AppointmentStatus` enum before calling the service.

**Actual object identity:**

The query returns existing Appointment objects inside a new list. It does not create replacement Appointment, Patient or Practitioner objects.

**Error handling and unchanged state on rejection:**

Expected `ValueError` and `LookupError` exceptions are caught by the console. Invalid operations are rejected and the program remains running. Valid session data remains available after a rejected action.

---

## C. Implementation and query verification

| Requirement / test ID    | Code location                                                      | Case and meaningful assertion                                                    | Actual result                  | Evidence link |
| ------------------------ | ------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------ | ------------- |
| QRY-01                   | `project/smartcare/queries.py`, `project/tests/test_queries.py`    | Only requested practitioner's appointment is returned                            | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| QRY-02                   | Same                                                               | Default includes all statuses; explicit status filters correctly                 | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| QRY-03                   | Same                                                               | Equal-time appointments ordered by appointment ID                                | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| FP-01                    | Same                                                               | No I/O, global store or external state used                                      | Passed by tests and inspection | [https://github.com/jaidenchandra/st1-assignment-3]        |
| FP-02                    | Same                                                               | `source == before` and `result is not source`                                    | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| FP-03                    | Same                                                               | Named key directly returns `(date_time, appointment_id)` and is used by `sorted` | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| Known-empty service case | `project/smartcare/services.py`, `project/tests/test_workflows.py` | Registered practitioner with no matches returns `[]`                             | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| Unknown service case     | Same                                                               | Unknown practitioner raises `LookupError`                                        | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| Invalid service case     | Same                                                               | Blank ID or invalid status raises `ValueError`                                   | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |
| Retained history         | Same                                                               | Cancelled appointment remains in default listing                                 | Passed                         | [https://github.com/jaidenchandra/st1-assignment-3]        |

**Purity explanation from code inspection, including absence of hidden state and I/O:**

`select_appointments` receives all information through parameters. It does not access a global store, read input, print output or perform file operations. It builds a local result and returns `sorted(...)`, so the source collection is not sorted in place.

**What the tests do and do not establish:**

The tests establish the expected observable behaviour for the tested cases, including filtering, ordering, fresh-list behaviour and unchanged source order. Passing tests alone do not prove the absence of every possible side effect, so code inspection was also used to confirm that the query contains no hidden global state, store access or I/O.

---

## D. Integrated console and workflow evidence

| Scenario / acceptance ID     | Reproducible inputs / artefact                                                             | Expected result                                                        | Observed result and state check                                               | Evidence link     |
| ---------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------- |
| UI-01 full menu workflow     | `python main.py --interactive`; register patient/practitioner, book, find, cancel and list | Valid operations succeed and session data remains available until exit | Menu launched successfully and valid workflow operations worked               | [link/screenshot] |
| UI-02 invalid-input recovery | Invalid menu option and malformed date                                                     | Error shown, menu continues and valid state remains usable             | Invalid menu choice and malformed date were tested; program continued running | [link/screenshot] |
| Automated service workflow   | `python -m pytest -q` from `project/`                                                      | Full test suite passes                                                 | **60 passed**                                                                 | [link/screenshot] |


---

## E. GitHub Copilot review and human decisions

**Human design completed before AI:**  
The Stage 9 query, service and console design had already been implemented and tested before this Copilot review. Copilot was used only as a review tool to identify possible defects, missing validation or weak test coverage.

**Actual prompt/context supplied:**  
Copilot was asked to review the Stage 9 SmartCare implementation for purity, source-list mutation, practitioner/status filtering, deterministic ordering, service validation/delegation, responsibility separation, shared-session behaviour, error recovery, cancelled-appointment retention and test coverage. 

**Actual response:**  
Copilot found no issues with `appointment_sort_key`, `select_appointments`, deterministic ordering, practitioner/status filtering, cancellation retention or the overall domain/query/service responsibility split. It identified one low-severity uncertainty: `list_practitioner_appointments()` does not explicitly validate a blank practitioner ID itself, so correct behaviour depends on `SmartCareDataStore.find_practitioner()`. Copilot also noted that it could not directly verify the console and test requirements because those files were not included in the review context.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
| --- | --- | --- | --- | --- | --- |
| `appointment_sort_key` and `select_appointments` are pure and non-mutating | `queries.py`, `test_queries.py` | None | Accept – this matches the implemented design and tests | No change | Query tests passed |
| Deterministic ordering by `(date_time, appointment_id)` is correct | `queries.py`, equal-time ordering test | None | Accept – this matches QRY-03 | No change | Sorting test passed |
| Cancelled appointments are retained rather than deleted | `services.py`, cancellation workflow tests | None | Accept – this matches the Stage 9 history requirement | No change | Workflow tests passed |
| Blank practitioner ID validation may rely on datastore validation | `services.py`, blank-ID workflow test | Low | Reject as a required code change – the existing datastore contract already raises `ValueError` for blank/invalid IDs and the workflow test confirms this behaviour | No change | Blank practitioner ID test passed |
| Console and test coverage could not be verified from the supplied Copilot context | Manual console checks, `test_queries.py`, `test_workflows.py` | Informational | Accept as a limitation of the review context, not as a product defect | No change | Manual console testing completed and full suite passed |

**Responsibility check:**

Domain objects enforce their own state and invariants. `SmartCareDataStore` owns the session collections. Services coordinate validation and workflows. The query functions perform pure filtering and sorting. The console owns input/output and menu behaviour. `main.py` selects the demo or interactive entry point.

---

## F. Required reflections

### 1. Which integration concern was architectural rather than a filtering/sorting detail?

The main architectural concern was keeping one shared `SmartCareDataStore` and service set for the entire interactive session. If a new store were created for every menu action, registrations and appointments would disappear between actions even if the filtering code itself was correct.

### 2. Which Copilot suggestion did you reject as over-engineering, and why?

Copilot suggested that `AppointmentService.list_practitioner_appointments()` could explicitly validate the practitioner ID before querying the datastore. I rejected this as an unnecessary change because the existing `SmartCareDataStore.find_practitioner()` contract already validates blank or invalid practitioner IDs and raises `ValueError`. Adding the same validation again in the service would duplicate an existing responsibility without changing observable behaviour. The existing workflow test for a blank practitioner ID also passed, confirming that the required behaviour was already satisfied.

### 3. How did you prove cancelled appointments remain retrievable and listable in the same session?

I booked an appointment, cancelled it and then queried the same shared session. The same Appointment object remained in the store with status `CANCELLED`. The automated workflow test also confirmed that the default practitioner listing still returned the cancelled appointment.
---

## G. Ten formative answers

### 1. What makes `select_appointments` pure, and what side effect breaks purity?

It receives all required data through parameters, returns a result and does not modify external state or perform I/O. Sorting the source list in place, accessing a global store, printing or reading input would break the intended pure-query behaviour.

### 2. Which explicit inputs are needed, and why avoid a global store?

The function requires the appointment list, practitioner ID and optional status. Avoiding a global store removes hidden dependencies and makes the function easier to test and reason about.

### 3. How can a new list reuse Appointment objects safely?

The result can contain references to the existing Appointment objects while using a new list container. This is safe because the query does not modify those Appointment objects.

### 4. Why use a named key, and what breaks equal-time ties?

A named sorting key makes the ordering rule clear, reusable and directly testable. The key uses `(date_time, appointment_id)`, so appointment ID breaks ties when times are equal.

### 5. How do default and explicit status filters differ?

`status=None` means all statuses are included. Supplying an `AppointmentStatus` restricts the result to that status.

### 6. How do empty, unknown practitioner and invalid filter cases differ?

A known practitioner with no matches returns an empty list. An unknown valid practitioner ID raises `LookupError`. A blank/invalid ID or invalid status raises `ValueError`.

### 7. Which console errors recover, and how is unchanged state checked?

The console recovers from expected `ValueError` and `LookupError` exceptions and also handles an invalid menu choice without terminating. State can be checked by performing a valid action after the error and confirming earlier records are still available.

### 8. What is data integrity for registered participants, conflicts and history?

Appointments must reference the actual registered Patient and Practitioner objects. Duplicate or invalid operations and scheduling conflicts are rejected. Cancellation preserves the appointment as history rather than deleting it.

### 9. What is Copilot's review role, and who verifies findings?

Copilot provides review suggestions only. The student/team must evaluate each suggestion against the requirements and code, decide whether to accept, modify or reject it, and then verify any changes using tests and manual checks.

### 10. How do pure functions and OOP responsibilities work together?

OOP components manage domain entities, state, validation and shared storage, while pure functions handle deterministic collection processing. The service layer coordinates them without mixing responsibilities.

---

## H. Review, completion and common handover

**Issues and bounded branches:**
`feature/stage9-queries`
`fix/restore-test-starter`

**PR/diff and another-member human reviewer:**
[https://github.com/jaidenchandra/st1-assignment-3/pulls]

**Review responses and Copilot comparison:**
[Complete after actual review]

**Integrated common Stage 9 SHA:**
`3112b59d36889b767a55228a0e589583ac8e30a7`

**Full regression command:**
`python -m pytest -q`

**Working directory:**
`project/`

**Actual count/result:**
`60 passed`

**Evidence:**
[https://github.com/jaidenchandra/st1-assignment-3]

**README run instructions and scope/limitations:**
The README should explain how to run `python main.py`, `python main.py --interactive` and `python -m pytest -q`. It should also state that data is session-only and is lost on exit.

**Unresolved issues and support/action:**
[Write any actual unresolved issue, or `None known` if final verification shows none.]

**UG common candidate / PG future branch plan:**
UG work continues from Stage 9 directly to Stage 12. Stage 10 and Stage 11 PG extension work is not required for the UG pathway.

- Query contracts, purity, new lists and named-key ordering verified.
- Service empty/unknown/invalid cases and cancellation history verified.
- Console menu and invalid-input recovery verified.
- Query/workflow tests plus previous tests pass: **60 passed**.
- Human design, Copilot critique, review and integration recorded honestly.
- Reflections and ten formative responses completed.
- README updated.
- Earlier code, tests and records preserved.
- Common Stage 9 SHA recorded for Stage 12 handover.
