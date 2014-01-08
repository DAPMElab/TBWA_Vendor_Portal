
#Admin


###Project Structure

`base.html`

- the base html file used on all pages
- all js file imports are here

`js`

- `app.js`
  - app file where everything is tied together
- `controllers.js`
  - declares all controllers
- `services.js`
  - reusable functions
- `values.js`
  - constant values used in various parts of the app
- `controllers`
  - `reviews.js`
    - controls `/admin#/`
    - lists all pending reviews with an option to approve or dismiss
    - tied to `/partials/reviews.html`
  - `companies.js`
    - controls `/admin#/companies`
    - lists all companies with options to edit them
    - tied to `/partials/listCompany.html`
  - `editCompany.js`
    - facilitates editting the information of a company
    - controls `admin#/companies/edit/< cid >`
    - tied to `/partials/editCompanyButtons.html`
    - shares `/partials/company.html` with `newCompany.js`
  - `newCompany.js`
    - facilitates the creation of a company
    - controls `admin#/companies/new`
    - tied to `/partials/company.html` & `/partials/newCompanyButtons.html`
  - `newAdmin.js`
    - allows the admin to create another admin profile
    - controls `/admin#/new`
    - tied to `/partials/newAdmin.html`
  - `navbar.js`
    - controls highlighting the correct menu item based on the current page
    - tied to `/partials/navbar.html`

