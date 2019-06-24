<template>
	<div>
		<p class="total-meta">
			Found {{meta.total_found}} items for {{keyword}} in {{meta.time}}s.
		</p>
		<div class="list">
			<div class="item" v-for="item in items">
				<div class="name">
					<a :href="'/h/' + item.id">{{item.name}}</a>
				</div>
				<div class="meta">
					{{item.files.length}} files, {{item.len | size}}, {{item.reqs}} requests, logged {{item.atime | time}} ago
				</div>
				<div class="files">
					<div v-for="file in item.files.slice(0, 5)">
						<p><span v-html="file.path"></span> {{file.length | size}}</p>
					</div>
					<p>....</p>
				</div>
			</div>
		</div>
		<div>
			<el-pagination
			  background
			  layout="prev, pager, next"
			  @current-change="handleChangePage"
			  :current-page="currentPage"
			  :page-size="10"
			  :total="Math.min(meta.total, meta.total_found)">
			</el-pagination>
		</div>
	</div>
</template>


<script type="text/javascript">
export default {
	layout: 'search',

	async asyncData({query, $axios}) {
        try{
            console.log(new Date(), 'search', query.q)
            const page = parseInt(query.p || 1)
            const params = {
                keyword: query.q,
                detail: 1,
                start: (page - 1) * 10,
                count: 10
            }
            const res = await $axios.$get('/apis/search', {params: params})
            const data = {
                items: res.items,
                meta: res.meta,
                keyword: query.q,
                currentPage: page,
                words: query.q.replace(/。|，|,|！|…|!|《|》|<|>|\"|'|:|：|？|\?|、|\||“|”|‘|’|；|—|（|）|·|\(|\)|　|\.|【|】|『|』|@|&|%|\^|\*|\+|\||<|>|~|`|\[|\]/g, ' ').split(' ').filter((x) => x!='')
            }
            data.items.forEach((v) => {
                if(!v.files) {
                    v.files = [{path: v.name, length: v.len}]
                }
                v.files.sort((a, b) => b.length - a.length)
                v.files = v.files.slice(0, 5)
                v.files.forEach((s) => {
                    for(const w of data.words) {
                        s.path = s.path.replace(new RegExp(w, 'ig'), (p1) => {
                            return '<span class="highlight">' + p1 + '</span>'
                        })
                    }
                })
            })
            return data
        }catch(e){
            console.error(new Date(), query, e)
        }
	},

	methods: {
		handleChangePage(val) {
			const query = this.$route.query
			window.location = '/search?q=' + encodeURIComponent(query.q) + '&p=' + val
		}
	},

	head() {
		return {
			title: this.$route.query.q + ' - 手撕包菜'
		}
	}
};
</script>

<style scoped>
.list {

}
.item {
	padding: 10px 0;
}
.item .meta {
	font-size: .8em;
	color: #2b8200;
	padding: 5px 0;
}

.item .files {
	font-size: .8em;
	color: #555;
}


.el-pagination {
	margin: 30px 0 10px 0;
}

.total-meta {
	margin: 0 0 10px 0;
}

</style>
