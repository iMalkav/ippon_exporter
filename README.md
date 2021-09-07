Change ipponexporter/conf.yml<br>
```
global:
   serverurl: https://urlipponagent:8888/ 
   log_level: INFO
   port: 9096
```

Prometheus job
```
- job_name: 'ups-state'
    honor_timestamps: true
    metrics_path: '/metrics'
    scrape_interval: 1m
    scrape_timeout: 30s
    scheme: 'http'
    static_configs:
    - targets: ['ipponexporter:9096']
      labels:
        env: 'prod'
        service: 'ups_exporter'
```

Docker compose example:
```
ipponexporter:
    image: imalkav/ipponexporter:latest
    container_name: ipponexporter
    hostname: ipponexporter
    volumes: 
      - ./ipponexporter/conf.yml:/ipponexporter/conf.yml
    ports:
      - "9096:9096"
    labels:
      org.label-schema.group: "monitoring"
```
