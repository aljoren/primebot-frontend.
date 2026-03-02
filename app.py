<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AJ-ROELFSE PrimeBot</title>
  <!-- PayPal SDK -->
  <script src="https://www.paypal.com/sdk/js?client-id=YOUR_PAYPAL_CLIENT_ID&currency=USD"></script>
  <!-- Solana Web3.js -->
  <script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.js"></script>

  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      background-color: #f3f3f3;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      margin: 50px auto;
      background: #fff;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    h1 { color: #1a1a1a; }
    #paypal-button-container, #solana-pay-container { margin-top: 20px; }
    #solana-pay-button {
      padding: 15px 25px;
      font-size: 16px;
      background-color: #00FFA3;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>AJ-ROELFSE PrimeBot</h1>
    <p>Pay to unlock access to your AI assistant instantly!</p>

    <!-- PayPal Button -->
    <div id="paypal-button-container"></div>

    <!-- Solana Payment -->
    <div id="solana-pay-container">
      <h3>Or pay with Solana</h3>
      <button id="solana-pay-button">Pay with Solana</button>
    </div>
  </div>

  <script>
    // === PAYPAL BUTTON ===
    paypal.Buttons({
      style: { layout: 'vertical', color: 'blue', shape: 'rect', label: 'pay' },
      createOrder: function(data, actions) {
        return actions.order.create({
          purchase_units: [{
            amount: { value: '5.00' },  // Payment amount in USD
            custom_id: 'primebot_user'   // Optional: dynamic user ID
          }]
        });
      },
      onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
          alert('Thank you ' + details.payer.name.given_name + '! Your PrimeBot access is unlocked.');
          // Notify backend to unlock user
          fetch('https://primebot-backend.onrender.com/paypal/webhook', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(details)
          });
        });
      },
      onError: function(err) {
        console.error(err);
        alert('PayPal payment failed. Please try again.');
      }
    }).render('#paypal-button-container');

    // === SOLANA BUTTON ===
    document.getElementById('solana-pay-button').onclick = async () => {
      if (!window.solana) {
        alert('Please install a Solana wallet like Phantom.');
        return;
      }
      try {
        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
        await window.solana.connect();
        const toPublicKey = new solanaWeb3.PublicKey('AyE3U2wkUm7GApn76bHYT9PN72TvFDvDviLCZV9hVTD3');
        const amount = 0.01 * 1e9; // 0.01 SOL in lamports
        const transaction = new solanaWeb3.Transaction().add(
          solanaWeb3.SystemProgram.transfer({
            fromPubkey: window.solana.publicKey,
            toPubkey: toPublicKey,
            lamports: amount
          })
        );
        const { signature } = await window.solana.signAndSendTransaction(transaction);
        await connection.confirmTransaction(signature);
        alert('Solana payment successful! Transaction signature: ' + signature);
        // Notify backend
        fetch('https://primebot-backend.onrender.com/solana/verify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tx_signature: signature, user_id: 'sol_user' })
        });
      } catch (err) {
        console.error(err);
        alert('Solana payment failed. Make sure you have a connected wallet.');
      }
    };
  </script>
</body>
</html>
