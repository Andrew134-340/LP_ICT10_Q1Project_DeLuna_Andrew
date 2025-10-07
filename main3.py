from pyscript import document
import js
from pyodide.ffi import create_proxy

def send_message(event):
    event.preventDefault()  # stop page reload

    name = document.getElementById("contactName").value.strip()
    email = document.getElementById("contactEmail").value.strip()
    message = document.getElementById("contactMessage").value.strip()
    output = document.getElementById("messageOutput")

    if not name or not email or not message:
        js.alert("⚠️ Please fill in all fields before submitting.")
        return

    # Display a success message
    output.innerText = f"✅ Thank you, {name}! Your message has been sent successfully."
    output.style.display = "block"

    # Reset fields
    document.getElementById("contactForm").reset()

    # Hide message after a few seconds
    def hide_message():
        output.style.display = "none"
    js.setTimeout(create_proxy(hide_message), 4000)

# Attach listener
document.getElementById("submitBtn").addEventListener("click", create_proxy(send_message))
