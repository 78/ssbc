import Vue from 'vue'
import moment from 'moment'

function size (length) {
	if(length < 1024)
		return Math.ceil(length) + ' bytes'
	length /= 1024
	if(length < 1024) 
		return Math.ceil(length) + ' KB'
	length /= 1024
	if(length < 1024) 
		return Math.ceil(length) + ' MB'
	length /= 1024
	if(length < 1024) 
		return Math.ceil(length) + ' GB'
}

function time (t) {
	let delta = new Date() - new Date(t)
	delta /= 60*1000
	if(delta < 60)
		return Math.floor(delta) + ' minutes'
	delta /= 60
	if(delta < 24)
		return Math.floor(delta) + ' hours'
	delta /= 24
	if(delta < 30)
		return Math.floor(delta) + ' days'
	delta /= 30
	if(delta < 12)
		return Math.floor(delta) + ' months'
	delta = delta * 30 / 365
	return Math.floor(delta) + ' years'
}

function datetime (t) {
	return moment(t).format('YYYY-MM-DD HH:mm:ss')
}

Vue.filter('size', size)
Vue.filter('time', time)
Vue.filter('datetime', datetime)
