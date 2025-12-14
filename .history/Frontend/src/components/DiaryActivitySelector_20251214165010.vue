<script setup>
/**
 * ========== COMPONENT: DiaryActivitySelector.vue ==========
 * Purpose: Activity selection grid - displays 6 farming activity buttons
 * User selects one activity type (gieo, compost, pest, water, weeding, harvest)
 * 
 * Architecture:
 *   - Parent: DiaryPage
 *   - Child: None
 *   - Communication: Props down, emits event on selection
 * 
 * Features:
 *   - 2x3 grid layout (2 columns on mobile, 3 columns on desktop)
 *   - Visual selection feedback: Active button highlighted in green
 *   - Check circle icon indicator for selected state
 *   - Icon scale animation on hover
 *   - Responsive design (grid-cols-2 sm:grid-cols-3)
 * 
 * Props:
 *   - activities (Array): List of activity objects [{id, name, icon, color}]
 *   - selectedActivity (String): Currently selected activity ID
 * 
 * Emits:
 *   - select (String): Activity ID when user clicks button
 */

// ========== IMPORTS ==========
// (No imports needed - using only Vue template features)

// ========== PROPS ==========
// Define props for activity data and current selection state
defineProps({
  // activities: Array of activity objects
  // Structure: {id: string, name: string, icon: string, color: string}
  // Used to render button grid and get icon/name for display
  activities: Array,
  
  // selectedActivity: Currently selected activity ID (string)
  // Used to apply active styling and show check icon
  selectedActivity: String
});

// ========== EMITS ==========
// Define custom event emitted when activity selected
// Event name: 'select'
// Payload: activity.id (string) - ID of clicked activity
const emit = defineEmits(['select']);

/**
 * handleActivityClick: Handler for activity button click
 * Not needed here - using inline @click="$emit('select', activity.id)"
 * Could be extracted if we need additional logic (validation, analytics, etc)
 */

</script>

