# Meeting Notes

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

Meet with Rashmin and Nimisha

The direction for the UX is determined by our understanding of the Problem Space and Solution Space.  We need to have a clear understanding of these before we can proceed with UX design.

- Discuss strategic vision for NeoGuardian
  - Recruiting dev sites?
  - Competing with Phillips or Angel Eye?
  - Understand and define Problem Space 
    - What is our hypothesis about customer needs
    - How do we measure progress toward a solution
- Understand and define target market
- Understand and define Solution Space
- Understand where we are in the product cycle
  - Not ready for prime time - Many UI's needed

[al]: ./neog-limitations.md
