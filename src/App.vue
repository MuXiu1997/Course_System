<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
  /*body {*/
  /*      margin: 0;*/
  /*      padding: 0;*/
  /*      overflow: hidden !important;*/
  /*    }*/

  /*#app {*/
  /*  font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
  /*  -webkit-font-smoothing: antialiased;*/
  /*  -moz-osx-font-smoothing: grayscale;*/
  /*  text-align: center;*/
  /*  color: #2c3e50;*/
  /*}*/
  /*#nav {*/
  /*  padding: 30px;*/
  /*  a {*/
  /*    font-weight: bold;*/
  /*    color: #2c3e50;*/
  /*    &.router-link-exact-active {*/
  /*      color: #42b983;*/
  /*    }*/
  /*  }*/
  /*}*/
  /*.ivu-input[disabled], fieldset[disabled] .ivu-input {*/
  /*  background-color: #fff !important;*/
  /*  color: #000 !important;*/
  /*}*/

  /*.el-input-number__decrease, .el-input-number__increase {*/
  /*  background-color: #fff !important;*/
  /*}*/
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
