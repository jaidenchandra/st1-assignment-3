# Stage 12 activities and evidence

**Group/tutorial:** Thursday 2:30-4:30 Group 2

**Members and UG/PG applicability:**  
Musab Master – Stage 6 implementation and verification.  
Saja Nasser – Stage 7 implementation and testing.  
Yashmeen Dandiwal – Stage 8 debugging and refactoring.  
Jaiden Chandra – Stage 9 queries and console integration, testing and Stage 12 release verification.  

UG pathway only. Stage 10 and Stage 11 PG extensions are not applicable.

---

## A Release scope and starting SHA

**Release label/version and requirements baseline:**  
SmartCare UG Final Release Candidate – Stage 12. Common UG scope covers the accumulated requirements from Stages 6, 7, 8 and 9, including registration, lookup, booking, conflict prevention, cancellation/history, practitioner appointment queries and interactive console operation.

**Common starting SHA / branch / applicable members:**  
Branch: `main`  
SHA: `c8c6ea1c3a592932f8beabdd99ffb53e05207578`  
Applicable to UG/common members.

**PG starting SHA / branch / applicable members or not applicable:**  
Not applicable to the UG pathway. Stage 10 and Stage 11 PG extension work was not undertaken.

**Working-state review and approved integration:**  
Stage 9 was integrated and verified before Stage 12. The previously recorded Stage 9 integration checkpoint was `3112b59d36889b767a55228a0e589583ac8e30a7`. The integrated suite passed before Stage 12 release verification.

**Protected common candidate and PG differences:**  
The common UG candidate is based on integrated `main`. No PG rescheduling or assurance extensions are included.

**Feature freeze / owner / verifier:**  
Feature freeze applied for Stage 12 release verification. No further feature development is planned. Owner: Jaiden Chandra (U3321093). Verifier: Musab Master.

---

## B Requirements and release readiness matrix

**Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify:**

**Do not release yet.** Passing tests alone are not sufficient for a release decision. The incomplete README affects reproducibility, the unreviewed dependency represents an unresolved release risk, and the undocumented limitation means users do not have an accurate description of the system. These gaps should be corrected and the candidate rechecked before release.

