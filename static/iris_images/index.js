async function authenticateIris(imagePath) {
    const response = await fetch("http://127.0.0.1:5001/authenticate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_path: imagePath }),
    });

    const data = await response.json();
    if (data.authenticated) {
        alert("Authenticated! Proceeding to payment...");
        processPayment(data.customer_id, 50);
    } else {
        alert("Authentication Failed");
    }
}

async function processPayment(customerId, amount) {
    const response = await fetch("http://127.0.0.1:5001/pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ customer_id: customerId, amount: amount }),
    });

    const data = await response.json();
    alert(data.message);
}
