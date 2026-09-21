# Security Policy

Cron Builder is an offline parser and preview tool. It does **not** execute crontab commands, invoke a shell, or contact remote services.

## Supported version

Security fixes target the latest release on `main`.

## Reporting

Please report security concerns through GitHub's available private security-reporting mechanism when enabled, rather than publishing exploitable details in a public issue. Do not include credentials or private production schedules.

## Security boundaries

- Input is treated as a cron expression, never as executable code.
- Preview count is capped at 100 and the search horizon is bounded.
- There are no network requests, telemetry hooks, API keys, or secret stores.
- The project does not claim that a schedule accepted here is supported by every scheduler; dialect differences must be checked against the target platform.

## العربية

الأداة محلية ولا تنفذ أوامر النظام ولا تتصل بالشبكة. تعامل مع الجداول القادمة من مصادر غير موثوقة كنصوص فقط، ولا تضع أسرارًا داخل تقارير الأعطال العامة. التحقق هنا لا يعني أن كل منصة Cron ستفسر التعبير بالطريقة نفسها.

Author: **Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2**
