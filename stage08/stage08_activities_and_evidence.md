# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 2 (Thursday 2:30 - 4:30)
Members and UG/PG cohorts: Yashmeen, Saja, Jaiden, Musab
Record owner contribution links for each member:

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

“Appointment disappears after cancellation.” — Symptom.
Describes an observed problem, but does not establish whether the appointment was either deleted or hidden during the lookup.

“The data-store removal path is probably being called.” — Hypothesis/opinion.
Suggests a possible cause which requires testing. The current project has no public delete operation, so removal should not be assumed.

“The failing test shows store.find_appointment('A1') returns None.” — Evidence.
Reports a specific, verifiable test result. It demonstrates failed lookup, but does not prove deletion.

“The service layer is badly designed.” — Hypothesis/opinion.
Makes a subjective judgement without specific evidence connecting the design to the failure.

“Traceback points to smartcare/services.py line 42 in the example.” — Evidence.
Identifies a location reported by a traceback, rather than proving the root cause. Line 42 is illustrative;  actual run showed services.py line 146 calling lookup and line 136 raising LookupError.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Expected behaviour: After cancellation, the appointment should remain stored and retrievable by its ID with status CANCELLED. FR-07 requires appointment history to be retained.
Observed behaviour: In test_cancelled_appointment_remains_in_store, lookup of appointment A2 returned None after cancellation, causing assert found is appointment to fail.
Minimal reproduction:1. Create a SmartCareDataStore.
2. Register patient P2 and practitioner PR2.
3. Create and store appointment A2.
4. Call appointment.cancel().
5. Call store.find_appointment('A2') and compare the result with the original appointment.

Hypothesis to investigate: The lookup method may filter out cancelled appointments even though they remain stored. A competing explanation is that cancellation removes the appointment.
Evidence to inspect: Inspect Appointment.cancel(), SmartCareDataStore.find_appointment() and list_appointments(). Check whether the cancelled object remains in the collection and whether lookup excludes its status. This distinguishes deletion from filtering



### A.3 Test defect or product defect

A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

The test should be modified because it is against FR-07, which mandates that history be kept, to anticipate cancelled appointments to be erased. It should verify that the appointment is still saved and accessible with the status CANCELLED. The programme also needs to be fixed if it removes or conceals it from lookup.

According to AC-04.2, a test that anticipates conflicts amongst multiple practitioners at the same time is flawed. Scheduled appointments for the same practitioner at the same time are subject to the conflict rule. The test should confirm that the different-practitioner reservation is approved while the same-practitioner reservation is denied.

Before altering the application code, a failing test should be verified for accuracy because expected behaviour must originate from the requirements.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.




The hypothetical method contains these code smells. Small refactorings can improve its structure while preserving required behaviour.

| Code smell | Small refactoring |
| --- | --- |
| Long method with mixed responsibilities | Extract small, clearly named helpers for validation and conflict checking. |
| Duplicate status strings | Replace magic status strings with the existing AppointmentStatus enum. |
| Direct collection manipulation | Use existing SmartCareDataStore methods to access and update records. |
| Printing inside service logic | Move display responsibilities to the console layer while preserving required output. |
| Four nested conditionals | Use guard clauses where they preserve validation order, exceptions and results. |

Proposed changes:

| Proposed change | Classification | Reason |
| --- | --- | --- |
| Rename appt to appointment | Refactoring | Improves readability without the change of behaviour. |
| Extract a repeated conflict helper | Refactoring | Removes duplication while preserving the conflict rule. |
| Add rescheduling | Feature | Introduces new capability. |
| Restore retained cancellation lookup | Repair | Corrects behaviour which violates history requirement. |
| Replace a magic status string with the existing enum | Refactoring | Improves clarity while preserving the status comparison. |

Return values, exceptions, validation rules, state transitions, and stored records must all be preserved during refactoring. Appointments that are cancelled must be kept on file and accessible. While other practitioners may reserve that time, scheduled appointments for the same practitioner at the same time must conflict. It is best to keep the current SmartCareDataStore border without implementing a new architecture. Before and after every refactoring, pertinent tests must be successful.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.



