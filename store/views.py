from django.http import HttpResponse


def home(request):
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>General Store</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; color: #222; }
            nav { background: #1f2937; padding: 18px 25px; }
            nav a { color: white; text-decoration: none; margin-right: 18px; font-weight: 600; }
            .container { max-width: 1100px; margin: 32px auto; padding: 0 20px; }
            .hero { background: linear-gradient(135deg, #0f766e, #14b8a6); color: white; padding: 48px; border-radius: 18px; }
            .btn { display:inline-block; background:#f59e0b; color:#111827; padding:12px 18px; border-radius:10px; text-decoration:none; font-weight:600; margin-top:12px; }
            .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:18px; margin-top:30px; }
            .card { background:white; padding:20px; border-radius:12px; box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
        </style>
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/products/">Products</a>
            <a href="/cart/">Cart</a>
            <a href="/checkout/">Checkout</a>
            <a href="/admin-panel/">Admin</a>
        </nav>
        <div class="container">
            <section class="hero">
                <h1>Welcome to General Store</h1>
                <p>Daily essentials, groceries, home care and personal care products in one place.</p>
                <a href="/products/" class="btn">Shop Now</a>
            </section>

            <div class="grid">
                <div class="card"><h3>Rice</h3><p>Premium long grain rice</p></div>
                <div class="card"><h3>Sugar</h3><p>Daily use sugar</p></div>
                <div class="card"><h3>Soap</h3><p>Gentle personal care</p></div>
                <div class="card"><h3>Detergent</h3><p>Household cleaning</p></div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


def products(request):
    items = [
        ("Rice", "Groceries", "80.00"),
        ("Sugar", "Groceries", "60.00"),
        ("Soap", "Personal Care", "45.00"),
        ("Detergent", "Household", "200.00"),
    ]
    rows = "".join(
        f"<li><strong>{name}</strong> - {category} - KES {price}</li>" for name, category, price in items
    )
    html = f"""
    <!doctype html>
    <html><head><title>Products</title>
    <style>body {{ font-family: Arial,sans-serif; padding: 24px; }} nav a {{ margin-right: 12px; }}</style>
    </head><body>
    <nav><a href="/">Home</a> | <a href="/products/">Products</a> | <a href="/cart/">Cart</a> | <a href="/checkout/">Checkout</a> | <a href="/admin-panel/">Admin</a></nav>
    <h1>Products</h1>
    <ul>{rows}</ul>
    </body></html>
    """
    return HttpResponse(html)


def cart(request):
    html = """
    <!doctype html><html><head><title>Cart</title></head><body>
    <nav><a href="/">Home</a> | <a href="/products/">Products</a> | <a href="/cart/">Cart</a> | <a href="/checkout/">Checkout</a> | <a href="/admin-panel/">Admin</a></nav>
    <h1>Your Cart</h1>
    <p>Your cart is currently empty.</p>
    </body></html>
    """
    return HttpResponse(html)


def checkout(request):
    html = """
    <!doctype html><html><head><title>Checkout</title></head><body>
    <nav><a href="/">Home</a> | <a href="/products/">Products</a> | <a href="/cart/">Cart</a> | <a href="/checkout/">Checkout</a> | <a href="/admin-panel/">Admin</a></nav>
    <h1>Checkout</h1>
    <p>Checkout page is ready.</p>
    </body></html>
    """
    return HttpResponse(html)


def admin_panel(request):
    html = """
    <!doctype html><html><head><title>Admin</title></head><body>
    <nav><a href="/">Home</a> | <a href="/products/">Products</a> | <a href="/cart/">Cart</a> | <a href="/checkout/">Checkout</a> | <a href="/admin-panel/">Admin</a></nav>
    <h1>Admin Panel</h1>
    <p>Admin dashboard is available.</p>
    </body></html>
    """
    return HttpResponse(html)
