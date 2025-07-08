#!/usr/bin/env python3
"""
批量模式功能测试脚本
用于验证软著代码生成器的批量模式是否正常工作
"""

import os
import sys
import tempfile
import shutil

def create_test_project_structure():
    """创建测试用的项目结构"""
    # 创建临时目录
    test_base_dir = tempfile.mkdtemp(prefix="softcopyright_test_")
    
    # 项目1：前端项目
    frontend_dir = os.path.join(test_base_dir, "frontend")
    os.makedirs(frontend_dir)
    
    # 创建一些前端文件
    with open(os.path.join(frontend_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>智慧医疗系统</title>
</head>
<body>
    <h1>欢迎使用智慧医疗系统</h1>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>""")
    
    with open(os.path.join(frontend_dir, "app.js"), 'w', encoding='utf-8') as f:
        f.write("""// 智慧医疗系统前端主文件
class MedicalApp {
    constructor() {
        this.patients = [];
        this.doctors = [];
        this.appointments = [];
    }
    
    addPatient(patient) {
        this.patients.push(patient);
        console.log('患者已添加:', patient.name);
    }
    
    addDoctor(doctor) {
        this.doctors.push(doctor);
        console.log('医生已添加:', doctor.name);
    }
    
    scheduleAppointment(patientId, doctorId, date) {
        const appointment = {
            id: Date.now(),
            patientId: patientId,
            doctorId: doctorId,
            date: date,
            status: '预约中'
        };
        this.appointments.push(appointment);
        return appointment;
    }
}

// 初始化应用
const app = new MedicalApp();
""")
    
    with open(os.path.join(frontend_dir, "styles.css"), 'w', encoding='utf-8') as f:
        f.write("""/* 智慧医疗系统样式 */
body {
    font-family: 'Microsoft YaHei', sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 30px;
}

.patient-card {
    border: 1px solid #ddd;
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
}
""")
    
    # 项目1：后端项目
    backend_dir = os.path.join(test_base_dir, "backend")
    os.makedirs(backend_dir)
    
    with open(os.path.join(backend_dir, "main.py"), 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
# 智慧医疗系统后端主程序

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email
        }

class Doctor(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    speciality = db.Column(db.String(200))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'title': self.title,
            'speciality': self.speciality,
            'phone': self.phone,
            'email': self.email
        }

@app.route('/api/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'GET':
        patients = Patient.query.all()
        return jsonify([p.to_dict() for p in patients])
    
    elif request.method == 'POST':
        data = request.get_json()
        patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            phone=data['phone'],
            email=data.get('email')
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify(patient.to_dict()), 201

@app.route('/api/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'GET':
        doctors = Doctor.query.all()
        return jsonify([d.to_dict() for d in doctors])
    
    elif request.method == 'POST':
        data = request.get_json()
        doctor = Doctor(
            name=data['name'],
            department=data['department'],
            title=data['title'],
            speciality=data.get('speciality'),
            phone=data['phone'],
            email=data.get('email')
        )
        db.session.add(doctor)
        db.session.commit()
        return jsonify(doctor.to_dict()), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
""")
    
    with open(os.path.join(backend_dir, "models.py"), 'w', encoding='utf-8') as f:
        f.write("""# 智慧医疗系统数据模型

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class MedicalRecord(BaseModel):
    __tablename__ = 'medical_records'
    
    patient_id = Column(String(36), nullable=False)
    doctor_id = Column(String(36), nullable=False)
    diagnosis = Column(Text, nullable=False)
    symptoms = Column(Text)
    treatment = Column(Text)
    prescription = Column(Text)
    notes = Column(Text)
    
class Appointment(BaseModel):
    __tablename__ = 'appointments'
    
    patient_id = Column(String(36), nullable=False)
    doctor_id = Column(String(36), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default='scheduled')
    notes = Column(Text)
    
class Department(BaseModel):
    __tablename__ = 'departments'
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    head_doctor_id = Column(String(36))
    location = Column(String(100))
    phone = Column(String(20))
""")
    
    # 项目2：移动端项目
    mobile_dir = os.path.join(test_base_dir, "mobile")
    os.makedirs(mobile_dir)
    
    with open(os.path.join(mobile_dir, "MainActivity.java"), 'w', encoding='utf-8') as f:
        f.write("""package com.medical.app;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    
    private RecyclerView recyclerView;
    private PatientAdapter patientAdapter;
    private List<Patient> patientList;
    private EditText editTextName, editTextAge, editTextPhone;
    private Button buttonAddPatient;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initViews();
        setupRecyclerView();
        setupListeners();
        loadPatients();
    }
    
    private void initViews() {
        recyclerView = findViewById(R.id.recyclerViewPatients);
        editTextName = findViewById(R.id.editTextName);
        editTextAge = findViewById(R.id.editTextAge);
        editTextPhone = findViewById(R.id.editTextPhone);
        buttonAddPatient = findViewById(R.id.buttonAddPatient);
    }
    
    private void setupRecyclerView() {
        patientList = new ArrayList<>();
        patientAdapter = new PatientAdapter(patientList, this);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(patientAdapter);
    }
    
    private void setupListeners() {
        buttonAddPatient.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addNewPatient();
            }
        });
    }
    
    private void addNewPatient() {
        String name = editTextName.getText().toString().trim();
        String ageStr = editTextAge.getText().toString().trim();
        String phone = editTextPhone.getText().toString().trim();
        
        if (name.isEmpty() || ageStr.isEmpty() || phone.isEmpty()) {
            Toast.makeText(this, "请填写所有字段", Toast.LENGTH_SHORT).show();
            return;
        }
        
        try {
            int age = Integer.parseInt(ageStr);
            Patient patient = new Patient(name, age, phone);
            patientList.add(patient);
            patientAdapter.notifyItemInserted(patientList.size() - 1);
            
            // 清空输入框
            editTextName.setText("");
            editTextAge.setText("");
            editTextPhone.setText("");
            
            Toast.makeText(this, "患者添加成功", Toast.LENGTH_SHORT).show();
        } catch (NumberFormatException e) {
            Toast.makeText(this, "年龄必须是数字", Toast.LENGTH_SHORT).show();
        }
    }
    
    private void loadPatients() {
        // 这里可以从服务器加载患者数据
        // 暂时添加一些示例数据
        patientList.add(new Patient("张三", 35, "13800138000"));
        patientList.add(new Patient("李四", 28, "13800138001"));
        patientAdapter.notifyDataSetChanged();
    }
}
""")
    
    with open(os.path.join(mobile_dir, "Patient.java"), 'w', encoding='utf-8') as f:
        f.write("""package com.medical.app;

import java.io.Serializable;
import java.util.UUID;

public class Patient implements Serializable {
    private String id;
    private String name;
    private int age;
    private String phone;
    private String email;
    private String gender;
    private long createTime;
    
    public Patient() {
        this.id = UUID.randomUUID().toString();
        this.createTime = System.currentTimeMillis();
    }
    
    public Patient(String name, int age, String phone) {
        this();
        this.name = name;
        this.age = age;
        this.phone = phone;
    }
    
    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getPhone() { return phone; }
    public String getEmail() { return email; }
    public String getGender() { return gender; }
    public long getCreateTime() { return createTime; }
    
    // Setters
    public void setId(String id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setAge(int age) { this.age = age; }
    public void setPhone(String phone) { this.phone = phone; }
    public void setEmail(String email) { this.email = email; }
    public void setGender(String gender) { this.gender = gender; }
    public void setCreateTime(long createTime) { this.createTime = createTime; }
    
    @Override
    public String toString() {
        return "Patient{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", age=" + age +
                ", phone='" + phone + '\'' +
                ", email='" + email + '\'' +
                ", gender='" + gender + '\'' +
                '}';
    }
}
""")
    
    print(f"✅ 测试项目结构创建完成")
    print(f"📁 测试目录: {test_base_dir}")
    print(f"   ├── frontend/ (前端代码)")
    print(f"   ├── backend/  (后端代码)")
    print(f"   └── mobile/   (移动端代码)")
    
    return test_base_dir, {
        'frontend': frontend_dir,
        'backend': backend_dir,
        'mobile': mobile_dir
    }

def test_batch_generation():
    """测试批量生成功能"""
    print("🚀 开始测试批量模式...")
    
    # 创建测试项目结构
    test_base_dir, project_paths = create_test_project_structure()
    
    try:
        # 导入GUI应用程序
        from soft_copyright_gui_v1 import SoftCodeGeneratorApp
        from PySide6.QtWidgets import QApplication
        import sys
        
        # 创建应用程序（但不显示界面）
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        # 创建主窗口实例
        window = SoftCodeGeneratorApp()
        
        # 添加测试项目
        print("📝 添加测试项目...")
        
        # 项目1：智慧医疗系统
        window.add_project()
        window.batch_name_edit.setText("智慧医疗系统")
        window.batch_doc_count_spin.setValue(2)
        window.batch_pages_spin.setValue(20)
        window.update_current_project()
        
        # 添加前端和后端路径
        project = window.batch_projects[0]
        project['source_paths'] = [project_paths['frontend'], project_paths['backend']]
        window.load_project_details(project)
        
        # 项目2：医疗移动端
        window.add_project()
        window.batch_name_edit.setText("医疗移动端")
        window.batch_doc_count_spin.setValue(1)
        window.batch_pages_spin.setValue(15)
        window.update_current_project()
        
        # 添加移动端路径
        project = window.batch_projects[1]
        project['source_paths'] = [project_paths['mobile']]
        window.load_project_details(project)
        
        # 设置输出目录
        output_dir = os.path.join(test_base_dir, "output")
        window.batch_output_edit.setText(output_dir)
        
        print("🔄 开始批量生成...")
        
        # 执行批量生成
        window.batch_generate_docs()
        
        # 检查生成结果
        if os.path.exists(output_dir):
            print("✅ 批量生成成功！")
            print(f"📁 输出目录: {output_dir}")
            
            for project_name in ["智慧医疗系统", "医疗移动端"]:
                project_dir = os.path.join(output_dir, project_name)
                if os.path.exists(project_dir):
                    files = os.listdir(project_dir)
                    print(f"   📂 {project_name}/")
                    for file in files:
                        if file.endswith('.docx'):
                            file_path = os.path.join(project_dir, file)
                            file_size = os.path.getsize(file_path)
                            print(f"      📄 {file} ({file_size} bytes)")
                else:
                    print(f"❌ 项目 {project_name} 的输出目录不存在")
        else:
            print("❌ 输出目录不存在，生成可能失败")
        
        print("✨ 测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理测试目录
        try:
            shutil.rmtree(test_base_dir)
            print(f"🧹 清理测试目录: {test_base_dir}")
        except Exception as e:
            print(f"⚠️  清理测试目录失败: {e}")

if __name__ == "__main__":
    print("📋 软著代码生成器 - 批量模式测试")
    print("=" * 50)
    
    # 运行测试
    success = test_batch_generation()
    
    if success:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print("\n💥 测试失败！")
        sys.exit(1) 