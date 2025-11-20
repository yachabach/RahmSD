# Test Strategy Document - Vital Signs Detection, Acquisition and Reporting Module

## Document Information

- **Project Name:** Guardian Line of Health Monitoring Devices  
- **Document Version:** 1.0  
- **Date:** 11/17/2025  
- **Author(s):** David Yachabach, Neil Euliano
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

- Jail cells (low lighting, movement interruptions, etc.)  
- Retirement/elderly care (pan-tilt tracking integration, backgrounds, etc.)  
- Healthcare/NICU (extended acquisition time, clinical documentation requirements, etc.)  

<div style="page-break-after: always;"></div>
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

<div style="page-break-after: always;"></div>
---

## 4. Test Approach

### 4.1 Test Levels

- **Component Testing**: Validate individual detection components function correctly in isolation
- **Integration Testing**: Verify that detection components work together and reporting logic correctly responds to component states
- **System Testing**: End-to-end validation of detection, acquisition, and reporting across all deployment scenarios
- **Acceptance Testing**: Clinical and operational validation with stakeholders (Dave, Neil, clinical staff)

### 4.2 Test Types

- **Functional Testing**: Verify all detection requirements, acquisition timing, and reporting logic meet specifications
- **Accuracy Testing**: Validate HR/RR measurements against FDA Class II requirements and reference standards
- **Boundary Testing**: Test threshold values (80°F thermal, detection distance limits, acquisition timing boundaries)
- **State Transition Testing**: Verify immediate suppression when requirements fail and proper recovery when requirements are re-established
- **Negative Testing**: Confirm system correctly suppresses output for invalid conditions (cold objects, excessive motion, noise interference)
- **Environmental Testing**: Validate performance across deployment scenarios (low light, blankets, multiple orientations, pan-tilt tracking)  
- **Regression Testing**: Ensure hardware changes (24 GHz boards, baseboard variants) don't break existing functionality

<div style="page-break-after: always;"></div>
---

## 5. Requirements Traceability

