import { ref } from "vue";

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

     // Mock data danh sách nhật ký hoạt động
     const diaryList = ref([
          {
               id: 1,
               type: "fertilizer",
               title: "Bón thúc đợt 1",
               field: "Thửa A (Gần nhà)",
               details: "Sử dụng NPK 20-20-15. Liều lượng 50kg/công. Thời tiết mát mẻ.",
               dateDay: "08",
               dateMonth: "T12",
          },
          {
               id: 2,
               type: "spray",
               title: "Phun thuốc trừ rầy",
               field: "Thửa B (Bãi bồi)",
               details: "Phát hiện rầy nâu mật độ cao. Phun kèm thuốc bám dính.",
               dateDay: "05",
               dateMonth: "T12",
          },
          {
               id: 3,
               type: "water",
               title: "Tưới nước",
               field: "Thửa A (Gần nhà)",
               details: "Chạy máy bơm 2 giờ để giữ ẩm chân ruộng.",
               dateDay: "04",
               dateMonth: "T12",
          },
          {
               id: 4,
               type: "tillage",
               title: "Làm đất gieo sạ",
               field: "Thửa C (Sau đồi)",
               details: "Cày ải phơi đất chuẩn bị cho vụ Đông Xuân.",
               dateDay: "01",
               dateMonth: "T12",
          },
          {
               id: 5,
               type: "sow",
               title: "Xuống giống lúa",
               field: "Thửa D (Mới thuê)",
               details: "Gieo sạ giống ST25. Mật độ 120kg/ha.",
               dateDay: "28",
               dateMonth: "T11",
          },
     ]);

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
