<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
}

</script>

<style lang="scss">
  body {
        margin: 0;
        padding: 0;
        overflow: hidden !important;
      }

  .scrollStyle::-webkit-scrollbar {
    width: 9px;
    height: 9px;
  }

  .scrollStyle::-webkit-scrollbar-button, .scrollStyle::-webkit-scrollbar-track {
    display: none;
  }

  .scrollStyle::-webkit-scrollbar-button {
    display: none;
  }

  .scrollStyle::-webkit-scrollbar-track-piece {
    background: rgba(140, 140, 140, 0.25);
  }

  .scrollStyle::-webkit-scrollbar-thumb {
    background: rgba(64, 158, 255, 0.6);
    border-radius: 6px;
  }
</style>
