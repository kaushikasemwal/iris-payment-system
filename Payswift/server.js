const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const multer = require("multer");
const { exec } = require("child_process");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public"));

// Multer setup for image uploads
const upload = multer({ dest: "uploads/" });

// Payment processing route with Iris Authentication
app.post("/process-payment", upload.single("iris_scan"), (req, res) => {
    const { amount } = req.body;
    const imagePath = req.file.path;

    if (!amount || amount <= 0) {
        return res.status(400).json({ message: "Invalid payment amount" });
    }

    // Call the Python script to authenticate the user
    exec(`python3 iris_auth.py ${imagePath}`, (error, stdout, stderr) => {
        if (error || stderr) {
            console.error("Error:", error || stderr);
            return res.status(500).json({ message: "Authentication error" });
        }

        const result = stdout.trim();
        if (result === "FAILED") {
            return res.status(401).json({ message: "Authentication failed!" });
        }

        // Authentication successful, process payment
        console.log(`User ${result} authorized payment of ₹${amount}`);
        return res.json({ message: `✅ Payment of ₹${amount} successful for ${result}!` });
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
