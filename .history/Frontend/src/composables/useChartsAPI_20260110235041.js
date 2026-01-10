/**
 * ========== COMPOSABLE: useChartsAPI.js ==========
 * Purpose: Fetch real chart data từ Backend API
 */

import { ref } from "vue";
import axios from "axios";

export function useChartsAPI() {
     const dashboardStats = ref(null);
     const exportMarkets = ref(null);
     const cropProduction = ref(null);
     const productivityTrend = ref(null);
     const farmStatus = ref(null);
     const activityTimeline = ref(null);
     const isLoading = ref(false);
     const error = ref(null);

     // Fetch dashboard statistics
     const fetchDashboardStats = async () => {
          isLoading.value = true;
          try {
               const response = await axios.get("/api/charts/dashboard-stats");
               dashboardStats.value = response.data;
               console.log("✅ Dashboard stats loaded:", dashboardStats.value);
          } catch (err) {
               console.error("❌ Error fetching dashboard stats:", err);
               // Fallback data
               dashboardStats.value = {
                    total_farms: 0,
                    active_farms: 0,
                    total_area: 0,
                    total_activities: 0
               };
          } finally {
               isLoading.value = false;
          }
     };

     // Fetch export markets pie chart
     const fetchExportMarkets = async () => {
          try {
               const response = await axios.get("/api/charts/export-markets");
               exportMarkets.value = response.data;
               console.log("✅ Export markets loaded");
          } catch (err) {
               console.error("❌ Error fetching export markets:", err);
               exportMarkets.value = [];
          }
     };

     // Fetch crop production bar chart
     const fetchCropProduction = async () => {
          try {
               const response = await axios.get("/api/charts/crop-production");
               cropProduction.value = response.data;
               console.log("✅ Crop production loaded");
          } catch (err) {
               console.error("❌ Error fetching crop production:", err);
               cropProduction.value = [];
          }
     };

     // Fetch productivity trend line chart
     const fetchProductivityTrend = async () => {
          try {
               const response = await axios.get("/api/charts/productivity-trend");
               productivityTrend.value = response.data;
               console.log("✅ Productivity trend loaded");
          } catch (err) {
               console.error("❌ Error fetching productivity trend:", err);
               productivityTrend.value = { months: [], data: [] };
          }
     };

     // Fetch farm status pie chart
     const fetchFarmStatus = async () => {
          try {
               const response = await axios.get("/api/charts/farm-status");
               farmStatus.value = response.data;
               console.log("✅ Farm status loaded");
          } catch (err) {
               console.error("❌ Error fetching farm status:", err);
               farmStatus.value = [];
          }
     };

     // Fetch activity timeline
     const fetchActivityTimeline = async () => {
          try {
               const response = await axios.get("/api/charts/activity-timeline");
               activityTimeline.value = response.data;
               console.log("✅ Activity timeline loaded");
          } catch (err) {
               console.error("❌ Error fetching activity timeline:", err);
               activityTimeline.value = { months: [], data: [] };
          }
     };

     // Fetch all charts data
     const fetchAllCharts = async () => {
          isLoading.value = true;
          await Promise.all([
               fetchDashboardStats(),
               fetchExportMarkets(),
               fetchCropProduction(),
               fetchProductivityTrend(),
               fetchFarmStatus(),
               fetchActivityTimeline()
          ]);
          isLoading.value = false;
     };

     return {
          dashboardStats,
          exportMarkets,
          cropProduction,
          productivityTrend,
          farmStatus,
          activityTimeline,
          isLoading,
          error,
          fetchDashboardStats,
          fetchExportMarkets,
          fetchCropProduction,
          fetchProductivityTrend,
          fetchFarmStatus,
          fetchActivityTimeline,
          fetchAllCharts
     };
}
