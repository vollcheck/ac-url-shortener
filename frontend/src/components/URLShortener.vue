<template>
  <div class="frame">
    <div class="container">
      <div class="logo">
        <img :src="logoSrc" />
      </div>

      <div class="content">
        <h1>Short link</h1>

        <form @submit.prevent="shortenURL">
          <label id="input-filled">Link to shortcut</label>
          <input
            v-model="url"
            type="url"
            required
            :class="{ invalid: !isValidURL }"
          />
          <button type="submit" :disabled="!isValidURL">Shorten it</button>
        </form>
        <div v-if="shortenedURL" class="result">
          <span>{{ shortenedURL }}</span>
          <button @click="copyToClipboard" class="copy-button">
            <img class="copy-icon" :src="iconCopy" />
          </button>
        </div>
      </div>
    </div>

    <div v-if="recentURLs.length > 0" class="recent-urls">
      <span>Last links</span>
      <div class="recent-urls-container-border">
        <div class="recent-urls-container">
          <ul>
            <li
              v-for="(item, index) in recentURLs"
              :key="index"
              class="recent-url"
            >
              <div class="left">
                <p>{{ item.original }}</p>
                <a :href="item.short" target="_blank">{{ item.short }}</a>
              </div>
              <div class="right">
                <button @click="copyToClipboard" class="copy-button">
                  <img class="copy-icon" :src="iconCopy" />
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import axios from 'axios'
import logoSrc from '@/assets/Vector.svg'
import iconCopy from '@/components/icons/icon_copy.svg'

interface URLPair {
  original: string
  short: string
}

export default defineComponent({
  name: 'URLShortener',
  setup() {
    const url = ref('')
    const shortenedURL = ref('')
    const recentURLs = ref<URLPair[]>([])

    const isValidURL = computed(() => {
      try {
        new URL(url.value)
        return true
      } catch {
        return false
      }
    })

    const shortenURL = async () => {
      if (!isValidURL.value) return

      try {
        const response = await axios.post('/api/shorten/', { url: url.value })
        shortenedURL.value = response.data.short_url
        addToRecentURLs({ original: url.value, short: shortenedURL.value })
      } catch (error) {
        console.error('Error shortening URL:', error)
      }
    }

    const copyToClipboard = () => {
      navigator.clipboard
        .writeText(shortenedURL.value)
        .then(() => {})
        .catch(err => console.error('Error copying text: ', err))
    }

    const addToRecentURLs = (urlPair: URLPair) => {
      recentURLs.value.unshift(urlPair)
      if (recentURLs.value.length > 3) {
        recentURLs.value.pop()
      }
      localStorage.setItem('recentURLs', JSON.stringify(recentURLs.value))
    }

    // Load recent URLs from localStorage on component mount
    const loadRecentURLs = () => {
      const stored = localStorage.getItem('recentURLs')
      if (stored) {
        recentURLs.value = JSON.parse(stored)
      }
    }
    loadRecentURLs()

    return {
      url,
      shortenedURL,
      recentURLs,
      isValidURL,
      shortenURL,
      copyToClipboard,
      logoSrc,
      iconCopy,
    }
  },
})
</script>

<style scoped>
.frame {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 24px;
  width: 480px;
  left: calc(50% - 480px / 2);
  top: calc(50% - 462px / 2);
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 480px;
  height: 462px;
  background: #ffffff;
  box-shadow: 0px 15px 80px rgba(34, 3, 134, 0.06);
  border-radius: 30px;
}

.logo {
  width: 300px;
  height: 92px;
  margin: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
}

h1 {
  display: flex;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: -0.02em;
  color: #363c56;
}

label#input-filled {
  font-size: 12px;
  color: #4a24ac;
}

form input {
  width: 100%;
  padding: 4px;
  padding-left: 0px;
  background-color: transparent;
  font-size: 16px;
  color: #333;
  border: none;
  border-bottom: 1px solid #4a24ac;
}

form input:focus {
  outline: none;
}

form button {
  width: 100%;
  background-color: #4a24ac;
  font-size: 16px;
  font-weight: 500;
  color: white;
  border: none;
  gap: 2px;
  padding: 12px;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 20px;
}

form button:hover {
  background-color: #553c9a;
}

.copy-icon {
  cursor: pointer;
}

.result {
  height: 56px;
  border-radius: 8px;
  background-color: #fafafa;
  font-weight: 700;
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #4a24ac;
  padding-left: 16px;
  padding-right: 16px;
}

.copy-button {
  border: 0px;
  background-color: transparent;
}

.recent-urls-container-border {
  border: 2px solid #e1e2e7;
  border-radius: 40px;
}

.recent-urls {
  width: 100%;
  font-weight: 700;
  font-size: 12px;
  line-height: 17px;
  color: #363c56;
}

.recent-urls span {
  margin: 12px;
  padding: 12px;
  margin-bottom: 30px;
}

.recent-urls-container ul {
  list-style-type: none;
  padding-inline-start: 0;
}

.recent-url {
  display: flex;
  background: #ffffff;
  border-radius: 16px;
  justify-content: space-between;
  align-items: center;
  padding-left: 32px;
  padding-right: 32px;
  padding-top: 8px;
  padding-bottom: 8px;
  margin: 12px;
}

.recent-urls-container ul li:first-child {
  border-top-left-radius: 32px;
  border-top-right-radius: 32px;
}

.recent-urls-container ul li:last-child {
  border-bottom-left-radius: 32px;
  border-bottom-right-radius: 32px;
}

.left p {
  padding: 0;
  font-size: 12px;
  font-weight: 400;
  margin: 0;
}

a {
  text-decoration: none;
  color: #4a24ac;
}
</style>
