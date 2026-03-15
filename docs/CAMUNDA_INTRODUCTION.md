# Camunda 简介

## 什么是 Camunda？

**Camunda** 是一个开源的工作流和决策自动化平台，专为开发人员设计，用于实现业务流程自动化。它基于 **BPMN 2.0**（Business Process Model and Notation）标准，提供了强大的流程引擎和决策引擎。

---

## 核心组件

### 1. 流程引擎 (Process Engine)

- 执行 BPMN 2.0 定义的流程
- 支持长时间运行的流程实例
- 提供流程实例的持久化、监控和管理

### 2. 决策引擎 (Decision Engine)

- 执行 DMN（Decision Model and Notation）定义的决策
- 支持决策表、决策需求图等
- 可独立使用或与流程引擎集成

### 3. Cockpit / Web 应用

- 流程监控和管理界面
- 查看流程实例、任务、变量等
- 诊断和修复问题

### 4. Tasklist

- 用户任务管理界面
- 支持任务分配、认领、完成

### 5. Admin

- 用户和权限管理
- 授权和审计

---

## 主要特性

| 特性 | 说明 |
|------|------|
| **BPMN 2.0 支持** | 完整支持 BPMN 2.0 标准 |
| **DMN 支持** | 决策表和决策逻辑 |
| **REST API** | 丰富的 RESTful API |
| **Java API** | 原生 Java 集成 |
| **Spring 集成** | 无缝 Spring Boot 集成 |
| **微服务架构** | 支持 Spring Cloud、Kubernetes |
| **可扩展性** | 水平扩展、集群部署 |
| **多租户支持** | SaaS 场景支持 |

---

## 版本对比

| 版本 | 说明 |
|------|------|
| **Camunda 7** | 成熟稳定版本，广泛使用 |
| **Camunda 8** | 云原生架构，基于 Zeebe 引擎 |

---

## 典型应用场景

1. **审批流程** - 请假、报销、合同审批等
2. **订单处理** - 电商订单、供应链管理
3. **客户入驻** - KYC、账户开通
4. **IT 服务管理** - 工单处理、变更管理
5. **金融交易** - 贷款审批、风控流程

---

## 技术架构

```
┌─────────────────────────────────────────┐
│           Camunda Platform              │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
│  │ Cockpit │ │Tasklist │ │   Admin   │  │
│  └─────────┘ └─────────┘ └───────────┘  │
├─────────────────────────────────────────┤
│  ┌─────────────────┐ ┌───────────────┐  │
│  │  Process Engine │ │Decision Engine│  │
│  └─────────────────┘ └───────────────┘  │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐│
│  │          Database (H2/MySQL/...)    ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

---

## 快速示例 (Spring Boot 集成)

```java
@SpringBootApplication
@EnableProcessApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

```xml
<!-- pom.xml 依赖 -->
<dependency>
    <groupId>org.camunda.bpm.springboot</groupId>
    <artifactId>camunda-bpm-spring-boot-starter-rest</artifactId>
    <version>7.18.0</version>
</dependency>
```

---

## 与其他 BPM 工具对比

| 工具 | 特点 |
|------|------|
| **Camunda** | 开发者友好、轻量级、Java 原生 |
| **Activiti** | 轻量级、社区活跃 |
| **Flowable** | Activiti 分支、功能丰富 |
| **jBPM** | Red Hat 支持、功能全面 |

---

## 学习资源

- 官方文档：https://docs.camunda.org/
- BPMN 2.0 规范：https://www.omg.org/spec/BPMN/2.0/
- GitHub：https://github.com/camunda/camunda-bpm-platform