| Requirement ID | Requirement Description | Test Case ID(s) | Priority |
|----------------|------------------------|-----------------|----------|
| REQ-DET-001 | Motion detected within last X seconds | TC-DET-001, TC-DET-002 | High |
| REQ-DET-002 | Thermal signature >80°F detected | TC-DET-003, TC-DET-004 | High |
| REQ-DET-003 | Human pose detected and classified | TC-DET-005, TC-DET-006 | High |
| REQ-DET-004 | Presence = TRUE when REQ-DET-001 AND REQ-DET-002 AND REQ-DET-003 are all TRUE | TC-DET-007 | High |
| REQ-DET-005 | Presence = FALSE when no thermal signature detected for Y minutes (person has left) | TC-DET-008 | High |
| REQ-RNG-001 | Distance measured between 5-10 ft | TC-RNG-001, TC-RNG-002 | High |
| REQ-RNG-002 | Vitals suppressed when outside range defined in REQ-RNG-001 | TC-RNG-003 | High |
| REQ-STAT-001 | Motion index below threshold | TC-STAT-001 | High |
| REQ-STAT-002 | Pose classified as stationary (lying, sitting, resting) | TC-STAT-002 | High |
| REQ-STAT-003 | Thermal region stable (no shifting hotspots) | TC-STAT-003 | High |
| REQ-STAT-004 | Radar amplitude baseline stable | TC-STAT-004 | High |
| REQ-STAT-005 | Stationary = TRUE only when REQ-STAT-001, REQ-STAT-002, REQ-STAT-003, and REQ-STAT-004 are all TRUE | TC-STAT-005 | High |
| REQ-STAT-006 | Vitals suppressed immediately when REQ-STAT-005 becomes FALSE | TC-STAT-006 | High |
| REQ-ACQ-001 | Continuous stationary period of X-30 seconds required before vitals output | TC-ACQ-001, TC-ACQ-002 | High |
| REQ-ACQ-002 | System state signals "acquiring" during acquisition period | TC-ACQ-003 | Medium |
| REQ-ACQ-003 | Movement during acquisition resets timer to zero | TC-ACQ-004 | High |
| REQ-CONF-001 | High SNR detected in radar waveform | TC-CONF-001 | High |
| REQ-CONF-002 | One dominant peak detected in radar waveform | TC-CONF-002 | High |
| REQ-CONF-003 | No multi-path interference detected | TC-CONF-003 | High |
| REQ-CONF-004 | HR/RR rolling averages stable | TC-CONF-004 | High |
| REQ-CONF-005 | Radar confidence = TRUE only when REQ-CONF-001, REQ-CONF-002, REQ-CONF-003, and REQ-CONF-004 are all TRUE | TC-CONF-005 | High |
| REQ-CONF-006 | Vitals suppressed immediately when REQ-CONF-005 becomes FALSE | TC-CONF-006 | High |
| REQ-VIT-001 | Heart rate accuracy meets FDA Class II requirements | TC-VIT-001, TC-VIT-002 | High |
| REQ-VIT-002 | Respiration rate accuracy meets FDA Class II requirements | TC-VIT-003, TC-VIT-004 | High |
| REQ-REP-001 | Vitals output only when REQ-DET-004, REQ-RNG-001, REQ-STAT-005, REQ-ACQ-001, and REQ-CONF-005 are all TRUE | TC-REP-001 | High |
| REQ-REP-002 | Vitals immediately suppressed when any requirement in REQ-REP-001 becomes FALSE | TC-REP-002 | High |
| REQ-REP-003 | System state signals reason for suppression (e.g. DET, RNG, STAT, ACQ, CONF) | TC-REP-003 | Medium |
| REQ-ENV-001 | System functions in low-light jail cell environment | TC-ENV-001 | High |
| REQ-ENV-002 | System functions with pan-tilt tracking (elderly care) | TC-ENV-002 | High |
| REQ-ENV-003 | System meets extended acquisition requirements (healthcare/NICU) | TC-ENV-003 | High |

<div style="page-break-after: always;"></div>
---

## 6. Test Conditions & Scenarios

### 6.1 Human Presence Detection (REQ-DET-001 through REQ-DET-005)

**Purpose:** Validate that presence is correctly detected only when motion, thermal, and pose sensors all indicate a living human is present.

**Test Conditions:**

- Motion detected within last X seconds (threshold to be specified)
- Thermal signature >80°F
- Human pose detected and classified
- No thermal signature for Y minutes triggers presence = FALSE

**Expected Behavior:**

- Presence = TRUE when all three conditions met
- Presence = FALSE when any condition fails or thermal lost for Y minutes
- System continues to track presence even when person is stationary/sleeping (thermal + pose maintain presence)

**Test Scenarios:**

**Positive Tests:**

1. All three sensors detect valid human → Presence = TRUE
2. Person remains stationary but thermal + pose valid → Presence maintained
3. Person moves after period of stillness → Presence maintained

**Negative Tests:**

1. Motion detected but thermal <80°F (cold object) → Presence = FALSE
2. Motion and thermal valid but no pose detected → Presence = FALSE
3. Thermal signature lost for Y minutes → Presence = FALSE
4. Only motion detected, no thermal or pose → Presence = FALSE

**Boundary Tests:**

1. Thermal exactly at 80°F threshold
2. Motion detected at exactly X seconds boundary
3. Thermal lost at exactly Y minutes boundary

---

### 6.2 Range Validation (REQ-RNG-001, REQ-RNG-002)

**Purpose:** Ensure vitals are only output when person is within valid measurement range (5-10 ft).

**Test Conditions:**

- Person distance measured between 5-10 ft (valid range)
- Person distance <5 ft (too close)
- Person distance >10 ft (too far)

