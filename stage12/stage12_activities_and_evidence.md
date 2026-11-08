# Stage 12 activities and evidence

**Group/tutorial:** Thursday 2:30-4:30 Group 2

**Members and UG/PG applicability:**  
U3321093 – UG pathway. Completed Stage 12 common release verification, regression testing, console demonstration, evidence review and release preparation.  


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
Feature freeze applied for Stage 12 release verification. No new feature development is planned. Owner: U3321093. Verifier: [other member/verifier if applicable].

---

## B Requirements and release readiness matrix

**Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify:**

**Do not release yet.** Passing tests alone are not sufficient for a release decision. The incomplete README affects reproducibility, the unreviewed dependency represents an unresolved release risk, and the undocumented limitation means users do not have an accurate description of the system. These gaps should be corrected and the candidate rechecked before release.

### Tutorial activity 2 and actual readiness matrix

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Cancellation changes status without deleting the Appointment; cancelled appointment remained findable/listable | `services.py`, workflow tests, Stage 9 evidence | Musab | Yes | None known |
| Architecture responsibilities are appropriate | Domain, store, service, pure-query and console responsibilities remain separated | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | Musab | Yes | None known |
| Rescheduling is safe — PG only | Not applicable to UG pathway | N/A | N/A | N/A | PG only |
| AI use is responsible — common recheck / PG assurance | Copilot review findings were checked by a human and one proposed validation duplication was rejected with test evidence | Stage 9 Section E | U3321093 | Yes | Preserve AI evidence |
| System is maintainable | Focused modules, type hints, docstrings, tests and separation of responsibilities | `project/smartcare/`, `project/tests/` | Musab | Yes | Production concerns remain out of scope |
| FR-01–03 register/find and validation | Patient and practitioner registration/find behaviour covered by accumulated tests and console demo | accumulated tests + interactive demo | Musab | Yes | None known |
| FR-04–05 booking/conflict rules | Valid booking succeeds; same practitioner/time conflict rejected; different practitioner same time allowed | automated tests + Stage 12 demo | Musab | Yes | None known |
| FR-06–08 cancellation/history/find | Cancellation retained object and same-session lookup/history | tests + Stage 12 demo | Musab | Yes | None known |
| FR-09 and QRY/FP listing/filter/order/purity | Query tests verify practitioner filtering, status handling, deterministic ordering and non-mutation | `test_queries.py`, `test_workflows.py` | Musab | Yes | None known |
| UI full console sequence and error recovery | `python main.py --interactive` completed; errors recovered without terminating session | Stage 12 demo | U3321093 | Yes | None known |
| Session-only scope / FR-10 retired | Application explicitly uses in-memory session-only data | README / console / evidence | Musab | Yes | Accepted scope limitation |
| PG RES and assurance integration | Not applicable | N/A | N/A | N/A | UG pathway |

---

## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.15.2; pytest 8.3.5 | `project/` — `python -m pytest -q` | `c8c6ea1c3a592932f8beabdd99ffb53e05207578` | **60 passed in 0.07s** | https://github.com/jaidenchandra/st1-assignment-3 |
| Complete PG if applicable | Not applicable – UG pathway | N/A | N/A | N/A | N/A |
| Affected focused checks after correction | Restored complete `test_starter.py` and reran full suite | `project/` — `python -m pytest -q` | Stage 9 integration candidate | **60 passed** | https://github.com/jaidenchandra/st1-assignment-3 |
| Full integrated recheck | Python 3.15.2 | `project/` — `python -m pytest -q` | `c8c6ea1c3a592932f8beabdd99ffb53e05207578` | **60 passed in 0.07s** | https://github.com/jaidenchandra/st1-assignment-3 |

**Prior assertions preserved / reviewed test diff:**  
Existing accumulated tests were preserved. The damaged/truncated local `test_starter.py` was restored rather than weakening or deleting assertions. The complete suite subsequently passed.

**Remaining failure / limitation:**  
No known failing automated tests. The main intentional limitation is session-only in-memory storage; data is lost on exit.

---

## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | SmartCare synthetic clinic scenario | Support patients, practitioners and appointment management in one session | Application demonstrated the required session workflows | [evidence] |
| Register and find Patient and two Practitioners | P1/Alex Example; D1/Taylor Example/General Practice; D2/Jordan Example/Cardiology | Registered records remain available in same session | Registration succeeded | [evidence] |
| Valid booking | A1, P1, D1, `2026-10-01 09:00` | Valid registered participants produce SCHEDULED appointment | Booking succeeded | https://github.com/jaidenchandra/st1-assignment-3/pull/8 |
| Same practitioner exact-time conflict rejected | Attempt second D1 booking at same time | Prevent practitioner double-booking | Conflict rejected | https://github.com/jaidenchandra/st1-assignment-3/pull/8] |
| Different practitioner same time allowed | A2 with D2 at `2026-10-01 09:00` | Different practitioner may use same time | Booking succeeded | https://github.com/jaidenchandra/st1-assignment-3/pull/8 |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then find A1 | Status becomes CANCELLED without deletion | A1 remained retrievable as cancelled | https://github.com/jaidenchandra/st1-assignment-3/pull/8 |
| Invalid/repeated cancellation rejected | [run repeated cancellation if not already demonstrated] | Invalid transition raises expected error without corrupting state | [actual result] | [evidence] |
| Default all-status listing | List D1 with blank status | Includes appointment history regardless of status | Cancelled A1 remained visible | [evidence] |
| Explicit filtering / empty vs unknown / deterministic order | Automated query/workflow tests | Correct status filtering, empty/unknown distinction and ordering | Passed automated tests | [evidence] |
| Invalid date/status/menu/lookup recovery and continued operation | Invalid menu choice, malformed date and failed lookups | Error displayed and program continues | Recovery worked; menu remained active | [evidence] |
| Session-only limitation and normal exit | Select option `0` | Program exits normally and session data is not persisted | Normal exit completed | [evidence] |
| One meaningful requirement-linked pytest test explained | `test_sorting_uses_datetime_then_appointment_id` | QRY-03 deterministic ordering | Confirms date/time sort with appointment ID tie-break | `test_queries.py` |
| Architecture and one actual AI decision / known limitation | Copilot proposed possible explicit practitioner ID validation | Human verifies existing store already validates blank ID | Suggestion rejected as unnecessary duplication; blank-ID test passed | Stage 9 AI evidence |
| PG reschedule identity/participants/time and no-op | Not applicable | PG only | N/A | N/A |
| PG conflict/invalid status/failure non-mutation | Not applicable | PG only | N/A | N/A |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable | PG only | N/A | N/A |

**Stable demo owner / fresh process / command:**  
Owner: U3321093  
Command: `python main.py --interactive` from `project/`. The demonstration was run in a fresh process using synthetic data.

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
| Synthetic data / secrets / dependencies / provenance | demo/tests and requirements | Synthetic records only; pytest development dependency pinned | Verify final ZIP contains no secrets/cache/environment files |
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
| Purpose and included common/PG scope | root/project README | Musab | UG/common scope documented |
| Out-of-scope capabilities and known limitations | README | Musab | Session-only scope and excluded production features documented |
| Confirmed teaching Python version and dependency installation | README | Musab | Course materials technically verified Python 3.13/pytest 8.3.5; actual release verification used Python 3.15.2 with pytest 8.3.5 |
| Working directory / demo / interactive / test commands | README | Musab | `python main.py`, `python main.py --interactive`, `python -m pytest -q` documented |
| Repository structure and architecture responsibilities | README | Musab | [confirm] |
| Responsible AI summary / synthetic-data rule | README/evidence | Musab | [confirm] |
| Release label/version and SHA links | README/release evidence | Musab | Add final SHA after candidate frozen |

**Fresh clone or extracted ZIP / candidate identity:**  
The final source ZIP was generated from submitted commit `65fece90e0fa12857d2ac62bf9a4cc4988f15d53`, extracted into a separate verification folder and tested independently from the working repository.

**Verifier and clean environment / actual version:**  
Verifier: Musab Master.  
Verification was performed from the extracted release package using Python 3.15.2 and pytest 8.3.5.

**Setup/run/test commands and observed results:**  
`python -m pip install -r requirements-dev.txt`  
`python -m pytest -q`  

Dependencies were available successfully and the extracted release completed the full regression suite with **60 passed in 0.34s**.

**Missing local file or setup gap / remedy and recheck:**  
No required file or setup gap was identified during extracted-package verification.

