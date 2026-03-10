This is a personal project created by an **Agronomic Engineering student** who is also a developer.

As a Ruby (on Rails) developer, I decided that, in my university vacations, I was going to learn Python. I created a project named agro_tools [https://github.com/nandocp/agro_tools], where I implemented methods of subjects I was studying at the time (namely some related to climatology, such as calculation of photoperiod and evapotranspiration).

After that, I decided to learn how to create a web app - API only - using Python and, since I am at this field, I imagined creating an app that would allow land owners/leasers/managers to easily manage their properties.

The basic broad roadmap is as following:
1) model the basic entities that will support the app's logic;
2) implement endpoints that will allow user interaction;
3) develop a frontend;

Some thoughts on functions that I want to implement:
1) possibility to create plantings of various types of plants;
  1.1) these plantings will be inserted at a private blockchain that will enable tracking;
  1.2) harvest both perennial and crop plants, inserting them to the system, linked to the geographic data of the property and the blockchain;
2) allow for animal creation with all the inputs necessary.

Technologies used:
* Web framework: **FastAPI**
* Testing framework: **Pytest**
* Database: **Postgresql (with Postgis extension)**, **Sqlalchemy** and **Geoalchemy2**
* Dependencies management: **Poetry**
