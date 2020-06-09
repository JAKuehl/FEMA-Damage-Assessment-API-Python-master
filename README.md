
# FEMA Damage Assessment App

> Author: Vala Rahmani, Blake Franey, John Kim
> July 2019

## Table of contents


- [Overview](#Overview)

- [Client](#Client)

- [Problem and Solution](#Problem_and_Solution')

- [Approach](#Approach)

- [How to use](#How_to_use)

- [Suggested Work](#Suggested_Work)

- [Additional Resources](#Additional_Resources)






<a id='Overview'></a>
# Overview
---

FEMA Damage Assessment App is a pro bono project prepared for New Light Technologies, a small, award-winning origanization in DC that specializes in providing comprehensive information technology solutions to government agencies, commercial and non-profits
The goal of the application is to facilitate FEMA's (the Federal Emergency Management Agency) Individual Assistance Damage Assessment Teams Members assessing the damages caused to individual residential properties in the areas affected by the disasters. This app will speed up the process of damages assessment by user taking a photo of the affected property then uses google streetview to retrieve the pre-disaster photo of the location, and uses Zillow API to retrieve the latest information of that property. 


<a id='Client'></a>
# Client
---

New Light Technologies(NLT) is a small organization based in DC where it specializes in providing information Technology solutions for clients in government agencies, commercial and non-profits. 

For this task our contact at NLT is Ran Goldblatt, Ph.D., who is the Chief remote sencing Scientist and Senior Colsultant. His specialty is in geospatial analysis and image processing.Ran's team supports disaster response through innovative methods using image processing, and consolidation of multi source imagery at FEMA.
 

<a id='Problem_and_Solution'></a>
# Problem and Solution
---

During the recovery phase following a disaster, FEMA IA team members perform damage assessment 'On the ground' to assess the level of damage caused to residential parcels and critical infrastructures. This work is very labor intensive and inefficient if done manually. Also, due to verification measures put in place by FEMA, the assessment teams have to first report to the regional centeers and after the information has been verified the information will be passed to the FEMA headquarters to start restoration fundings. As expected this process can take very long time, and leaves a lot of people affected by disasters in shelters and out of their home.


This is where using our app the assessment team can speed up their process by taking a simple photo and forwarding the information directly to FEMA regional and headquarters databases. Currently we have a Web App working where the FEMA IA team members will take a photo of the affected residential parcel and then a form containing the pre-disaster and post-disaster photos will appear on the screen and provides the following information about the property:

- Address
- The zillow id for the unit
- Home type
- Year Built 
- Lot size
- Living area 
- Bathrooms
- Bedrooms
- Last time sold
- Last sold price
- Zestimate price

Also a form will appear on the bottom of these outputs where the FEMA member will input the following information from drop down menus dedicated to the metrics FEMA looks at before certifying fundings. 

- Disaster Type
- Damage Degree
- Occupancy Status 
- Rent Status of the neighborhood
- Property access
- Additional notes

After the submitting the above fields all the data will be saved into a PostGreSQL Database and can be accessed at both regional and headquarters.

<a id='Approach'></a>
# Approach
---

###  FEMA Assessment Web App API and interface

In order to tackle this problem and bring efficiency to damage assesment on the ground. It is very important for us to create a user friendly and robust system where we facilitate team members' *On the ground* damage assessment task. Hence, used the Following APIs(Application programming interface)provided to us by Google and Zillow and packages to build this app.

[Pillow](https://pillow.readthedocs.io/en/stable/installation.html)
[Googlemaps](https://pypi.org/project/googlemaps/)
[Google_streetview](https://pypi.org/project/google-streetview/)
[json](https://docs.python.org/3/library/json.html)
[pygeocoder](https://pypi.org/project/pygeocoder/)
[pyzillow](https://pypi.org/project/pyzillow/)

Once the photo is uploaded, the `master_query()` function will be called and the results will be provided to the user and pushed to the server.
**NOTE: All of the coding has been done using python and the assembly of the webapp used flask to render and view the python results.

### FEMA Assessment Mobile App v0.2.0

When agents are on the field, access the web app in order to input the data for damage assessment of the residential parcels.  Other issues like connectivity will present a challenge to data collection.  To address this, we designed a mobile app that agents will be able to use in the field that will have the same functionality as the web app.  Currently the app is in the development phase but the basic functionality can be demonstrated in a demo version.  

First, the user will be able to upload a picture to our web app API and return results pre-disaster and post-disaster.  They can choose either a photo from the phone's storage or take a picture right in the app.  Regardless of which option they choose, the photo will be stored in the app to upload later if connectivity is an issue.  Once uploaded, they user will be able to fill out a form for the criterias FEMA audits before securing restoration funds.  


The current version of the app is set up to call the web app API hosted on a server and return the mentioned results.  All of the outputs and the user inputs will be pushed to the SQL database hosted on Heroku.  Possible future additions include:

**NOTE: Mobile app has been developed with node.js and Angular7 using the Ionic framework.

<a id='How_to_Use'></a>
# How to use the app
---

As a user who wants to improve the app and add further features to the app refer to `func.py` and `application.py` to add new features or customize the outputs for the app. In order to successfully run the script on a local host users will need to obtain their API key directly from Google and Zillow. Directions on the packages needed to be installed on local host are also available on `func.py`.



<a id= 'Suggested_Work'></a>
# Further Additions
---

- Collecting reliable information from past disasters to build a model to predict damages to individual properties.

- Expanding the form portion of the app to collect more detailed data for stronger predictions.
- Including the damages cost estimate after submitting form responses.
- Embedded map functionality that can notify the user of road closures and for navigation.
- Including satellite imagery of the disaster area.




<a id='Additional_Resources'></a>
# Additional Resources
[FEMA user manual](https://www.fema.gov/media-library-data/1459972926996-a31eb90a2741e86699ef34ce2069663a/PDAManualFinal6.pdf)

[FEMA Dataset](https://www.fema.gov/openfema-dataset-individual-assistance-housing-registrants-large-disasters-v1)

[How to make a Heroku Database](https://devcenter.heroku.com/articles/getting-started-with-kotlin#use-a-database)