Actual failure: tests/test_starter.py::test_service_cancellation_and_guard.

- Expected behaviour: Cancelling an already cancelled appointment should raise ValueError through the domain transition guard. The appointment must remain stored and retrievable.
- Observed behaviour: The second cancellation raised LookupError('Appointment not found') instead of ValueError.
- Test line: tests/test_starter.py:175 calls cancel_appointment('A1') inside pytest.raises(ValueError).
- Application call path: The test calls AppointmentService.cancel_appointment() at smartcare/services.py:146. This calls AppointmentService.find_appointment(), which calls SmartCareDataStore.find_appointment(). The store returns None, causing services.py:136 to raise LookupError before appointment.cancel() is reached.
- Supporting requirement: FR-07 requires appointment history to be retained. The cancellation method's documented contract also requires invalid transitions to raise ValueError.

Three possible causes, ranked against the original failure evidence:

| Rank | Possible cause | Fit with available evidence | Discriminating check |
| --- | --- | --- | --- |
| 1 | Lookup filters out cancelled appointments. | Strongest fit: list_appointments() still contains the appointment, but lookup reports it missing after cancellation. | Inspect find_appointment() for a status filter and compare lookup results before and after cancellation. |
| 2 | The appointment ID or stored key changes during cancellation. | Could explain failed lookup while the object remains listed, but the failure output does not show an ID change. | Compare the appointment ID and stored dictionary key before and after cancellation. |
| 3 | Cancellation removes the appointment from storage. | Weakest fit: the preceding assertion confirms list_appointments() still returns the appointment. The project also has no public delete operation. | Inspect Appointment.cancel() and the cancellation service for collection mutation, then check whether the object remains stored. |

Inspection of the supplied faulty code confirmed the first cause: find_appointment() explicitly excluded appointments whose status value was "cancelled". The appointment was retained but hidden from lookup.

A traceback identifies the execution path and where the failure surfaced. It does not establish why the store returned None. Identifying the root cause requires checking runtime values, the relevant code and the required behaviour.

This analysis was reconstructed from the original failure output and inspected code after repair; it is not a claim that these ranked hypotheses were saved before editing.
### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Classification responses (1–5, each with reason):
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: 
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: 


Changing code immediately can lead to guessing, hiding the real cause or introducing new defects. A failure may come from the application, an incorrect test or the environment. First, reproduce the failure, check the expected behaviour against requirements, record a hypothesis and inspect evidence. Then make the smallest justified repair and run focused and full regression tests.

Classification responses (1–5, each with reason): See A.1.

Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: See A.2. The entry was reconstructed after repair, as stated there.

Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: See A.5.


## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 
- Baseline test command / working directory / observed result / evidence: 
- Clean preparation SHA if a record-only commit followed Stage 7: 
- Branch and preparer / how teammates obtained this branch: 
- Downloaded tool version, source SHA256 and --check outcome: 
- --apply and --verify output summaries / artefact references: 
- Bounded diff inspected and recovery location (not committed): 
- Prepared faulty-state commit SHA: 
- Preparation or recovery issues and resolution, if any: 
- Initial prepared full-suite command / result / key failures: 



- Stage 7 code SHA and requirement baseline: Not yet verified. Retrieve the passing integrated Stage 7 SHA and requirement version from the Stage 7 record. Relevant requirements include FR-07 (retained appointment history) and AC-04.2 (same-practitioner/time conflicts).

- Baseline test command / working directory / observed result / evidence: The original passing Stage 7 run has not yet been verified from its record. The later Stage 8 failing run is recorded below and is not a passing baseline.

- Clean preparation SHA if a record-only commit followed Stage 7: Not yet verified from Git history.

- Branch and preparer / how teammates obtained this branch: Work was performed on debug/stage08. Preparer identity and teammates' actual branch access steps still need recording.

- Downloaded tool version, source SHA256 and --check outcome: Not yet verified. Retrieve the actual utility details and original preparation output from the preparer or tutor.

