# Домашнее задание: Микросервисы: принципы

## Задача 1: API Gateway

### Сравнительная таблица решений для API Gateway

| Возможность | NGINX | Kong | Traefik | Envoy | Apache APISIX | Spring Cloud Gateway | AWS API Gateway | API7 Enterprise |
|-------------|-------|------|---------|-------|---------------|----------------------|-----------------|-----------------|
| **Маршрутизация на основе конфигурации** | ✅ (файлы .conf) | ✅ (админ API / декларативная) | ✅ (автоматическая из Docker/K8s) | ✅ (файлы .yaml / xDS) | ✅ (YAML, Admin API, K8s CRD) | ✅ (Java DSL / YAML) | ✅ (AWS Console, CDK, OpenAPI) | ✅ (ADC, K8s CRD, REST Admin API) |
| **Проверка аутентификации** | ⚠️ (через lua-скрипты или модули) | ✅ (JWT, Key-Auth, OAuth2, LDAP) | ✅ (JWT, Forward Auth) | ⚠️ (через external auth filter) | ✅ (JWT, OIDC, OAuth2, mTLS, Key-Auth) | ✅ (Spring Security) | ✅ (IAM, Cognito, Lambda authorizers) | ✅ (JWT, OIDC, OAuth2, mTLS, FIPS, RBAC) |
| **Терминация HTTPS** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Лимитирование запросов** | ✅ (через модули) | ✅ (встроенный rate-limiting) | ✅ (middleware) | ✅ | ✅ (встроенное, расширенное) | ✅ | ✅ (встроенное throttling) | ✅ (встроенное, расширенное) |
| **Логирование и мониторинг** | ✅ (access_log, metrics module) | ✅ (Prometheus, StatsD) | ✅ (Prometheus, Tracing) | ✅ (отличные метрики) | ✅ (Prometheus, Grafana, OpenTelemetry, SkyWalking) | ✅ (Micrometer) | ✅ (CloudWatch, X-Ray) | ✅ (Prometheus, Grafana, OpenTelemetry, Datadog) |
| **Динамическое обновление конфига** | ❌ (требует reload) | ✅ (через API) | ✅ (автоматически) | ✅ (через xDS) | ✅ (etcd, реальное время, <300 мс) | ⚠️ (требует перезапуска) | ✅ (мгновенно через AWS API) | ✅ (etcd, реальное время) |
| **Простота настройки** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (fully managed) | ⭐⭐⭐⭐ |
| **Производительность** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (23k QPS/ядро) | ⭐⭐⭐ | ⭐⭐⭐ (есть лимиты, cold start) | ⭐⭐⭐⭐⭐ (23k QPS/ядро) |
| **Поддержка gRPC** | ⚠️ (ограниченная) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ (только REST, HTTP, WebSocket) | ✅ |
| **Service Discovery** | ⚠️ (через DNS или сторонние модули) | ✅ (Consul, K8s) | ✅ (встроенная) | ✅ (через xDS) | ✅ (K8s, Consul, Nacos, Eureka, DNS) | ✅ (Eureka, K8s) | ✅ (через AWS services) | ✅ (K8s, Consul, Nacos, Eureka, DNS) |
| **Cloud Lock-in** | Нет | Низкий | Нет | Нет | **Нет** (Apache 2.0) | Нет | **Очень высокий** | **Нет** (Apache 2.0) |
| **Стоимость** | Бесплатно | OSS бесплатно; Enterprise платно | Бесплатно (OSS) | Бесплатно | **Бесплатно** (OSS) | Бесплатно | **Платно за запросы** | **Платно** (но дешевле Kong) |
| **Поддержка протоколов** | HTTP, TCP, UDP | HTTP, gRPC, TCP, UDP, WebSocket | HTTP, gRPC, TCP, UDP, WebSocket | HTTP, gRPC, TCP, UDP | HTTP/1.1, HTTP/2, HTTP/3, gRPC, TCP, UDP, MQTT | HTTP, gRPC, WebSocket | REST, HTTP, WebSocket | HTTP/1.1, HTTP/2, HTTP/3, gRPC, TCP, UDP, MQTT |
| **API Management** | ❌ | ✅ (Enterprise) | ❌ (только через Hub) | ❌ | ❌ (только через сторонние интеграции) | ❌ | ✅ (полный цикл) | ✅ (полный цикл, портал) |
| **Языки для плагинов** | – | Lua, Go | Go | C++ | **Lua, Go, Java, Python, Wasm** | Java | – | **Lua, Go, Java, Python, Wasm** |
### Мой выбор: **Apache APISIX**