**Expected Behavior:**

- Vitals output when person within 5-10 ft and all other requirements met
- Vitals immediately suppressed when person moves outside range
- Presence may still be tracked, but vitals not output

**Test Scenarios:**

**Positive Tests:**

1. Person at 7 ft (mid-range) → Vitals output (if all other requirements met)
2. Person moves from 6 ft to 8 ft → Vitals continue

**Negative Tests:**

1. Person at 4 ft (too close) → Vitals suppressed
2. Person at 11 ft (too far) → Vitals suppressed
3. Person sitting in corner outside range → Vitals suppressed

**Boundary Tests:**

1. Person at exactly 5 ft boundary
2. Person at exactly 10 ft boundary
3. Person transitions from 9.9 ft to 10.1 ft → vitals suppressed

---

### 6.3 Stationary State Detection (REQ-STAT-001 through REQ-STAT-006)

**Purpose:** Validate that vitals are only acquired when person is sufficiently still.

**Test Conditions:**

- Motion index below threshold
- Pose classified as stationary (lying, sitting, resting)
- Thermal region stable (no shifting hotspots)
- Radar amplitude baseline stable

**Expected Behavior:**

- Stationary = TRUE only when all four conditions met
- Vitals immediately suppressed when any stationary condition fails
- System can distinguish between stillness and motion

**Test Scenarios:**

**Positive Tests:**

1. Person lying still → Stationary = TRUE
2. Person sitting still → Stationary = TRUE
3. Person resting under blanket → Stationary = TRUE

**Negative Tests:**

1. Person walking → Stationary = FALSE, vitals suppressed
2. Person pacing → Stationary = FALSE, vitals suppressed
3. Person shifts position → Stationary = FALSE, vitals suppressed temporarily
4. Thermal region shifting (person rolling over) → Stationary = FALSE

**Boundary Tests:**

1. Motion index at threshold value
2. Minimal movement (fidgeting) near threshold

---

### 6.4 Acquisition Timing (REQ-ACQ-001 through REQ-ACQ-003)

**Purpose:** Validate that vitals require continuous stationary period before output.

**Test Conditions:**

- Person stationary for continuous X-30 seconds (product-dependent)
- Movement interrupts acquisition
- System signals "acquiring" state during acquisition period

**Expected Behavior:**

- Vitals not output until full acquisition period complete
- System state signals "acquiring" during this period
- Any movement resets acquisition timer to zero
- Once acquired, vitals output if all other requirements met

**Test Scenarios:**

**Positive Tests:**

1. Person stationary for 30 seconds → Vitals acquired and output
2. Acquisition at multiple distances within valid range
3. Acquisition under blankets
4. Acquisition at multiple body orientations

**Negative Tests:**

1. Person moves at 15 seconds → Timer resets to zero
2. Person moves repeatedly → Acquisition never completes
3. Person becomes stationary for 20 seconds then moves → No vitals output

**Boundary Tests:**

1. Movement at exactly X seconds (minimum acquisition time)
2. Movement at 29.9 seconds before 30-second completion

---

### 6.5 Radar Confidence Validation (REQ-CONF-001 through REQ-CONF-006)

**Purpose:** Ensure radar signal quality is sufficient for accurate vital signs measurement.

**Test Conditions:**

- High signal-to-noise ratio (SNR)
- One dominant peak in waveform
- No multi-path interference
- HR/RR rolling averages stable

**Expected Behavior:**

- Radar confidence = TRUE only when all quality conditions met
- Vitals immediately suppressed when confidence drops
- System distinguishes valid signal from noise

**Test Scenarios:**

**Positive Tests:**

1. Clear radar signal with high SNR → Confidence = TRUE
2. Single person in cell with clean waveform → Vitals output

**Negative Tests:**