- --apply and --verify output summaries / artefact references: Original preparation outputs have not yet been supplied. These outcomes cannot be confirmed from the test results alone.

- Bounded diff inspected and recovery location (not committed): The project/.stage8_faults folder was visible in PyCharm. Its recovery contents, original preparation diff and exclusion from Git still need verification.

- Prepared faulty-state commit SHA: The initial failing run was performed at d44b1c109d201641974dcba38e4095974e7018d8. Confirm from the preparation history whether this is the prepared faulty-state checkpoint.

- Preparation or recovery issues and resolution, if any: Original utility preparation issues are not yet verified. During test setup, pytest was missing from the active virtual environment. Installing the supplied requirements-dev.txt dependencies allowed the tests to run.

- Initial prepared full-suite command / result / key failures:
  - Working directory: ~/Documents/st1-assignment-3/project
  - Command: python -m pytest -q
  - Observed result: 3 failed, 13 passed in 0.05s.
  - tests/test_stage07.py::test_cancelled_appointment_remains_in_store: lookup returned None instead of the retained appointment.
  - tests/test_starter.py::test_conflict_rule_and_different_practitioner: the same-practitioner/time booking did not raise ValueError.
  - tests/test_starter.py::test_service_cancellation_and_guard: the second cancellation raised LookupError instead of ValueError.
  - Evidence: Original failing terminal output supplied during debugging. Add its saved repository artefact link.
## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: A second scheduled booking for the same practitioner at the same datetime was accepted instead of raising ValueError.

- Expected behaviour and requirement: FR-05 / AC-04.1 require rejection of a same-practitioner scheduled conflict. AC-04.2 permits different practitioners at the same time. A rejected booking must leave stored state unchanged.

- Minimal synthetic reproduction steps:
  1. Create a shared SmartCareDataStore and AppointmentService.
  2. Register patient P1 and practitioners D1 and D2.
  3. Book A1 for P1 with D1 at 09:00 on 1 October 2026.
  4. Attempt A2 with D1 at the same time; expect ValueError.
  5. Book A3 with D2 at that time; expect success.

- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner failed at line 152 with: Failed: DID NOT RAISE <class 'ValueError'>. The failure occurred before the different-practitioner assertion.

- Human hypothesis and intended checks: See E, F8-01. No independent pre-assistance hypothesis was saved; the retrospective explanation is disclosed there.

- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.has_practitioner_conflict() compared practitioner IDs using !=. This ignored appointments belonging to the requested practitioner and could incorrectly flag different practitioners.

- Smallest justified fix / diff / why other behaviour is preserved: Changed the practitioner comparison from != to ==. The date/time, scheduled-status and excluded-appointment conditions remained unchanged during this repair. The later enum change was committed separately as refactoring.

- Repair SHA / focused verification result: Repair checkpoint 3f24502d16277ec256e51cdc96ce123d9861c2fd. The full suite passed 16 tests in 0.01s after both repairs. A later focused run after the enum refactor passed 1 test in 0.02s. This later run is not claimed as an immediate post-repair focused run. See G/H for shared evidence and any additional regression results.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: Looking up a cancelled appointment returned None even though it remained stored. Repeated service cancellation raised LookupError instead of ValueError.

- Expected behaviour and requirement: FR-06/07 and BR-07 require guarded cancellation and retained history. FR-08 supports lookup, and AC-05.2 protects retained history. The same cancelled object must remain retrievable. Repeated cancellation must raise ValueError without changing state.

- Minimal synthetic reproduction steps:
  1. Create a SmartCareDataStore.
  2. Register patient P2 and practitioner PR2.
  3. Create and store appointment A2.
  4. Call appointment.cancel().
  5. Call store.find_appointment('A2'); expect the original object.
  6. In the service scenario, cancel an appointment twice; expect the second cancellation to raise ValueError while retaining the cancelled object.

