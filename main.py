import sqlite3
from plyer import notification
import json
import matplotlib.pyplot as plt
from kivymd.app import MDApp
from kivy.lang import Builder
from backup_manager import restore_data, save_data
# إعداد قاعدة البيانات SQLite
def create_db():
    conn = sqlite3.connect('debtbook.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        client_name TEXT,
                        amount REAL,
                        date TEXT)''')
    conn.commit()
    conn.close()

# دالة لإضافة معاملة جديدة
def add_transaction(client_name, amount, date):
    conn = sqlite3.connect('debtbook.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO transactions (client_name, amount, date)
                       VALUES (?, ?, ?)''', (client_name, amount, date))
    conn.commit()
    conn.close()

    # إشعار عند إضافة معاملة جديدة
    send_reminder(client_name, amount)

# دالة للإشعارات
def send_reminder(client_name, amount):
    notification.notify(
        title='Reminder',
        message=f'Client {client_name} has a pending debt of {amount} units.',
        timeout=10
    )

# دالة للتحقق من المدخلات
def validate_input(client_name, amount):
    if not client_name:
        return "Client name is required"
    try:
        amount = float(amount)
        if amount <= 0:
            return "Amount must be positive"
    except ValueError:
        return "Invalid amount"
    return None

# دالة لإظهار التقارير
def show_report():
    clients = ['Client1', 'Client2', 'Client3']
    amounts = [100, 200, 150]
    
    plt.bar(clients, amounts)
    plt.xlabel('Clients')
    plt.ylabel('Amount')
    plt.title('Debt Overview')
    plt.show()

# النسخ الاحتياطي
def backup_data():
    conn = sqlite3.connect('debtbook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    data = cursor.fetchall()
    conn.close()
    
    with open('backup.json', 'w') as f:
        json.dump(data, f)

# استعادة البيانات من النسخ الاحتياطي
def restore_data():
    with open('backup.json', 'r') as f:
        data = json.load(f)
    return data

# تطبيق KivyMD
class DebtBookApp(MDApp):

    def build(self):
        create_db()  # إنشاء قاعدة البيانات عند بدء التطبيق
        return Builder.load_file("main.kv")

    # إضافة معاملة من واجهة المستخدم
    def add_transaction_from_ui(self, client_name, amount, date):
        error = validate_input(client_name, amount)
        if error:
            # هنا يمكن إضافة نافذة منبثقة لعرض الأخطاء
            print(error)
        else:
            add_transaction(client_name, amount, date)
            print("Transaction added successfully")

    # عرض التقرير عند الضغط على الزر
    def show_report_from_ui(self):
        show_report()

    # إجراء النسخ الاحتياطي
    def backup_data_from_ui(self):
        backup_data()
        print("Backup completed successfully")

# تشغيل التطبيق
if __name__ == "__main__":
    DebtBookApp().run()
