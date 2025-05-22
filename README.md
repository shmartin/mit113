<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Simple Eatery POS</h3>

  <p align="center">
    a simple pos system for an eatery
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This website project is created by Juan Martin Abad, a student of Master in Information Technology in School of Advanced Studies, Saint Louise University for the subject Advanced Web Concepts.

A Point of Sale (POS) website for a mom-and-pop eatery for easier transactions and inventory management.

The website:

- Have a login system for different users
- Limit navigation based from logged in user
- Be used in different devices (Responsive Web)

The possible user of the website are the following:

- Inventory user
- Cashier user
- Manager(administrator)

The website design also considered for easy navigation and usage as it is desined with touchscreens in mind.

### Built With

* [![Django][django-shield]][django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- FEATURES -->
## Features

### Cashier Page Features

- Only accessible by Cashier account
- Dynamic Products section
- New products added in ***Inventory*** appears automatically
- Images for new products can easily be added by just copying image file to appropriate folder
- Built-in denominations numpad (numpad with denominations instead of traditional numpad)

### Reports Page Features

- Only accessible by Cashier account
- Simple UI for faster reports management
- Date range to filter transactions by date

### Inventory Page Features

- Only accessible by Inventory account
- Simple UI for easier inventory management
- Add, update or delete inventory entry within the webpage

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

### Add an admin account

Adding an admin account enables adding or modifying products, prices, and users.

1. Move to the `finals` directory
   ```sh
   cd finals
   ```

2. Create a superuser then add the corresponding information with the succeeding prompts
   ```sh
   python3 manage.py createsuperuser
   ```

3. Login with the newly created account with the URL
   ```sh
   localhost:8000/admin
   ```

### Add meal image

Images can easily be added to the menu grid. Simply add the image with the filename corresponding with the exact product name added into the `Products` model into the `images` folder within the `static` directory.

Example:

```sh
.
└── finals
    └── static
        └── images
            ├── Beef Tapa_gray.jpeg
            └── Beef Tapa.jpeg
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[django-shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[django-url]: https://www.djangoproject.com/


[product-screenshot]: images/screenshot.png