- Meaningful failing test path/name and exact relevant failure: tests/test_stage07.py::test_cancelled_appointment_remains_in_store failed at line 53 because assert found is appointment received None. The related tests/test_starter.py::test_service_cancellation_and_guard failed at line 175 because repeated cancellation raised LookupError('Appointment not found') instead of ValueError.

- Human hypothesis and intended checks: See E, F8-02. No independent pre-assistance hypothesis was saved; the retrospective explanation is disclosed there.

- Supported root cause and inspected code/runtime evidence: SmartCareDataStore.find_appointment() explicitly excluded appointments whose status value was "cancelled". The service test confirmed retained list membership. The object was hidden from lookup rather than deleted. Service lookup converted None into LookupError before the cancellation guard was reached.

- Smallest justified fix / diff / why other behaviour is preserved: Removed the cancelled-status filter from find_appointment(). ID validation, trimming, matching and the None result for a valid missing ID remained unchanged. The service and domain cancellation methods were unchanged.

- Repair SHA / focused verification result: Cancellation repair commit 6eb84bc799e0ecc696ad828c788fa146af5ca646. Both cancellation tests passed within the later full-suite run at 3f24502d16277ec256e51cdc96ce123d9861c2fd: 16 passed in 0.01s. A separate focused result at the cancellation repair commit has not been verified from the supplied evidence. See G for shared evidence and any additional regression results.
## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: 



- Likely cause and why plausible: No independent hypothesis was saved before AI assistance. Retrospective explanation: lookup filtering could explain why a cancelled appointment remained in list_appointments() but could not be found by ID. This explanation was developed with ChatGPT assistance.

- Evidence to inspect / competing explanation / discriminating check: Compare find_appointment() with list_appointments() after cancellation and inspect Appointment.cancel(). A competing explanation is removal from storage. Checking whether the same object remains stored distinguishes filtering from removal.

- Member and saved sequence/time or commit showing this preceded consultation: No pre-consultation evidence is available. This entry was written after AI-assisted diagnosis and repair. Record owner: [enter actual member name]. The missed sequence needs tutor guidance.


Actual prompt / output reference and member: Pending actual GitHub Copilot consultation. Earlier diagnosis and repair were assisted by ChatGPT, as recorded in E.

1. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
2. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
3. Ranked suggestion and evidence-based evaluation: Pending Copilot response.

Final human conclusion and comparison with initial hypothesis: Code inspection identified a cancelled-status filter in SmartCareDataStore.find_appointment(). Removing that filter restored lookup of retained cancelled appointments. Comparison with Copilot's actual findings remains pending. No independent initial human hypothesis was saved.


### F8-02 human entry
Likely cause and why plausible: - Likely cause and why plausible: No independent hypothesis was saved before AI assistance. Retrospective explanation: an incorrect practitioner comparison could explain why a second scheduled booking for the same practitioner and time was accepted. This explanation was developed with ChatGPT assistance.

- Evidence to inspect / competing explanation / discriminating check: Inspect has_practitioner_conflict() and its call from book_appointment(). Competing explanations include the conflict check being skipped or the date/time comparison not matching. Check that the helper is called, compare the input times and inspect the practitioner equality condition.

- Member and saved sequence/time or commit showing this preceded consultation: No pre-consultation evidence is available. This entry was written after AI-assisted diagnosis and repair. Record owner: [enter actual member name]. The missed sequence needs tutor guidance.


## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review

Actual prompt / output reference and member: Pending actual GitHub Copilot consultation. Earlier diagnosis and repair were assisted by ChatGPT, as recorded in E.

1. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
2. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
3. Ranked suggestion and evidence-based evaluation: Pending Copilot response.

Final human conclusion and comparison with initial hypothesis: Code inspection identified a cancelled-status filter in SmartCareDataStore.find_appointment(). Removing that filter restored lookup of retained cancelled appointments. Comparison with Copilot's actual findings remains pending. No independent initial human hypothesis was saved.

### F8-02 Copilot review

Actual prompt / output reference and member: Pending actual GitHub Copilot consultation. Earlier diagnosis and repair were assisted by ChatGPT, as recorded in E.

1. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
2. Ranked suggestion and evidence-based evaluation: Pending Copilot response.
3. Ranked suggestion and evidence-based evaluation: Pending Copilot response.

Final human conclusion and comparison with initial hypothesis: Code inspection identified an incorrect practitioner comparison in has_practitioner_conflict(). Changing != to == restored the same-practitioner conflict check. The full suite subsequently passed all 16 tests. Comparison with Copilot's actual findings remains pending. No independent initial human hypothesis was saved.
### F8-01 Copilot review

Actual prompt / output reference and member: Retrospective GitHub Copilot consultation performed by Yashmeen Kaur after ChatGPT-assisted repairs. Add the saved prompt/output link. The original human-first sequence was not followed, as disclosed in E.

1. Ranked suggestion: The practitioner comparison is inverted.
   - Evidence check: Inspect the original has_practitioner_conflict() condition and compare it with the failing same-practitioner test.
   - Observed evidence: The original condition used != for practitioner IDs. The test booked D1 twice at the same datetime and failed because ValueError was not raised. Changing the comparison to == was followed by passing tests.
   - Classification: Correct; supported by the supplied code and regression results.
   - Decision: Accept. The comparison contradicts the same-practitioner conflict rule and explains the observed failure.

2. Ranked suggestion: The datetime or scheduled-status condition does not match.
   - Evidence check: Compare the stored datetime and status with the helper arguments.
   - Observed evidence: The test uses the same when value for both bookings. No separate runtime inspection of all predicate values was recorded. The practitioner-only repair made the test pass without changing the datetime or status checks.
   - Classification: Plausible but unverified as a general possibility; not supported as the cause of this failure.
   - Decision: Reject as the diagnosed cause. Retain it as a check if a different conflict failure occurs.

3. Ranked suggestion: The booking path skips the helper or uses another store.
   - Evidence check: Inspect the service call and shared-store setup; runtime tracing could confirm the actual call and instance.
   - Observed evidence: The supplied service calls self.data_store.has_practitioner_conflict() before insertion. Correcting only the helper comparison resolved the test failure. No separate runtime call trace was recorded.
   - Classification: Weakly supported alternative, not established as the cause.
   - Decision: Reject as the diagnosed cause because the inspected call path and successful minimal repair support the predicate defect.

Final human conclusion and comparison with initial hypothesis: The supported cause was the inverted practitioner comparison. Copilot's first-ranked suggestion agreed with the already completed diagnosis. This was a retrospective review, not an independent diagnosis recorded before repair. Copilot also correctly identified that the original test did not establish unchanged stored state after a rejected booking; this needs an explicit regression assertion.

### F8-02 Copilot review

Actual prompt / output reference and member: Retrospective GitHub Copilot consultation performed by Yashmeen Kaur after ChatGPT-assisted repairs. Add the saved prompt/output link. The original human-first sequence was not followed, as disclosed in E.

1. Ranked suggestion: Store lookup skips cancelled appointments.
   - Evidence check: Inspect the original lookup condition and compare lookup with retained list membership.
   - Observed evidence: The original method explicitly excluded status.value == "cancelled". The tests showed failed lookup while the cancelled object remained listed. Removing only the status filter was followed by passing cancellation tests.
   - Classification: Correct; supported by code and test evidence.
   - Decision: Accept. The filter hides retained history and prevents repeated cancellation from reaching the domain guard.

2. Ranked suggestion: The appointment ID does not match the lookup argument.
   - Evidence check: Compare the stored ID with the trimmed lookup argument, including case and whitespace.
   - Observed evidence: The reproduction uses A2 for both storage and lookup. Removing the status filter resolved the failure without changing ID handling. No separate runtime repr comparison was recorded.
   - Classification: Plausible alternative, but not supported as the cause of this failure.
   - Decision: Reject as the diagnosed cause because the minimal filter repair resolved lookup without ID changes.

