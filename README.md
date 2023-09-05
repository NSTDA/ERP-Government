
[![Odoo](https://img.shields.io/badge/odoo-v15.0-a3478a)](https://github.com/odoo/odoo/tree/15.0)
[![AGPL-3.0 license](https://img.shields.io/badge/license-AGPL--3.0-success})](LICENSE)


# [ โครงการพัฒนาต้นแบบ ระบบ Open source ERP สำหรับหน่วยงานภาครัฐ   ](https://www.nstda.or.th/erp-government/)



&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ (สวทช.)  ได้ริเริ่มโครงการพัฒนาต้นแบบ ระบบ Open source ERP สำหรับหน่วยงานภาครัฐ   เพื่อเป็นระบบต้นแบบระบบสารสนเทศเพื่อการบริหารทรัพยากรขององค์กร (ERP) ที่พัฒนาโดยใช้ซอฟต์แวร์ Open source โดยใช้ชื่อเรียกว่า  [**ERP-Government (eGov)**](https://www.nstda.or.th/erp-government/)เหมาะสำหรับภาครัฐ/หน่วยงานที่มีความต้องการใช้ระบบ ERP ในการวางแผนบริหารจัดการทรัพยากรให้มีประสิทธิภาพ

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;การนำไปใช้งานสามารถติดตั้งแพ็คเกจ ERP-Government  พื้นฐาน สามารถนำไปกำหนดค่าตั้งต้นต่างๆ และปรับประยุกต์ใช้กับองค์กรของตนเองได้ ซึ่งครอบคลุมและรองรับกระบวนการทำงานอย่างประสิทธิภาพเชื่อมโยงส่วนการบริหารทรัพยากรองค์กรทั้งหมด และสอดคล้องกับกฎระเบียบที่เกี่ยวข้องขององค์กร รวมจำนวน 7 โมดูล (Modules)

1. Organization Structure การบริหารจัดการโครงสร้างองค์กร
2. Budgeting Module การบริหารงบประมาณ
3. Procurement Module การบริหารการจัดซื้อจัดจ้าง
4. Finance & Accounting Module การบริหารการเงินและบัญชี
5. Agreement and Contract Module การจัดการสัญญา
6. Assets Module การบริหารครุภัณฑ์
7. Inventory Module การบริหารวัสดุคงคลัง

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
**


# Credits

Copyright © National Science and Technology Development Agency. All rights reserved.

Licensed under [AGPL-3.0 license](LICENSE)

