# 🧠 AI-Powered MikroTik Management Platform
# منصة الذكاء الصناعي لإدارة MikroTik RouterOS

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/ai-mikrotik-platform)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 📖 نظرة عامة | Overview

### العربية

منصة متكاملة مدعومة بالذكاء الصناعي لإدارة وتشغيل شبكات MikroTik RouterOS. تستخدم **GPT-5** و **Google Gemini** كعقل صناعي مركزي يحلل، يقرر، وينفذ العمليات بذكاء وكفاءة عالية.

#### ✨ المميزات الرئيسية:

- 🧠 **عقل صناعي مركزي** - يجمع بين GPT-5 و Google Gemini لاتخاذ قرارات تقنية دقيقة
- ⚡ **تنفيذ آلي** - تنفيذ أوامر RouterOS بشكل آمن مع إمكانية الـ Rollback
- 📊 **مراقبة لحظية** - مراقبة CPU, RAM, Bandwidth, Connections في الوقت الفعلي
- 🔧 **إصلاح ذاتي** - Auto-Heal System يكتشف ويصلح المشاكل تلقائياً
- 💬 **محادثة ذكية** - AI Chat Widget للتواصل مع العقل الصناعي بلغة طبيعية
- 🎨 **واجهة عصرية** - تصميم متحرك وجذاب باستخدام React + TailwindCSS + Framer Motion
- 🔒 **أمان متقدم** - Auto Snapshot قبل كل عملية حرجة
- 📚 **تعلم مستمر** - يتعلم من التجارب السابقة ويحسن أداءه

---

### English

A comprehensive AI-powered platform for managing and operating MikroTik RouterOS networks. Uses **GPT-5** and **Google Gemini** as a central AI brain to analyze, decide, and execute operations intelligently and efficiently.

#### ✨ Key Features:

- 🧠 **Central AI Brain** - Combines GPT-5 & Google Gemini for precise technical decisions
- ⚡ **Automated Execution** - Safely executes RouterOS commands with rollback capability
- 📊 **Real-time Monitoring** - Monitors CPU, RAM, Bandwidth, Connections live
- 🔧 **Self-Healing** - Auto-Heal System detects and fixes issues automatically
- 💬 **Smart Chat** - AI Chat Widget for natural language communication
- 🎨 **Modern UI** - Animated, attractive design with React + TailwindCSS + Framer Motion
- 🔒 **Advanced Security** - Auto Snapshot before critical operations
- 📚 **Continuous Learning** - Learns from past experiences and improves

---

## 🏗️ البنية المعمارية | Architecture

```
ai-mikrotik-platform/
├── backend/                 # Backend (FastAPI)
│   ├── app/
│   │   └── main.py         # التطبيق الرئيسي
│   ├── engines/
│   │   ├── executor/       # محرك التنفيذ
│   │   ├── monitoring/     # محرك المراقبة
│   │   ├── ai_gateway/     # بوابة الذكاء الصناعي
│   │   ├── knowledge_base/ # قاعدة المعرفة
│   │   └── auto_heal/      # نظام الإصلاح التلقائي
│   ├── models/             # نماذج قاعدة البيانات
│   ├── schemas/            # Pydantic schemas
│   ├── api/
│   │   ├── routes/         # API routes
│   │   └── websocket/      # WebSocket handlers
│   └── requirements.txt
├── frontend/               # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/     # المكونات
│   │   ├── pages/          # الصفحات
│   │   ├── hooks/          # React hooks
│   │   ├── services/       # API services
│   │   └── styles/         # التصاميم
│   └── package.json
├── ai-core/               # العقل الصناعي المركزي
│   ├── brain/             # Core AI Brain
│   ├── integrations/      # GPT-5 & Gemini
│   ├── learning/          # نظام التعلم
│   └── scripts_generator/ # مولد السكربتات
├── database/              # قاعدة البيانات
│   ├── migrations/
│   └── models/
├── config/                # التكوينات
│   └── .env.example
├── tests/                 # الاختبارات
└── docs/                  # التوثيق
```

---

## 🚀 التثبيت والتشغيل | Installation & Setup

### المتطلبات | Requirements

- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 14+
- **Redis** (اختياري)
- **MikroTik RouterOS** 6.x or 7.x
- **API Keys**: OpenAI & Google Gemini

