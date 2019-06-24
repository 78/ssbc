<template>
  <el-container>
    <el-header>
      <h1 class="title">
        手撕包菜
      </h1>
    </el-header>
    <el-main>
      <div class="content">
        <p class="subtitle">
          Search <b>anything</b> you want :D
        </p>
        <div style="margin-top: 15px;" v-on:keyup.enter="submit">
          <el-input placeholder="Movie names" v-model="keyword" class="input-keyword">
            <el-button slot="append" v-on:click="submit" icon="el-icon-search">Search</el-button>
          </el-input>
        </div>
      </div>
    </el-main>
    <Footer />
  </el-container>
</template>

<script>
import Footer from '~/components/footer.vue'

export default {
  components: {
    Footer
  },

  data() {
    return {
      keyword: ''
    }
  },

  methods: {
    submit() {
      if(this.keyword) {
        const url = '/search?q=' + encodeURIComponent(this.keyword)
        window.location = url
      }
    }
  }
};
</script>

<style scoped>
.el-container {
  min-height: 100vh;
  width: 800px;
  margin: 0 auto;
}

.subtitle {
  text-align: center;
}

.title {
  line-height: 60px;
  text-align: center;
}

.input-keyword {
  width: 500px;
}

.el-main {
  position: relative;
  width: 100%;
}
.content {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -250px;
  margin-top: -50px;
}
</style>