### Tutorial activity 2 and actual readiness matrix

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Cancellation changes status without deleting the Appointment; cancelled appointment remained findable/listable | `project/smartcare/domain.py`, `project/smartcare/services.py`, `project/tests/test_workflows.py` | Musab Master | Yes | None known |
| Architecture responsibilities are appropriate | Domain, store, service, pure-query and console responsibilities remain separated | `project/smartcare/domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | Musab Master | Yes | None known |
| Rescheduling is safe — PG only | Not applicable to UG pathway | N/A | N/A | N/A | PG only |
| AI use is responsible — common recheck / PG assurance | Copilot review findings were checked by a human and one proposed validation duplication was rejected with test evidence | `stage09/stage09_activities_and_evidence.md` | U3321093 | Yes | Preserve AI evidence |
| System is maintainable | Focused modules, type hints, docstrings, tests and separation of responsibilities | `project/smartcare/`, `project/tests/` | Musab Master | Yes | Production concerns remain out of scope |
| FR-01–03 register/find and validation | Patient and practitioner registration/find behaviour covered by accumulated tests and console demo | `project/tests/test_starter.py`, `project/tests/test_stage07.py` | Musab Master | Yes | None known |
| FR-04–05 booking/conflict rules | Valid booking succeeds; same practitioner/time conflict rejected; different practitioner same time allowed | `project/tests/test_starter.py`, `project/tests/test_regressions.py`, Stage 12 demo | Musab Master | Yes | None known |
| FR-06–08 cancellation/history/find | Cancellation retained object and same-session lookup/history | `project/tests/test_workflows.py`, Stage 12 demo | Musab Master | Yes | None known |
| FR-09 and QRY/FP listing/filter/order/purity | Query tests verify practitioner filtering, status handling, deterministic ordering and non-mutation | `project/tests/test_queries.py`, `project/tests/test_workflows.py` | Musab Master | Yes | None known |
| UI full console sequence and error recovery | `python main.py --interactive` completed; errors recovered without terminating session | Stage 12 demo | U3321093 | Yes | None known |
| Session-only scope / FR-10 retired | Application explicitly uses in-memory session-only data | README / console / evidence | Musab Master | Yes | Accepted scope limitation |
| PG RES and assurance integration | Not applicable | N/A | N/A | N/A | UG pathway |

---

## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence |
|---|---|---|---|---|---|
| Complete common | Python 3.15.2; pytest 8.3.5 | `project/` — `python -m pytest -q` | `c8c6ea1c3a592932f8beabdd99ffb53e05207578` | **60 passed in 0.08s** | Terminal output and accumulated tests under `project/tests/` |
| Complete PG if applicable | Not applicable – UG pathway | N/A | N/A | N/A | N/A |
| Affected focused checks after correction | Complete `test_starter.py` restored and full suite rerun | `project/` — `python -m pytest -q` | Stage 9 integration candidate | **60 passed** | `project/tests/test_starter.py` |
| Full integrated recheck | Python 3.15.2 | `project/` — `python -m pytest -q` | `c8c6ea1c3a592932f8beabdd99ffb53e05207578` | **60 passed in 0.08s** | Terminal verification |

**Prior assertions preserved / reviewed test diff:**  
Existing accumulated tests were preserved. The damaged/truncated local `test_starter.py` was restored rather than weakening or deleting assertions. The complete suite subsequently passed.

**Remaining failure / limitation:**  
No known failing automated tests. The main intentional limitation is session-only in-memory storage; data is lost on exit.

---

## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence |
|---|---|---|---|---|
| Problem and stakeholders | SmartCare synthetic patient/practitioner appointment system | Support registration, booking and appointment management within one session | Required workflows operated within one shared session | `project/smartcare/console.py` and manual demonstration |
| Register and find Patient and two Practitioners | P1/Alex Example; D1/Taylor Example/General Practice; D2/Jordan Example/Cardiology | Records remain available during same session | Registration and same-session use succeeded | Manual interactive demonstration |
| Valid booking | A1, P1, D1, `2026-10-01 09:00` | Registered participants produce a SCHEDULED appointment | Booking succeeded | Manual demonstration + automated tests |
| Same practitioner exact-time conflict rejected | Second D1 appointment at same date/time | Prevent practitioner double-booking | Conflict was rejected and existing appointment remained unchanged | `test_starter.py`, `test_regressions.py` |
| Different practitioner same time allowed | A2, P1, D2, `2026-10-01 09:00` | Different practitioner may use same time | Booking succeeded | Manual demonstration + automated tests |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then retrieve A1 | Cancellation changes status without deletion | A1 remained stored and retrievable as CANCELLED | `test_workflows.py` and manual demonstration |
| Invalid/repeated cancellation rejected | Attempt to cancel A1 again after it is already CANCELLED | Invalid state transition must be rejected without changing history | Second cancellation was rejected with `ValueError`; appointment remained CANCELLED and retrievable | Cancellation tests and service/domain behaviour |
| Default all-status listing | D1 listing with blank status | All statuses including cancellation history returned | Cancelled A1 remained visible | `test_workflows.py` and manual listing |
| Explicit filtering / empty vs unknown / deterministic order | Status filters and query tests | Correct filters, empty-list behaviour, errors and stable ordering | Automated query/workflow tests passed | `test_queries.py`, `test_workflows.py` |
| Invalid date/status/menu/lookup recovery and continued operation | Invalid menu choice, malformed date and unknown lookup | Expected error printed without stopping the session | Menu recovered and continued accepting subsequent actions | Manual Stage 9/12 console testing |
| Session-only limitation and normal exit | Menu option `0` | Clean exit; session data not persisted | Program exited normally and data is intentionally session-only | `console.py`, README |
| One meaningful requirement-linked pytest test explained | `test_sorting_uses_datetime_then_appointment_id` | QRY-03 deterministic ordering | Verifies primary date/time ordering and appointment-ID tie-break | `project/tests/test_queries.py` |
| Architecture and one actual AI decision / known limitation | Copilot suggested possible additional practitioner ID validation | Human checks existing datastore validation and test evidence | Suggestion rejected as duplicated validation; existing blank-ID behaviour already passes | `stage09/stage09_activities_and_evidence.md` |
| PG reschedule identity/participants/time and no-op | Not applicable | PG only | N/A | N/A |
| PG conflict/invalid status/failure non-mutation | Not applicable | PG only | N/A | N/A |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | PG only | N/A | N/A |

**Stable demo owner / fresh process / command:**  
Owner: Jaiden Chandra (U3321093).  
Command: `python main.py --interactive` from `project/`.  
The demonstration was run using synthetic data in a fresh process.

**PG demonstrations through service/tests or not applicable:**  
Not applicable – UG pathway.

---

## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | Responsibilities remain separated | No change; full suite passed |
| PascalCase and snake_case naming | `project/smartcare/` | Classes use PascalCase; functions/variables use snake_case | No change |
| Useful type hints and meaningful docstrings | SmartCare modules | Type hints/docstrings used for major public functions/classes | No change |
| Four-space indentation and imports/layout | SmartCare modules | Code executes and pytest imports successfully | No change |
| Focused methods / duplication / dead or commented code | SmartCare modules | Methods remain focused; no major dead-code issue identified | No change |
| Globals / leakage / unnecessary inheritance or frameworks | SmartCare modules | No global datastore dependency or unnecessary framework introduced | No change |
| No SQLite/persistence/repository ABCs/speculative features | repository | No persistence/rescheduling/speculative architecture added | No change |
| Synthetic data / secrets / dependencies / provenance | demo/tests and requirements | Synthetic records only; pytest development dependency pinned | Final package must exclude secrets/cache/environment files |
| Significant common Copilot contributions and human verification | Stage 9 AI evidence | Copilot reviewed Stage 9 code; findings were not accepted automatically | Human checked against contracts/tests |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | N/A | UG pathway | N/A |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Explicit practitioner ID validation might be needed in service | `AppointmentService.list_practitioner_appointments` | Existing datastore validation and blank-ID test checked | Reject – would duplicate existing validation responsibility | No code change; test already passed |

**Access route or approved equivalent / limitations:**  
AI review was performed through GitHub Copilot using selected Stage 9 source files. Copilot could not verify console/test behaviour when those files were not included in its supplied context.

**Available AI evidence and missing evidence honestly disclosed:**  
Stage 9 Copilot prompt, response summary and human decision are recorded. Where Copilot lacked source context, manual testing and pytest evidence were used instead rather than claiming Copilot verified those areas.

---

## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | root README / `project/README.md` | Musab Master | Verified |
| Out-of-scope capabilities and known limitations | README | Musab Master | Verified – session-only and production exclusions documented |
| Confirmed teaching Python version and dependency installation | README | Musab Master | Verified |
| Working directory / demo / interactive / test commands | README | Musab Master | Verified – commands documented |
| Repository structure and architecture responsibilities | README | Musab Master | Verified |
| Responsible AI summary / synthetic-data rule | README/evidence | Musab Master | Verified |
| Release label/version and SHA links | Stage 12 evidence | Musab Master | Tested candidate SHA recorded |

**Root README index and project/README verified:**  
Verified by Musab Master. Required purpose, scope, commands, limitations, architecture information and responsible-AI/synthetic-data information are present.

**Fresh clone or extracted ZIP / candidate identity:**  
Final extracted-ZIP comparison is completed during the submission packaging step. The source package must correspond to the final submitted repository candidate.

**Verifier and clean environment / actual version:**  
Verifier: Musab Master.  
Actual local release verification environment: Python 3.15.2 with pytest 8.3.5.

**Setup/run/test commands and observed results:**  

`python -m pip install -r requirements-dev.txt`  
`python main.py`  
`python main.py --interactive`  
`python -m pytest -q`

Observed regression result: **60 passed in 0.08s**.

**Missing local file or setup gap / remedy and recheck:**  
No known missing required local files or setup gaps after final working-copy verification.

---

## G Known limitations debt and release notes

**Delivered features:**  
Patient and practitioner registration and lookup; appointment booking; practitioner conflict prevention; appointment lookup and cancellation; retained cancellation history; practitioner appointment listing; optional status filtering; deterministic query ordering; interactive console workflow and error recovery.

**Important fixes:**  
Completed Stage 9 query/service/console integration. Restored the complete starter test file after a truncated local copy was identified during integration verification.

**Architecture/quality improvements:**  
Pure query functions separate collection processing from the data store and console. One shared store is retained for the entire interactive session. Services coordinate workflows while domain objects retain state-transition responsibilities.

**Known limitations:**  
Data is stored only in memory and is lost when the process exits. The application uses minute-precision local date/time input. It is a teaching application and does not include production authentication, authorisation, persistence, notifications, billing, clinical decision support or large-scale concurrency features.

**AI-assisted development note:**  
AI/Copilot was used for bounded implementation assistance and review. AI findings were checked against requirements, source code and tests, and were not accepted automatically.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only storage | Data is lost on exit | Expected scope | Add persistence only in a future production version | Accepted – intentional course scope |
| Limited production security/access control | Unsuitable for real clinical deployment | High for production, outside course scope | Add authentication/roles/audit controls in future | Accepted for teaching release |
| Local minute-precision datetime only | Does not handle timezone/advanced scheduling requirements | Medium for production | Add explicit timezone/scheduling policy later | Accepted for teaching release |

**Session-only synthetic data and minute-precision local time:**  
Accepted scope limitations. SmartCare uses synthetic data and does not persist records beyond the process. Date/time input is handled at minute precision using the supplied parser.

**Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions:**  
These are intentionally outside the Assignment 3 teaching scope and are not claimed as delivered features.

**Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations:**  
These areas would require additional engineering before production use and are not part of the current release requirements.

**Difference between accepted scope limit and unresolved required behaviour:**  
An accepted scope limit is behaviour deliberately excluded by the requirements, such as persistence. An unresolved required behaviour is a required feature that fails or lacks adequate evidence. No unresolved required behaviour is currently known from the passing regression suite and completed demonstration.

**PG assurance residual risks / owner / status or not applicable:**  
Not applicable – UG pathway.

---

## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Complete starter regression file | `test_starter.py` was found locally truncated during integrated verification | High because test collection failed | U3321093 restored known-good complete test file and merged repair | `fix/restore-test-starter` | Full suite rerun: 60 passed | None |
| Stage 9 blank practitioner validation | Copilot raised possible duplicated service validation concern | Low | Human reviewed datastore contract and existing blank-ID test | No change | Existing test passed + full suite passed | None |

**Justified no-change conclusion if no defect found:**  
No further product defect was identified during the final Stage 12 regression and demonstration. The remaining limitations are documented scope limitations rather than failures of required behaviour.

**Release blockers still open / status:**  
No known code/test blocker. Final packaging and submission remain to be completed.

---

## I Git review and integration evidence

**Issue / PR / diff links and reviewed SHA:**  
Stage 9 implementation branch: `feature/stage9-queries`  
Regression repair branch: `fix/restore-test-starter`  
Evidence is retained in Git history and the stage activity/evidence files.  
Tested release candidate SHA: `c8c6ea1c3a592932f8beabdd99ffb53e05207578`.

**Independent reviewer / feedback / response:**  
Musab Master acted as the verifier/reviewer. Review was approved with no changes required. The release candidate was additionally verified through the accumulated automated test suite and interactive demonstration.

**Integration commit / full recheck:**  
Integrated `main` was checked with:

`python -m pytest -q`

Actual result: **60 passed in 0.08s**.

**Tracked and untracked file inspection / cleanliness:**  
Before the final Stage 12 evidence commit, `git status` showed only `stage12/stage12_activities_and_evidence.md` as intentionally modified. No unexpected executable source changes were present.

**Secrets/staff material/caches/tool-metadata exclusion check:**  
Final source package must exclude `.git`, virtual environments, caches, secrets, real clinical/personal data, private QA artefacts and unrelated staff solution material.

**Candidate recovery plan / known-good SHA:**  
Known-good tested release candidate:  
`c8c6ea1c3a592932f8beabdd99ffb53e05207578`

Earlier Stage 9 integrated checkpoint:  
`3112b59d36889b767a55228a0e589583ac8e30a7`

Git history and these SHAs provide recovery points.

**Named substantive contributions:**  
Musab Master – Stage 6 implementation and verification.  
Saja Nasser – Stage 7 implementation and testing.  
Yashmeen Dandiwal – Stage 8 debugging/refactoring.  
Jaiden Chandra – Stage 9 query/listing/console integration, automated and manual verification, integration repair and Stage 12 release verification.

---

## J Human release decision

**Decision — READY WITH DOCUMENTED LIMITATIONS**

**Approver / rationale and evidence:**  
Approver/verifier: Musab Master.  
Review approved with no changes required. The accumulated regression suite passed with **60 tests**, the interactive end-to-end workflow was demonstrated successfully, the required UG functionality is integrated and the remaining limitations are explicitly documented.

**What risks remain / conditions / owners:**  
Session-only storage, lack of production authentication/authorisation, limited date/time handling, scalability and other production capabilities remain accepted teaching-scope limitations. These do not represent failures of the assessed UG requirements.

**Can the team explain the system:**  
Yes. The system can be explained in terms of its domain objects, shared datastore, services, pure query functions, console interface, conflict rules, cancellation history and tests.

**Can a change be recovered:**  
Yes. Git history, focused branches and known-good SHAs provide recovery points. Full regression tests can be rerun after restoration.

**Common decision / PG decision where different:**  
UG/common release candidate is ready with documented limitations. PG decision is not applicable.

---

## K Final tested release SHA

**Exact common tested SHA:**  
`c8c6ea1c3a592932f8beabdd99ffb53e05207578`

**Exact PG tested SHA or not applicable:**  
Not applicable – UG pathway.

**Final submitted SHA / repository URL:**  
Tested executable candidate SHA:  
`c8c6ea1c3a592932f8beabdd99ffb53e05207578`

Repository:  
`https://github.com/jaidenchandra/st1-assignment-3`

