<script setup lang="ts">
const props = defineProps<{
  label: string;
}>();
</script>

<template>
  <span class="missing-field">{{ props.label }}</span>
</template>

<style scoped>
.missing-field {
  color: #888;
  font-style: italic;
  font-size: 0.9em;
}
</style>