---

**Source ZIP name / SHA correspondence / extracted comparison:**  
`SmartCare-release.zip` was generated using `git archive` from final submitted commit `65fece90e0fa12857d2ac62bf9a4cc4988f15d53`. The archive was extracted into a separate directory and the full regression suite was rerun successfully with **60 passed in 0.34s**. This confirmed that the submitted source package was reproducible from the recorded commit.

---

## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README checked.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository candidate and exact tested SHA identified.
- [x] One final source ZIP generated and checked.
- [x] `project/` source and all accumulated applicable tests included.
- [x] All common applicable stage records retained; PG-only stages not applicable.
- [x] Final ZIP reproduced successfully from the submitted commit.
- [x] No Stage 10/11 PG work is claimed for this UG-only group.
- [x] Group contributions and release evidence recorded.

**Remaining administration or release dependency:**  
No known technical release dependency remains. The final repository commit and source ZIP have been verified successfully and are ready for course submission.
**Setup/run/test commands and observed results:**  
`python -m pip install -r requirements-dev.txt`  
`python main.py`  
`python main.py --interactive`  
`python -m pytest -q`  
Observed regression result: **60 passed in 0.07s**.

**Missing local file or setup gap / remedy and recheck:**  
None known at current working-copy verification. Final extracted ZIP/fresh-clone check still needs to be recorded if not yet performed.

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
No known code/test blocker. Documentation, exact candidate SHA, final reproducibility/ZIP check and submission administration must be complete before submission.

---

## I Git review and integration evidence

**Issue / PR / diff links and reviewed SHA:**  
Stage 9 branch: `feature/stage9-queries`  
Repair branch: `fix/restore-test-starter`  
PR links: [insert actual links]  
Reviewed/final candidate SHA: `[insert final candidate SHA]`

**Independent reviewer / feedback / response:**  
[insert actual reviewer and summary]

**Integration commit / full recheck:**  
Integrated `main` was rechecked with `python -m pytest -q`. Actual Stage 12 result: **60 passed in 0.07s**.

**Tracked and untracked file inspection / cleanliness:**  
Run `git status` before final release. Expected result: clean working tree with only intentionally versioned files.

**Secrets/staff material/caches/tool-metadata exclusion check:**  
Final repository/ZIP must exclude `.git`, virtual environments, caches, secrets, real personal/clinical data, private QA material and unrelated staff solutions.

**Candidate recovery plan / known-good SHA:**  
Use the exact final tested `main` SHA as the known-good release candidate. Earlier known Stage 9 checkpoint: `3112b59d36889b767a55228a0e589583ac8e30a7`.

**Named substantive contributions:**  
U3321093 – Stage 9 appointment queries, practitioner listing integration, interactive console integration, automated query/workflow testing, manual verification, integration repair and Stage 12 release verification.  
[Add other members.]

---

## J Human release decision

**Decision — READY WITH DOCUMENTED LIMITATIONS**

**Approver / date / rationale and evidence:**  
Approver: [name/team]  
Date: [date]  
The accumulated automated suite passes with **60 passed**, the interactive end-to-end workflow was demonstrated successfully, required Stage 9 functions are integrated, and known limitations are documented. Final release remains subject to completing the README/reproducibility/package checks and recording the exact tested SHA.

**What risks remain / conditions / owners:**  
Session-only storage and production capabilities are accepted scope limitations. Final administrative/reproducibility checks remain the responsibility of the team before submission.

**Can the team explain the system:**  
Yes. The team should be able to explain the domain model, store, services, queries, console, test evidence, cancellation history and conflict behaviour.

**Can a change be recovered:**  
Yes. Git branches, commits and known-good SHAs provide recovery points, and the complete test suite can be rerun after restoration.

**Common decision / PG decision where different:**  
Common UG candidate: ready with documented limitations after final packaging/reproducibility checks. PG decision not applicable.

---

## K Final tested release SHA

**Exact common tested SHA:**  
`[RUN git rev-parse HEAD AFTER FINAL TESTS AND INSERT HERE]`

**Exact PG tested SHA or not applicable:**  
Not applicable – UG pathway.

**Final submitted SHA / repository URL:**  
SHA: `[final SHA]`  
Repository: `[GitHub repository URL]`