**Evidence-only later commit and difference explanation:**  
The Stage 12 activities/evidence file was completed after the executable candidate was tested. Any later commit containing only Stage 12 documentation/evidence does not alter executable SmartCare behaviour. If this evidence file is committed, its SHA should be recorded separately as an evidence-only commit.

**Executable changes after testing and re-verification:**  
No executable code changes were made after the tested candidate verification. Any future executable change would require the complete regression suite to be rerun and a new tested SHA recorded.

**Source ZIP name / SHA correspondence / extracted comparison:**  
The final source ZIP should be generated from the final submitted repository state while preserving the tested executable candidate identified above. Extracted contents should be checked against the repository and rerun using the documented commands.

---

## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README checked.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository candidate and exact tested SHA identified.
- [ ] One final source ZIP generated and checked.
- [x] `project/` source and all accumulated applicable tests included in repository.
- [x] All common applicable stage records retained; PG-only stages not applicable.
- [ ] Final ZIP exclusion check for `.git`, environments, caches and other excluded material.
- [x] No Stage 10/11 PG work is claimed for this UG-only group.
- [x] Group contributions and release evidence recorded.

**Confirmed assessment item/upload route:**  
Not required for this evidence record.

**Deadline/timezone:**  
Not required for this evidence record.

**Repository access arrangement:**  
Repository available at `https://github.com/jaidenchandra/st1-assignment-3`.

