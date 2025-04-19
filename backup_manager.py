# استيراد الدوال
from backup_manager import restore_data, save_data

# تحميل البيانات عند بدء التطبيق
data = restore_data()

# إضافة عميل جديد
new_client = {
    "name": "أحمد",
    "transactions": [
        {"type": "سحب", "amount": 150, "date": "2025-04-20"},
        {"type": "دفع", "amount": 50, "date": "2025-04-21"}
    ]
}
data["clients"].append(new_client)

# حفظ البيانات بعد التعديل
save_data(data)
