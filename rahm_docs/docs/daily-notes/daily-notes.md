# Daily Notes

## 2025-11-05

### Sales Meeting with Kevin

- Kevin O'Connor
- James Edwards
- Laura Johnson
- Johnnys Edwards - Jail Administrator.  National Sheriff's Association Speaker

- LIDAR - heat & temp?
- Photos do not really show what the presentation is
- County does not allow connection to their internet
- Bluetooth/WiFi requested
- Staff pushback on extra monitoring duties
- Central control room monitoring
- Sending alerts to officers' phones
- Security grade housing questions
- Death
-- single cell
-- booking
- Not a replacement for a camera
- Sounds like they are looking for a transparent, pro-active, push notification monitoring solution

### Vik Wednesday Catchup

- Davood believes 24ghz is better than 5.8ghz for vital signs
- No one is discussing the failures in the current installations
- Plan is to tune gain for FDA approval then add dynamic range functionality

## 2025-11-04

- Graphana dashboard: <https://grafana.rahmsd.com/d/f53a2e36-731f-4a8c-a93f-79315b6cf80e/production-rahm-device-fault-monitoring?orgId=1&refresh=5s>
- Revealed that current installations are not working
- Was given access to Graphana dashboard to monitor devices
- Deva needs to make alerts more visible - issues have persisted for several days without resolution

## 2025-10-31

### Marketing Meeting with Kevin

- Varun: processes in place for correcting software bugs
- Theoretically, it appears we are being listened to...

## 2025-10-30

### UX Meet with Gretchen and Kevin

- Dec 1st Conference Info?
- User needs from Gretchen are excellent
- Creep toward shiny things
  - Spending too much time on suicide and cell phone detection
  - Can I sell this to Vik? - No one is promising in the product yet
- Need to talk to Justin Weiss - installer.  
  - Internal construction is "shabby".  
  - Cannot even survive shipping.  
  - Must be able to withstand a drop on the floor.  
  - Device rattles when it's shaken.  
  - Can't handle carryon luggage abuse.
- Lots of interest in the product
  - Staffing and incarceration rates
  - Automated inmate monitoring
  - Bad look to have a inmate death or injury


### Requirements

- See the whole cell
- Vital sign monitoring - Most important
- Thermal imaging - must be same size as rgb image
- Fall detection - not working well - too many false positives
- Switchboard
- False Alarms
- Authentication and Authorization
- Customer Technical Service
- Physical

### Competition

- Reassurance has already solved the vital sign problem - how?

### CG UI Debug with Deva

- Implement switchboard rather than fix bug.
- Would be good to identify difference in environments that is causing the bug.
- Web pages should be responsive

## 2025-10-29

### AI Discussion

- 8G Jetson memory issue involves how it's run in docker.
- Cole is shrinking the model from 16 bits to 8 bits.
- Plans to share model with Austin and Dave Holden next week
- Dave holden is using AI to generate training photos of people committing suicide
- Regular AI models are safety filtered to prevent harmful content
- Need to expand dataset with positive and negative images.
- If they can make it work without all positives set in a jail cell it will be more generalized
- I will have to demo and explain this model at the Dec 1st conference.
- Trying to put all CM4 software on the Jetson so that they can use a Jetson carrier board instead of a CM4 carrier board.
  - Jetson integrates differently with peripherals
  - Mike Terr and Greg are working on this
- Planning to give Mike Terry the 24ghz sensor board

### 24ghz Tech Meeting

- How do we control noise with fidgeting targets?
  - Adjust gain
  - Increase dyunamic range with oversampling
  - Update hardware to 20 or 24bit ADC

### Phone call with Vik

- I'm driving the project
- Contact Vik if I can't make progress with people
- TODO
  - Contact Kevin about a discussing user needs
  - Build requirements document for Cell Guardian - Look at NeoGuardian docs

## 2025-10-28

SancSoft Catchup

- NeoGuardian App - in app store and google play
  - monday demo
- Silver Guardian App - Publilshed to App Store and Google Play
  - Becomming a B->C product - needs to be more reliable and robust
- Updates for Silver Guardian become baseline tech for Cell Guardian
- Tighten up and move away from SancSoft in the next 120 days
- 24ghz - gain too high - signal saturation and clipping

## 2025-10-21

Meeting with Rashmin and Neil

- Discussed strategic vision for Neo
  - Delivery room - still requires validated vital monitoring
  - Rashmin meeting with Mike and Helen 2025-10-27 to discuss IRB progress

## 2025-10-06

Meeting with Vik

- Moving from NeoGuardian to product owner of Silver and Cell Guardian.
- Need hardware and documentation to understand Silver and Cell Guardian.

## 2025-09-25

Meeting with Vik and Neil

- IRB Data Collection Verbiage
- Pilot vs. Validation Study
- LEAN MVP Process
- UI Progress
- Work terms (Equity, Wage Rate, etc.)
- IRB is th focus.  No work on UX.

## 2025-09-08

### Meeting with Deva

- Discussed architecture of NeoGuardian system
- Discuss ancillary UI applications needed
  - https://app.dev.neo-guardian.com/
  - Do testing on this site
- Discuss current [app limitations][al]
- Discussed data storage options for study
- Inform Helen of data storage decisions for IRB purposes

## 2025-09-05

Meeting with Vik and Neil

- Expressed a need for better understanding of the product vision
- Expressed a need for clarity on where we are in the product cycle if not in development
- Talked about major missing pieces
  - Integration with existing hospital systems
  - Admin dashboard and UI
  - Clean up login
  - Setup workflow
- Deeva Seeta is my primary technical contact

## Future Meetings

[al]: ./neog-limitations.md
