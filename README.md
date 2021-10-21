# capstone FSND - Casting Agency
Udacity FSND capstone project

## Getting Started


## Motivation for project

Motivation for the project, this being the capstone project of Udacity Full-stack developer nanodegree program. This project is done in Flask, SQLAlchemy, Auth0, gunicorn and deployed using heroku. RBAC is done using Auth0. Logins for every role mentioned in the specification document is listed at the end of this document.    

### Installing Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the project base directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


## Users

1. **Casting Assistant** -    
Email: casting_assistant@udacity.com     
Password: Test12345
JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE3YWQ0MmNmYmUwMDY5MGQ3MGEzIiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NTcyOCwiZXhwIjoxNjM0ODUyOTI4LCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycy1kZXRhaWwiLCJnZXQ6bW92aWVzLWRldGFpbCJdfQ.s3OXTEjoqxLjnihJPyDySBfbId9ztVtgvqZXQF_HJ0HGU6ypUsfsAOmrxgNrlhw1ZU3_hdH5Lwo7UDRb6HqC_k28t5Hky9a2kBZp-SKXKmcqETq8cPyuD94OD2Kuyc_NE6w7mXHYKmfZXWBUjRZ-riHPyAH2ohoYOFUq3fXTqClVmMyntjY6VYWsOCpIuxAHLruoRVa3i0_uO-9zc0d-wl3cUscWMwxP14VF8iguhA8MdRqFEdyk9o4xyPXRrZRdGrfHSHUVcO2jV2p11fXEiPdWR196UpQnL2GCDB1uRnuovCSZD5xByvtiXGqK2AK-DVFcoSrgn7_bjkGyogv_Jw         

2. **Casting. Director** -    
Email: casting_director@udacity.com    
Password: Test12345    
JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE3ZWQxYzI3ODkwMDY4MzFjMjM4IiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NTk4NCwiZXhwIjoxNjM0ODUzMTg0LCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMtZGV0YWlsIiwiZ2V0Om1vdmllcy1kZXRhaWwiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.uC7yNQBcBMVodKm3HRelhEeWQEJ9R6-ujK36Cx6MFwjEuOsu52WNvxdsiWxcdXtmMfaj4ZjSYJpvAvF8Mu6oTNFUi0bFo5MqZV6WoX1x541g1RI64Dwvh4NVrLUmU2DctatU7yU0MZaJVvP90J1SnH8Q44LkNg6jBMgEZI8-aHVU2OMAcOcBxpS6NkBUruBffbohJQBnUQNe9esGTJhj7Y3j7E6cF_7mGWppeJ6MqshEe2Yz4Lu1G4WtfzjsG5dyqSNz7XknreMCz1BCzJRIKlcXNxtfzFisVttYOE4ctO5JX9hzN77QX8ePeGQGNJOeve_xMYmkjfIPCWjAVKO8hg       

3. **Executive Producer** -    
Email: executive_producer@udacity.com    
Password: Test12345     
JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFHbVNvLXplMEtHRFE1NUlid3BqMCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zbmNkcjZlby5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDE4M2M1Y2Q5NmIwMDcwMzI4NWMzIiwiYXVkIjoiY2FzdGluZ0FnZW5jeSIsImlhdCI6MTYzNDg0NjA2NCwiZXhwIjoxNjM0ODUzMjY0LCJhenAiOiJyRWdDRGtYWTNXN2ZmWTgyN2Y5R2hzdGUxWHlnSjUzeSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMtZGV0YWlsIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.HxU4MoYOYLncj7wZqYcs1inRbYhV-yvzrAFpywPShBTm5ub1firfg9edPRoshTr69tdtJlXl9T3DA4jKyEUlruW4-ZpmN-SzesEzckceOepRchI2-jvXIGOhbI0pYX3XfHsNlcWQ1bh2vMO6NYl17T6wChrEDsvJMjdHskCp4-i4aNGPMldg4Sc9M2PGbG2k3mMTIcqFV26HAbGKRwlYfktQNvap5GQVfvS1aodpLf6IDWs17WNZ-VPmgmNOsGJzwuMy3Xr5GCBwy-bPu1cNpYLZeA9oJ6pPtDuXouvz48owILW44PQThTl2Fo4kxmkTVtQ-4grEQrJdEZp0SsQl-A

## App URL
https://fsnd-capstone-pranay.herokuapp.com/ 
## Heroku git
https://git.heroku.com/fsnd-capstone-pranay.git
## Database URL
DATABASE_URL: postgres://qsddbmjunllkib:af8798d20d60936e0b969f76c464050f80f9899c404486e1d1a419be3663ad48@ec2-3-218-71-191.compute-1.amazonaws.com:5432/dqfnmdfqk1k69