# Test Strategy Document - Vital Signs Detection, Acquisition and Reporting System

## Document Information

- **Project Name:** Guardian Line of Health Monitoring Devices
- **Document Version:** 1.0
- **Date:** 11/17/2025
- **Author(s):** David Yachabach
- **Reviewers:** Neil Euliano
- **Approval:** 

---

## 1. Executive Summary

The Guardian line of health monitoring devices provides contactless vital signs monitoring using radar and thermal imaging technologies. This test strategy outlines the validation approach for the Detection, Acquisition and Reporting System.  This system  ensures that vital signs (heart rate and respiration rate) are reported only when all detection requirements are met.  Vital signs reporting is immediately suppressed when any requirement fails. Testing will validate accuracy, gated reporting behavior, and performance across three deployment environments: jail cells, elderly care facilities, and healthcare/NICU settings. The system prioritizes safety by defaulting to suppressed output rather than reporting questionable data.

---

## 2. Test Objectives

**Validate Vital Sign Accuracy**: Ensure reported heart rate and respiration rate meet FDA Class II medical device requirements for accuracy and precision
**Validate Gated Vitals Reporting**: Confirm vital signs are reported only when all detection requirements are met and immediately suppressed when any requirement fails
**Validate Application-Specific Performance**: Confirm system meets requirements across all deployment environments:

- Jail cells (low lighting, pixelation requirements, movement interruptions)
- Retirement/elderly care (pan-tilt tracking integration, telemedicine readiness)
- Healthcare/NICU (extended acquisition time, clinical documentation requirements)

---

## 3. Scope

### 3.1 In Scope

- Detection system (presence, range, stationary state validation)
- Vital signs acquisition system (HR/RR calculation)
- Reporting logic (output control and system state signaling)
- All three deployment environments (jail, elderly care, healthcare/NICU)
- Hardware variants (24 GHz radar boards, baseboard configurations)

### 3.2 Out of Scope

- User interface and display rendering
- Network and IT infrastructure
- Data storage and backend systems
- Administrative and configuration tools
- Alert/notification delivery
- Long-term reliability and operational testing

---

## 4. Test Approach

### 4.1 Test Levels
- **Unit Testing:** Component-level validation
- **Integration Testing:** Multi-component interaction
- **System Testing:** End-to-end functional validation
- **Acceptance Testing:** User/stakeholder validation

### 4.2 Test Types
- **Functional Testing:** Verify requirements are met
- **Performance Testing:** Response time, accuracy metrics
- **Boundary Testing:** Min/max thresholds
- **Negative Testing:** Invalid inputs and error conditions
- **Regression Testing:** Ensure changes don't break existing functionality

---

## 5. Requirements Traceability

| Requirement ID | Requirement Description | Test Case ID(s) | Priority |
|----------------|------------------------|-----------------|----------|
| REQ-001 | Motion detection within X seconds | TC-001, TC-002 | High |
| REQ-002 | Thermal threshold > 80°F | TC-003, TC-004 | High |

---

## 6. Test Conditions & Scenarios

### 6.1 [Feature/Gate Name]
**Requirement:** [Brief description]

**Test Conditions:**
- Condition 1: [Description]
- Condition 2: [Description]

**Expected Behavior:**
- [What should happen]
- [Edge cases]

**Test Scenarios:**
1. **Positive Tests:** Valid inputs that should pass
2. **Negative Tests:** Invalid inputs that should fail gracefully
3. **Boundary Tests:** Min/max threshold values

---

## 7. Test Environment

### 7.1 Hardware Requirements
- Device models/versions
- Radar boards (e.g., 24 GHz boards)
- Camera systems

### 7.2 Software Requirements
- Firmware versions
- Software builds
- Required libraries

### 7.3 Test Facility Setup
- Physical environment (jail cell mockup, lab, clinical setting)
- Distance markers (5-10 ft range)
- Environmental controls (lighting, temperature)

---

## 8. Test Data Requirements
- Sample subjects (human presence testing)
- Thermal profiles
- Motion patterns
- Edge case scenarios (blankets, multiple orientations)

---

## 9. Entry and Exit Criteria

### 9.1 Entry Criteria
- [ ] Test environment setup complete
- [ ] Test hardware available and calibrated
- [ ] Test software build delivered
- [ ] Test cases reviewed and approved

### 9.2 Exit Criteria
- [ ] All high-priority test cases executed
- [ ] X% pass rate achieved
- [ ] Critical defects resolved
- [ ] Test report completed and approved

---

## 10. Test Deliverables
- Test Plan document
- Test cases with steps and expected results
- Test execution reports
- Defect reports
- Traceability matrix
- Final test summary report

---

## 11. Schedule & Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| Test plan approval | [Date] | [Name] | Pending |
| Test environment ready | [Date] | [Name] | Pending |
| Test execution start | [Date] | [Name] | Pending |
| Test completion | [Date] | [Name] | Pending |

---

## 12. Resources

### 12.1 Team
- **Test Lead:** [Name]
- **Test Engineers:** [Names]
- **Subject Matter Experts:** [Dave, Neil, etc.]

### 12.2 Tools
- Test management: [e.g., TestRail, Jira]
- Defect tracking: [e.g., Jira, Bugzilla]
- Test automation: [if applicable]

---

## 13. Risk Assessment

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Hardware delays | High | Medium | Order backup units, parallel testing |
| Environmental variation | Medium | High | Document all test conditions |

---

## 14. Assumptions and Dependencies
- Assumption 1: [e.g., Test subjects available for all scenarios]
- Dependency 1: [e.g., New 24 GHz boards delivered by [date]]

---

## 15. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Manager | | | |
| Project Manager | | | |
| Technical Lead | | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial draft |