// import "leaflet/dist/leaflet.css";
// import "./assets/styles/tailwind.css";
// import "./assets/main.css";

// import { createApp } from "vue";
// import App from "./App.vue";
// import router from "./router";

// const app = createApp(App);

// app.use(router);

// app.mount("#app");
// --- CODE ĐỂ KIỂM TRA ---
import "./assets/styles/tailwind.css";
import "./assets/main.css";

import { createApp } from "vue";
import router from "./router";

// Tạm thời thay thế App.vue bằng một template đơn giản
const TestApp = {
  template: '<h1 style="color: black; font-size: 30px; text-align: center; margin-top: 50px;">Test OK: Lỗi nằm trong App.vue</h1>'
};

const app = createApp(TestApp);
app.use(router);
app.mount("#app");
// --- HẾT CODE KIỂM TRA ---