3. Ranked suggestion: Lookup and listing use different store state.
   - Evidence check: Compare store identities and the object seen by lookup and listing.
   - Observed evidence: The direct failing test creates one store and performs insertion and lookup through it. The service test uses the shared store. No separate runtime identity trace was recorded.
   - Classification: Weakly supported alternative, inconsistent with the supplied direct reproduction.
   - Decision: Reject as the diagnosed cause. The explicit status filter better explains both failures.

Final human conclusion and comparison with initial hypothesis: The appointment was retained but excluded from lookup. The service converted None into LookupError before the cancellation guard was reached. Copilot's first-ranked suggestion confirmed the already completed diagnosis. No independent initial human hypothesis was saved. Copilot also correctly noted that LookupError alone does not demonstrate unchanged state after repeated cancellation; that behaviour needs explicit regression assertions.
## G. Failing to passing regression evidence

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: 
Unrelated failures investigated / resolution: 

Both original failures were observed in the same full-suite run. Both repaired behaviours were subsequently verified in the passing full suite.

Working directory for the recorded runs: ~/Documents/st1-assignment-3/project.

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
| --- | --- | --- | --- |
| F8-01 before repair | d44b1c109d201641974dcba38e4095974e7018d8 | python -m pytest -q; project directory above | Cancellation lookup returned None instead of the original appointment. Repeated cancellation raised LookupError instead of ValueError. See original failure output, evidence reference below. |
| F8-01 after repair | Cancellation repair committed at 6eb84bc799e0ecc696ad828c788fa146af5ca646; passing verification captured later at 3f24502d16277ec256e51cdc96ce123d9861c2fd | python -m pytest -q; project directory above | Both cancellation tests passed within the later 16-test full suite. A separate test result at the first repair commit has not been verified. See passing evidence below. |
| F8-02 before repair | d44b1c109d201641974dcba38e4095974e7018d8 | python -m pytest -q; project directory above | test_conflict_rule_and_different_practitioner failed with: DID NOT RAISE <class 'ValueError'>. See original failure output below. |
| F8-02 after repair | 3f24502d16277ec256e51cdc96ce123d9861c2fd | python -m pytest -q; project directory above | Conflict test passed within the full suite. A separate focused-run result has not been verified. See passing evidence below. |
| Full suite after both repairs, before refactor | 3f24502d16277ec256e51cdc96ce123d9861c2fd | python -m pytest -q; project directory above | 16 passed in 0.01s. See passing evidence below. |

Evidence references:- [Focused regression results](evidence/regressions_after.txt)
- [Full-suite results](evidence/full_suite_after_regressions.txt)
- Original failure output: 3 failed, 13 passed in 0.05s. Repository artefact link still to be added.
- Passing output: Screenshot showing SHA 3f24502d16277ec256e51cdc96ce123d9861c2fd and 16 passed in 0.01s. Repository artefact link still to be added.

Explain how  assertions detect each relevant incorrect result and protect previous behaviour:

For F8-01, assert found is appointment checks that lookup returns the original retained object rather than None or a replacement. The service cancellation test checks that cancellation returns the same object, sets its status to CANCELLED and retains it in list_appointments(). Its pytest.raises(ValueError) assertion verifies that repeated cancellation reaches the domain transition guard instead of failing lookup.

For F8-02, pytest.raises(ValueError) detects acceptance of a conflicting same-practitioner/time booking. The following assertion checks that a different practitioner can be booked at that time. Together, these protect against both missed conflicts and incorrect rejection of valid bookings.

The full suite also reruns the earlier domain and service tests to detect regressions in previously tested behaviour.

Unrelated failures investigated / resolution:

No unrelated test failures were observed in the supplied initial run. The two cancellation failures were explained by the same lookup filter defect; the third failure concerned the practitioner conflict comparison. The earlier missing-pytest error was an environment setup issue resolved by installing requirements-dev.txt.
### Additional focused regression verification

The two focused tests were added after repairs and refactoring.

