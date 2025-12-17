# 📝 Coding Standards

## 🇻🇳 Tiêu chuẩn code / 🇺🇸 Coding Standards

---

## 📦 Vue 3 Composition API

### ✅ DO - Nên làm

```vue
<script setup>
import { ref, computed, onMounted } from "vue";
import { useHome } from "@/composables/useHome";

// Props & Emits
const props = defineProps({
     data: { type: Array, required: true },
     title: { type: String, default: "" },
});

const emit = defineEmits(["update", "delete"]);

// Composables
const { searchQuery, filteredItems } = useHome();

// Local state
const isLoading = ref(false);

// Computed
const itemCount = computed(() => props.data.length);

// Methods
function handleClick(item) {
     emit("update", item);
}

// Lifecycle
onMounted(() => {
     console.log("Component mounted");
});
</script>
```

### ❌ DON'T - Không nên

```vue
<!-- Không dùng Options API -->
<script>
export default {
     data() {
          return { count: 0 };
     },
     methods: {
          increment() {
               this.count++;
          },
     },
};
</script>
```

---

## 🎨 Tailwind CSS

### ✅ DO - Nên làm

```vue
<!-- Sử dụng Tailwind utility classes -->
<div
     class="flex items-center justify-between p-4 bg-white rounded-lg shadow-md"
>
  <span class="text-sm font-medium text-gray-700">Label</span>
  <button class="px-4 py-2 text-white bg-emerald-600 rounded-lg hover:bg-emerald-700">
    Action
  </button>
</div>
```

### ❌ DON'T - Không nên

```vue
<!-- Không dùng inline styles -->
<div style="display: flex; padding: 16px; background: white;">
  <span style="font-size: 14px;">Label</span>
</div>
```

---

## 📁 File Structure

### Component file structure

```vue
<script setup>
// 1. Imports
import { ref, computed } from 'vue'
import ChildComponent from './ChildComponent.vue'

// 2. Props & Emits
const props = defineProps({ ... })
const emit = defineEmits([...])

// 3. Composables
const { data } = useComposable()

// 4. Reactive state
const isOpen = ref(false)

// 5. Computed properties
const count = computed(() => ...)

// 6. Methods
function handleClick() { ... }

// 7. Lifecycle hooks
onMounted(() => { ... })
</script>

<template>
     <!-- Template content -->
</template>

<style scoped>
/* Scoped styles if needed */
</style>
```

---

## 📝 Naming Conventions

### Files

| Type        | Convention               | Example            |
| ----------- | ------------------------ | ------------------ |
| Components  | PascalCase               | `MapComponent.vue` |
| Composables | camelCase với use prefix | `useHome.js`       |
| Views       | PascalCase               | `HomeView.vue`     |
| Utilities   | camelCase                | `statusHelpers.js` |

### Variables

| Type          | Convention  | Example                              |
| ------------- | ----------- | ------------------------------------ |
| Reactive refs | camelCase   | `const isLoading = ref(false)`       |
| Computed      | camelCase   | `const filteredList = computed(...)` |
| Functions     | camelCase   | `function handleSubmit()`            |
| Constants     | UPPER_SNAKE | `const MAX_ITEMS = 100`              |

### CSS Classes

| Type           | Convention    | Example             |
| -------------- | ------------- | ------------------- |
| Custom classes | kebab-case    | `.floating-sidebar` |
| Tailwind       | utility-first | `flex items-center` |

---

## 💬 Comments

### ✅ Good comments

```javascript
// Fetch data from API and update local state
async function fetchData() {
     // ...
}

/**
 * Calculate total area of all farming zones
 * @param {Array} zones - Array of zone objects
 * @returns {number} Total area in hectares
 */
function calculateTotalArea(zones) {
     return zones.reduce((sum, zone) => sum + zone.area, 0);
}
```

### ❌ Bad comments

```javascript
// increment i
i++;

// return data
return data;
```

---

## 📊 Chart.js Standards

```javascript
const chartOptions = {
     responsive: true,
     maintainAspectRatio: false, // Cho responsive containers
     plugins: {
          legend: {
               position: "top",
               labels: {
                    font: { size: 10 }, // Nhỏ cho mobile
                    usePointStyle: true,
               },
          },
          tooltip: {
               callbacks: {
                    // Custom tooltip formatting
               },
          },
     },
};
```

---

## 🗺️ Leaflet Standards

```javascript
// Initialize map with proper options
const map = L.map("map", {
     center: [10.762622, 106.660172],
     zoom: 13,
     zoomControl: false, // Custom zoom control position
});

// Always cleanup on unmount
onUnmounted(() => {
     if (map) {
          map.remove();
     }
});
```

---

## ✅ Pre-commit Checklist

-    [ ] No console.log() in production code
-    [ ] All props have type definitions
-    [ ] Composables are properly exported
-    [ ] Tailwind classes are sorted (prettier-plugin-tailwindcss)
-    [ ] No unused imports
-    [ ] Proper error handling for async operations
-    [ ] Mobile responsive checked

---

## 🔗 Related

-    [[Git Workflow|Git Workflow]]
-    [[Pull Request Guide|PR Guide]]
-    [[Styling Guide|Styling Guide]]
