<template>
	<div>
		<el-page-header @back="goBack" title="" :content="'Logs Rank ' + date">
		</el-page-header>
	    <el-table
	      size="small"
	      :data="tableData"
	      style="width: 100%">
	      <el-table-column
	        label="Name"
	        width="500">
		      <template slot-scope="scope">
		        <a :href="'/h/' + scope.row.info.id">{{ scope.row.info.name }}</a>
		      </template>
	      </el-table-column>
	      <el-table-column
	        prop="reqs"
	        label="Requests"
	        width="90">
	      </el-table-column>
	      <el-table-column
	        label="Last Log Time">
		      <template slot-scope="scope">
		        {{ scope.row.atime | datetime }}
		      </template>
	      </el-table-column>
	    </el-table>
		<div>
			<el-pagination
			  background
			  layout="prev, pager, next"
			  @current-change="handleChangePage"
			  :current-page="currentPage"
			  :page-size="20"
			  :pager-count="11"
			  :total="2000">
			</el-pagination>
		</div>
	</div>
</template>


<script type="text/javascript">
export default {
	layout: 'search',

	async asyncData({$axios, error, query}) {
        const page = parseInt(query.p || 1)
        const params = {
            start: (page - 1) * 10,
            count: 20
        }
		const res = await $axios.$get('/apis/log', {params: params})
		return {tableData: res.items, currentPage: page, date: res.date}
	},

	methods: {
		goBack() {
			window.history.length > 1
		        ? this.$router.go(-1)
		        : this.$router.push('/')
		},
		handleChangePage(val) {
			window.location = '/log?p=' + val
		}
	}
};
</script>

<style type="text/css" scoped>
	
.el-pagination {
	margin: 30px 0 10px 0;
}
.el-page-header {
	margin: 0 0 10px 0;
}
</style>