**Mixed-candidate upload arrangement:**  
Not applicable – UG-only group.

**Oral/video recording/accessibility arrangements:**  
No additional arrangement recorded in this evidence file.

**Remaining administration or release dependency:**  
Generate the final source ZIP, verify its contents/exclusions, record the evidence-only final SHA if the Stage 12 evidence file is committed, and submit through the required course process.

---

## M Formative questions

### 1. What is a release candidate?

A release candidate is a specific integrated version of the software that is believed to satisfy the release requirements and is frozen for final verification before submission or release.

### 2. What is feature freeze and why is it used?

Feature freeze means stopping new feature development while final verification is performed. It reduces the risk that late changes introduce new defects or invalidate existing evidence.

### 3. What is regression testing in a release context?

Regression testing reruns the accumulated test suite to ensure that integration, fixes or release changes have not broken behaviour that previously worked.

### 4. What is a known limitation?

A known limitation is a documented restriction or capability the system intentionally does not provide. It is different from hiding or ignoring a failed required behaviour.

### 5. What is technical debt?

Technical debt is a design, implementation or maintenance compromise that may be acceptable now but increases future work, risk or complexity.

### 6. What are release notes?

Release notes summarise what the release delivers, important fixes and quality changes, known limitations and other information needed to understand the released version.

