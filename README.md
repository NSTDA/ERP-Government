[![Doodba deployment](https://img.shields.io/badge/deployment-doodba-informational)](https://github.com/Tecnativa/doodba)
[![Last template update](https://img.shields.io/badge/last%20template%20update-v4.2.0-informational)](https://github.com/Tecnativa/doodba-copier-template/tree/v4.2.0)
[![Odoo](https://img.shields.io/badge/odoo-v15.0-a3478a)](https://github.com/odoo/odoo/tree/15.0)
[![AGPL-3.0 license](https://img.shields.io/badge/license-AGPL--3.0-success})](LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

# ERP Government Thailand

TODO: Objective

# วิธีติดตั้งระบบ

1. Download source code
    ```
    git clone https://github.com/NSTDA/ERP-Government.git
    ```
2. ไปที่ Folder ที่ Download
3. รัน Docker image โดยใช้คำสั่ง
    ```
    docker-compose -f egov-prod.yaml up -d
    ```
    หากต้องการ Build Image ใหม่ให้ใช้คำสั่ง
    ```
    docker-compose -f egov-prod-build.yaml up -d
    ```
4. เมื่อการติดตั้งเสร็จสมบูรณ์ สามารถทดสอบโดยการเข้าถึง URL http://localhost/ หรือ http://127.0.0.1/


# Credits

This project is maintained by:

- NSTDA <https://www.nstda.or.th>
- Ecosoft <https://www.ecosoft.co.th>

Also, special thanks to
[Technitiva](https://www.tecnativa.com/r/bb4) for doodba tools.
