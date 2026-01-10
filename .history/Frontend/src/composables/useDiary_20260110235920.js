import { ref } from "vue";
import axios from "axios";

// Composable quản lý logic Nhật ký đồng ruộng
export function useDiary() {
     // Danh sách các loại hoạt động với icon emoji
     const activityTypes = [
          { id: "tillage", icon: "🚜", label: "Cày ải" },
          { id: "sow", icon: "🌱", label: "Gieo sạ" },
          { id: "fertilizer", icon: "🌾", label: "Bón phân" },
          { id: "spray", icon: "💊", label: "Phun thuốc" },
          { id: "water", icon: "💧", label: "Tưới nước" },
          { id: "harvest", icon: "💰", label: "Thu hoạch" },
     ];

     // Danh sách nhật ký từ API
     const diaryList = ref([]);
     const isLoading = ref(false);
     const error = ref(null);

     // Lấy ngày tháng hiện tại theo định dạng Việt Nam
     const getCurrentDate = () => {
          return new Date().toLocaleDateString("vi-VN", {
               day: "numeric",
               month: "long",
               year: "numeric",
          });
     };

     // Lấy icon emoji theo loại hoạt động
     const getActivityIcon = (activityId) => {
          const activity = activityTypes.find((a) => a.id === activityId);
          return activity ? activity.icon : "📝";
     };

     // Lấy nhãn hoạt động
     const getActivityLabel = (activityId) => {
          const activity = activityTypes.find((a) => a.id === activityId);
          return activity ? activity.label : "Khác";
     };

     // ========== API CALLS ==========
     
     // Fetch tất cả diary entries từ API
     const fetchDiaryList = async () => {
          isLoading.value = true;
          error.value = null;
          try {
               const response = await axios.get("/api/diary/");
               const entries = response.data.data || response.data || [];
               
               // Transform data từ API
               diaryList.value = entries.map(entry => {
                    const date = new Date(entry.ngay_thuc_hien || entry.ngay_tao);
                    return {
                         id: entry.id,
                         type: entry.loai_hoat_dong?.ma_loai || "fertilizer",
                         title: entry.loai_hoat_dong?.ten_loai || "Hoạt động",
                         field: entry.vung_trong?.ten_vung || "Vùng trồng",
                         details: entry.mo_ta || "",
                         dateDay: date.getDate().toString().padStart(2, '0'),
                         dateMonth: `T${date.getMonth() + 1}`,
                         vung_trong_id: entry.vung_trong_id,
                         loai_hoat_dong_id: entry.loai_hoat_dong_id,
                         ngay_thuc_hien: entry.ngay_thuc_hien,
                         fullData: entry
                    };
               });
               
               console.log(`✅ Loaded ${diaryList.value.length} diary entries from API`);
          } catch (err) {
               console.error("❌ Error fetching diary:", err);
               error.value = err.message;
          } finally {
               isLoading.value = false;
          }
     };

     // Thêm hoạt động mới vào database
     const addDiaryEntry = async (entry) => {
          isLoading.value = true;
          error.value = null;
          try {
               const payload = {
                    vung_trong_id: entry.vung_trong_id || 1,
                    loai_hoat_dong_id: entry.loai_hoat_dong_id || 1,
                    ngay_thuc_hien: entry.ngay_thuc_hien || new Date().toISOString().split('T')[0],
                    mo_ta: entry.details || entry.mo_ta || ""
               };
               
               const response = await axios.post("/api/diary/", payload);
               console.log("✅ Diary entry created:", response.data);
               
               // Refresh list
               await fetchDiaryList();
               return response.data;
          } catch (err) {
               console.error("❌ Error creating diary:", err);
               error.value = err.response?.data?.detail || err.message;
               throw err;
          } finally {
               isLoading.value = false;
          }
     };

     // Cập nhật hoạt động
     const updateDiaryEntry = async (id, entry) => {
          isLoading.value = true;
          error.value = null;
          try {
               const payload = {
                    vung_trong_id: entry.vung_trong_id,
                    loai_hoat_dong_id: entry.loai_hoat_dong_id,
                    ngay_thuc_hien: entry.ngay_thuc_hien,
                    mo_ta: entry.details || entry.mo_ta
               };
               
               const response = await axios.put(`/api/diary/${id}`, payload);
               console.log("✅ Diary entry updated:", response.data);
               
               // Refresh list
               await fetchDiaryList();
               return response.data;
          } catch (err) {
               console.error("❌ Error updating diary:", err);
               error.value = err.response?.data?.detail || err.message;
               throw err;
          } finally {
               isLoading.value = false;
          }
     };

     // Xóa hoạt động
     const removeDiaryEntry = async (id) => {
          isLoading.value = true;
          error.value = null;
          try {
               await axios.delete(`/api/diary/${id}`);
               console.log("✅ Diary entry deleted:", id);
               
               // Remove from local list
               diaryList.value = diaryList.value.filter((item) => item.id !== id);
          } catch (err) {
               console.error("❌ Error deleting diary:", err);
               error.value = err.response?.data?.detail || err.message;
               throw err;
          } finally {
               isLoading.value = false;
          }
     };

     return {
          activityTypes,
          diaryList,
          isLoading,
          error,
          getCurrentDate,
          getActivityIcon,
          getActivityLabel,
          fetchDiaryList,
          addDiaryEntry,
          updateDiaryEntry,
          removeDiaryEntry,
          getCurrentDate,
          getActivityIcon,
          getActivityLabel
     };
}