Evidence-only later commit SHA: 0813d3edae3acf8d6711193f8de20b1da9e5c83d.

The executable SmartCare candidate was tested at c8c6ea1c3a592932f8beabdd99ffb53e05207578. The later commit only completed Stage 6 and Stage 12 evidence/documentation and did not change executable application code. Therefore the previously recorded 60-test regression result remains evidence for the executable candidate.
**Executable changes after testing and re-verification:**  
No executable change may be made after the final tested SHA without rerunning the full regression suite and recording the new SHA/result.

**Source ZIP name / SHA correspondence / extracted comparison:**  
`[final ZIP filename]` corresponds to `[final submitted SHA]`.  
[Comp~~lete after extracted ZIP verification.]~~

---

## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] `project/` source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway.
- [ ] No `.git`, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

**Confirmed assessment item/upload route:**  
[enter LMS/assessment submission location]

**Deadline/timezone:**  
[enter official deadline and timezone]

**Repository access arrangement:**  
[confirm marker/tutor access]

**Mixed-candidate upload arrangement:**  
Not applicable if this is an UG-only group. [Confirm if mixed.]

**Oral/video recording/accessibility arrangements:**  
[enter actual arrangement]

**Remaining administration or release dependency:**  
Final ZIP creation/extraction comparison, exact SHA recording, repository access confirmation and submission.

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
Focused Stage 9 query/service/console work and automated testing worked well. Rework occurred when a starter test file became truncated and during some working-directory/indentation issues. Future delivery would improve by checking `git status`, reviewing diffs before commits, protecting supplied tests and verifying integrated `main` immediately after every merge.

**One paragraph — If AI can write code why do we still need software engineers:**  
AI can generate or review code quickly, but it does not replace responsibility for understanding what the software must do, choosing architecture, protecting data integrity, evaluating trade-offs, diagnosing integration failures and deciding whether evidence is sufficient for release. In SmartCare, generated suggestions still had to be compared with domain contracts, existing datastore behaviour and automated/manual tests. A software engineer is responsible for deciding whether a change is appropriate, understanding its consequences and being able to explain and recover the released system.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare manages synthetic patient, practitioner and appointment workflows for a teaching clinic scenario. [link] |
| Two requirements and acceptance criteria | Booking/conflict prevention and cancellation/history are demonstrated through tests and console workflows. [link] |
| Domain model and architecture | Patient, Practitioner, Appointment; shared store; services; pure queries; console. [link] |
| Design trade-off | Session-only in-memory storage keeps scope simple but loses data on exit. [link] |
| Meaningful test and its limits / 100 percent coverage | Equal-time query ordering test verifies date/time and ID ordering; one passing test cannot prove every system behaviour. [link] |
| Diagnosed defect and verification | Truncated `test_starter.py` caused collection failure; restored known-good file and reran full suite: 60 passed. [link] |
| Shared store and session-state/query responsibilities | One store is created for the console session; queries receive explicit lists rather than accessing global storage. [link] |
| What would break if session-state lookup/query responsibilities changed? | Creating a new store per action would lose registrations/appointments; allowing queries to own storage would introduce hidden state and blur responsibilities. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Appointment owns its status transition; service coordinates store lookup and cross-appointment scheduling rules. |
| FR-07 retained history test | Cancelled appointment remains the same stored object and appears in all-status/cancelled listing. [link] |
| Actual AI change rejected/modified or honestly accepted with verification | Explicit service ID validation suggestion rejected as duplicate because datastore validation already produced required `ValueError`; blank-ID test passed. |
| Unresolved limitation / future production work | Persistence, authentication/roles, timezone policy, concurrency, monitoring and other production concerns. |
| Personal implementation contribution | U3321093 implemented Stage 9 queries, listing service integration and interactive console work. |
| Personal test/review/design/integration contribution | U3321093 created query/workflow tests, performed manual console verification, AI review evaluation, integration repair and Stage 12 regression/demo. |
| PG agentic change and rescheduling verification | Not applicable – UG pathway. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable – UG pathway. |

**Practice question/change and reasoning:**  
Not undertaken. No additional coding change was made after the release candidate was frozen.

**Separate reflection / peer / common team viva evidence links and routing:**  
[insert actual links/routes]

No further coding stage. Later corrections should follow the published assessment process.