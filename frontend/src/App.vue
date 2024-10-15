<template>
  <div id="app">
    <URLShortener />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import URLShortener from './components/URLShortener.vue';

export default defineComponent({
  name: 'App',
  components: {
    URLShortener
  }
});
</script>
