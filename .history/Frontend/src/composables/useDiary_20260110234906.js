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

     // Thêm hoạt động mới
     const addDiaryEntry = (entry) => {
          diaryList.value.unshift({
               id: Date.now(),
               ...entry,
          });
     };

     // Xóa hoạt động
     const removeDiaryEntry = (id) => {
          diaryList.value = diaryList.value.filter((item) => item.id !== id);
     };

     return {
          activityTypes,
          diaryList,
          getCurrentDate,
          getActivityIcon,
          getActivityLabel,
          addDiaryEntry,
          removeDiaryEntry,
     };
}