1. Low SNR (noisy environment) → Confidence = FALSE, vitals suppressed
2. Multiple peaks (wall reflections) → Confidence = FALSE
3. Multi-path interference from metal surfaces → Confidence = FALSE
4. HR/RR values unstable/erratic → Confidence = FALSE
5. Aliasing from pacing motion → Confidence = FALSE

**Boundary Tests:**

1. SNR at minimum threshold
2. HR/RR stability at threshold limits

---

### 6.6 Vital Signs Accuracy (REQ-VIT-001, REQ-VIT-002)

**Purpose:** Validate that HR and RR measurements meet FDA Class II accuracy requirements.

**Test Conditions:**

- Heart rate measurement compared to reference standard
- Respiration rate measurement compared to reference standard
- Multiple test subjects
- Various physiological states

**Expected Behavior:**

- HR accuracy meets FDA Class II specifications
- RR accuracy meets FDA Class II specifications
- Measurements stable and repeatable

**Test Scenarios:**

**Positive Tests:**

1. HR measurement within acceptable tolerance of reference
2. RR measurement within acceptable tolerance of reference
3. Multiple subjects with varying HR/RR → all within tolerance

**Validation Tests:**

1. Comparison against FDA-cleared reference device
2. Multiple measurements over time for consistency
3. Testing across physiological range (low/normal/elevated HR and RR)

---

### 6.7 Reporting Logic (REQ-REP-001 through REQ-REP-003)

**Purpose:** Validate overall system reporting behavior integrating all gates.

**Test Conditions:**

- All detection requirements met (presence, range, stationary, acquisition, confidence)
- Any single requirement fails
- System state signaling

**Expected Behavior:**

- Vitals output ONLY when all requirements met
- Vitals immediately suppressed when ANY requirement fails
- System signals reason for suppression

**Test Scenarios:**

**Positive Tests:**

1. All gates pass → Vitals output with HR and RR values
2. System transitions from suppressed to output when requirements met
3. System maintains output while all requirements remain valid

**Negative Tests:**

1. Presence fails → Vitals suppressed, system signals "no presence"
2. Range fails → Vitals suppressed, system signals "out of range"
3. Motion detected → Vitals suppressed, system signals "motion detected"
4. Confidence drops → Vitals suppressed, system signals "low confidence"

**State Transition Tests:**

1. System correctly transitions between all states (acquiring → outputting → suppressed → acquiring)
2. Multiple rapid state changes handled correctly
3. State signals accurately reflect current system condition

---

### 6.8 Application-Specific Scenarios (REQ-ENV-001 through REQ-ENV-003)

**Purpose:** Validate system performance in target deployment environments.

#### 6.8.1 Jail Cell Environment (REQ-ENV-001)

**Test Conditions:**

- Low lighting conditions
- Pixelation requirements applied
- Frequent movement interruptions
- Person lying on bunk

**Expected Behavior:**

- Thermal sensor dominant in low light
- System functions with pixelated video
- Conservative behavior (prefers suppressing vitals)

**Test Scenarios:**

1. Complete darkness → System relies on thermal + radar
2. Person under blanket in dark cell → Detection and acquisition function
3. Person pacing then lying down → System correctly transitions
4. Pixelation applied → System still functions

#### 6.8.2 Elderly Care Environment (REQ-ENV-002)

**Test Conditions:**

- Pan-tilt camera tracking integration
- Person moving around room
- Telemedicine connection readiness

**Expected Behavior:**

- Vitals acquired when camera centered and person stationary
- System coordinates with pan-tilt tracking
- HR/RR stabilization before telemedicine connection

**Test Scenarios:**

1. Camera tracks person, acquires vitals when stationary
2. Person moves → camera follows, vitals suppressed during movement
3. Telemedicine initiated → system confirms stable vitals

#### 6.8.3 Healthcare/NICU Environment (REQ-ENV-003)

**Test Conditions:**

- Extended acquisition time (20-30 seconds)
- Clinical documentation requirements
- FDA Class II compliance

