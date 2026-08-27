# 招聘信息管理系统

招聘部门内部使用的候选人流程、工作量、招聘漏斗和数据看板系统。

## 当前状态

项目处于 V1 开发阶段 0，已建立：

- Vue 3 + TypeScript 前端骨架
- FastAPI 后端骨架
- PostgreSQL 数据库配置
- Docker Compose 本地环境
- Nginx 统一入口
- 健康检查和基础测试

产品与技术文档：

- `产品文档/招聘信息管理系统-V1-产品需求文档.md`
- `技术设计/招聘信息管理系统-V1-技术设计.md`
- `技术设计/招聘信息管理系统-V1-开发计划.md`

## 本地启动

### 1. 准备环境变量

Linux/macOS：

```bash
cp .env.example .env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

开发环境可以先使用示例密码；生产环境必须更换数据库密码和 `APP_SECRET_KEY`。

### 2. 启动

```bash
docker compose up --build
```

访问：

- 系统入口：`http://localhost:8080`
- API 文档：`http://localhost:8080/api/docs`
- 存活检查：`http://localhost:8080/api/v1/health/live`
- 就绪检查：`http://localhost:8080/api/v1/health/ready`

### 3. 停止

```bash
docker compose down
```

删除本地数据库卷会清空开发数据，仅在明确需要重建本地环境时执行：

```bash
docker compose down -v
```

## 目录

```text
backend/       FastAPI 后端
frontend/      Vue 3 前端
deploy/        Nginx 等部署配置
storage/       本地附件和运行数据
产品文档/      产品需求与业务规则
技术设计/      技术架构与开发计划
数据源/        原始 Excel，只读保留
原型/          交互原型
```

## 安全约定

- 不将 `.env`、密码、令牌或真实生产凭据提交到仓库。
- 不修改或覆盖 `数据源/` 中的原始 Excel。
- 生产环境通过内部域名和 HTTPS 访问。
- 附件必须通过后端权限校验下载，不直接暴露服务器路径。

