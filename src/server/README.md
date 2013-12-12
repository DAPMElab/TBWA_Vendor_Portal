
#Routes


##Data

GET `/data`

- @data: none
- @return: json list w/ limited data on every company

GET `/data/< uid >`

- @data: none
- @return: json with all data for that exact company


##Reviews

POST `/review/create`

- @data: json w/ `company`, `submitter`, `rating`, `title` & `description`
- @return: 201 w/ `uid` for review

GET `/review/get/< uid >`

- @data: None
- @return: 200 & json w/ `company`, `submitter`, `rating`, `title`, `description` & `approved` (boolean status)

GET  `/review/list`

- @data: none
- @return: 200 & json w/ two fields, `count` & `data` (list of reviews)

PATCH `/review/edit/< uid >`

- @data: json w/ data being changed
- @return: 200

POST `/review/approve/< uid >`

- @data: none
- @return: 200

DELETE `/review/delete/< uid >`

- @data: none
- @return: 202


##Admin

POST `/admin/create`

- @data: json w/ `email`, `password` & `repeat_password` fields
- @return: 201 & json w/ `uid`

POST `/admin/login`

- @data: json w/ `email` & `password`
- @return: 201




