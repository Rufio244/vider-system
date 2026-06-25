from fastapi import FastAPI, UploadFile, File, BackgroundTasks
import os, uuid, json
from legal_connector import generate_qr_payment
from protocol_analyzer import analyze_rules

app = FastAPI(title="VIDER-Security-Analyzer & Integrator")

BASE = "storage/"
os.makedirs(f"{BASE}/docs", exist_ok=True)

@app.post("/analyze-system")
async def start_analysis(system_name: str, permission_proof: str, file: UploadFile = File(...)):
    # 1. รับไฟล์และบันทึก
    work_id = f"SYS-{str(uuid.uuid4())[:6]}"
    file_path = f"{BASE}/docs/{work_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. คำนวณความยากและราคา (Logic ของคุณ)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    points = content.count("@app.") * 5 + content.count("if ") * 1
    price = (points * 100) + 49 # ค่าบริการรายเดือน 49 บาท + ค่าวิเคราะห์
    
    # 3. สร้าง QR Code ผ่าน FlowAccount
    qr_url = generate_qr_payment(work_id, price)

    return {
        "work_id": work_id,
        "price_summary": f"{price} บาท",
        "payment_qr": qr_url,
        "status": "รอการชำระเงิน"
    }

@app.post("/webhook/payment-success")
async def webhook(data: dict, background_tasks: BackgroundTasks):
    # รับค่าจาก FlowAccount และเริ่มรันงาน
    if data.get("status") == "paid":
        background_tasks.add_task(run_full_pipeline, data.get("work_id"))
        return {"message": "ชำระเงินสำเร็จ ระบบกำลังวิเคราะห์"}
