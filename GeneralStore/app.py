import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "general-store-secret-key"

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image TEXT,
            description TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
        """
    )

    existing_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if existing_count == 0:
        sample_products = [
            ("Rice", "Groceries", 80.00, 30, "https://images.unsplash.com/photo-1586201375761-83865001a7a9?auto=format&fit=crop&w=800&q=80", "Premium long-grain rice."),
            ("Sugar", "Groceries", 60.00, 40, "https://images.unsplash.com/photo-1519996521430-02b1d5f7f4bf?auto=format&fit=crop&w=800&q=80", "Fine white sugar for daily use."),
            ("Biscuits", "Snacks", 35.00, 50, "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=800&q=80", "Crunchy and fresh biscuits."),
            ("Cooking Oil", "Groceries", 120.00, 25, "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=800&q=80", "Healthy cooking oil for all meals."),
            ("Soap", "Personal Care", 45.00, 60, "https://images.unsplash.com/photo-1556228578-8c89e6adf883?auto=format&fit=crop&w=800&q=80", "Gentle cleansing soap."),
            ("Shampoo", "Personal Care", 150.00, 18, "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=800&q=80", "Nourishing hair care product."),
            ("Detergent", "Household", 200.00, 22, "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=800&q=80", "Effective detergent for household cleaning."),
            ("Toilet Paper", "Household", 90.00, 30, "https://images.unsplash.com/photo-1582719478182-8f6c7c7d934b?auto=format&fit=crop&w=800&q=80", "Soft and strong toilet paper."),
        ]
        conn.executemany(
            "INSERT INTO products (name, category, price, stock, image, description) VALUES (?, ?, ?, ?, ?, ?)",
            sample_products,
        )

    conn.commit()
    conn.close()


def get_cart():
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def add_to_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart


def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session["cart"] = cart


def get_cart_items_with_totals():
    cart = get_cart()
    if not cart:
        return [], 0

    product_ids = [int(item_id) for item_id in cart.keys()]
    placeholders = ",".join("?" for _ in product_ids)
    conn = get_db_connection()
    query = f"SELECT * FROM products WHERE id IN ({placeholders})"
    products = conn.execute(query, product_ids).fetchall()
    conn.close()

    items = []
    total = 0.0
    for product in products:
        quantity = cart.get(str(product["id"]), 0)
        if quantity <= 0:
            continue
        subtotal = product["price"] * quantity
        total += subtotal
        items.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "subtotal": subtotal,
            "image": product["image"],
        })
    return items, total


def place_order(customer_name, phone, address):
    cart = get_cart()
    if not cart:
        return None

    conn = get_db_connection()
    items, total = get_cart_items_with_totals()
    if not items:
        conn.close()
        return None

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_name, phone, address, total_amount) VALUES (?, ?, ?, ?)",
        (customer_name, phone, address, total),
    )
    order_id = cursor.lastrowid

    for item in items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item["id"], item["quantity"], item["price"]),
        )
        current_product = conn.execute("SELECT stock FROM products WHERE id = ?", (item["id"],)).fetchone()
        if current_product:
            new_stock = max(0, current_product["stock"] - item["quantity"])
            cursor.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, item["id"]))

    conn.commit()
    conn.close()
    session["cart"] = {}
    return order_id


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    search_query = request.args.get("q", "").strip()
    conn = get_db_connection()
    if search_query:
        products_list = conn.execute(
            "SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?) OR LOWER(category) LIKE LOWER(?) ORDER BY name",
            (f"%{search_query}%", f"%{search_query}%"),
        ).fetchall()
    else:
        products_list = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
    conn.close()
    return render_template("products.html", products=products_list, search_query=search_query)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_product_to_cart(product_id):
    add_to_cart(product_id)
    return redirect(url_for("products"))


@app.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_product_from_cart(product_id):
    remove_from_cart(product_id)
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    items, total = get_cart_items_with_totals()
    return render_template("cart.html", cart_items=items, total=total)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = get_cart_items_with_totals()

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not customer_name or not phone or not address or not items:
            return render_template("checkout.html", cart_items=items, total=total, error="Please complete all fields and add products to your cart.")

        order_id = place_order(customer_name, phone, address)
        if order_id is None:
            return render_template("checkout.html", cart_items=items, total=total, error="Your cart is empty.")

        return render_template("checkout.html", success=True, order_id=order_id, total=total)

    return render_template("checkout.html", cart_items=items, total=total)


@app.route("/admin")
def admin():
    conn = get_db_connection()
    orders = conn.execute(
        "SELECT * FROM orders ORDER BY created_at DESC"
    ).fetchall()
    order_items = conn.execute(
        "SELECT oi.order_id, p.name, oi.quantity, oi.price FROM order_items oi JOIN products p ON oi.product_id = p.id ORDER BY oi.order_id DESC"
    ).fetchall()
    conn.close()
    return render_template("admin.html", orders=orders, order_items=order_items)


init_db()


if __name__ == "__main__":
    app.run(debug=True)
