# Django-Backend-Server-Project
Django Server Assignment for Users, Banks, and Branches. Implemented Login, Authentication, Form Validation, and CRUD views/ API Endpoints w/ Basic Front-End.

In this assignment, I created a small Django application. Since it was an educational assignment, the overall goal was to obtain initial experience in backend development and Django.
I will be detailing the requirements and features outlined in the handout to show what I have experience with.

The server is coded with Python 3.8, 3.9, 3.10, or 3.11 and Django version 4.1.

## Detailed Overview and Tasks From Handout:
- You are to create two models: Bank and Branch. A bank has a name, swift code, institution number, and description. All of them are strings that do not exceed 100 characters and cannot be null. Moreover, each bank has an owner that points to Django's User model. A bank also has a set of branches.

- A branch has a name, transit number, and address, all of which are strings that do not exceed 100 characters and cannot be null. Moreover, every branch has an email (with its specific validations) which is by default set to ```admin@utoronto.ca.``` Each branch has a capacity (non-negative integer) that could be left unspecified. It should also have last_modified, a field that stores the last modification time. The primary key for both models must remain the default auto-incrementing integers.

## General behavior of forms
The following general rules applies to every endpoint that accepts both GET and POST methods:

- The GET request expects an HTML form with the fields listed by payload. That is, each payload field must appear as an <input> with the appropriate type and name.
- Upon submission, a POST request should be sent to the same endpoint. If data is valid, the specified task should be fulfilled, and the user is redirected to the success URL. Otherwise, the same form must be rendered with all relevant error messages listed in validation errors.
- In case of invalid data, all user inputs (except for passwords) must be preserved so that the user will not have to re-enter everything again.
- Input types must adhere to the original field type of their models. For example, the password fields should be rendered with <input type="password">, email fields should be rendered <input type="email">, etc.
- The above rule (or, in general, adding attributes to the form) is merely for UX purposes and has nothing to do with your backend. That is, your backend code must still check for the required fields and validations. 

Note: Your code must be resilient towards invalid/malicious requests. For example, the client might intentionally discard some fields and not send them (note that this is different from sending empty or blank values). Moreover, it can send additional fields that are not listed. In either case, your code must not break. Instead, it should treat missing values as blanks and ignore extra fields.

## HTTP status codes
All requests should be responded to with an HTTP 200 OK status code unless otherwise specified. In case of redirects, your status code must be 302 FOUND. You must check for client errors in the following order: 401 UNAUTHORIZED, 404 NOT FOUND, and 403 FORBIDDEN. That is, for example, at the create branch view, if the request is not authenticated and the bank ID is invalid as well, you should return 401 UNAUTHORIZED. Your server must never return a 500 INTERNAL SERVER ERROR.

# Section 1: As simple as Auth!
You will start off with the authentication views. You are to implement views for register, login, and logout. You are very well allowed to use the default User model in Django. In fact, you are strongly advised against creating your own custom auth model as it may mess with Django's default User model. Moreover, why bother yourselves?

- Endpoint: ```/accounts/register/```

  Methods: ```GET```, ```POST```

  Fields/payload: ```username, password1, password2, email, first_name, last_name```

  Success URL: ```/accounts/login/```

  Validation errors: (copy and paste the exact error message)

  - ```The two password fields didn't match```
  - ```A user with that username already exists```
  - ```This password is too short. It must contain at least 8 characters```
  - ```Enter a valid email address```
  - Username, password, and repeat password are required. If empty, show the following error above the problematic field(s): ```This field is required```

  Additional notes:
  Only ```username```, ```password1```, and ```password2``` are required. The other fields are optional.
  All fields will be at most 100 characters long in our tests for this specific endpoint.
---
* Endpoint: ```/accounts/login/```

  Methods: ```GET, POST```

  Fields/payload: ```username, password```

  Success URL: ```/accounts/profile/view/```

  Invalid inputs: (copy and paste the exact error message)
  - ```Username or password is invalid```
    
  Additional notes: If the credentials are valid, use Django's session authentication to log the user in.
---

- Endpoint: ```/accounts/logout/```

  Methods: ```GET```

  Description: Log the user's session out of Django. If the user is unauthenticated, simply ignore the request. In either case, return a redirect to ```/accounts/login/```

# Section 2: Profile heroes
In this question, you will implement the view and edit profile functionalities. Note that you should return HTTP 401 UNAUTHORIZED if the request is unauthenticated.

- Endpoint: ```/accounts/profile/view/```
 
  Methods: ```GET```
  
  Fields: ```id, username, email, first_name, last_name```
  
  Description: Return a JSONLinks to an external site. string with the above fields, disclosing data of the logged-in user. Note that your response should not contain any HTML at all.
  
  Example response:
  ```{"id": 1, "username": "Demon", "email": "demon@gmail.com", "first_name": "", "last_name": ""}```
---

- Endpoint: ```/accounts/profile/edit/```

  Methods: ```GET, POST```

  Fields/payload: ```first_name, last_name, email, password1, password2```

  Success URL: ```/accounts/profile/view/```

  Validation errors: (copy and paste the exact error message)
  - ```The two password fields didn't match```
  - ```This password is too short. It must contain at least 8 characters```
  - ```Enter a valid email address```
  
  Additional notes:
  - At GET requests, the form (except for the password fields) must be already filled out with the current user's values.
  - At the POST requests, no field is required. If any field is empty or missing, the corresponding value should be updated to empty, with the only exception of passwords. If ```password1``` and ```password2``` are empty, it means that the user did not want to change its password; so no changes will be made to the user's password.
  - The redirect should show the user's info without having to log in again.

# Section 3: If you know forms, you know.

