import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);

const pinia = createPinia();
app.use(pinia);

// Инициализация стора избранного (загрузка из localStorage)
import { useFavoritesStore } from "./stores/favorites";
const favoritesStore = useFavoritesStore(pinia);
favoritesStore.init();

app.mount("#app");
