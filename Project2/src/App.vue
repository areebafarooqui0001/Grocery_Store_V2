<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #828080;
}

::-webkit-scrollbar-thumb {
  background: #0b0a0a;
  border-radius: 30px;
}

::-webkit-scrollbar-thumb:hover {
  background: #141414;
}

body {
  overflow-y: hidden;
  overflow-x: scroll;
  background: rgb(205, 237, 249);
}

.content {
  /* padding-left: 32px;
  padding-right: 32px; */
  padding-bottom: 100px;
  min-height: 100vh;
  max-height: 100vh;
  overflow-y: auto;

}
</style>