### 7. What is software maintenance?

Software maintenance is the ongoing work of correcting defects, adapting software to changing requirements or environments, improving quality and managing technical debt after initial development.

### 8. What is the purpose of the individual demonstration/viva?

The demonstration/viva verifies that the student understands the system, requirements, architecture, tests, engineering decisions and personal contributions rather than relying only on submitted artefacts.

### 9. What should the final responsible-AI check establish before release?

It should establish what AI contributed, whether its suggestions were independently checked, whether any unsupported claims remain, and whether the human team retains responsibility for the final code, tests and release decision.

### 10. What is the main course conclusion about AI and the role of the software engineer?

AI can assist with coding, review and reasoning, but the software engineer remains responsible for requirements, architecture, verification, risk decisions, integration, maintainability and the correctness of the released system.

---

## N Reflection viva and handover

**Strongest evidence SmartCare is ready:**  
The strongest evidence is the combination of the full accumulated regression suite passing with **60 tests**, the successful interactive end-to-end demonstration and the traceability between requirements, implementation and tests.

**Weakest area:**  
The application remains a teaching-scale, session-only system and has not been designed for production security, persistence, concurrency or clinical deployment.

**How AI use changed from Stage 1 to Stage 12:**  
AI use became more bounded and verification-focused. Rather than treating generated output as automatically correct, AI suggestions were compared with requirements, code behaviour and tests, with human Accept/Modify/Reject decisions recorded.

