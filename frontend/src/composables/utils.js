import { ref, onMounted, onUnmounted, computed } from 'vue';

export function useFetch(apiEndpoint, options = {}) {
  const data = ref(null);
  const error = ref(null);

  const fetchData = async () => {
    try {
      let body = options.body;
      const contentType = options.headers?.['Content-Type'];
      
      if (body) {
        if (contentType === 'application/x-www-form-urlencoded') {
          body = new URLSearchParams(body).toString();
        } else if (contentType === 'application/json') {
          body = JSON.stringify(body);
        }
      }
      const headers = {
        ...options.headers,
        ...(options.method && 
           options.method !== 'GET' && 
           !apiEndpoint.includes('/auth/') && 
           !apiEndpoint.includes('/users/') && {
          'API-KEY': import.meta.env.VITE_APP_API_KEY
        })
      };

      const response = await fetch(apiEndpoint, {
        ...options,
        headers,
        body,
        credentials: 'include',
        mode: 'cors',
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Response error:', errorData);
        throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
      }

      data.value = response.status !== 204 ? await response.json() : null;
    } catch (err) {
      console.error('Fetch error:', err);
      error.value = err.message;
    }
  };

  return { data, error, fetchData };
}

export function timeSince(date) {
  const seconds = Math.floor((new Date() - new Date(date)) / 1000);
  
  let interval = Math.floor(seconds / 31536000);
  if (interval >= 1) return `${interval} ${declineWord(interval, ['год', 'года', 'лет'])} назад`;
  interval = Math.floor(seconds / 2592000);
  if (interval >= 1) return `${interval} ${declineWord(interval, ['месяц', 'месяца', 'месяцев'])} назад`;
  interval = Math.floor(seconds / 86400);
  if (interval >= 1) return `${interval} ${declineWord(interval, ['день', 'дня', 'дней'])} назад`;
  interval = Math.floor(seconds / 3600);
  if (interval >= 1) return `${interval} ${declineWord(interval, ['час', 'часа', 'часов'])} назад`;
  interval = Math.floor(seconds / 60);
  if (interval >= 1) return `${interval} ${declineWord(interval, ['минута', 'минуты', 'минут'])} назад`;
  
  return `${seconds} ${declineWord(seconds, ['секунда', 'секунды', 'секунд'])} назад`;
}

export function formatDuration(seconds) {
  if (!seconds) return '0 секунд'

  let interval = Math.floor(seconds / 31536000)
  if (interval >= 1) return `${interval} ${declineWord(interval, ['год', 'года', 'лет'])}`
  interval = Math.floor(seconds / 2592000)
  if (interval >= 1) return `${interval} ${declineWord(interval, ['месяц', 'месяца', 'месяцев'])}`
  interval = Math.floor(seconds / 86400)
  if (interval >= 1) return `${interval} ${declineWord(interval, ['день', 'дня', 'дней'])}`
  interval = Math.floor(seconds / 3600)
  if (interval >= 1) return `${interval} ${declineWord(interval, ['час', 'часа', 'часов'])}`
  interval = Math.floor(seconds / 60)
  if (interval >= 1) return `${interval} ${declineWord(interval, ['минута', 'минуты', 'минут'])}`

  return `${seconds} ${declineWord(seconds, ['секунда', 'секунды', 'секунд'])}`
}

export function formatSleepDuration(hours) {
  const totalHours = Math.floor(hours);
  const minutes = Math.round((hours - totalHours) * 60);

  const hourText = totalHours > 0 ? `${totalHours} ч` : '';
  const minuteText = minutes > 0 ? `${minutes} мин` : '';

  if (totalHours > 0 && minutes > 0) {
    return `${hourText} ${minuteText}`;
  } else if (totalHours > 0) {
    return hourText;
  } else {
    return minuteText;
  }
}

export function declineWord(number, forms) {
  const cases = [2, 0, 1, 1, 1, 2];
  return forms[
    (number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number % 10 < 5) ? number % 10 : 5]
  ];
}


export function formatDate(dateString) {
  if (!dateString) return '';
  let dtStr = dateString.toString().replace(' ', 'T');
  if (!dtStr.endsWith('Z')) {
    dtStr += 'Z';
  }
  const date = new Date(dtStr);
  date.setUTCHours(date.getUTCHours() + 3);

  const day = String(date.getUTCDate()).padStart(2, '0');
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const year = String(date.getUTCFullYear()).slice(-2);
  const hours = String(date.getUTCHours()).padStart(2, '0');
  const minutes = String(date.getUTCMinutes()).padStart(2, '0');
  return `${day}.${month}.${year} ${hours}:${minutes}`;
}


export function useScrollToTop() {
  const showScrollToTop = ref(false);

  const handleScroll = () => {
    showScrollToTop.value = window.scrollY > 200;
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  onMounted(() => {
    window.addEventListener('scroll', handleScroll);
  });

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
  });

  return {
    showScrollToTop,
    scrollToTop,
  };
}
