<script setup>
import { ref } from 'vue';

// Khai báo biến để đóng mở Form (Gửi sự kiện lên cho cha App.vue)
const emit = defineEmits(['dong-form', 'luu-du-lieu']);

// Dữ liệu mẫu của Form
const form = ref({
      tenVung: '',
      loaiCay: '',
      trangThai: 'canh_tac',
      nhatKy: [] // Danh sách nhật ký
});

// Dữ liệu cho dòng nhật ký đang nhập
const logMoi = ref({
      ngay: '',
      hanhDong: 'bon_phan',
      chiTiet: ''
});

// Hàm thêm dòng nhật ký vào danh sách tạm
const themNhatKy = () => {
      if (logMoi.value.ngay && logMoi.value.chiTiet) {
            // Copy dữ liệu logMoi vào danh sách
            form.value.nhatKy.push({ ...logMoi.value });

            // Reset ô nhập
            logMoi.value.chiTiet = '';
      } else {
            alert("Vui lòng nhập ngày và chi tiết công việc!");
      }
};

// Hàm xóa dòng nhật ký (nếu nhập sai)
const xoaNhatKy = (index) => {
      form.value.nhatKy.splice(index, 1);
};

// Hàm lưu (Gửi dữ liệu ra ngoài)
const xuLyLuu = () => {
      if (!form.value.tenVung) return alert("Chưa nhập tên vùng!");
      emit('luu-du-lieu', form.value);
};
</script>

<template>
      <div class="modal-overlay">
            <div class="modal-content">
                  <div class="modal-header">
                        <h3>🌾 Nhật ký Canh tác & Vùng trồng</h3>
                        <button class="btn-close" @click="$emit('dong-form')">✖</button>
                  </div>

                  <div class="modal-body">
                        <div class="section-title">1. Thông tin Vùng trồng</div>
                        <div class="form-grid">
                              <div class="form-group">
                                    <label>Tên Vùng / Mã số</label>
                                    <input v-model="form.tenVung" type="text" placeholder="VD: Vùng Xoài 01">
                              </div>
                              <div class="form-group">
                                    <label>Loại cây</label>
                                    <select v-model="form.loaiCay">
                                          <option value="xoai">Xoài</option>
                                          <option value="thanh_long">Thanh Long</option>
                                          <option value="lua">Lúa</option>
                                    </select>
                              </div>
                              <div class="form-group">
                                    <label>Trạng thái</label>
                                    <select v-model="form.trangThai">
                                          <option value="canh_tac">Đang canh tác (Xanh)</option>
                                          <option value="thu_hoach">Đang thu hoạch (Vàng)</option>
                                          <option value="sau_benh">Sâu bệnh (Đỏ)</option>
                                    </select>
                              </div>
                        </div>

                        <div class="section-title">2. Lịch sử Canh tác (Ghi chép)</div>

                        <div class="log-input-box">
                              <div class="log-row">
                                    <input v-model="logMoi.ngay" type="date">
                                    <select v-model="logMoi.hanhDong">
                                          <option value="bon_phan">Bón phân</option>
                                          <option value="phun_thuoc">Phun thuốc</option>
                                          <option value="gieo_giong">Gieo giống</option>
                                          <option value="thu_hoach">Thu hoạch</option>
                                    </select>
                                    <input v-model="logMoi.chiTiet" type="text"
                                          placeholder="Tên thuốc/phân, liều lượng...">
                                    <button @click="themNhatKy" class="btn-add">+</button>
                              </div>
                        </div>

                        <div class="log-list" v-if="form.nhatKy.length > 0">
                              <table>
                                    <thead>
                                          <tr>
                                                <th>Ngày</th>
                                                <th>Hành động</th>
                                                <th>Chi tiết</th>
                                                <th></th>
                                          </tr>
                                    </thead>
                                    <tbody>
                                          <tr v-for="(log, index) in form.nhatKy" :key="index">
                                                <td>{{ log.ngay }}</td>
                                                <td>
                                                      <span class="badge" :class="log.hanhDong">{{ log.hanhDong
                                                            }}</span>
                                                </td>
                                                <td>{{ log.chiTiet }}</td>
                                                <td><span class="delete-btn" @click="xoaNhatKy(index)">🗑</span></td>
                                          </tr>
                                    </tbody>
                              </table>
                        </div>
                        <p v-else class="empty-text">Chưa có nhật ký nào.</p>

                  </div>

                  <div class="modal-footer">
                        <button class="btn-cancel" @click="$emit('dong-form')">Hủy bỏ</button>
                        <button class="btn-save" @click="xuLyLuu">💾 Lưu dữ liệu</button>
                  </div>
            </div>
      </div>
</template>

<style scoped>
/* CSS HIỆN ĐẠI (MODAL) */
.modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      /* Nền tối mờ */
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 2000;
      backdrop-filter: blur(3px);
      /* Hiệu ứng làm mờ nền map */
}

.modal-content {
      background: white;
      width: 600px;
      max-width: 90%;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
      overflow: hidden;
      font-family: 'Segoe UI', sans-serif;
      animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
      from {
            transform: translateY(20px);
            opacity: 0;
      }

      to {
            transform: translateY(0);
            opacity: 1;
      }
}

.modal-header {
      background: #42b883;
      padding: 15px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: white;
}

.modal-body {
      padding: 20px;
      max-height: 60vh;
      overflow-y: auto;
}

.section-title {
      font-weight: bold;
      margin-bottom: 10px;
      color: #2c3e50;
      border-bottom: 2px solid #eee;
      padding-bottom: 5px;
      margin-top: 10px;
}

/* Form Styles */
.form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-bottom: 20px;
}

.form-group {
      display: flex;
      flex-direction: column;
}

.form-group label {
      font-size: 0.85rem;
      color: #666;
      margin-bottom: 5px;
}

.form-group input,
.form-group select {
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 6px;
      outline: none;
}

.form-group input:focus {
      border-color: #42b883;
}

/* Log Styles */
.log-input-box {
      background: #f8f9fa;
      padding: 10px;
      border-radius: 8px;
      margin-bottom: 10px;
}

.log-row {
      display: flex;
      gap: 5px;
}

.log-row input[type="text"] {
      flex-grow: 1;
}

.btn-add {
      background: #42b883;
      color: white;
      border: none;
      width: 30px;
      border-radius: 4px;
      cursor: pointer;
}

table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
}

th {
      text-align: left;
      color: #888;
      font-weight: normal;
      padding: 5px;
}

td {
      padding: 8px 5px;
      border-bottom: 1px solid #eee;
}

.badge {
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.75rem;
      color: white;
      background: #95a5a6;
}

.badge.bon_phan {
      background: #e67e22;
}

.badge.phun_thuoc {
      background: #e74c3c;
}

.badge.thu_hoach {
      background: #f1c40f;
      color: #333;
}

.delete-btn {
      cursor: pointer;
      color: #aaa;
}

.delete-btn:hover {
      color: red;
}

.modal-footer {
      padding: 15px 20px;
      background: #f8f9fa;
      display: flex;
      justify-content: flex-end;
      gap: 10px;
}

.btn-save {
      background: #42b883;
      color: white;
      padding: 8px 20px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
}

.btn-cancel {
      background: white;
      border: 1px solid #ddd;
      padding: 8px 15px;
      border-radius: 6px;
      cursor: pointer;
}

.btn-close {
      background: none;
      border: none;
      color: white;
      font-size: 1.2rem;
      cursor: pointer;
}
</style>