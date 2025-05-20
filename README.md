<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/shmartin/mit113">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Simple Eatery POS</h3>

  <p align="center">
    a simple pos system for an eatery
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This website project is created by Juan Martin Abad, a student of Master in Information Technology in School of Advanced Studies, Saint Louise University for the subject Advanced Web Concepts.

A Point of Sale (POS) website for a mom-and-pop eatery for easier transactions and inventory management.

The website should be able to:

- Have a login system for different users
- Limit navigation based from logged in user
- Be used in different devices (Responsive Web)

The possible user of the website are the following:

- Owner
- Cashier
- Manager(administrator)

The website design should also be considered for easy navigation and usage.

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started. To avoid retyping too much info, do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`, `project_license`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- FEATURES -->
## Features

### Cashier Page Features

- Dynamic Products section*
- New products added in ***Inventory*** appears automatically**
- Images for new products can easily be added by just copying image file to appropriate folder***
- Built-in numpad
- Quick search for product

> *Notes:*
>  
> **Unavailable products will not appear*
>
> ***Dynamic loading of UI elements*
>
> ****Image folder is in static/images/*

### Inventory Page Features

- Simple UI for easier inventory management
- Add, update or delete inventory entry within the webpage

### Database design

The database will have to store daily transactions and inventory changes. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Django][django-shield]][django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

For the website to work, the Django Python library should be installed

* django
  ```sh
  pip3 install django
  ```

### Starting the server

1. Clone the repo
   ```sh
   git clone https://github.com/shmartin/mit113.git
   ```
2. Move into root directory
   ```sh
   cd mit113/finals
   ```
3. Start server 
   ```js
   python3 manage.py runserver 0.0.0.0:8000
   ```
4. Access the website from a browser. Enter in URL bar
   ```sh
   localhost:8000
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[django-url]: https://www.djangoproject.com/


[product-screenshot]: images/screenshot.png