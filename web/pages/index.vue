<template>
  <el-container>
    <el-header>
    </el-header>
    <el-main>
      <div class="content">
        <h1 class="title">
          手撕包菜
        </h1>
        <p class="subtitle">
          Search <b>anything</b> you want :D
        </p>
        <div style="margin-top: 30px;" v-on:keyup.enter="submit">
          <el-input placeholder="Movie names" v-model="keyword" class="input-keyword">
            <el-button slot="append" v-on:click="submit" icon="el-icon-search">Search</el-button>
          </el-input>
        </div>
        <p class="rank">
          <el-button type="text" @click="goLogsRank">Logs Rank</el-button>
          <el-button type="text" @click="goSpider">Spider Report</el-button>
        </p>
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
    },

    goLogsRank() {
      window.location = '/log'
    },

    goSpider() {
      window.location = '/spider'
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
  top: 20%;
  left: 50%;
  margin-left: -250px;
  margin-top: -50px;
}

.rank {
  text-align: center;
  margin-top: 15px;
}
</style>
