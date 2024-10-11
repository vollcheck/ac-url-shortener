<!-- URLShortener.vue -->
<template>
<div class="url-shortener">

  <img id="logo" :src="svgLogo" />

  <h1>Short link</h1>
  <form @submit.prevent="shortenURL">
    <label>Link to shortcut</label>
    <input
      v-model="url"
      type="url"
      required
      :class="{ 'invalid': !isValidURL }"
      >
    <button type="submit" :disabled="!isValidURL">Shorten it</button>
  </form>
  <div v-if="shortenedURL" class="result">
    <p>Shortened URL:</p>
    <div class="shortened-url">
      <span>{{ shortenedURL }}</span>
      <button @click="copyToClipboard" class="copy-button">
        <i class="copy-icon"></i>
      </button>
    </div>
  </div>
  <div v-if="recentURLs.length > 0" class="recent-urls">
    <ul>
      <li v-for="(item, index) in recentURLs" :key="index">
        <a :href="item.short" target="_blank">{{ item.original }}</a>
      </li>
    </ul>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import axios from 'axios';

interface URLPair {
    original: string;
    short: string;
}

export default defineComponent({
    name: 'URLShortener',
    setup() {
        const url = ref('');
        const shortenedURL = ref('');
        const recentURLs = ref<URLPair[]>([]);

        const isValidURL = computed(() => {
            try {
                new URL(url.value);
                return true;
            } catch {
                return false;
            }
        });

        const shortenURL = async () => {
            if (!isValidURL.value) return;

            try {
                const response = await axios.post('/api/shorten/', { url: url.value });
                shortenedURL.value = response.data.short_url;
                addToRecentURLs({ original: url.value, short: shortenedURL.value });
            } catch (error) {
                console.error('Error shortening URL:', error);
                // TODO: format it better?
            }
        };

        const copyToClipboard = () => {
            navigator.clipboard.writeText(shortenedURL.value)
                .then(() => {
                    // Optionally, show a "Copied!" message
                })
                .catch(err => console.error('Error copying text: ', err));
        };

        const addToRecentURLs = (urlPair: URLPair) => {
            recentURLs.value.unshift(urlPair);
            if (recentURLs.value.length > 3) {
                recentURLs.value.pop();
            }
            localStorage.setItem('recentURLs', JSON.stringify(recentURLs.value));
        };

        // Load recent URLs from localStorage on component mount
        const loadRecentURLs = () => {
            const stored = localStorage.getItem('recentURLs');
            if (stored) {
                recentURLs.value = JSON.parse(stored);
            }
        };
        loadRecentURLs();

        const svgLogo = 1;


        return {
            url,
            shortenedURL,
            recentURLs,
            isValidURL,
            shortenURL,
            copyToClipboard,
            svgLogo
        };
    }
});
</script>

<style scoped>
  .url-shortener {
  position: relative;
  width: 1280px;
  height: 832px;
  background: #FBFCFE;

  /* container */

  /* Auto layout */
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  gap: 32px;

  width: 480px;
  height: 462px;

  background: #FFFFFF;
  box-shadow: 0px 15px 80px rgba(34, 3, 134, 0.06);
  border-radius: 30px;

  }

  .other {
/* Inside auto layout */
  flex: none;
  order: 0;
  flex-grow: 0;

  }

</style>
