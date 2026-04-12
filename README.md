My first todo APi in fast api. 

what can it do:
-sign up/login
-create todo
-get todo
-update todo
-delete todo

After login it gives jwt token everytime and with this token user can skip login next time, and only access to his datas.

Endpoints:
- POST /signup
- POST /login
- POST /todo
- GET /todo
- DELETE /todo
- PATCH /todo

To use:
pip install -r requirements.txt
uvicorn app.main:app --reload