**Start doing — engineering and AI use:**  
Start giving AI smaller, requirement-bounded review tasks and explicitly recording how each suggestion is verified.

**Stop doing — engineering and AI use:**  
Stop treating passing output or an AI recommendation as sufficient evidence without checking the relevant contract, state and regression behaviour.

**Continue doing — engineering and AI use:**  
Continue using focused branches, small changes, automated tests, manual workflow verification, code review and explicit evidence.

**What worked / caused rework / future delivery improvement:**  
Focused Stage 9 query/service/console work and automated testing worked well. Rework occurred when a starter test file became truncated and during working-directory/indentation issues. Future delivery would improve by checking `git status`, reviewing diffs before commits, protecting supplied tests and verifying integrated `main` immediately after every merge.

**One paragraph — If AI can write code why do we still need software engineers:**  
AI can generate or review code quickly, but it does not replace responsibility for understanding what the software must do, choosing architecture, protecting data integrity, evaluating trade-offs, diagnosing integration failures and deciding whether evidence is sufficient for release. In SmartCare, generated suggestions still had to be compared with domain contracts, existing datastore behaviour and automated/manual tests. A software engineer is responsible for deciding whether a change is appropriate, understanding its consequences and being able to explain and recover the released system.

| Preparation item | Own explanation and evidence |
|---|---|
| Problem and stakeholders | SmartCare manages synthetic patient, practitioner and appointment workflows for a teaching clinic scenario. Evidence: README and `project/smartcare/`. |
| Two requirements and acceptance criteria | Booking/conflict prevention and cancellation/history. Evidence: `test_starter.py`, `test_regressions.py`, `test_workflows.py`. |
| Domain model and architecture | Patient, Practitioner, Appointment; shared store; services; pure queries; console. Evidence: `project/smartcare/`. |
| Design trade-off | Session-only in-memory storage simplifies the assignment scope but loses all data when the process exits. Evidence: README and console behaviour. |
| Meaningful test and its limits / 100 percent coverage | Equal-time ordering test verifies date/time and ID tie-breaking; one test cannot prove every behaviour. Evidence: `test_queries.py`. |
| Diagnosed defect and verification | Truncated `test_starter.py` caused test collection failure; known-good test file restored and complete suite rerun with 60 passing tests. |
| Shared store and session-state/query responsibilities | Console creates one datastore for the session; queries use explicit appointment-list inputs rather than global state. Evidence: `console.py`, `queries.py`. |
| What would break if session-state lookup/query responsibilities changed? | A new datastore per menu operation would lose registrations and appointments; queries owning the datastore would introduce hidden state and responsibility leakage. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Appointment controls its own cancellation transition; service coordinates store lookup and cross-appointment conflict rules. Evidence: `domain.py`, `services.py`. |
| FR-07 retained history test | Cancelled appointment remains stored and available through lookup/listing. Evidence: `test_workflows.py`. |
| Actual AI change rejected/modified or honestly accepted with verification | Additional explicit service validation was rejected as duplicated because datastore validation already raises the required error and the blank-ID test passed. Evidence: Stage 9 Section E. |
| Unresolved limitation / future production work | Persistence, security/roles, timezone handling, concurrency, monitoring and production deployment requirements remain outside the assessed UG scope. |
| Personal implementation contribution | Jaiden Chandra completed Stage 9 query, listing and console integration and Stage 12 release work. |
| Personal test/review/design/integration contribution | Jaiden Chandra completed query/workflow tests, manual console verification, AI-review evaluation, integration repair and Stage 12 release verification. |
| PG agentic change and rescheduling verification | Not applicable – UG pathway. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable – UG pathway. |

**Practice question/change and reasoning:**  
Not undertaken. No additional coding change was made after the release candidate was frozen.

**Separate reflection / peer / common team viva evidence links and routing:**  
Evidence is retained in the relevant stage activity files, accumulated test suite and repository history. Separate confidential peer/reflection material should follow the course submission process where applicable.

No further coding stage. Later corrections should follow the published assessment process.