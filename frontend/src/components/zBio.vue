<template>
  <div class="container mx-auto flex justify-center">
    <div class="max-w-lg space-y-3 sm:space-y-4 text-center">
      <img class="w-28 h-28 sm:w-32 sm:h-32 rounded-full mx-auto" src="../assets/pvlppv.jpg" alt="Profile picture">
      <h1 class="text-lg sm:text-xl font-semibold">Меня зовут Павел Попов</h1>
      <p class="text-sm sm:text-base text-gray-600">
        Привет! Здесь я качаю свою осознанность в различных сферах жизни.
        Учусь в ВШЭ ФКН, работаю аналитиком в Т-Банке, пилю стартапы, пишу музыку.
      </p>
      <div class="flex items-center justify-center gap-3 sm:gap-2 flex-wrap">
        <a href="https://t.me/pvlppv" class="p-0.5 sm:p-1 rounded-lg flex items-center border border-gray-300 justify-center transition-all duration-300 hover:border-gray-100 hover:bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 72 72" fill="none">
            <path
              d="M17.5822 33.5652C17.5822 33.5652 36.2102 25.7194 42.6707 22.9567C45.1473 21.8518 53.546 18.3155 53.546 18.3155C53.546 18.3155 57.4224 16.7685 57.0993 20.5256C56.9916 22.0728 56.1302 27.4874 55.2688 33.3442C53.9767 41.6322 52.5769 50.6935 52.5769 50.6935C52.5769 50.6935 52.3615 53.2352 50.5311 53.6772C48.7006 54.1192 45.6856 52.1302 45.1473 51.6881C44.7165 51.3566 37.0715 46.3838 34.272 43.9527C33.5182 43.2897 32.6569 41.9637 34.3796 40.4166C38.256 36.7699 42.886 32.2392 45.6856 29.3661C46.9778 28.04 48.2698 24.9459 42.886 28.703C35.2411 34.1178 27.7038 39.201 27.7038 39.201C27.7038 39.201 25.9809 40.306 22.7507 39.3115C19.5203 38.317 15.7516 36.9909 15.7516 36.9909C15.7516 36.9909 13.1675 35.3334 17.5822 33.5652Z"
              fill="#111827" />
          </svg>
        </a>
        <a href="https://github.com/pvlppv" class="p-1.5 sm:p-2 rounded-lg flex items-center border border-gray-300 justify-center transition-all duration-500 hover:border-gray-100 hover:bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 64 64" aria-labelledby="title"
            aria-describedby="desc" role="img" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path data-name="layer2"
              d="M32 0a32.021 32.021 0 0 0-10.1 62.4c1.6.3 2.2-.7 2.2-1.5v-6c-8.9 1.9-10.8-3.8-10.8-3.8-1.5-3.7-3.6-4.7-3.6-4.7-2.9-2 .2-1.9.2-1.9 3.2.2 4.9 3.3 4.9 3.3 2.9 4.9 7.5 3.5 9.3 2.7a6.93 6.93 0 0 1 2-4.3c-7.1-.8-14.6-3.6-14.6-15.8a12.27 12.27 0 0 1 3.3-8.6 11.965 11.965 0 0 1 .3-8.5s2.7-.9 8.8 3.3a30.873 30.873 0 0 1 8-1.1 30.292 30.292 0 0 1 8 1.1c6.1-4.1 8.8-3.3 8.8-3.3a11.965 11.965 0 0 1 .3 8.5 12.1 12.1 0 0 1 3.3 8.6c0 12.3-7.5 15-14.6 15.8a7.746 7.746 0 0 1 2.2 5.9v8.8c0 .9.6 1.8 2.2 1.5A32.021 32.021 0 0 0 32 0z"
              fill="#202020">
            </path>
            <path data-name="layer1" d="M12.1 45.9c-.1.2-.3.2-.5.1s-.4-.3-.3-.5.3-.2.6-.1c.2.2.3.4.2.5zm1.3 1.5a.589.589 0 0 1-.8-.8.631.631 0 0 1 .7.1.494.494 0 0 1 .1.7zm1.3 1.8a.585.585 0 0 1-.7-.3.6.6 0 0 1 0-.8.585.585 0 0 1 .7.3c.2.3.2.7 0 .8zm1.7 1.8c-.2.2-.5.1-.8-.1-.3-.3-.4-.6-.2-.8a.619.619 0 0 1 .8.1.554.554 0 0 1 .2.8zm2.4 1c-.1.3-.4.4-.8.3s-.6-.4-.5-.7.4-.4.8-.3c.3.2.6.5.5.7zm2.6.2c0 .3-.3.5-.7.5s-.7-.2-.7-.5.3-.5.7-.5c.4.1.7.3.7.5zm2.4-.4q0 .45-.6.6a.691.691 0 0 1-.8-.3q0-.45.6-.6c.5-.1.8.1.8.3z"
              fill="#202020">
            </path>
          </svg>
        </a>
      </div>
      <details class="group px-3 sm:px-5">
        <summary class="cursor-pointer text-sm sm:text-base flex items-center justify-center gap-1">
          <span class="text-sm sm:text-base font-semibold">Подробнее о сайте</span>
          <span class="transition-transform duration-300 transform group-open:rotate-180">
              <svg class="w-5 h-5" fill="none" height="24" shape-rendering="geometricPrecision"
                  stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                  stroke-width="3" viewBox="0 0 24 24" width="24">
                  <path d="M6 9l6 6 6-6"></path>
              </svg>
          </span>
        </summary>
        <div class="overflow-hidden transition-all duration-300 ease-in-out max-h-0 group-open:max-h-96">
          <p class="mt-3 text-sm sm:text-base text-gray-600">
            Как-то, воодушевившись культурой трекинга, я создал личную базу данных, в которой начал полностью отслеживать свою жизнь.
            Я решил не останавливаться на этом и превратил её в проект по оцифровыванию себя, в котором стараюсь публично переносить всё из своей физической памяти в цифровую.
            В перспективе с этим проектом я могу заниматься аналитикой на своих же данных, собирать датасет для научного сообщества, увековечивать себя на этой странице интернета.
          </p>
        </div>
      </details>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
details > summary {
  list-style: none;
}

details > summary::-webkit-details-marker {
  display: none;
}
</style>
