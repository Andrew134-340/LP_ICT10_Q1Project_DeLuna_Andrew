from pyscript import document, display
import js
from pyodide.ffi import create_proxy

order_in_progress = False

def update_summary(event=None):
    """Updates the order summary and total when quantities change."""
    order_list = document.getElementById("orderList")
    total_display = document.getElementById("totalDisplay")
    qty_inputs = document.querySelectorAll(".quantity-input")

    order_list.innerHTML = ""
    total = 0

    # Loop through all quantity inputs
    for input_el in qty_inputs:
        qty_value = input_el.value.strip()
        if not qty_value:
            continue
        qty = int(qty_value)
        price = float(input_el.getAttribute("data-price"))
        name = input_el.getAttribute("data-name")

        if qty > 0:
            item_total = qty * price
            total += item_total
            li = document.createElement("li")
            li.innerText = f"{name} × {qty} — ₱{item_total:.2f}"
            order_list.appendChild(li)

    total_display.innerText = f"Total: ₱{total:.2f}"


def create_order(event):
    """Handles order submission."""
    global order_in_progress
    if order_in_progress:
        js.alert("Order already submitted! Please wait before placing another.")
        return

    name = document.getElementById("custName").value.strip()
    address = document.getElementById("custAddress").value.strip()
    number = document.getElementById("custNumber").value.strip()

    qty_inputs = document.querySelectorAll(".quantity-input")
    selected_items = []

    for input_el in qty_inputs:
        qty = int(input_el.value or 0)
        if qty > 0:
            selected_items.append({
                "name": input_el.getAttribute("data-name"),
                "qty": qty,
                "price": float(input_el.getAttribute("data-price"))
            })

    if not name or not address or not number or len(selected_items) == 0:
        js.alert("⚠️ Please fill all fields and order at least one item.")
        return

    # Prevent double submission
    order_in_progress = True
    order_btn = document.getElementById("orderBtn")
    order_btn.disabled = True
    order_btn.innerText = "Processing..."

    order_list = document.getElementById("orderList")
    total_display = document.getElementById("totalDisplay")

    # Show summary details
    order_list.innerHTML = f"""
        <li><strong>Order for:</strong> {name}</li>
        <li><strong>Address:</strong> {address}</li>
        <li><strong>Contact:</strong> {number}</li>
        <li><strong>Items:</strong></li>
    """

    total = 0
    for item in selected_items:
        item_total = item["qty"] * item["price"]
        total += item_total
        li = document.createElement("li")
        li.innerText = f"{item['name']} × {item['qty']} — ₱{item_total:.2f}"
        order_list.appendChild(li)

    total_display.innerText = f"Total: ₱{total:.2f}"
    js.alert("✅ Your order has been placed successfully!")

    # Re-enable order button after 5 seconds
    def reset_button():
        global order_in_progress
        order_in_progress = False
        order_btn.disabled = False
        order_btn.innerText = "Place Order"

    js.setTimeout(create_proxy(reset_button), 5000)


def setup_event_listeners():
    """Ensures listeners are properly attached after DOM loads."""
    for input_el in document.querySelectorAll(".quantity-input"):
        input_el.addEventListener("input", create_proxy(update_summary))

    document.getElementById("orderBtn").addEventListener("click", create_proxy(create_order))


# Run setup after small delay to ensure DOM is ready
js.setTimeout(create_proxy(setup_event_listeners), 500)
