# HW3 — Safe Deployment Strategies for ML model (Blue-Green)

Домашнее задание 3 (модуль CI/CD): реализован ML-сервис с эндпоинтами `/health` и `/predict`, контейнеризация через Docker и стратегия Blue-Green. Деплой автоматизирован через GitHub Actions (pipeline поднимает `kind`-кластер и выполняет blue/green rollout).

## Структура репозитория

- `Dockerfile` — сборка образа ML-сервиса
- `app/` — код сервиса и модель (`main.py`, `model.pkl`, `requirements.txt`)
- `docker-compose.blue.yml`, `docker-compose.green.yml` — локальный blue/green (две версии)
- `kubernetes/` — манифесты для деплоя в Kubernetes (используются в CI)
- `.github/workflows/deploy.yml` — CI/CD pipeline (build+push в GHCR + деплой в kind + blue/green переключение)

---

## API

### `/health`
Возвращает статус и версию модели (через env `MODEL_VERSION`).

Ожидаемый формат:
```json
{"status":"ok","version":"v1.0.0"}
