# Stage 6 activities and evidence

This record documents the Stage 6 implementation and the available issue, review, and testing evidence. Items not substantiated by the available record are explicitly identified; no unobserved reviews, issue links, or merge details are assumed.

- Group/tutorial: Not supplied in the available record.
- Members:
  - Musab Master (Stage 6 — Development)
  - Saja Nasser (Stage 7 — Testing)
  - Jaiden Chandra (Stage 8 — Debugging)
  - Yashmeen Dandiwal (Stage 9 — Queries and Console Integration)
- GitHub username/handle for each member: not independently verified in the available record.
- Repository URL: https://github.com/jaidenchandra/st1-assignment-3
- Starting SHA: Not established from the available Git history evidence.

## A. Requirement-to-issue activities

### FR-02 Patient Search
- Title: Implement patient lookup by ID (FR-02)
- Context: The SmartCare application needs a reliable way to retrieve an existing patient from its shared data store.
- Requirement: PatientService.find_patient retrieves a patient by ID and handles missing or invalid IDs consistently.
- Acceptance criteria:
  - An existing patient ID returns the matching patient.
  - A missing ID raises LookupError.
  - An invalid ID raises ValueError.
  - Focused automated tests pass.
- Scope: Patient service lookup and its focused tests; no unrelated data model changes.
- Definition of Done:
  - Implementation and tests committed
  - Another-member PR review completed
  - Merged to main
  - Integrated tests passing
- Owner: Issue assignee not established; Musab implemented the corresponding Stage 6 service code.
- Actual issue link: Issue #2 or #3; exact requirement mapping has not been established.

### FR-06 Appointment Cancellation with FR-07 retained history
- Title: Implement appointment cancellation while retaining history (FR-06/FR-07)
- Context: SmartCare must cancel eligible appointments without losing historical appointment records.
- Requirement: AppointmentService.cancel_appointment locates an appointment, calls its cancellation guard, and retains the appointment record in the shared store.
- Acceptance criteria:
  - An eligible appointment can be cancelled.
  - Missing IDs raise LookupError.
  - Invalid IDs raise ValueError.
  - Prohibited cancellation is rejected by the appointment's domain guard.
  - Appointment history remains retained in the shared store.
  - Focused automated tests pass.
- Scope: Cancellation service behavior and tests; no deletion of appointment history or unrelated refactoring.
- Definition of Done:
  - Focused tests
  - PR review and approval
  - Merge
  - Passing tests on main
- Owner: Issue assignee not established; Musab implemented the corresponding Stage 6 service code.
- Actual issue link: Issue #2 or #3; exact requirement mapping has not been established.

## B. Commit quality

| Original example | Strong or Weak | Reason |
| --- | --- | --- |
| changes | Weak | Does not identify the feature, purpose, or affected behavior. |
| final version | Weak | Ambiguous and implies finality without explaining the change. |
| Add patient search by ID | Strong | Identifies a specific capability and scope. |
| fix stuff | Weak | Does not identify what was fixed or why. |
| Prevent cancellation of completed appointments | Strong | Clearly states the behavioral rule being enforced. |

## C. Over-scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code, and adds a new dependency.

- Scope concerns:
  - The PR combines unrelated changes, making the cancellation requirement harder to trace and review.
- Responsibility and architecture concerns:
  - Renaming patient fields may break callers.
  - Restructuring unrelated modules may blur responsibilities.
  - A new dependency needs justification and maintenance reasoning.
- Testing and review concerns:
  - The diff is larger than necessary.
  - It obscures cancellation defects.
  - It demands regression tests for unrelated changes.
- Changes to remove or separate, with reasons:
  - Keep the cancellation service and focused tests in this PR.
  - Move patient-field renames, general refactoring, and dependency additions to separate, justified follow-up changes.

## D. Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass." This is a hypothetical exercise, not a review that occurred on PR #1.

- Missing evidence:
  - No cited lines
  - No test command/output
  - No requirement mapping
  - No edge-case analysis
  - No assessment of scope and architecture
- Follow-up review question 1:
  - Which changed lines implement FR-06 and preserve FR-07 history?
- Follow-up review question 2:
  - Which tests demonstrate successful cancellation and rejection of prohibited cancellation?
- Follow-up review question 3:
  - How are missing and invalid appointment IDs handled?
- Follow-up review question 4:
  - Are any unrelated changes or dependencies included in the diff?
- Follow-up review question 5:
  - Did you run tests, or are you only inferring success from the PR description? What exact output supports the claim?
- Additional questions if useful:
  - Does cancellation retain the appointment in the data store?
  - Are existing tests still passing?

## E. Team workflow agreement

Proposed workflow; the available record does not establish formal team agreement.