<template>
  <!-- ========== ACTIVITY SELECTOR SECTION ========== -->
  <!-- Section: Main container for activity selection grid -->
  <section>
    
    <!-- ========== SECTION HEADER ========== -->
    <!-- Header: Flex layout with title and optional controls -->
    <!-- mb-4 = 16px bottom margin before grid -->
    <div class="flex items-center justify-between mb-4">
      <!-- Title: "Chọn hoạt động" = Select Activity -->
      <!-- h3 = heading level 3, text-lg = 18px font size, font-bold -->
      <!-- flex items-center gap-2 = icon + text horizontally with 8px gap -->
      <!-- text-gray-800 = dark gray color for good contrast -->
      <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
        <!-- Icon: grid_view = Material Symbol for grid layout/selection -->
        <span class="material-symbols-outlined text-[#2E7D32]">grid_view</span>
        <!-- Label text -->
        Chọn hoạt động
      </h3>
    </div>
    
    <!-- ========== ACTIVITY BUTTONS GRID ========== -->
    <!-- Grid container: grid-cols-2 = 2 columns on mobile, sm:grid-cols-3 = 3 columns on tablet+ -->
    <!-- gap-4 = 16px gap between items horizontally and vertically -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
      
      <!-- ========== ACTIVITY BUTTON LOOP ========== -->
      <!-- v-for: Loop through each activity in activities array -->
      <!-- :key: Unique identifier (activity.id) for Vue's list rendering -->
      <button
        v-for="activity in activities"
        :key="activity.id"
        @click="$emit('select', activity.id)"
        :class="[
          // Base classes: Always applied to all buttons
          'group relative flex flex-col items-center justify-center p-6 rounded-3xl shadow-sm border transition-all duration-300 hover:-translate-y-1',
          // Conditional classes: Applied based on selectedActivity
          // Active state (button selected): Green background with white text
          selectedActivity === activity.id
            // Active styling:
            // bg-[#2E7D32] = green background
            // text-white = white text (name + badge)
            // shadow-[0_0_15px_rgba(76,175,80,0.3)] = green glowing shadow
            // transform scale-[1.02] = slightly enlarged (102% size)
            // ring-4 ring-[#E8F5E9] = thick green ring outline
            ? 'bg-[#2E7D32] text-white shadow-[0_0_15px_rgba(76,175,80,0.3)] transform scale-[1.02] ring-4 ring-[#E8F5E9]'
            // Inactive state (button not selected): White background with hover effects
            // bg-white = white background
            // border-transparent = no visible border (but border exists in markup)
            // hover:border-[#2E7D32]/30 = faint green border on hover
            // hover:shadow-[...] = subtle shadow lift on hover for depth
            : 'bg-white border-transparent hover:border-[#2E7D32]/30 hover:shadow-[0_4px_20px_-2px_rgba(46,125,50,0.1)]'
        ]"
      >
        <!-- ========== CHECK ICON (ACTIVE INDICATOR) ========== -->
        <!-- Conditional render: Show only when this button is selected -->
        <!-- v-if: Only display when selectedActivity === activity.id -->
        <!-- Positioned: absolute top-3 right-3 = top-right corner with slight margin -->
        <div v-if="selectedActivity === activity.id" class="absolute top-3 right-3">
          <!-- Icon: check_circle = Material Symbol for checked/confirmed status -->
          <!-- text-white/80 = white with 80% opacity for subtle appearance -->
          <!-- text-xl = 20px icon size -->
          <span class="material-symbols-outlined text-white/80 text-xl">check_circle</span>
        </div>
        
        <!-- ========== ACTIVITY ICON ========== -->
        <!-- Icon container: h-14 w-14 = 56px x 56px square -->
        <!-- rounded-2xl = rounded corners (2xl = 16px border-radius) -->
        <!-- flex items-center justify-center = center icon inside square -->
        <!-- mb-3 = 12px bottom margin before activity name -->
        <!-- transition-transform = smooth animation for scale changes -->
        <div
          :class="[
            // Base icon classes
            'h-14 w-14 rounded-2xl flex items-center justify-center mb-3 transition-transform',
            // Conditional background color
            selectedActivity === activity.id
              // Active icon background: Semi-transparent white (20% opacity)
              // Blends with green button background
              ? 'bg-white/20'
              // Inactive icon background: Tailwind color based on activity.color property
              // Uses template string to build class dynamically (e.g., bg-emerald-100, bg-red-100)
              // Note: Dynamic class names work with safelist in tailwind.config
              : `bg-${activity.color}-100 text-${activity.color}-600`,
            // Hover animation: Scale up icon when hovering inactive button
            // group-hover:scale-110 = 110% size on hover (only when group is hovered)
            selectedActivity !== activity.id && 'group-hover:scale-110'
          ]"
        >
          <!-- Material Symbol icon for activity -->
          <!-- text-4xl = 36px icon size -->
          <!-- :data = Dynamic icon name from activity.icon property -->
          <span class="material-symbols-outlined text-4xl">{{ activity.icon }}</span>
        </div>
        
        <!-- ========== ACTIVITY NAME ========== -->
        <!-- Activity name text: text-base = 16px, font-bold = 700 weight -->
        <!-- Dynamic color: white when active, gray with hover effect when inactive -->
        <span :class="[
          'text-base font-bold',
          // Text color conditional on selection state
          selectedActivity === activity.id
            // Active: white text
            ? 'text-white'
            // Inactive: dark gray text, green on hover
            : 'text-gray-700 group-hover:text-[#2E7D32]'
        ]">
          <!-- Display activity name (e.g., "Bón phân", "Gieo hạt") -->
          {{ activity.name }}
        </span>
        
        <!-- ========== STATUS BADGE ========== -->
        <!-- Badge: "Đang nhập..." = "Currently Entering..." status indicator -->
        <!-- v-if: Only show when button is selected (active state) -->
        <!-- text-xs = very small font (12px) -->
        <!-- bg-white/20 = semi-transparent white background -->
        <!-- px-2 py-0.5 = 8px horizontal, 2px vertical padding -->
        <!-- rounded-full = fully rounded edges (pill shape) -->
        <!-- mt-1 = 4px top margin to space from name -->
        <span v-if="selectedActivity === activity.id" class="text-xs bg-white/20 px-2 py-0.5 rounded-full mt-1">
          <!-- Badge text: Status indicator -->
          Đang nhập...
        </span>
      </button>
    </div>
  </section>
</template>
