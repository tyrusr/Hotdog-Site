# Hotdog

This site was more of a fast food clone that allowed users to brows a menu. And if they wanted to order something they need to create a profile and then they can add items in their cart, once they can remove the items in the cart and "purchase" items which then puts their items into a different models object for purchase history which currently isnt available to the user and only for admin purposes currently.

## Video Demo

[Watch the Demo](https://youtu.be/5NOn56OB5FQ)

## Features

- User authentication (registration, login, logout)
- Browse menu items without logging in
- Add items to a shopping cart (authenticated users only)
- Remove items from the cart before checkout
- Place an order and simulate a purchase
- Orders are stored in a separate purchase history model (admin access only)
- Admin interface for managing menu items, orders, and users via Django's admin panel

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Django
- Database: SQLite
