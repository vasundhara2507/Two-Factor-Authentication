// Import necessary modules
import express from 'express';
import sgMail from '@sendgrid/mail';
import cors from 'cors'; // Add CORS middleware

// Create an Express app
const app = express();
const port = 3000; // Or any port you prefer

// Set SendGrid API key
sgMail.setApiKey('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');

// Generate a random OTP
function generateOTP() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

// Object to store OTPs (in-memory storage, replace with database in production)
const otpStorage = {};

// Middleware to enable CORS
app.use(cors());
app.use(express.json()); // Parse JSON bodies

// Endpoint to generate and send OTP
app.post('/send-otp-email', async (req, res) => {
    const { email } = req.body;
    const otp = generateOTP();

    // Store OTP in memory
    otpStorage[email] = otp;

    try {
        await sgMail.send({
            from: 'poonam81175@gmail.com',
            to: email,
            subject: 'Your OTP',
            text: `Your OTP is: ${otp}`
        });
        console.log('OTP email sent successfully');
        res.json({ success: true });
    } catch (error) {
        console.error('Error sending OTP email:', error);
        res.status(500).json({ success: false, error: 'Failed to send OTP email' });
    }
});

// Endpoint to verify OTP
app.post('/verify-otp', (req, res) => {
    const { email, enteredOTP } = req.body;
    const storedOTP = otpStorage[email]; // Retrieve stored OTP from memory

    if (!storedOTP) {
        return res.json({ verified: false, error: 'OTP not found' });
    }

    // Compare enteredOTP with storedOTP
    const verified = enteredOTP === storedOTP;
    res.json({ verified });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
});
