# Django-Backend-Server-Project
Django Server Assignment for Users, Banks, and Branches. Implemented Login, Authentication, Form Validation, and CRUD views/ API Endpoints w/ Basic Front-End

In this assignment, I created a small Django application. Since it was an educational assignment, the overall goal was to obtain initial experience in backend development and Django.

The server is coded with Python 3.8, 3.9, 3.10, or 3.11 and Django version 4.1.

# Overview and Tasks Completed:
- You are to create two models: Bank and Branch. A bank has a name, swift code, institution number, and description. All of them are strings that do not exceed 100 characters and cannot be null. Moreover, each bank has an owner that points to Django's User model. A bank also has a set of branches.

- A branch has a name, transit number, and address, all of which are strings that do not exceed 100 characters and cannot be null. Moreover, every branch has an email (with its specific validations) which is by default set to ```admin@utoronto.ca.``` Each branch has a capacity (non-negative integer) that could be left unspecified. It should also have last_modified, a field that stores the last modification time. The primary key for both models must remain the default auto-incrementing integers.
