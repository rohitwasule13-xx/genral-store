from django.http import HttpResponse


PRODUCTS = [
    {"name": "Rice", "category": "Groceries", "price": 80.00, "stock": 30},
    {"name": "Sugar", "category": "Groceries", "price": 60.00, "stock": 40},
    {"name": "Biscuits", "category": "Snacks", "price": 35.00, "stock": 50},
    {"name": "Cooking Oil", "category": "Groceries", "price": 120.00, "stock": 25},
    {"name": "Soap", "category": "Personal Care", "price": 45.00, "stock": 60},
    {"name": "Detergent", "category": "Household", "price": 200.00, "stock": 22},
]


def nav_html(active_page="home"):
    pages = {
        "home": "/",
        "products": "/products/",
        "cart": "/cart/",
        "checkout": "/checkout/",
        "admin": "/admin-panel/",
    }
    items = []
    for name, url in [
        ("Home", pages["home"]),
        ("Products", pages["products"]),
        ("Cart", pages["cart"]),
        ("Checkout", pages["checkout"]),
        ("Admin", pages["admin"]),
    ]:
        current = "style='font-weight:bold; color:#f59e0b;'" if name.lower() == active_page else ""
        items.append(f"<a href='{url}' {current}>{name}</a>")
    return "".join(items)


def home(request):
    cards = "".join(
        f"<div class='card'><h3>{item['name']}</h3><p>{item['category']}</p><strong>KES {item['price']:.2f}</strong></div>"
        for item in PRODUCTS[:4]
    )
    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>General Store | Home</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f4f6; color: #111827; }}
            nav {{ background: #111827; padding: 18px 30px; display: flex; gap: 20px; flex-wrap: wrap; }}
            nav a {{ color: white; text-decoration: none; font-weight: 600; }}
            .container {{ max-width: 1100px; margin: 32px auto; padding: 0 18px; }}
            .hero {{ background: linear-gradient(135deg, #0f766e, #14b8a6); color: white; padding: 50px; border-radius: 18px; }}
            .hero h1 {{ font-size: 2.5rem; margin-top: 0; }}
            .btn {{ display:inline-block; background:#f59e0b; color:#111827; padding:12px 18px; border-radius:10px; text-decoration:none; font-weight:700; margin-top:12px; }}
            .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:18px; margin-top:30px; }}
            .card {{ background:white; padding:22px; border-radius:12px; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }}
            .card h3 {{ margin-bottom: 8px; }}
        </style>
    </head>
    <body>
        <nav>{nav_html('home')}</nav>
        <div class="container">
            <section class="hero">
                <h1>Welcome to General Store</h1>
                <p>Everyday essentials, groceries, snacks, household items, and personal care products—all in one place.</p>
                <a href="/products/" class="btn">Shop Now</a>
            </section>

            <div class="grid">
                {cards}
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def products(request):
    product_cards = "".join(
        f"<div class='card'><h3>{item['name']}</h3><p>{item['category']}</p><strong>KES {item['price']:.2f}</strong><p>Stock: {item['stock']}</p><button>Add to cart</button></div>"
        for item in PRODUCTS
    )
    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Products | General Store</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f4f6; color: #111827; }}
            nav {{ background: #111827; padding: 18px 30px; display: flex; gap: 20px; flex-wrap: wrap; }}
            nav a {{ color: white; text-decoration: none; font-weight: 600; }}
            .container {{ max-width: 1100px; margin: 32px auto; padding: 0 18px; }}
            h1 {{ margin-bottom: 20px; }}
            .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:18px; }}
            .card {{ background:white; padding:22px; border-radius:12px; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }}
            button {{ background:#16a34a; color:white; border:none; padding:10px 14px; border-radius:8px; cursor:pointer; margin-top:10px; }}
        </style>
    </head>
    <body>
        <nav>{nav_html('products')}</nav>
        <div class="container">
            <h1>Our Products</h1>
            <div class="grid">
                {product_cards}
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def cart(request):
    cart_items = [
        ("Rice", "1", "KES 80.00"),
        ("Soap", "2", "KES 90.00"),
    ]
    rows = "".join(f"<tr><td>{name}</td><td>{qty}</td><td>{price}</td></tr>" for name, qty, price in cart_items)
    html = f"""
    <!doctype html>
    <html>
    <head><title>Cart | General Store</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f4f6; color: #111827; }}
        nav {{ background: #111827; padding: 18px 30px; display: flex; gap: 20px; flex-wrap: wrap; }}
        nav a {{ color: white; text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 900px; margin: 32px auto; padding: 0 18px; }}
        table {{ width:100%; background:white; border-collapse: collapse; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }}
        th, td {{ padding: 14px; border-bottom: 1px solid #e5e7eb; text-align:left; }}
    </style>
    </head>
    <body>
        <nav>{nav_html('cart')}</nav>
        <div class="container">
            <h1>Your Cart</h1>
            <table>
                <thead><tr><th>Product</th><th>Qty</th><th>Price</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def checkout(request):
    html = f"""
    <!doctype html>
    <html>
    <head><title>Checkout | General Store</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f4f6; color: #111827; }}
        nav {{ background: #111827; padding: 18px 30px; display: flex; gap: 20px; flex-wrap: wrap; }}
        nav a {{ color: white; text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 800px; margin: 32px auto; padding: 0 18px; }}
        form {{ background:white; padding:24px; border-radius:12px; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }}
        input, button {{ display:block; width:100%; margin:10px 0; padding:12px; border-radius:8px; border:1px solid #d1d5db; }}
        button {{ background:#111827; color:white; border:none; }}
    </style>
    </head>
    <body>
        <nav>{nav_html('checkout')}</nav>
        <div class="container">
            <h1>Checkout</h1>
            <form>
                <input type="text" placeholder="Customer name" />
                <input type="text" placeholder="Phone number" />
                <textarea placeholder="Delivery address" rows="4" style="width:100%; margin:10px 0; padding:12px; border-radius:8px; border:1px solid #d1d5db;"></textarea>
                <button type="submit">Place Order</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def admin_panel(request):
    orders = [
        ("#1001", "Aisha", "0712345678", "KES 350.00"),
        ("#1002", "Daniel", "0798765432", "KES 520.00"),
    ]
    rows = "".join(f"<tr><td>{oid}</td><td>{name}</td><td>{phone}</td><td>{total}</td></tr>" for oid, name, phone, total in orders)
    html = f"""
    <!doctype html>
    <html>
    <head><title>Admin | General Store</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f3f4f6; color: #111827; }}
        nav {{ background: #111827; padding: 18px 30px; display: flex; gap: 20px; flex-wrap: wrap; }}
        nav a {{ color: white; text-decoration: none; font-weight: 600; }}
        .container {{ max-width: 900px; margin: 32px auto; padding: 0 18px; }}
        table {{ width:100%; background:white; border-collapse: collapse; box-shadow: 0 8px 22px rgba(0,0,0,0.08); }}
        th, td {{ padding: 14px; border-bottom: 1px solid #e5e7eb; text-align:left; }}
    </style>
    </head>
    <body>
        <nav>{nav_html('admin')}</nav>
        <div class="container">
            <h1>Admin Panel</h1>
            <table>
                <thead><tr><th>Order ID</th><th>Customer</th><th>Phone</th><th>Total</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