**Expected Behavior:**

- Longer acquisition period for clinical accuracy
- All data suitable for clinical documentation
- Meets FDA requirements

**Test Scenarios:**

1. 30-second acquisition period → Vitals output
2. Clinical validation against reference monitors
3. Documentation includes all required metadata

<div style="page-break-after: always;"></div>
---

## 7. Test Environment

### 7.1 Hardware Requirements

**Radar Systems**:

24 GHz radar boards (new configuration for FDA trials)
Baseboard configurations (variants to be tested)
Radar mounting hardware and fixtures

**Thermal Imaging**:

- Thermal camera sensors
- Thermal calibration equipment

**Pose Detection**:

- Camera systems for pose classification
- Pan-tilt mechanisms (for elderly care testing)

**Reference Equipment**:

- FDA-cleared vital signs monitor (reference standard for accuracy validation)
- Distance measurement tools (laser rangefinder for range validation)
- Thermal reference sources (for thermal calibration)

### 7.2 Software Requirements

- Firmware version(s) under test
- Software build numbers
- Configuration files and parameters
- Data logging and analysis tools

### 7.3 Test Facility Setup

**Laboratory Environment**:

- Controlled testing area with adjustable lighting
- Distance markers at 5 ft, 7 ft, 10 ft, and beyond
- Mounting positions for radar and cameras
- Temperature control (for thermal testing)

**Application-Specific Mockups**:

- **Jail Cell Mockup**: Low-light environment, bunk bed setup, corner areas, metal surfaces
- **Elderly Care Room**: Pan-tilt tracking setup, typical furniture layout, variable lighting
- **Healthcare/NICU Setup**: Clinical environment simulation, reference monitor placement

**Environmental Controls**:

- Lighting control (full darkness to normal illumination)
- Temperature monitoring
- Reflective surface positioning (for multi-path interference testing)

<div style="page-break-after: always;"></div>
---

## 8. Test Data Requirements

### 8.1 Human Test Subjects

- Multiple test subjects with varying physiological characteristics
- Range of body types, sizes, and age groups
- Subjects with different baseline HR/RR values (low, normal, elevated)

### 8.2 Physical Test Materials

- Blankets of varying thickness and materials
- Various clothing types and fabrics
- Cold objects for false detection testing
- Non-human heat sources for negative testing

### 8.3 Reference Standards and Calibration

- FDA-cleared vital signs monitor (reference standard)
- Thermal calibration sources
- Distance measurement tools (laser rangefinder)
- Timestamp synchronization system

### 8.4 Data Logging Requirements

- Synchronized reference vital signs data
- Environmental condition logs (temperature, lighting levels, distance)
- System state logs (presence, stationary, confidence, acquisition status)
- Video/photo documentation of test configurations

### 8.5 Test Configuration Documentation

- Distance markers and measurements (5-10 ft)
- Body orientation documentation
- Environmental setup photos
- Hardware configuration records (board versions, firmware builds)

<div style="page-break-after: always;"></div>
---

## 9. Entry and Exit Criteria

### 9.1 Entry Criteria

- [ ] Test environment setup complete and verified (distance markers, lighting controls, mockups)
- [ ] Hardware available and functional (24 GHz radar boards, baseboards, thermal/pose sensors)
- [ ] Software build delivered with release notes and known issues documented
- [ ] Test cases reviewed and approved by stakeholders
- [ ] Reference equipment calibrated and operational (FDA-cleared monitor, measurement tools)
- [ ] Test subjects scheduled and available
- [ ] Data logging systems configured and tested
- [ ] Test team trained on equipment and procedures

### 9.2 Exit Criteria

