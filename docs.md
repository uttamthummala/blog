# Django Blog CMS Views Documentation

This documentation provides information about the views in the Django Blog CMS application.

## Table of Contents

1. [User Logout (`user_logout`)](#user-logout)
2. [User Login (`user_login`)](#user-login)
3. [User Register (`user_register`)](#user-register)
4. [Dashboard (`dashboard`)](#dashboard)
5. [Article Detail (`article_detail`)](#article-detail)
6. [Edit Article (`edit_article`)](#edit-article)

## User Logout (`user_logout`)

The `user_logout` view logs out the currently authenticated user.

- **URL:** `/logout`
- **Method:** `GET`
- **Authentication:** Required
- **Success Response:**
  - Redirects to the login page
- **Usage:**
  ```html
  <a href="{% url 'user_logout' %}" class="btn btn-danger">Logout</a>

# User Login (`user_login`)

The `user_login` view handles user login.

## Endpoint

- **URL:** `/login`
- **Method:** `GET` and `POST`
- **Authentication:** Not required

## Description

This view allows users to log in to the Django Blog CMS application. Users provide their credentials, and upon successful authentication, they are redirected to the dashboard.

## Usage

### Login Form

```html
 <form method="post" action="{% url 'login' %}">
        {% csrf_token %}
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" class="form-control" id="username" name="username" required>
        </div>

        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" class="form-control" id="password" name="password" required>
        </div>

        <button type="submit" class="btn btn-primary">Login</button>
    </form>
```
- **Success Response:**
  - Redirects to the dashboard page
- **Error Response:**
  - Displays Error message

# User Register (`user_register`)

The `user_register` view handles user registration.

## Endpoint

- **URL:** `/register`
- **Method:** `GET` and `POST`
- **Authentication:** Not required

## Description

This view allows users to register for a new account in the Django Blog CMS application. Users provide their desired username and password. Upon successful registration, they can log in to the system.

## Usage

### Registration Form

```html
 <form method="post" action="{% url 'register' %}">
        {% csrf_token %}

        <div class="form-group">
          <label for="username">Username:</label>
          <input
            type="text"
            class="form-control"
            id="username"
            name="username"
            required
          />
        </div>

        <div class="form-group">
          <label for="password1">Password:</label>
          <input
            type="password"
            class="form-control"
            id="password1"
            name="password1"
            required
          />
        </div>

        <div class="form-group">
          <label for="password2">Confirm Password:</label>
          <input
            type="password"
            class="form-control"
            id="password2"
            name="password2"
            required
          />
        </div>

        <button type="submit" class="btn btn-success">Register</button>
      </form>
```
- **Success Response:**
  - Redirects to the login page
- **Error Response:**
  - Displays Error message
# Article Detail (`article_detail`)

The `article_detail` view displays detailed information about a specific article.

## Endpoint

- **URL:** `/article/{article_id}`
- **Method:** `GET`
- **Authentication:** Required (User must be logged in)

## Description

This view provides a detailed overview of a specific article. It displays the title, content, author, publication date, and tags associated with the article. Additionally, it checks if the logged-in user is a staff member.

## Usage

### Article Detail Information

```html
<div class="container mt-5">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">{{ article.title }}</h2>
                <p class="card-text">{{ article.content|safe }}</p>

                {% if article.file %}
                <div class="mt-3">
                    <h4>Attached Files:</h4>
                    <ul>
                        <li>
                            <a href="{{ article.file.url }}" target="_blank">{{ article.file.name }}</a>
                        </li>
                    </ul>
                </div>
                {% endif %}

                <p class="card-text">
                    <small class="text-muted">
                        Author: {{ article.author.username }} | Published on: {{ article.publication_date }}
                    </small>
                </p>

                {% if user.is_authenticated and user == article.author or user.is_staff %}
                <div class="btn-group">
                    <a href="{% url 'edit_article' article.id %}" class="btn btn-primary">Edit</a>
                    <a href="{% url 'delete_article' article.id %}" class="btn btn-danger custom" onclick="return confirmDelete();">Delete</a>

                    <script>
                        function confirmDelete() {
                            return confirm("Are you sure you want to delete this article?");
                        }
                    </script>
                </div>
                {% endif %}
            </div>
        </div>
        <a href="{% url 'dashboard' %}" class="btn btn-primary mt-3">Back to Dashboard</a>
    </div>
```
- **Delete Confirmation:**
  - A confirmation dialog is displayed when the user attempts to delete the article.
- **Success Response:**
  - The view successfully renders with detailed information about the article, and additional options such as edit and delete are available to the article owner or staff.
- **Error Response:**
  - If there is an issue retrieving the article or the user does not have the required permissions, an error message will be displayed.
# Edit Article (`edit_article`)

The `edit_article` view allows the author or a staff member to modify the details of a specific article.

## Endpoint

- **URL:** `/edit/{article_id}`
- **Method:** `GET` (to display the edit form), `POST` (to submit changes)
- **Authentication:** Required (User must be logged in)

## Description

This view provides a form for editing the details of a specific article, including the title, content, and tags. If the logged-in user is the author of the article or a staff member, they can make changes and save the updated article.

## Usage

### Edit Article Form

```html
<div class="container mt-5">
    <div class="card">
        <div class="card-header bg-primary text-white">
            <h2 class="mb-0">Edit Article</h2>
        </div>
        <div class="card-body">
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="form-group">
                    <label for="id_title">Title</label>
                    <input type="text" id="id_title" name="title" value="{{ article.title }}" class="form-control">
                </div>
                <div class="form-group">
                    <label for="id_content">Content</label>
                    <textarea id="id_content" name="content" class="form-control">{{ article.content }}</textarea>
                </div>
                <div class="form-group">
                    <label for="id_tags">Tags</label>
                    <input type="text" id="id_tags" name="tags" value="{{ article.tags }}" class="form-control">
                </div>
                <div class="form-group">
                    <label for="id_file">File</label>
                    <input type="file" id="id_file" name="file" class="form-control-file">
                    {% if article.file %}
                        <p class="mt-2">Current File: <a href="{{ article.file.url }}" target="_blank">{{ article.file.name }}</a></p>
                    {% endif %}
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
        </div>
    </div>
</div>


```
- **Success Response:**
  - The view successfully renders with detailed information about the edited article, and a successfully edited message is displayed.
- **Error Response:**
  -If there are validation errors in the form or the user does not have the necessary permissions, appropriate error messages may be displayed.
  
