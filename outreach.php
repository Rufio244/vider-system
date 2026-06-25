<?php
// ตัวอย่างระบบส่งอีเมลแบบกำหนดเป้าหมาย
function sendPromotionEmail($recipientEmail, $userName) {
    $apiKey = 'YOUR_EMAIL_API_KEY';
    $message = "สวัสดีคุณ $userName, เชิญทดลองใช้ Gemini Way/nano ระบบจัดการงานอัตโนมัติของคุณ! 
                ลองใช้ฟรีที่: https://your-domain.com";
    
    // ใช้ cURL ส่งผ่าน API
    $ch = curl_init('https://api.sendgrid.com/v3/mail/send');
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Authorization: Bearer ' . $apiKey, 'Content-Type: application/json']);
    // ... (ตั้งค่า Payload สำหรับส่งอีเมล)
    curl_exec($ch);
    curl_close($ch);
}

// ระบบวนลูปส่งรายชื่อ (ใช้ Cron Job ตั้งเวลาทำงาน)
$users = [['email' => 'user1@example.com', 'name' => 'User One'], /* ... */];
foreach ($users as $user) {
    sendPromotionEmail($user['email'], $user['name']);
    sleep(1); // หน่วงเวลาเพื่อป้องกันระบบ Spam detection
}
?>
