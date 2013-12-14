
#Routes


-------------------------------------------------------------------------------------------------------
##Companies

####POST `/company/create`

- @data: json w/ `Name`, & `URL` and hopefully more data
- @return: 201 w/ `uid` for review

####GET `/company/get/< uid >`

- @data: None
- @return: 200 & json w/ all fields & reviews
- @return: 200 & json w/ all data for a company

Example:

```javascript
'data': {
  "Agency":  "BBDO" ,
  "AltName":  " " ,
  "Categories": [
    "Directorial" ,
    "Production"
  ] ,
  "Classifications": [
    "MBE"
  ] ,
  "Clients": [ ],
  "Contact": {
    "Email":  "" ,
    "Name":  "" ,
    "Phone":  ""
  } ,
  "DBA":  "" ,
  "Name":  "La Fabrica Films USA, LLC" ,
  "Path":  "busdev/vpd/Lists/Best In Class Small  Minority Owned Vendors" ,
  "PhysicalAddress": {
    "Address":  "" ,
    "City":  "Miami  " ,
    "State":  "" ,
    "ZipCode":  ""
  } ,
  "RemitAddress": {
    "Address":  "" ,
    "City":  "" ,
    "State":  "" ,
    "ZipCode":  ""
  } ,
  "ReviewIds" : [ ],
  "URL": http://www.lafabrica.tv/, »
  "id":  "0b7fd79f-7a44-455b-8f65-33b779f80878"
}
```

####GET  `/company/list`

- @data: none
- @return: 200 & json w/ two fields, `count` & `data` (list of companies with limited data)

```javascript
{
  count: 2,
  data: [
    {
      Name: "The Studio ",
      AverageReview: null,
      URL: "http://www.studionyc.com/",
      DBA: "",
      ReviewIds: [ ],
      id: "054d9cb7-a822-43d1-8886-cb49dd36e11b"
    },
    {
      Name: "Crossroads Films",
      AverageReview: null,
      URL: "http://crossroadsfilms.com/",
      DBA: "",
      ReviewIds: [ ],
      id: "09a39b24-d392-4962-8357-9fc687f0926f"
    }
  ]
}
```


####GET  `/company/list/all`

- admin only
- @data: none
- @return: 200 & json w/ two fields, `count` & `data` (list of companies with all data)
- @PLANNED: include relevant review id's

####PATCH `/company/edit/< uid >`

- @data: json w/ data being changed
- @return: 200


####DELETE `/company/delete/< uid >`

- @data: none
- @return: 202

-------------------------------------------------------------------------------------------------------
##Reviews

####POST `/review/create`

- @data: json w/ `company`, `submitter`, `rating`, `title` & `description`
- @return: 201 w/ `uid` for review

####GET `/review/get/< uid >`

- admin only
- @data: None
- @return: 200 & json w/ `company`, `submitter`, `rating`, `title`, `description` & `approved` (boolean status)

####GET  `/review/list`

- admin only
- @data: none
- @return: 200 & json w/ two fields, `count` & `data` (list of reviews)

####PATCH `/review/edit/< uid >`

- admin only
- @data: json w/ data being changed
- @return: 200

####POST `/review/approve/< uid >`

- admin only
- @data: none
- @return: 200

####DELETE `/review/delete/< uid >`

- admin only
- @data: none
- @return: 202


-------------------------------------------------------------------------------------------------------
##Admin

####POST `/admin/create`

- @data: json w/ `email`, `password` & `repeat_password` fields
- @return: 201 & json w/ `uid`

####POST `/admin/login`

- @data: json w/ `email` & `password`
- @return: 201