- Working directory: ~/Documents/st1-assignment-3/project.
- Focused command: python -m pytest tests/test_regressions.py -v.
- Actual result: 2 passed in 0.02s.
- Full-suite command: python -m pytest -q.
- Actual result: 18 passed in 0.01s.
- [Test evidence](evidence/regression_tests_18_passed.png).
- [Regression tests](../project/tests/test_regressions.py).

Execution of these new tests against the original faulty checkpoint is not yet verified.
## H. Refactoring decision and before/after verification



- Smell and exact location: A magic status string in SmartCareDataStore.has_practitioner_conflict(), located in project/smartcare/data_store.py.

- Small proposed structural change / why justified: Replace appointment.status.value == "scheduled" with appointment.status == AppointmentStatus.SCHEDULED. This uses the existing enum and removes a literal status string without introducing new functionality.

- External behaviour to preserve / relevant tests: Only scheduled appointments for the same practitioner at the same time should conflict. Different practitioners remain bookable at that time. The excluded appointment ID remains excluded. Appointment lookup, cancellation history, return values and exceptions must remain unchanged. Relevant tests include test_conflict_rule_and_different_practitioner and the existing cancellation tests.

- Before result: See G for the full passing suite at 3f24502d16277ec256e51cdc96ce123d9861c2fd: 16 passed in 0.01s. Confirm the current suite passes immediately before editing.
- Actual change / diff / separate refactor SHA: Replaced appointment.status.value == "scheduled" with appointment.status == AppointmentStatus.SCHEDULED in SmartCareDataStore.has_practitioner_conflict(). The inspected diff contained one insertion and one deletion. Separate refactor SHA: c143ba3b8009e04d43a786413a6a5cdb9ea8e349.

- Focused and full after-refactor commands / working directory / results / evidence:
  - Working directory: ~/Documents/st1-assignment-3/project.
  - Focused command: python -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v.
  - Focused result: 1 passed in 0.02s.
  - Full command: python -m pytest -q.
  - Full result: 16 passed in 0.01s.
  - These results were captured after the edit and before committing it.
  - Evidence: Add the saved test-output screenshot link.
  - Result: Accepted. The enum comparison removes the magic status string. The focused test and full regression suite passed, supporting preservation of the tested behaviour.## I. Git, human review and integration
## I. Git, human review and integration

- Issues for both defects / refactor scope and owners:
  - F8-01: Restore lookup of retained cancelled appointments. Owner: Yashmeen . Issue: https://github.com/jaidenchandra/st1-assignment-3/issues/6
  - F8-02: Correct the same-practitioner/time conflict comparison. Owner: Yashmeen. Issue: https://github.com/jaidenchandra/st1-assignment-3/issues/7
  - Refactor: Replace the scheduled-status string comparison with the existing AppointmentStatus enum. Owner: Yashmeen . Completion and verification: see H.

- Branch / prepared, repair and refactor checkpoints:
  - Branch: debug/stage08.
  - Initial tested faulty-state checkpoint: d44b1c109d201641974dcba38e4095974e7018d8. Preparation verification: see B.
  - Cancellation lookup repair: 6eb84bc799e0ecc696ad828c788fa146af5ca646.
  - Both-repair checkpoint: 3f24502d16277ec256e51cdc96ce123d9861c2fd.
  - Refactor checkpoint: See H; separate refactor SHA still needs recording.

- PR link and another member's reviewer identity: PR: Reviewer: Jaiden (jaidenchandra) . Review status: Pending verification.

- Key human feedback, difference from Copilot findings and response/outcome: Pending actual human review. Record the reviewer's feedback, how it compares with the actual Copilot findings in F, and the changes or explanations provided in response.

- Actual review approval / merge evidence: Pending approval and merge. Add the actual approval and merge links after these occur.

- Integrated code SHA and team pull/retest command / working directory / result: Pending post-merge verification. The existing 16-test passing result applies to the repair branch checkpoint and does not establish that the integrated branch passes.

- Evidence-only later SHA / explanation if different: Pending final evidence commit. If documentation is committed after the verified integrated code, record its SHA and confirm whether it changes evidence only.


