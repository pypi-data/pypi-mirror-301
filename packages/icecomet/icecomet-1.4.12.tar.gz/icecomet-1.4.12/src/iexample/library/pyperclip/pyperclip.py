import pyperclip

# คัดลอกข้อความไปยังคลิปบอร์ด
text_to_copy = "สวัสดีจากคลิปบอร์ด!"
pyperclip.copy(text_to_copy)
print("คัดลอกข้อความ:", text_to_copy)

# วางข้อความจากคลิปบอร์ด
copied_text = pyperclip.paste()
print("ข้อความที่วางจากคลิปบอร์ด:", copied_text)