- [ ] All high-priority test cases executed
- [ ] 95% pass rate achieved for critical requirements (REQ-DET, REQ-RNG, REQ-STAT, REQ-ACQ, REQ-CONF, REQ-VIT, REQ-REP)
- [ ] All critical and high-severity defects resolved or have approved workarounds
- [ ] Vital signs accuracy validated against FDA Class II requirements
- [ ] All three application environments tested (jail, elderly care, healthcare/NICU)
- [ ] Hardware variants validated (24 GHz boards, baseboard configurations)
- [ ] Traceability matrix complete (all requirements mapped to test cases and results)
- [ ] Test execution reports completed and reviewed
- [ ] Test summary report approved by stakeholders

<div style="page-break-after: always;"></div>
---

## 10. Test Deliverables

### 10.1 Planning Documents

- Test Strategy Document (this document)
- Detailed Test Plan with schedule and resource allocation
- Test cases with step-by-step procedures and expected results
- Requirements Traceability Matrix (RTM)

### 10.2 Execution Documents

- Test execution logs with pass/fail results
- Defect reports with severity, priority, and reproduction steps
- Test data logs (vital signs, environmental conditions, system states)
- Video/photo documentation of test configurations

### 10.3 Analysis and Reporting

- Test summary report with overall results and metrics
- Accuracy validation report (HR/RR vs. reference standards)
- Environment-specific test reports (jail, elderly care, healthcare/NICU)
- Hardware validation report (24 GHz boards, baseboard variants)
- Traceability matrix with test results mapped to requirements

### 10.4 Regulatory and Compliance

- FDA Class II accuracy validation documentation
- Design Verification Testing (DVT) documentation for healthcare/NICU
- Clinical testing documentation (as applicable)

### 10.5 Sign-off and Approval

- Test completion certificate with stakeholder signatures
- Known issues and limitations document
- Recommendations for deployment readiness

<div style="page-break-after: always;"></div>
---

## 11. Schedule & Milestones

| Milestone | Target Date | Owner | Status |
|-----------|-------------|-------|--------|
| Test strategy approval | [Date] | [Test Lead] | Pending |
| Test cases development complete | [Date] | [Test Engineers] | Pending |
| Test environment setup complete | [Date] | [Dave, Neil] | Pending |
| Hardware delivery (24 GHz boards, baseboards) | [Date] | [Hardware Team] | Pending |
| Entry criteria verification | [Date] | [Test Lead] | Pending |
| **Phase 1: Component Testing** | | | |
| Detection gate testing (presence, range, stationary) | [Date] | [Test Engineers] | Pending |
| Radar confidence testing | [Date] | [Test Engineers] | Pending |
| **Phase 2: Integration Testing** | | | |
| Acquisition timing and state transitions | [Date] | [Test Engineers] | Pending |
| Reporting logic integration | [Date] | [Test Engineers] | Pending |
| **Phase 3: Accuracy Validation** | | | |
| HR/RR accuracy testing vs. reference standard | [Date] | [Test Engineers] | Pending |
| FDA Class II requirements validation | [Date] | [Clinical Team] | Pending |
| **Phase 4: Application-Specific Testing** | | | |
| Jail cell environment testing | [Date] | [Test Engineers] | Pending |
| Elderly care environment testing | [Date] | [Test Engineers] | Pending |
| Healthcare/NICU environment testing | [Date] | [Clinical Team] | Pending |
| **Phase 5: Hardware Validation** | | | |
| 24 GHz radar board validation | [Date] | [Dave, Neil] | Pending |
| Baseboard variant testing | [Date] | [Dave, Neil] | Pending |
| Range testing (5-10 ft validation) | [Date] | [Dave, Neil] | Pending |
| Test execution complete | [Date] | [Test Lead] | Pending |
| Defect resolution and regression testing | [Date] | [Test Engineers] | Pending |
| Test report and documentation complete | [Date] | [Test Lead] | Pending |
| Final approval and sign-off | [Date] | [Stakeholders] | Pending |

<div style="page-break-after: always;"></div>
---

## 12. Resources

### 12.1 Test Team

