# devops-project777 — Helm chart

Helm chart для деплоя Flask-приложения (health-check + метрики Prometheus) в Kubernetes.
Дополняет существующий pipeline проекта: Docker → GitHub Actions → Kubernetes (см. основной README репозитория).

## Структура

```
devops-project777/
├── Chart.yaml          # метаданные chart'а
├── values.yaml         # настраиваемые параметры (реплики, образ, ресурсы, порты)
├── README.md
└── templates/
    ├── _helpers.tpl     # генерация имён и лейблов
    ├── deployment.yaml  # Deployment с liveness/readiness пробами и метриками Prometheus
    ├── service.yaml     # Service (NodePort по умолчанию — совместимо с Minikube)
    ├── hpa.yaml          # опциональное автомасштабирование (выключено по умолчанию)
    └── NOTES.txt         # подсказка после установки
```

## Проверка перед установкой

```bash
# Синтаксическая проверка chart'а
helm lint ./devops-project777

# Посмотреть, во что раскроются шаблоны, без реальной установки
helm template my-release ./devops-project777

# Проверка с конкретными значениями (например, другой тег образа)
helm template my-release ./devops-project777 --set image.tag=v1.2.3
```

## Установка в Minikube

```bash
# Убедитесь, что образ доступен Minikube (для локальной сборки):
eval $(minikube docker-env)
docker build -t xwarhamx/devops-project777:latest .

# Установка релиза
helm install my-release ./devops-project777

# Обновление после изменения values.yaml или кода
helm upgrade my-release ./devops-project777

# Откат к предыдущей версии релиза
helm rollback my-release 1

# Удаление
helm uninstall my-release
```

## Настройка под своё окружение

Переопределить параметры можно через `--set` или собственный values-файл:

```bash
helm install my-release ./devops-project777 \
  --set replicaCount=2 \
  --set service.nodePort=30090
```

Либо создать `values-prod.yaml` с нужными значениями и запустить:

```bash
helm install my-release ./devops-project777 -f values-prod.yaml
```

## Метрики Prometheus

Deployment проставляет аннотации `prometheus.io/scrape`, `prometheus.io/port`, `prometheus.io/path` —
стандартный способ автообнаружения таргетов Prometheus без установки prometheus-operator.
Если в кластере используется Prometheus Operator — этот подход можно заменить на ServiceMonitor
(не включён в этот chart намеренно, чтобы chart оставался простым и переносимым).

## Автомасштабирование (опционально)

По умолчанию выключено. Включается через:

```bash
helm install my-release ./devops-project777 --set autoscaling.enabled=true
```

Требует наличия metrics-server в кластере (в Minikube: `minikube addons enable metrics-server`).
