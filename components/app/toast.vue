<template>
  <Toast position="top-center" class="z-46">
    <template #container="{ message }">
      <div v-if="message.meta?.level === 'info'" class="alert alert-info">
        <span>{{ message.detail }}</span>
      </div>
      <div
        v-if="message.meta?.level === 'success'" class="alert alert-success"
      >
        <span>{{ message.detail }}</span>
      </div>
      <div
        v-if="message.meta?.level === 'error'" class="alert alert-error"
      >
        <span>{{ message.detail }}</span>
      </div>
    </template>
  </Toast>
</template>