### 1️⃣ استنساخ المشروع | Clone Repository

```bash
git clone https://github.com/yourusername/ai-mikrotik-platform.git
cd ai-mikrotik-platform
```

### 2️⃣ إعداد Backend

```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv

# تفعيل البيئة الافتراضية
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt

# نسخ ملف التكوين
cp ../config/.env.example .env

# تعديل ملف .env بمفاتيح API الخاصة بك
nano .env
```

#### ملف `.env` الأساسي:

```env
# AI Configuration
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key

# MikroTik Configuration
MIKROTIK_HOST=192.168.88.1
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your-password

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mikrotik_ai_db
```

### 3️⃣ إعداد قاعدة البيانات | Database Setup

```bash
# إنشاء قاعدة بيانات PostgreSQL
createdb mikrotik_ai_db

# تشغيل Migrations (إذا كانت متوفرة)
alembic upgrade head
```

### 4️⃣ تشغيل Backend

```bash
# تشغيل خادم FastAPI
python -m app.main

# أو باستخدام uvicorn مباشرة
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend سيعمل على: `http://localhost:8000`

### 5️⃣ إعداد Frontend

```bash
cd ../frontend

# تثبيت المكتبات
npm install

# تشغيل خادم التطوير
npm run dev
```

Frontend سيعمل على: `http://localhost:5173`

---

## 📚 الاستخدام | Usage

### 🎯 الوصول للمنصة | Access Platform

افتح المتصفح وتوجه إلى:
```
http://localhost:5173
```

### 💬 استخدام AI Chat

1. انقر على زر **💬 المحادثة** في أسفل يمين الشاشة
2. اكتب سؤالك أو طلبك بلغة طبيعية، مثل:
   - "ما حالة الراوتر الآن؟"
   - "الراوتر بطيء، كيف أحسن الأداء؟"
   - "أضف مستخدم جديد اسمه Ahmed"
   - "افحص الأمان وأخبرني بالمشاكل"

3. العقل الصناعي سيحلل طلبك ويقدم:
   - ✅ فهم النية
   - 📋 خطة عمل تفصيلية
   - 💻 سكربت MikroTik (إذا لزم)
   - 🔄 خطة Rollback
   - ⚠️ تقييم المخاطر

### 📊 مراقبة النظام | System Monitoring

- **Dashboard الرئيسي**: يعرض حالة النظام لحظياً
- **المقاييس**: CPU, Memory, Bandwidth, Connections
- **التنبيهات**: تنبيهات فورية عند وجود مشاكل
- **الرسوم البيانية**: تصور بياني للأداء

### ⚡ تنفيذ الأوامر | Execute Commands

يمكنك تنفيذ أوامر RouterOS مباشرة عبر:

```python
# مثال: تنفيذ سكربت
POST /api/execute
{
  "script": "/system identity set name=\"AI-Router\"",
  "dry_run": true,
  "description": "تحديث اسم الراوتر"
}
```

---

## 🔧 API Documentation

### الـ Endpoints الرئيسية | Main Endpoints

#### 1. Health Check
```http
GET /api/health
```
فحص صحة النظام

#### 2. System Status
```http
GET /api/status
```
الحصول على حالة كاملة للنظام

#### 3. Chat with AI
```http
POST /api/chat
Content-Type: application/json

{
  "message": "ما حالة الراوتر؟",
  "user_role": "technician"
}
```

#### 4. Execute Script
```http
POST /api/execute
Content-Type: application/json

{
  "script": "RouterOS script here",
  "dry_run": true,
  "description": "وصف العملية"
}
```

#### 5. Get Metrics
```http
GET /api/metrics
```

#### 6. Get Alerts
```http
GET /api/alerts
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws')

// الاستماع للتحديثات
ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Update:', data)
}

// إرسال رسالة
ws.send(JSON.stringify({
  type: 'chat',
  message: 'مرحباً'
}))
```

---

## 🧪 الاختبارات | Testing

### Backend Tests

```bash
cd backend

# تشغيل جميع الاختبارات
pytest

# مع تقرير التغطية
pytest --cov=app tests/

# اختبار محدد
pytest tests/test_ai_brain.py
```

### Frontend Tests