## J. Required reflections
1. Which Copilot diagnosis appeared convincing but lacked evidence?

  Since no real GitHub Copilot reaction has been noted in F, this reflection is still pending. Although ChatGPT helped with the repairs, Copilot cannot provide its recommendations. After consultation, compare the code and test evidence to the real Copilot idea that has the least amount of support.


2. What evidence changed your group's view?

   
The service test verified that the appointment was still in list_appointments(), but the cancellation test revealed that lookup returned None. This separated deletion from unsuccessful lookup. Examining find_appointment() showed that cancelled appointments were filtered out. A same-practitioner/time booking was approved for the conflict defect because of the failing test and the != practitioner comparison. All 16 tests were successful following the repairs, confirming both diagnoses.

3. How did regression tests protect the refactoring?

The regression suite provides checks for booking conflicts, cancellation, retained history and previously tested domain and service behaviour. Running it before and after the enum refactor helps detect unintended changes. However, the supplied 16-test passing result was recorded after repairs and before refactoring. Behaviour preservation can only be confirmed once the actual after-refactor results are recorded in H.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Reproduce the failure, record expected and observed behaviour, check the requirements, and form a hypothesis to investigate using evidence.

2. Where should expected behaviour come from during debugging?

Response: The agreed requirements and acceptance criteria, supported by documented contracts. A failing test must also be checked against these sources.

3. What is a debugging hypothesis?

Response: A testable explanation of a failure's possible cause. Evidence is used to support or reject it.

4. What is a regression test and why is it retained?

Response: A test that checks previously required behaviour still works after changes. It is retained to detect returning defects or unintended effects.

5. What is meant by root cause?

Response: The underlying fault that explains the observed failure and is supported by investigation, rather than just the location where an error appears.

6. What is refactoring?

Response: Improving the internal structure of code without changing its externally observable behaviour.

7. What is a swallowed exception?

Response: An exception that is caught and suppressed without appropriate handling or reporting, potentially hiding a failure.

8. What is a code smell?

Response: A sign that code may need structural improvement, such as duplication, long methods or deeply nested conditionals. It does not necessarily indicate a defect.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As unverified hypotheses. Check each suggestion against requirements, code and runtime evidence before accepting, modifying or rejecting it.

10. What is the Stage 8 engineering rule?

Response: Reproduce and record the failure, form human hypotheses before consulting Copilot, verify diagnoses with evidence, make the smallest justified repair, and retain regression tests. Refactor only from a passing baseline, verify behaviour afterward, and complete human review and integrated testing.

## L. Completion and handover


- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: Pending the merge and integrated retest described in I. The verified repair-branch checkpoint is 3f24502d16277ec256e51cdc96ce123d9861c2fd, where python -m pytest -q returned 16 passed in 0.01s. This is not yet evidence of integrated verification.

Submitted SHA and evidence-only difference, if any: Pending final submission checkpoint. Record the submitted SHA and explain any documentation-only difference from the tested code SHA.

Unresolved issues or incomplete checks / owner / next action:
- Record owner: Yashmeen
- B: Verify the passing Stage 7 baseline and original preparation evidence.
- E/F: No independent pre-assistance hypotheses were saved. Keep the retrospective disclosure, obtain tutor guidance and complete the actual Copilot review.
- G: Add accessible evidence links and any missing focused verification results.
- H: Complete or verify the separate refactor commit and passing before/after tests.
- I: Record actual member contributions, issue and PR links, another member's review, approval, merge and integrated retest.
- J: Finish reflections using the actual Copilot and refactoring results.
- Confirm earlier project artefacts are preserved and recovery metadata is excluded from Git.

Handover note: Both identified defects have been repaired, and all 16 existing tests passed at the recorded repair checkpoint. Continue with the same repository and preserve earlier tests and stage records. Stage 8 remains incomplete until the outstanding evidence, refactoring, review and integration checks are resolved. Begin Stage 9 only after Stage 8 has been integrated, verified and recorded.
