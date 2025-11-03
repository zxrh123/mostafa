# ⚡ دليل البدء السريع | Quick Start Guide

## 🚀 تشغيل المنصة في 5 دقائق

### 1️⃣ التحضير السريع

```bash
# 1. استنساخ المشروع
git clone https://github.com/yourusername/ai-mikrotik-platform.git
cd ai-mikrotik-platform

# 2. نسخ ملف التكوين
cp config/.env.example backend/.env

# 3. تعديل المفاتيح الضرورية
nano backend/.env
```

#### المفاتيح الأساسية في `.env`:

```env
# مفاتيح الذكاء الصناعي (إلزامية)
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here

# معلومات الراوتر (إلزامية)
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your-password

# قاعدة البيانات (اختيارية - يمكن استخدام SQLite مؤقتاً)
DATABASE_URL=sqlite:///./mikrotik_ai.db
```

---

### 2️⃣ تشغيل Backend

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt

# تشغيل الخادم
python -m app.main
```

✅ Backend يعمل الآن على: `http://localhost:8000`

---

### 3️⃣ تشغيل Frontend

افتح **terminal جديد**:

```bash
cd frontend

# تثبيت المكتبات
npm install

# تشغيل خادم التطوير
npm run dev
```

✅ Frontend يعمل الآن على: `http://localhost:5173`

---

### 4️⃣ الوصول للمنصة

افتح المتصفح وتوجه إلى:

```
http://localhost:5173
```

---

## 💬 اختبار سريع

### 1. افتح AI Chat Widget
انقر على الزر **💬** في أسفل يمين الشاشة

### 2. جرب هذه الأوامر:

```
"ما حالة الراوتر الآن؟"

"افحص استخدام CPU والذاكرة"

"أريد تحسين الأداء"

"اعرض قائمة المستخدمين المتصلين"
```

---

## 🔧 حل المشاكل السريع

### مشكلة: فشل الاتصال بالراوتر

```bash
# تحقق من:
1. IP صحيح (192.168.88.1)
2. SSH مفعّل على الراوتر
3. اسم المستخدم وكلمة المرور صحيحة
4. لا يوجد Firewall يحجب المنفذ 22
```

### مشكلة: خطأ في API Keys

```bash
# تأكد من:
1. المفاتيح صحيحة في ملف .env
2. الرصيد كافٍ في حساب OpenAI
3. المفاتيح غير منتهية
```

### مشكلة: Backend لا يعمل

```bash
# جرب:
cd backend
pip install -r requirements.txt --upgrade
python -m app.main
```

### مشكلة: Frontend لا يعمل

```bash
# جرب:
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📚 الخطوات التالية

بعد التشغيل الناجح:

1. ✅ استكشف **Dashboard** الرئيسي
2. ✅ راقب **المقاييس اللحظية**
3. ✅ جرب **AI Chat** المتقدم
4. ✅ راجع **التنبيهات النشطة**
5. ✅ اقرأ [الوثائق الكاملة](README.md)

---

## 🎯 نصائح للاستخدام الأمثل

### للمبتدئين:
- ابدأ بأوامر بسيطة مثل "ما حالة الراوتر؟"
- راقب Dashboard لفهم حالة الشبكة
- لا تفعّل `auto_execute` حتى تتعرف على النظام

### للمحترفين:
- استخدم سكربتات RouterOS مباشرة
- فعّل Auto-Heal للإصلاح التلقائي
- راجع logs للتحليل المتقدم

---

## 🆘 الدعم السريع

- 📖 [التوثيق الكامل](README.md)
- 🐛 [الإبلاغ عن مشكلة](https://github.com/yourusername/ai-mikrotik-platform/issues)
- 💬 [المناقشات](https://github.com/yourusername/ai-mikrotik-platform/discussions)

---

<div align="center">

**🎉 مبروك! منصتك جاهزة الآن! 🎉**

استمتع بإدارة شبكة MikroTik بذكاء اصطناعي متقدم 🧠

</div>