Now, let us move to the banks app. You will implement two important forms; one for creating a new bank and another one for creating a new branch. You might want to create a forms directory in your app and put a Form class for each view there.

Moreover, the below views are login required. If the request is unauthenticated, a 401 UNAUTHORIZED response must be returned.

- Endpoint: ```/banks/add/```

  Methods: ```GET, POST```

  Fields/payload: ```name, description, inst_num, swift_code```

  Success URL: ```/banks/<bank_id>/details/```

  Validation error:
  - If a field's input has more than 100 characters, put the following error above that field: ```Ensure this value has at most 100 characters (it has <X>)```, where <X> is the current input's length.
  - All fields are mandatory and cannot be left blank. If so, the following error must be shown above the problematic field(s): ```This field is required```

  Additional notes:

  Your code must infer the owner of the new account from the current logged-in user of the session. Therefore, you must not include an owner field in your form.
  bank_id is the ID of the newly-created bank.
---
  
- Endpoint: ```/banks/<bank_id>/branches/add/```

  Methods: ```GET, POST```

  Fields/payload: ```name, transit_num, address, email, capacity```

  Success URL: ```/banks/branch/<branch_id>/details/```

  Validation errors:
  - ```This field is required``` (for all fields except for capacity)
  - If a field's input has more than 100 characters, put the following error above that field: ```Ensure this value has at most 100 characters (it has <X>)```, where <X> is the current input's length. This applies to all fields except for email and capacity.
  - If capacity is negative, put ```Ensure this value is greater than or equal to 0``` above it.
  - ```Enter a valid email address```
  
  Additional notes:
  - The form must prefill the email input with the default value. Obviously, the user should be able to edit it. 
  - The bank to which the new branch belongs must be fetched using ```bank_id``` from the URL args. If no bank exists with such an ID, both GET and POST should return 404 NOT FOUND.
  - The user must be the owner of the corresponding bank; otherwise, a 403 FORBIDDEN must be returned (both GET and POST). In other words, users must not be able to add a branch to someone else's bank.
  - The ```branch_id``` in the success URL is the ID of the newly-created branch.

# Section 4: Digital banking

Now, it is time for some CRUD views for banks. These views should be accessible by everyone, even unauthenticated requests.

- Endpoint: ```/banks/all/```

  Methods: ```GET```

  Description: An HTML response must be returned that lists all banks. The page should show the name and institution number of each bank in an unordered list (separated by space), where each name links to the details page of the corresponding bank.

  Example response (source): The auto tester will only check the \<ul> tag's content, so feel free to modify the rest of the HTML in any way.
    ```
    <html>
    <body>
     List of banks
     <ul>
      <li><a href="/banks/1/details">CIBC</a> 010</li>
      <li><a href="/banks/2/details">BMO</a> 001</li>
      <li><a href="/banks/3/details">TD</a> 004</li>
     </ul>
    </body>
    </html>
    ```
  ---
- Endpoint: ```/banks/<bank_id>/details/```

  Methods: ```GET```

  Description: An HTML response must be returned that contains the information of a specific bank (or a 404 NOT FOUND if it does not exist) and some info about its branches. The bank information to be shown is the bank name (wrapped by an \<h1>), its description, swift code, institution number, and its branches. Display the branch information in a table, where each row contains a branch's name, transit number, and address. If the bank does not have any branches, include ```No branch found``` in your HTML response.

  Example response (rendered): Note that in this part, and only this part, we only check values and ignore the labels. So it does not matter if you use different labels or structure your HTML differently, as long as they comply with the above description.

# Section 5: Branching

Finally, we end this assignment with some branch CRUD views. Both views are authenticated, meaning that you should return 401 UNAUTHORIZED if the user is not logged in. Using a FormView for the second view is recommended.

- Endpoint: ```/banks/branch/<branch_id>/details/```

    Methods: ```GET```

    Description: A JSON response that returns the detailed info of a branch (or a 404 NOT FOUND if it does not exist). Note that the entire HTTP response is a JSON string.

    Fields: ```id```, ```name```, ```transit_num```, ```address```, ```email```, ```capacity```, ```last_modified```

    Example response:

    ```{"id": 1, "name": "jkl", "transit_num": "12", "address": "jlk", "email": "admin@utoronto.ca", "capacity": 12, "last_modified": "2022-01-08T22:30:40.419Z"}```

---
- Endpoint: ```/banks/branch/<branch_id>/edit/```

  Methods: ```GET, POST```

  Fields/payload: ```name, transit_num, address, email, capacity```

  Success URL: ```/banks/branch/<branch_id>/details/```

  Validation errors:
  - ```This field is required``` (for all fields except for capacity)
  - If a field's input has more than 100 characters, put the following error above that field: ```Ensure this value has at most 100 characters (it has <X>)```, where <X> is the current input's length. This applies to all fields except for email and capacity.
  - If capacity is negative, put ```Ensure this value is greater than or equal to 0``` above it.
  - ```Enter a valid email address```
  

  Additional notes:
  - The form must be pre-filled with the current values of the branch instance.
  - The branch's bank is not changeable; hence it should not be a part of the form.
  - The user must be the owner of the corresponding bank; otherwise, a 403 FORBIDDEN response must be returned (both GET and POST). In other words, users must not be able to modify someone else's branches.

--- 
# Tester for Correctness
A tester is provided to you that runs some basic checks on my project. For example, it checks the endpoints and sends some simple requests to them.

### Here the instructions on running the pre-tests here:
File: a2-pretester.py

### How to run:
```pip install requests or python3 -m pip install requests
python3 a2-pretester.py
```

### Assignment grade after submission: 97/100.


