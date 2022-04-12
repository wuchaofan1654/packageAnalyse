<template>
  <router-view/>
</template>

<script>
export default {
  name: 'App',
  methods: {
    gotoPage(path) {
      this.$router.push({path: path})
    },
  }
}
</script>

<style>
body::-webkit-scrollbar {
  display: none;
}

.clearfix {
  height: 25px;
  alignment: center;
}

</style>