| Practice | Team agreement |
| --- | --- |
| Branch naming | Proposed: feature/<short-description> or docs/<short-description> |
| Commit message convention | Proposed: Short, imperative, behavior-specific messages (e.g., Add patient search by ID) |
| PR size | Proposed: One focused requirement or closely related change per PR |
| Another-member review requirement | Proposed: A teammate checks the actual diff, requirements, and tests before approving |
| Merge rule | Proposed: Merge only after approval and passing tests; record the merge SHA |
| Significant Copilot disclosure rule | Proposed: Record material AI assistance, verify its claims, and never present an unsubmitted review as completed |

## F. Issue and backlog index

Issue #2 and issue #3 were identified in the earlier project record. Their precise requirement mapping, current status, and assignees have not been independently verified for this final document.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
| --- | --- | --- | --- | --- |
| https://github.com/jaidenchandra/st1-assignment-3/issues/2 | Requirement mapping not verified | Unassigned on GitHub; responsible member not confirmed | See issue description; verify alignment with Section ... | Not independently verified |
| https://github.com/jaidenchandra/st1-assignment-3/issues/3 | Requirement mapping not verified | Unassigned on GitHub; responsible member not confirmed | See issue description; verify alignment with Section ... | Not independently verified |

Practitioner lookup (supporting FR-03 operation): PractitionerService.find_practitioner was implemented and tested in PR #1. The available record does not establish a separate issue or tutor-approved mapping for this service.

## G. Pull request evidence

- PR link and title:
  - https://github.com/jaidenchandra/st1-assignment-3/pull/1
  - Exact PR title not independently verified.
- Linked issue and requirement:
  - Issues #2 and #3 document the service work.
  - The available record does not establish that both issues were linked to PR #1 before merge or identify their exact mapping.
- Feature branch:
  - feature/stage6-service-lookups
- Changed behaviour:
  - Added patient and practitioner lookups by ID
  - Guarded appointment cancellation that retains the record
- Meaningful commits:
  - https://github.com/jaidenchandra/st1-assignment-3/commit/c729ef5
- Test command, directory, and observed result:
  - Command: python3 -m pytest
  - Directory: project/
  - Result: 10 passed in 0.02s (verified on merged main)
