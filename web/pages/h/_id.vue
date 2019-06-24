<template>
	<div>
		<div>
			<el-page-header @back="goBack" title="" :content="item.name">
			</el-page-header>
		</div>
		<div>
			<el-collapse v-model="activeNames" @change="handleChange">
			  <el-collapse-item title="Hash Information" name="1">
			    <div>First Log Time: {{item.ctime | datetime}}</div>
			    <div>Last Log Time: {{item.atime | datetime}}</div>
			    <div>File Size: {{item.len | size}}</div>
			    <div>Total Requests: {{item.reqs}}</div>
			    <div>
			    	Magnet Link:
				      <a rel="nofollow" :href="magnetLink">
				      	magnet:?xt=urn:btih:{{item.hash}}
				      </a>
				      &nbsp;
				      <a rel="nofollow" :href="magnetLink">
				      	Download
				      </a>
			    </div>
			  </el-collapse-item>
			  <el-collapse-item :title="item.files.length + ' Files'" name="2">
			    <div v-for="file in item.files">{{file.path}} {{file.length | size}}</div>
			  </el-collapse-item>
			  <el-collapse-item title="Download" name="4">
			    <div>If you want to get the torrent file or original data of {{item.name}}, please use uTorrent, BitTorrent or Thunder.
			    </div>
			    <div>
					<a rel="nofollow" target="_blank" :href="'http://www.haosou.com/s?q=' + encodeURIComponent(item.name) + '&src=ssbc'">
					Click here to locate the torrent file of {{item.name}}...
					</a>
				</div>
			  </el-collapse-item>
			  <el-collapse-item title="Related Resources" name="5">
			    <div v-for="ritem in related">
			    	<a :href="'/h/' + ritem.id">{{ritem.name}}</a> {{ritem.len | size}}
			    </div>
			  </el-collapse-item>
			  <el-collapse-item title="Copyright Infringement" name="6">
			    <div>If the content above is not authorized, please contact us via contact[AT]cilibaba.com. Remember to include the full url in your complaint.</div>
			  </el-collapse-item>
			</el-collapse>	
		</div>
	</div>
</template>

<script type="text/javascript">
export default {
	layout: 'search',

	async asyncData({params, $axios, error}) {
        try{
            const res = await $axios.$get('/apis/info', {params: {ids: params.id}})
            if(!res.items[0]) {
                error({statusCode: 404, message: 'Hash not found.'})
                return
            }
            const data = {
                item: res.items[0],
                activeNames: ['1', '2', '3', '4', '5', '6']
            }
            const res2 = await $axios.$get('/apis/related', {params: {keyword: data.item.name, count: 11}})
            data.related = res2.items.filter((x) => x.id != params.id)

            if(!data.item.files) {
                data.item.files = [{path: data.item.name, length: data.item.len}]
            }
            data.magnetLink = 'magnet:?xt=urn:btih:' + data.item.hash + '&dn=' + data.item.name
            return data
        }catch(e) {
            console.error(new Date(), params, e)
        }
	},

	methods: {
		goBack() {
			window.history.length > 1
		        ? this.$router.go(-1)
		        : this.$router.push('/')
		},
		handleChange() {

		}
	}
};
</script>

<style scoped>
</style>
