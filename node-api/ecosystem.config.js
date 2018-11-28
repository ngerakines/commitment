module.exports = {
  "apps": [{
    "name": "yolo",
    "script": "/data/web/cb.pe/apps/yolo/index.js",
    "cwd": "/data/web/cb.pe/apps/yolo",
    "watch": false,
    "env": {
      "NODE_ENV": "development"
    },
    "env_production": {
      "NODE_ENV": "production"
    }
  }]
}
