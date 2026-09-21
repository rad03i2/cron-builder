# Cron Builder

A small, dependency-free Python toolkit for building, validating, explaining, and previewing **standard five-field cron expressions**. It is useful when writing scheduler configuration, CI jobs, server tasks, or deployment automation and you want a local sanity check before saving a schedule.

> No network calls, accounts, telemetry, API keys, or background services.

## Features

- Parse and validate five-field cron (`minute hour day-of-month month day-of-week`).
- Supports `*`, lists, ranges, and steps, including combinations such as `1-10/2`.
- Accepts `JAN`–`DEC` and `SUN`–`SAT` names, case-insensitively.
- Preview up to 100 upcoming run times from an explicit or current local starting time.
- Implements traditional Vixie-cron day-of-month/day-of-week OR behavior when both are restricted.
- Build expressions from individual fields.
- Human-readable explanations for common schedules plus deterministic field summaries for arbitrary schedules.
- JSON preview output for scripts and developer tooling.
- Reusable Python API as well as CLI.
- Standard-library runtime: no third-party runtime dependency.

## Requirements

Python 3.10 or newer.

## Installation

From a clone:

```bash
git clone https://github.com/rad03i2/cron-builder.git
cd cron-builder
python -m pip install -e .
```

## Usage

```bash
cron-builder validate "*/15 9-17 * * MON-FRI"
cron-builder explain "0 0 * * *"
cron-builder build --minute 30 --hour 8 --weekday MON-FRI
cron-builder next "0 9 * * MON-FRI" --count 5
cron-builder next "*/30 * * * *" --from 2026-09-21T10:07 --count 3 --json
cron-builder --version
```

Python API:

```python
from datetime import datetime
from cron_builder import CronExpression

schedule = CronExpression.parse("*/15 9-17 * * MON-FRI")
print(schedule.explain())
print(schedule.next_runs(datetime.now(), count=5))
```

## Preview guidance

A useful repository screenshot is a terminal showing `validate`, `explain`, and `next --json` side by side. No screenshot is committed because terminal rendering varies by platform.

## Configuration

There is no configuration file and no environment variable. `next` uses the machine's local wall-clock time unless `--from` is supplied. For reproducible automation, pass an ISO-8601 `--from` value explicitly.

## Project structure

```text
src/cron_builder/core.py   parser, validation, matching, preview, explanations
src/cron_builder/cli.py    command-line interface
src/cron_builder/__init__.py public API
tests/test_core.py         automated unit tests
.github/workflows/ci.yml   cross-platform CI
```

## Testing

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

CI runs the suite on Python 3.10, 3.12, and 3.13 on Ubuntu, Windows, and macOS.

## Semantics and limitations

Cron Builder targets classic **five-field** cron only. It does not support seconds, years, Quartz-only syntax (`?`, `L`, `W`, `#`), systemd calendar syntax, Jenkins hashed `H`, or crontab macros such as `@reboot`. Previewing is minute-resolution and uses naive local datetimes; DST/time-zone policy belongs to the scheduler that ultimately executes the expression. The preview search is deliberately bounded to ten years. Human explanation is concise rather than a natural-language grammar for every possible expression.

Different cron implementations can have edge-case differences. Always confirm production schedules against the documentation for the actual scheduler you deploy to.

## Security & privacy

All processing is local and deterministic. Cron Builder does not execute commands from a crontab and does not access the network. Treat schedule strings from untrusted sources as data; this project only parses them. See [SECURITY.md](SECURITY.md).

## Optional roadmap

Possible future additions include explicit IANA timezone previews, crontab-file linting, and opt-in dialect adapters. These are not implemented today.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, tested, dependency-light, and explicit about cron dialect semantics.

## License

MIT — see [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

## نظرة عامة

**Cron Builder** أداة Python محلية وخفيفة لبناء تعبيرات Cron القياسية ذات الحقول الخمسة والتحقق منها وشرحها ومعاينة مواعيد التشغيل القادمة. تفيد عند تجهيز مهام الخوادم وCI والأتمتة قبل حفظ الجدول في النظام الفعلي.

لا تستخدم الأداة الشبكة أو التتبع، ولا تحتاج حسابًا أو مفتاح API أو خدمة تعمل في الخلفية.

## لماذا المشروع؟

كتابة Cron يدويًا سهلة، لكن خطأ صغير في مجال رقم أو ترتيب حقل قد يغيّر موعد المهمة بالكامل. يوفر المشروع طبقة تحقق ومعاينة محلية يمكن استخدامها من الطرفية أو من كود Python.

## المزايا

- التحقق من `الدقيقة الساعة يوم-الشهر الشهر يوم-الأسبوع`.
- دعم النجمة والقوائم والمجالات والخطوات.
- دعم أسماء الأشهر `JAN` إلى `DEC` وأيام الأسبوع `SUN` إلى `SAT`.
- معاينة حتى 100 موعد قادم.
- تطبيق سلوك Vixie cron التقليدي عند تقييد يوم الشهر ويوم الأسبوع معًا.
- إنشاء التعبير من الحقول منفردة.
- شرح الجداول الشائعة وتلخيص واضح لبقية الحقول.
- إخراج JSON مناسب للأتمتة.
- API برمجي وCLI.
- لا توجد تبعيات تشغيل خارج مكتبة Python القياسية.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/cron-builder.git
cd cron-builder
python -m pip install -e .
```

## الاستخدام

```bash
cron-builder validate "*/15 9-17 * * MON-FRI"
cron-builder explain "0 0 * * *"
cron-builder build --minute 30 --hour 8 --weekday MON-FRI
cron-builder next "0 9 * * MON-FRI" --count 5
```

ولنتيجة قابلة للمعالجة برمجيًا:

```bash
cron-builder next "*/30 * * * *" --from 2026-09-21T10:07 --count 3 --json
```

## الإعداد والمعاينة

لا يوجد ملف إعدادات ولا متغيرات بيئة. يستخدم أمر `next` وقت الجهاز المحلي إن لم تمرر `--from`. للحصول على نتائج قابلة للتكرار استخدم وقت بداية ISO-8601 صريحًا. ولصورة عرض للمشروع، يمكن التقاط الطرفية أثناء تشغيل أوامر `validate` و`explain` و`next --json`.

## بنية المشروع والاختبارات

المحرك في `src/cron_builder/core.py`، والواجهة الطرفية في `src/cron_builder/cli.py`، والاختبارات في `tests/test_core.py`.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## القيود

يدعم المشروع Cron القياسي بخمسة حقول فقط. لا يدعم الثواني أو السنوات أو صيغة Quartz الخاصة أو systemd أو Jenkins `H` أو `@reboot`. المعاينة بدقة دقيقة وتستخدم وقتًا محليًا بلا منطقة زمنية مرفقة؛ سلوك DST والمنطقة الزمنية النهائي تحدده المنصة التي ستنفذ الجدول. البحث عن الموعد القادم محدود بعشر سنوات للحماية من البحث غير المنتهي.

## الأمان والخصوصية

كل المعالجة محلية. الأداة لا تنفذ أوامر crontab ولا تتصل بالإنترنت؛ هي تتعامل مع تعبير الجدولة كنص فقط. راجع [SECURITY.md](SECURITY.md).

## التطوير المستقبلي الاختياري

يمكن لاحقًا إضافة معاينة بمناطق IANA الزمنية، وفحص ملفات crontab كاملة، ومحولات اختيارية للهجات Cron الأخرى. هذه الميزات غير موجودة حاليًا ولا يدعي المشروع دعمها.

## المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص برخصة MIT؛ راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