- Another-member reviewer:
  - jaidenchandra (GitHub approval recorded on PR #1)
- Human observations recorded before Copilot:
  - No specific written review observations available; do not invent review timing or findings.
- Requirement, responsibilities, test assertions, and unrelated-scope checks:
  - Implementation and tests address the three service methods.
  - No written human review checklist is available.
- Key feedback:
  - No specific written feedback available from the recorded approval.
- Author response/change and verification:
  - No documented review-requested changes.
  - Integrated tests passed.
- Reviewer recheck and approval:
  - Approval on https://github.com/jaidenchandra/st1-assignment-3/pull/1
  - Direct review-event URL not established; see PR #1.
- Merge outcome and SHA:
  - Merged to main
  - 50e1b12
- Significant Copilot assistance:
  - Copilot review was requested, but no submitted Copilot review or comments appear in PR #1.
- Linked issue closure:
  - Issues #2 and #3 were previously reported open.
  - Current status and appropriate closure have not been verified.
- Each member updated main:
  - Musab previously recorded pulling main.
  - No individual confirmation is available for the other members.
- Integrated verification after merge:
  - python3 -m pytest in project/ on main at 50e1b12
  - 10 passed in 0.02s (Python 3.13.7; pytest 8.3.5)

## H. Copilot collaboration record

- Member and task:
  - GitHub Copilot review requested for Pull Request #1.
- Prompt/purpose and relevant issue/diff:
  - Review the changes in Pull Request #1.
- Summary of output:
  - No review comments or suggestions were received.
  - GitHub shows the pull request was approved by jaidenchandra; no Copilot review was submitted.
- Human check against actual code, requirements, and tests:
  - No Copilot recommendations were available to check.
- Decision — Accept / Modify / Reject:
  - Not applicable.
- Reason:
  - No Copilot recommendations were received or applied.
- Verification/evidence:
  - Pull Request #1 review list contains only the approval by jaidenchandra.
  - Review threads list is empty.

## I. Human versus Copilot review comparison

- The human reviewer approved the pull request.
- Copilot provided no actionable feedback, so there were no suggestions to compare or accept.
- The merge decision relied on human review and passing automated tests.
- GitHub shows no submitted Copilot review; therefore, there is no evidence that Copilot completed a review and found no issues.
- Human reviewer observations and specific review findings:
  - Not recorded in the available PR review.
- Copilot observations, overlap, missed findings, and unsupported suggestions:
  - Not applicable; no Copilot review comments were submitted.
- Evidence for merge approval:
  - Human approval recorded on Pull Request #1 and passing automated tests (10 passed in 0.02s).

## J. Contributions

- Member: Musab
  - GitHub username not independently verified.
  - Implementation: Implemented PatientService.find_patient, PractitionerService.find_practitioner, and AppointmentService.cancel_appointment in project/smartcare/services.py; commit c729ef5 and PR #1.
  - Testing: Added focused tests in project/tests/test_starter.py; post-merge python3 -m pytest returned 10 passing tests.
  - Review: Submitted work for another-member review; PR #1 was approved by jaidenchandra. No separate PR review by Musab is documented.
  - Issue refinement: Issues #2 and #3 created; issue authorship and refinement contributions have not been established.
  - Design and responsibility discussion: No evidence of a separate design discussion is available.
  - Debugging or integration: Pulled merged main and verified tests at 50e1b12.
  - Documentation or team support: Updated project/README.md as part of PR #1; Stage 6 evidence draft in progress.

Other members’ contributions (complete only after confirmation):
- Saja Nasser — assigned Stage 7 Testing. No separate Stage 6 contribution evidenced in the available record.
- Jaiden Chandra (jaidenchandra) — assigned Stage 8 Debugging; approved Stage 6 PR #1. No additional Stage 6 contributions evidenced in the available record.
- Yashmeen Dandiwal — assigned Stage 9 Queries and Console Integration. No separate Stage 6 contribution evidenced in the available record.

## K. Exit question

### Why is a high commit count not necessarily evidence of strong contribution?

Commit count measures how often changes were recorded, not their value or quality. A developer can make many tiny or low-impact commits, while another contributes through design, difficult debugging, testing, code review, or coordination. Contribution quality depends on the significance, correctness, and impact of the work, not merely on the number of recorded commits.

## L. Stage 6 formative questions

1. What is version control?
   A system that tracks changes to files over time so team members can collaborate, inspect history, and recover earlier versions.
2. Why is a feature branch useful?
   It isolates a focused change from the shared main branch until it is tested and reviewed.
3. What makes a commit a good engineering commit?
   A focused, coherent change with a clear message explaining the behavior or purpose, ideally supported by appropriate tests.
4. What is a pull request?
   A request to review and merge changes from one branch into another, with a diff, discussion, and verification evidence.
5. What is the purpose of code review?
   To identify defects, confirm requirements and design responsibilities, assess tests and scope, and share understanding before integration.
6. What does a Git diff show?
   The lines added, removed, or changed between file versions or commits.
7. What is a Definition of Done?
   Agreed conditions that must be met before work is considered complete, such as implemented acceptance criteria, tests, review, and integration.
8. What is the appropriate role of GitHub Copilot in pull-request review?
   Copilot can offer additional suggestions, but its claims must be checked against the code and tests. It does not replace human review, and a requested review is not evidence of a completed review.
9. Why should individual contribution not be judged only by commit count?
   Commit counts omit the significance and quality of changes and non-commit work such as testing, review, debugging, design, and coordination.
10. What is the Stage 6 engineering rule?
    The exact wording of the Stage 6 engineering rule is not established in the available evidence. Working principle: trace each requirement through a focused issue, implementation, tests, human-reviewed pull request, and verified integration.

## M. Completion and handover

### Recorded evidence
- Final Stage 6 code SHA: c729ef5
- Merged main SHA: 50e1b12
- PR: https://github.com/jaidenchandra/st1-assignment-3/pull/1
- Test command: python3 -m pytest
- Working directory: project/
- Observed result: 10 passed in 0.02s
- Integrated verification: main at 50e1b12, Python 3.13.7, pytest 8.3.5
- Stage 7 handover: Three Stage 6 service operations are recorded as integrated and tests passing at the listed SHA. Stage 7 can build additional requirement-focused tests on the same project; outstanding record gaps remain in issue mapping and some team confirmations.
- Starting SHA: Not established from the available record.
- PR and another-member reviewer: PR #1; approved by jaidenchandra (see PR link above).
- Unresolved issue or none: Issue status remains unverified; no submitted Copilot review is evidenced; team integration confirmations are unavailable.
- Final submitted SHA if later than tested SHA: Not applicable at the time of writing; the evidence-only commit SHA can be recorded in the submission notes after committing. Explain that a later documentation commit differs from the tested code SHA when submitting.

- [x] Three Stage 6 service targets completed and checked by automated tests.
- [ ] Original supplied tests retained and passing. Original supplied tests have not been independently compared against the starter baseline.
- [ ] At least two focused issues link requirements and acceptance criteria. Exact issue-to-requirement mapping and links have not been verified.
- [x] Feature work reviewed and approved by another member (PR #1).
- [ ] Human-first review and required Copilot comparison recorded. No submitted Copilot review was evidenced.
- [ ] Feedback resolved and approval recorded before merge. Approval is recorded; precise sequence and feedback details are not evidenced.
- [ ] Everyone pulled main and integrated checks passed. Other members’ pull/integration confirmations are not available.
- [ ] Required activities, quiz responses, and contribution notes completed. Other members’ contributions and the exact Stage 6 rule wording are not established.
- [ ] Only synthetic data included; confidential peer material kept out. Dataset confidentiality and use of synthetic data have not been independently audited.
- [ ] Tutor can trace a requirement through issue, code, tests, PR, and checkpoint. Issue mapping and PR cross-links have not been independently verified.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.

Evidence boundary: The test result above is the previously recorded result for main at 50e1b12, not a fresh test run or verification of later group changes. This document records available evidence rather than making unsupported claims about later work.