**Обоснование выбора:**
Apache APISIX — это современный стандарт для API Gateway в крупных микросервисных проектах. Он сочетает:
   - Производительность NGINX
   - Гибкость Kong
   - Отсутствие вендор-лока


---

## Задача 2: Брокер сообщений

### Сравнительная таблица брокеров сообщений

| Возможность | RabbitMQ | Apache Kafka | Redis Pub/Sub | NATS | ActiveMQ Artemis |
|-------------|----------|--------------|---------------|------|-------------------|
| **Кластеризация для надёжности** | ✅ (queues mirroring) | ✅ (копии партиций) | ⚠️ (Sentinel/Cluster, но не основное предназначение) | ✅ (Leaf nodes / Super cluster) | ✅ (master-slave) |
| **Хранение сообщений на диске** | ✅ | ✅ (по умолчанию) | ❌ (в основном в памяти) | ⚠️ (опционально через JetStream) | ✅ |
| **Высокая скорость работы** | ⭐⭐⭐⭐ (~50k msg/s) | ⭐⭐⭐⭐⭐ (~100k+ msg/s) | ⭐⭐⭐⭐⭐ (но в память) | ⭐⭐⭐⭐⭐ (очень низкая задержка) | ⭐⭐⭐ |
| **Поддержка форматов сообщений** | ✅ (JSON, XML, Protobuf, binary) | ✅ (любые) | ✅ (строки/байты) | ✅ (Protobuf, JSON, binary) | ✅ (JMS, любые) |
| **Разделение прав доступа** | ✅ (vhost + user permissions) | ✅ (ACL по темам) | ❌ (очень простые) | ✅ (Nkeys, JWT, ACL) | ✅ (JAAS, role-based) |
| **Простота эксплуатации** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Гарантии доставки** | at-least-once (confirm) | exactly-once (transactions) | at-most-once | at-least-once / exactly-once | at-least-once |
| **Поддержка очередей и тем** | оба | темы (log-based) | publish/subscribe | оба (через JetStream) | оба |
| **Документация и сообщество** | огромное | огромное | большое | растущее | среднее |

### Мой выбор: **Apache Kafka**

**Обоснование выбора:**

1. **Полное соответствие требованиям**:
   - ✅ Кластеризация с репликацией (даже при отказе 2 брокеров из 3 данные не теряются)
   - ✅ Все сообщения хранятся на диске с настраиваемым retention
   - ✅ Высокая скорость (миллионы сообщений в секунду на кластере)
   - ✅ Любые форматы (сериализуем в JSON/Avro/Protobuf)
   - ✅ ACL с детализацией read/write на топики
   - ⚠️ Простота эксплуатации — сложнее RabbitMQ, но управляется через инструменты (Kafka UI, Cruise Control)

2. **Почему не RabbitMQ** — при больших объёмах данных (логи заказов, события корзины, аналитика) RabbitMQ начинает деградировать из-за хранения очередей в памяти и на диске менее эффективно, чем Kafka.

3. **Почему не Redis** — не хранит данные на диске (основной недостаток), не подходит для надёжной доставки критичных событий (заказы, платежи).

4. **Почему не NATS** — хорошая альтернатива, но JetStream (постоянное хранение) появился недавно, экосистема инструментов меньше, чем у Kafka.

**Для интернет-магазина** Kafka идеально подходит для:
- Потока заказов (обеспечивает exactly-once доставку)
- Событий корзины и аналитики
- Логов и метрик (Kafka Connect → ClickHouse/Elasticsearch)
- CDC (Change Data Capture) между сервисами

**Недостаток Kafka** (сложность эксплуатации) решается наймом одного опытного SRE или использованием Managed Kafka (Confluent Cloud, Yandex Managed Kafka).

---

## Задача 3: API Gateway * (практическая)

### Решение: конфигурация NGINX + docker compose

#### Структура проекта:
<p align="center">
  <img src="S/S2.png" width="300"/>
  <br>
</p>
Проверка работоспособности
<p align="center">
  <img src="S/S1.png" width="900"/>
  <br>
</p>

