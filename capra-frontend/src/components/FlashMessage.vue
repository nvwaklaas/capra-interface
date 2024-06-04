<template>
  <div class="fixed top-0 right-0 m-6">
    <div
      :class="{
        'bg-nvwa-rood text-white': type === 'error',
        'bg-nvwa-groen text-white': type === 'success',
      }"
      class="rounded-lg shadow-md p-6 pr-10"
      style="min-width: 240px"
    >
      <button
        class="opacity-75 cursor-pointer absolute top-0 right-0 py-2 px-3 hover:opacity-100"
      >
        ×
      </button>
      <div class="flex items-center">
        {{ message }}
      </div>
    </div>
  </div>
</template>
 
<script>
export default {
    props: {
        type: String,
        message: String,
    }
}
</script>