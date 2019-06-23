<template>
  <el-container>
    <el-header>
      <div class="title">
        <a href="/">手撕包菜</a>
      </div>
      <div class="search-box" v-on:keyup.enter="submit">
        <el-input size="small" placeholder="Movie names" v-model="keyword" class="mini-input-keyword">
          <el-button size="small" slot="append" v-on:click="submit" icon="el-icon-search"></el-button>
        </el-input>
      </div>
    </el-header>
    <el-main>
      <nuxt />
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

  mounted() {
    this.keyword = this.$route.query.q
  },

  methods: {
    submit() {
      window.location = '/search?q=' + encodeURIComponent(this.keyword)
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

.title {
  line-height: 60px;
  float: left;
  padding: 0 30px 0 0;
}

.title a {
  color: #555;
  text-decoration: none;
  font-size: 1.2em;
}

.search-box {
  line-height: 60px;
  float: left;
}

.mini-input-keyword {
  width: 250px;
}

.el-header {
  height: 160px;
}

</style>
