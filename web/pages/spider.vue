<template>
	<div>
		<el-page-header @back="goBack" title="" content="Spider Status">
		</el-page-header>
	    <el-table
	      size="small"
	      :data="tableData"
	      style="width: 100%">
	      <el-table-column
	        label="Date"
	        prop="_id"
	        width="200">
	      </el-table-column>
	      <el-table-column
	        prop="new_hashes"
	        label="New Hashes"
	        width="200">
	      </el-table-column>
	      <el-table-column
	        prop="total_reqs"
	        label="Total Requests"
	        width="200">
	      </el-table-column>
	      <el-table-column
	        prop="valid_reqs"
	        label="Valid Requests"
	        width="200">
	      </el-table-column>
	    </el-table>
	</div>
</template>


<script type="text/javascript">
export default {
	layout: 'search',

	async asyncData({$axios, error, query}) {
		const params = {}
		const res = await $axios.$get('/apis/spider', {params: params})
		return {tableData: res.items.slice(0, 30)}
	},

	methods: {
		goBack() {
			window.history.length > 1
		        ? this.$router.go(-1)
		        : this.$router.push('/')
		}
	}
};
</script>

<style type="text/css" scoped>
	
.el-page-header {
	margin: 0 0 10px 0;
}
</style>

