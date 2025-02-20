paypal.Buttons({
    createOrder: function (data, actions) {
        return fetch("/api/orders", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: "10.00" }),
        })
        .then(res => res.json())
        .then(order => order.approval_url);
    },
    
    onApprove: function (data, actions) {
        return fetch("/api/orders/capture", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                payment_id: data.paymentID,
                payer_id: data.payerID,
            }),
        })
        .then(res => res.json())
        .then(details => alert("Transaction Successful!"));
    }
}).render("#paypal-button-container");