```bash
cd frontend

# تشغيل الاختبارات
npm test

# مع التغطية
npm run test:coverage
```

---

## 🔒 الأمان | Security

### ⚠️ نصائح أمنية مهمة | Security Best Practices

1. **🔑 مفاتيح API**: 
   - لا تشارك مفاتيح API الخاصة بك
   - استخدم متغيرات البيئة فقط

2. **🛡️ Auto Execute**:
   - `auto_execute = false` افتراضياً
   - فعّله فقط في بيئة آمنة وتحت إشرافك

3. **📸 Snapshots**:
   - تفعيل `auto_snapshot = true` دائماً
   - احتفظ بنسخ احتياطية منتظمة

4. **🔐 Authentication**:
   - استخدم كلمات مرور قوية
   - فعّل المصادقة الثنائية (2FA)

5. **🌐 Network**:
   - لا تعرّض API للإنترنت بدون حماية
   - استخدم HTTPS في الإنتاج
   - قيّد الوصول بـ Firewall

---

## 🛠️ استكشاف الأخطاء | Troubleshooting

### المشاكل الشائعة | Common Issues

#### 1. فشل الاتصال بالراوتر | Router Connection Failed

**الحل:**
```bash
# تحقق من:
- صحة IP و Port
- Username و Password
- SSH مفعل على الراوتر
- Firewall لا يحجب الاتصال
```

#### 2. خطأ في API Keys

**الحل:**
```bash
# تأكد من:
- صحة OPENAI_API_KEY و GEMINI_API_KEY
- الرصيد كافٍ في حساب OpenAI
- المفاتيح مفعّلة وغير منتهية
```

#### 3. WebSocket لا يتصل

**الحل:**
```bash
# تحقق من:
- Backend يعمل على المنفذ الصحيح
- CORS مكوّن بشكل صحيح
- Proxy settings في vite.config.ts
```

---

## 📈 الأداء | Performance

### توصيات للأداء الأمثل | Performance Recommendations

1. **قاعدة البيانات**:
   - استخدم PostgreSQL 14+
   - فعّل Connection Pooling
   - نفذ Indexes على الجداول الكبيرة

2. **Redis**:
   - استخدم Redis للتخزين المؤقت
   - قلل الضغط على قاعدة البيانات

3. **Monitoring**:
   - اضبط `check_interval` حسب حجم الشبكة
   - قلل `history_size` إذا كانت الذاكرة محدودة

4. **Frontend**:
   - استخدم Production build: `npm run build`
   - فعّل Code Splitting
   - استخدم CDN للأصول الثابتة

---

## 🤝 المساهمة | Contributing

نرحب بمساهماتكم! لتقديم مساهمة:

1. Fork المشروع
2. أنشئ فرعاً للميزة الجديدة: `git checkout -b feature/AmazingFeature`
3. Commit التغييرات: `git commit -m 'Add amazing feature'`
4. Push للفرع: `git push origin feature/AmazingFeature`
5. افتح Pull Request

---

## 📝 الترخيص | License

هذا المشروع مرخص تحت **MIT License** - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 👨‍💻 المطور | Developer

تم تطويره بواسطة **AI System Architect & Full Stack Developer**

- 🌐 Website: [your-website.com](https://your-website.com)
- 📧 Email: your-email@example.com
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 🐦 Twitter: [@yourusername](https://twitter.com/yourusername)

---

## 🙏 شكر وتقدير | Acknowledgments

- **OpenAI** - GPT-5 API
- **Google** - Gemini Pro API
- **MikroTik** - RouterOS
- **FastAPI** - Modern Python framework
- **React** - UI Library
- **TailwindCSS** - CSS Framework
- **Framer Motion** - Animation Library

---

## 📞 الدعم | Support

إذا واجهت أي مشاكل أو لديك أسئلة:

- 📖 [التوثيق الكامل](docs/)
- 🐛 [فتح Issue](https://github.com/yourusername/ai-mikrotik-platform/issues)
- 💬 [المناقشات](https://github.com/yourusername/ai-mikrotik-platform/discussions)

---

<div align="center">

**⭐ إذا أعجبك المشروع، لا تنسَ إضافة نجمة! ⭐**

Made with ❤️ and 🧠 AI

</div>
