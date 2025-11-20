# RahmSD Website Test Data Capture

This app touches cell guardian installation websites for the purpose of capturing test data.

This is a python app that runs in a virtual environment.  It uses `selenium` to visit websites and scrape data points of interest.  Scraped data is logged to CSV files for later analysis.

## Goals

- Periodically visit specified websites.
- Capture and log test data from these websites.
- Log captured data to a CSV file for analysis.

---

## Websites

[Nelson](https://app.cell-guardian.com/monitor/20fab0eb-d91d-497c-8eeb-06d491f7ba61/dashboard)  
[Archer](https://app.cell-guardian.com/monitor/06789238-2655-417a-8765-23577a07743a/dashboard)  
[Faulk](https://app.cell-guardian.com/monitor/1ece78ad-cd9f-4052-84fd-41040a42dbac/dashboard)  
[Ripley](https://app.cell-guardian.com/monitor/ce19c800-7521-41dd-90db-6148a13dc6e7/dashboard)  

Faulk and Ripley have multiple cameras installed.  The app should select and scrape each.  To reach a camera, **select** `button` elements in the `units-container` div.  Select cameras in sequence storing the button label as the camera name.

```html
<div _ngcontent-ng-c4119936837="" class="units-container ng-tns-c4119936837-10">
    <div _ngcontent-ng-c4119936837="" class="groups-container ng-tns-c4119936837-10 ng-star-inserted">
        <div _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-10 ng-star-inserted">
            <div _ngcontent-ng-c4119936837="" class="group-container ng-tns-c4119936837-10">
                <span _ngcontent-ng-c4119936837="" class="group-name ng-tns-c4119936837-10">Ripley :</span>
                <div _ngcontent-ng-c4119936837="" class="d-flex flex-wrap gap-3 ng-tns-c4119936837-10">
                    <button
                        _ngcontent-ng-c4119936837="" type="button"
                        class="btn btnEastCss ng-tns-c4119936837-10 ng-star-inserted"
                        style="background-color: red; border: 2px solid red; color: white;"> Single Unit
                    </button>
                    <button _ngcontent-ng-c4119936837="" type="button"
                        class="btn btnEastCss ng-tns-c4119936837-10 ng-star-inserted"
                        style="background-color: red; border: 2px solid red; color: white;"> Detox Cell 
                    </button><!---->
                </div>
            </div>
        </div><!---->
    </div><!----><!---->
</div>
```

## Data Points Captured

- Presence of Fall or Motion Alerts
- HR
- RR
- Acquisition Range Flag
- Acquisition Range
- Stationary Flag
- Acquisition Time Flag
- Room Temp Max
- Room Temp Min

---

### Fall Alerts

Here we only detect the presence of a fall and/or motion alert.  If an alert is present, the `<div>` element with the `main-content-container` class will have the following structure.

```html
<div _ngcontent-ng-c4119936837=""
    class="alert-section-container ng-tns-c4119936837-3 ng-trigger ng-trigger-sectionAnimation ng-star-inserted">
    <div _ngcontent-ng-c4119936837=""
        class="alert-text-container ng-tns-c4119936837-3 ng-trigger ng-trigger-alertItemAnimation ng-star-inserted"
        style=""><span _ngcontent-ng-c4119936837="" class="boldTempCss ng-tns-c4119936837-3">Fall Alert : </span><span
            _ngcontent-ng-c4119936837="" class="paragCss ng-tns-c4119936837-3"> Fall Detected! Immediate assistance
            required. </span></div><!----><!----><!---->
    <div _ngcontent-ng-c4119936837=""
        class="alert-text-container ng-tns-c4119936837-3 ng-trigger ng-trigger-alertItemAnimation ng-star-inserted"
        style=""><span _ngcontent-ng-c4119936837="" class="boldTempCss ng-tns-c4119936837-3">Last Motion Alert :
        </span><span _ngcontent-ng-c4119936837="" class="paragCss ng-tns-c4119936837-3"> No motion detected for the last
            10 minutes or more. </span></div><!----><!----><!----><!---->
</div>
```

### Device Status Section

This is where status dots and all textual data points are located.  It lives in the `div` element with `device-status-container` class.

This section is divided into a left side and a right side.  The order of data points and their classes are:

|**`left-side-container`**|**`right-side-container`**|
|---------------------|----------------------|
|`status-item-container` (Acquisition Status Dots)|~~`device-buttons-container`~~ |
|`stat-box` (HR)|~~`stat-box` (Last Motion)~~|
|`stat-box` (RR)|~~`stat-box` (Last Fall)~~|
|~~`stat-box` (Behavior State)~~|`stat-box` (Room Temp)|

> ~~Strikethrough~~ indicates data points that are not currently captured.

#### Acquisition Status Dots

In this example, Acquisition Range is not available.  There is no green dot and `-` is reported (the `ft` should be removed from the scrape result). Stationary is good (green), and Acquisition Time is good (green).

```html
<div _ngcontent-ng-c4119936837="" class="status-items-container ng-tns-c4119936837-2">
    <div _ngcontent-ng-c4119936837="" class="status-item-container ng-tns-c4119936837-2"><app-status-indicator
            _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-2" _nghost-ng-c2038734381="">
            <div _ngcontent-ng-c2038734381="" class="dot-container">
                <div _ngcontent-ng-c2038734381="" class="inner-container"></div>
            </div>
        </app-status-indicator>
        <div _ngcontent-ng-c4119936837="" class="status-text ng-tns-c4119936837-2"><span _ngcontent-ng-c4119936837=""
                class="ng-tns-c4119936837-2">Acquisition Range</span><span _ngcontent-ng-c4119936837=""
                class="ng-tns-c4119936837-2 ng-star-inserted"> - ft</span><!----></div>
    </div>
    <div _ngcontent-ng-c4119936837="" class="status-item-container ng-tns-c4119936837-2"><app-status-indicator
            _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-2" _nghost-ng-c2038734381="">
            <div _ngcontent-ng-c2038734381="" class="dot-container">
                <div _ngcontent-ng-c2038734381="" class="inner-container green"></div>
            </div>
        </app-status-indicator>
        <div _ngcontent-ng-c4119936837="" class="status-text ng-tns-c4119936837-2">Stationary</div>
    </div>
    <div _ngcontent-ng-c4119936837="" class="status-item-container ng-tns-c4119936837-2"><app-status-indicator
            _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-2" _nghost-ng-c2038734381="">
            <div _ngcontent-ng-c2038734381="" class="dot-container">
                <div _ngcontent-ng-c2038734381="" class="inner-container green"></div>
            </div>
        </app-status-indicator>
        <div _ngcontent-ng-c4119936837="" class="status-text ng-tns-c4119936837-2"><span _ngcontent-ng-c4119936837=""
                class="ng-tns-c4119936837-2">Acquisition Time</span><!----></div>
    </div>
</div>
```

#### Heart Rate (HR) and Respiration Rate (RR)

These are whole number located in a list of `div` elements within the `device-status-container` class.  Each data point has this structure:

```html
<div _ngcontent-ng-c4119936837="" class="stat-box ng-tns-c4119936837-7">
    <div _ngcontent-ng-c4119936837="" class="stat-icon ng-tns-c4119936837-7"><img _ngcontent-ng-c4119936837=""
            src="../../../../assets/svgs/hr-icon.svg" alt="HR Image"
            class="ng-tns-c4119936837-7 ng-star-inserted"><!----><!----></div>
    <div _ngcontent-ng-c4119936837="" class="stat-content ng-tns-c4119936837-7">
        <div _ngcontent-ng-c4119936837="" class="stat-text-container ng-tns-c4119936837-7"><span
                _ngcontent-ng-c4119936837="" class="stat-text ng-tns-c4119936837-7"><span _ngcontent-ng-c4119936837=""
                    class="ng-tns-c4119936837-7 ng-star-inserted">-</span><!----><!----></span><span
                _ngcontent-ng-c4119936837="" class="stat-unit-text ng-tns-c4119936837-7"> HR </span></div>
        <div _ngcontent-ng-c4119936837="" class="stat-description ng-tns-c4119936837-7"> Heart Rate </div>
    </div>
</div>
```

In this example for HR, data was not available and the value is `-`.

#### Min and Max Temperature

Room temperature values are whole numbers located in a list of `span` elements within the `temp-stat-text` class.  Each data point has this structure:

```html
<div _ngcontent-ng-c4119936837="" class="stat-box ng-tns-c4119936837-7 green-border">
    <div _ngcontent-ng-c4119936837="" class="stat-icon ng-tns-c4119936837-7"><img _ngcontent-ng-c4119936837=""
            src="../../../../assets/svgs/temp-icon.svg" alt="Temparature Image"
            class="ng-tns-c4119936837-7 ng-star-inserted"><!----><!----></div>
    <div _ngcontent-ng-c4119936837="" class="stat-content ng-tns-c4119936837-7">
        <div _ngcontent-ng-c4119936837="" class="stat-text-container ng-tns-c4119936837-7"><span
                _ngcontent-ng-c4119936837="" class="stat-text temp-stat-text ng-tns-c4119936837-7"><span
                    _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-7 ng-star-inserted"><span
                        _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-7"> 59.54</span><span
                        _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-7"> - </span><span
                        _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-7">69.98</span><span
                        _ngcontent-ng-c4119936837="" class="ng-tns-c4119936837-7">° F</span></span><!----><!----></span>
        </div>
        <div _ngcontent-ng-c4119936837="" class="stat-description ng-tns-c4119936837-7"> Min and Max Temp </div>
    </div>
</div>
```

This should be parsed and stored in separate column in the csv file.

---

## Logging Data to CSV

Create a separate CSV file for each website.  Files should be located in the `data` directory of the project root. Each row should contain:

- Timestamp
- Camera Name
- Presence of Fall Alert (Yes/No)
- Presence of Motion Alert (Yes/No)
- Acquisition Range Flag (True/False)
- Acquisition Range
- Acquisition Time Flag (True/False)
- Stationary Flag (True/False)
- HR
- RR
- Room Temp Max
- Room Temp Min
