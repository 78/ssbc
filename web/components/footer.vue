<template>
  <el-footer>
    <div>
        <h5>About ShouSiBaoCai</h5>
        <p>
          ShouSiBaoCai is a Search Engine based on DHT protocol. All resources are automatically indexed from the DHT network. Instead of torrent files, we store meta information only for indexing. 
        </p>
        <h5>About Magnet Links</h5>
        <p>
          Magnet URI Scheme is a de facto standard defining a uniform resource identifier (URI) scheme for Magnet links, which mainly refer to resources available for download via peer-to-peer networks. --Wikipedia
        </p>
    </div>
    <div>
        <p class="copyright">
        &copy; 2013 ~ 2019 www.shousibaocai.org
        </p>
    </div>
  </el-footer>
</template>

<style scoped>

.el-footer p{
  font-size: .8em;
}

.el-footer {
  height: 150px !important;
  margin: 20px auto;
  color: #555;
}

.el-footer p {
  padding: 5px 0;
}

.copyright {
  text-align: center;
  color: #888;
}
</style>
