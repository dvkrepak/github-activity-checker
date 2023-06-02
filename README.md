<img align="right" src="https://i.imgur.com/EkmzUIf.png" alt="GitHub Logo" width="400" height="200">

## **GitHub analyzer**
This is a GitHub Analyzer project developed by **<u> Denis Krepak</u>**.
## Links
- [**<u>Project Description</u>**](#project-description-a-nameproject-descriptiona)
- [**<u> Used Technologies </u>**](#used-technologies-a-nameused-technologiesa)
- [**<u> Deployment on local machine </u>**](#deployment-on-local-machine-a-namedeployment-locala)
- [**<u> Accesable Endpoints </u>**](#accesable-endpoints-a-nameendpointsa)
- [**<u> Examples of Usage </u>**](#examples-of-usage-a-nameexamples-usagea)
- [**<u> C4 model </u>**](#c4-model-a-namec4-modela)
## **Project Description** <a name="project-description"></a>
A web service that enables you to analyze activities (events) occurring on GitHub.
## **Features:**
- Calculates the average time between pull requests.
- Retrieves the total number of events grouped by event type within a specified time offset[1].
- Provides visualizations of event statistics.

[1] - The offset determines the time range for event counting. For example, if the offset is set to 10, it means that only the events created within the last 10 minutes will be counted. Adjust the offset value according to your desired time range.

## **Used Technologies** <a name="used-technologies"></a>
**[Events GitHub API](https://api.github.com/events)**: Event streaming from the GitHub API.  
**[Django](https://docs.djangoproject.com/en/4.2/)**:  Framework for creating the web application.  
**[Django REST framework](https://www.django-rest-framework.org/)**: Library for providing endpoints for the web service.  
**[PostgreSQL](https://www.postgresql.org/docs/)**: Relational database management system used for data storage.  
**[Matplotlib](https://matplotlib.org/stable/index.html)**: Library for visualizing statistics.
## Deployment on Local Machine <a name="deployment-local"></a>
1. Run the following commands to create the database:
```
psql -U postgres;
DROP DATABASE IF EXISTS checkerdb;
CREATE DATABASE checkerdb;
```
2. Clone the repository and change to the project directory:
```
git clone git@github.com:dvkrepak/github-activity-checker.git github-checker && cd github-checker
```
3. Create and activate a virtual environment:
```
python3 -m venv venv && source venv/bin/activate
```
4. Install all the required packages from requirements.txt:
```
pip3 install -r requirements.txt
```
5. Apply database migrations:
```
cd githubchecker && python3 manage.py makemigrations && python3 manage.py migrate
```
6. [Optional] Create a superuser:
```
python3 manage.py createsuperuser
```
7. Set parser and token settings in manage.py  
```
To configure the parser and token settings in your `manage.py` file, follow these steps:

1. Put your GitHub token into the variable named `TOKEN` (line 23).
2. [Optional] Set the parser to be active by setting the variable named `ACTIVE_PARSER` to `True` (line 24).
3. [Optional] Adjust the number of requests by modifying the variable named `AMOUNT_OF_REQUEST_PER_MINUTE` (line 28).
```
8. Launch the project:
```
python3 manage.py runserver
```
The project will be accessible at **http://127.0.0.1:8000/**.

* **Note:** The parser may not be active on your platform after launching. You might need to activate it by running the `manage.py` file.
## Accesable Endpoints <a name="endpoints"></a>
- **Admin Page**: Accessible at **<u> http://127.0.0.1:8000/admin/ </u>**. Requires superuser credentials.
- **Pull Request Metrics**: Accessible at **<u>  http://127.0.0.1:8000/metrics/pull-request/<int:repository_id> </u>**.
- **Events Metrics**: Accessible at **<u>  http://127.0.0.1:8000/metrics/events/<int:offset> </u>**.
- **Events Metrics Visualization**: Accessible at **<u>  http://127.0.0.1:8000/metrics/events_visualization/<int:repository_id> </u>**.
## Examples of Usage <a name="examples-usage"></a>
1. Retrieving Pull Request Metrics:
* Endpoint: **<u>  /metrics/pull-request/int:repository_id </u>**.
* Example: **<u> /metrics/pull-request/123 </u>**.
* Description: Replace `int:repository_id` with the GitHub ID of the desired repository to get the pull request metrics for that repository.

2. Getting Event Metrics:

* Endpoint: **<u>  /metrics/events/int:offset </u>**.
* Example: **<u>  /metrics/events/10 </u>**.
* Description: Replace `int:offset` with the desired time offset (in minutes) to get the event metrics for that time range.

3. Visualizing Event Metrics:

* Endpoint: **<u>  /metrics/events_visualization/int:offset </u>**.
* Example: **<u>  /metrics/events_visualization/10 </u>**.
* Description: Replace `int:offset` with the desired time offset (in minutes) to visualize the event metrics for that time range.
## C4 model <a name="c4-model"></a>
**<u> [C4 model using IcePanel](https://s.icepanel.io/ZoOSKTSb1gNrOi/bZcl) </u>**

**<u> [C4 model as PDF](https://c4model-github-analyzer.tiiny.site/) </u>**

<img src="https://i.imgur.com/VfPZhwz.png" alt="GitHub Logo" width="328" height="600">

