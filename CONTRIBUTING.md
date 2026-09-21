# Contributing / المساهمة

Thanks for improving Cron Builder. Keep changes focused on standard five-field cron semantics unless a new dialect is explicitly isolated behind an opt-in interface.

1. Use Python 3.10+.
2. Install with `python -m pip install -e .`.
3. Add or update tests for behavioral changes.
4. Run `python -m unittest discover -s tests -v`.
5. Keep runtime dependencies at zero unless there is a strong documented reason.
6. Update both English and Arabic README sections when user-facing behavior changes.
7. Never commit credentials, machine-specific data, generated build output, or user schedules containing secrets.

Bug reports should include the expression, expected behavior, actual behavior, Python version, and operating system. Do not include confidential command lines or production secrets.

## العربية

نرحب بالمساهمات المركزة والقابلة للاختبار. أضف اختبارًا لأي تغيير سلوكي، وشغّل مجموعة الاختبارات قبل الإرسال، وحدّث قسمي README الإنجليزي والعربي عند تغيير سلوك المستخدم. لا ترفع أسرارًا أو بيانات جهاز أو مخرجات بناء مولدة أو جداول إنتاج تحتوي معلومات حساسة.

Maintainer/Author: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2**
