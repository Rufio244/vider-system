def generate_qr_payment(invoice_id, amount):
    # ในส่วนนี้คุณธันวานำ API Key จาก FlowAccount มาใส่ที่นี่
    # นี่คือจำลองการสร้าง URL ของ QR Code
    return f"https://api.flowaccount.com/qr?id={invoice_id}&amount={amount}"