**Test Lead**: [Name] - Overall test strategy, planning, and execution oversight  
**Test Engineers**: [Names] - Test case development, execution, and defect reporting  
**Test Data Analyst**: [Name] - Data logging, analysis, and accuracy validation  

### 12.2 Subject Matter Experts

**Hardware Engineers**: [Names] - Radar board validation, range testing, hardware configuration  
**Clinical Specialists**: [Names] - FDA requirements validation, clinical testing protocols  
**Software Engineers**: [Names] - Technical support for system behavior and troubleshooting  

### 12.3 Stakeholders and Approvers

**Project Manager**: [Name] - Schedule coordination and resource allocation  
**Technical Lead**: [Name] - Requirements clarification and technical decisions  
**Quality Manager**: [Name] - Test strategy approval and final sign-off  

### 12.4 Management Tools

**Test Management**: [e.g., TestRail, Jira, Excel]  
**Defect Tracking**: [e.g., Jira, Bugzilla]  
**Document Management**: [e.g., Confluence, SharePoint, Google Drive]  
**Communication**: [e.g., Slack, Teams, Email]  

<div style="page-break-after: always;"></div>
---

## 13. Risk Assessment

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| 24 GHz radar boards delayed | High | Medium | Order backup units early, parallel testing with existing boards, maintain buffer in schedule |
| Test subjects unavailable for extended periods | Medium | Medium | Schedule subjects in advance, maintain roster of backup subjects, coordinate with HR/recruitment |
| Reference monitor calibration issues | High | Low | Maintain calibration schedule, have backup reference device, establish relationship with calibration service |
| Environmental mockup setup delays | Medium | Medium | Begin setup early, have contingency testing space, document alternative configurations |
| FDA accuracy requirements not met on first attempt | High | Medium | Plan for iterative testing cycles, allocate time for algorithm tuning, engage clinical experts early |
| Hardware variants show inconsistent behavior | High | Medium | Test each variant thoroughly, document differences, establish baseline performance criteria |
| Application environment testing access limited | Medium | Low | Coordinate with deployment sites early, create realistic mockups, use video documentation from actual sites |
| Data logging system failures | Medium | Low | Implement redundant logging, regular backups, test logging systems before critical tests |
| Test team resource constraints | Medium | Medium | Cross-train team members, prioritize critical tests, adjust schedule to match available resources |
| Defect resolution delays test completion | High | Medium | Establish clear defect triage process, maintain communication with development team, plan regression buffer |

<div style="page-break-after: always;"></div>
---

## 14. Assumptions and Dependencies

### 14.1 Assumptions

- Test subjects will be available for all planned test scenarios
- Environmental mockups will adequately represent actual deployment conditions
- FDA-cleared reference monitor will be available and calibrated throughout testing
- Software builds will be stable enough for testing by entry criteria date
- Test team will have adequate training on equipment and procedures
- Test environment will remain available for the full testing duration
- Defects will be addressed by development team within agreed timeframes

### 14.2 Dependencies

- Hardware Delivery: 24 GHz radar boards and baseboard variants must be delivered by [date] for Phase 5 testing
- Dave and Neil Availability: Hardware validation protocol and range testing requires Dave and Neil's expertise and availability
- Clinical Team: FDA accuracy validation requires clinical specialist availability and reference equipment
- Development Team: Defect resolution and software updates depend on development team capacity
- Deployment Sites: Access to actual jail cell, elderly care, or healthcare facilities for environment validation (if applicable)
- Regulatory Guidance: FDA Class II requirements and documentation standards must be clearly defined before accuracy testing
- Procurement: Test materials (blankets, positioning equipment, etc.) must be procured before test execution

<div style="page-break-after: always;"></div>
---

## 15. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | | | |
| Project Manager | | | |
| Technical Lead | | | |
| Quality Manager | | | |
| Clinical Specialist (if applicable) | | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-112-17 | David Yachabach | Initial draft |
