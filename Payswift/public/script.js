async function processPayment() {
    let amount = document.getElementById("amount").value;
    let fileInput = document.getElementById("iris_scan");
    
    if (!amount || amount <= 0) {
        document.getElementById("result").innerText = "❌ Invalid Amount!";
        return;
    }

    if (fileInput.files.length === 0) {
        document.getElementById("result").innerText = "⚠️ Please upload an iris scan!";
        return;
    }

    let formData = new FormData();
    formData.append("amount", amount);
    formData.append("iris_scan", fileInput.files[0]);

    try {
        let response = await fetch("http://localhost:5000/process-payment", {
            method: "POST",
            body: formData,
        });

        let data = await response.json();
        document.getElementById("result").innerText = data.message;
    } catch (error) {
        document.getElementById("result").innerText = "⚠️ Payment failed!";
    }
}


