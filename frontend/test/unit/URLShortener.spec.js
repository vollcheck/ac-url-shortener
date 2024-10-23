import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import URLShortener from '@/components/URLShortener.vue'
import axios from 'axios'

describe('URLShortener.vue', () => {
  let wrapper;
  let consoleSpy;
  const url = "http://short.url/abc123";

  beforeEach(() => {
    vi.mock('axios');

    localStorage.clear();

    // console mock
    consoleSpy = vi.spyOn(console, 'log');

    // AJAX mock
    axios.post.mockResolvedValue({ data: { short_url: url } });

    // clipboard mock
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn().mockImplementation(() => Promise.resolve()),
      }
    });

    wrapper = mount(URLShortener);
  });

  afterEach(() => {
    consoleSpy.mockRestore();
  });


  describe('URLShortener', () => {
    it('should render the input and button', () => {
      const wrapper = mount(URLShortener)
      const input = wrapper.find('#urlInput')
      const button = wrapper.find('button[type="submit"]')

      expect(input.exists()).toBe(true)
      expect(button.exists()).toBe(true)
    });

    it('disables the button when the URL is invalid', async () => {
      const wrapper = mount(URLShortener)
      const input = wrapper.find('#urlInput')
      await input.setValue('invalid-url')

      const button = wrapper.find('button[type="submit"]')
      expect(button.element.disabled).toBe(true)
    });

    it('enables the button for valid URL', async () => {
      const wrapper = mount(URLShortener)
      const input = wrapper.find('#urlInput')
      await input.setValue('https://example.com')

      const button = wrapper.find('button[type="submit"]')
      expect(button.element.disabled).toBe(false)
    });

    it('shows the shortened URL after submit', async () => {
      await wrapper.find('input[id="urlInput"]').setValue('https://example.com');
      await wrapper.find('button[type="submit"]').trigger('submit');

      expect(wrapper.find('.result').text()).toContain(url)
    });
  });


  describe('Copy Functionality', () => {
    it('copies shortened URL to clipboard', async () => {
      await wrapper.find('input[id="urlInput"]').setValue('https://example.com');
      await wrapper.find('button[type="submit"]').trigger('submit');

      await wrapper.find('.copy-button-main').trigger('click');

      expect(consoleSpy).toHaveBeenCalledWith("Link saved to a clipboard!");
    });
  });
});
