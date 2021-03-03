import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Main from './views/Main.vue'
import FlushCache from './views/flushcache/index.vue'
import applist from './views/configmanage/applist.vue'
import nodelist from './views/configmanage/nodelist.vue'
import template from './views/configmanage/template.vue'
import MasterConfig from './views/configmanage/MasterConfig.vue'
import dashbord from './views/dashbord/index.vue'
import auth from './views/auth/index.vue'
import appLog from './views/logs/index.vue'
import masterLog from './views/logs/masterlog.vue'
import nodeLog from './views/logs/nodelog.vue'
import templateLog from './views/logs/templatelog.vue'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/',
        component: Home,
        name: '',
        iconCls: 'fa el-icon-share',
        leaf: true,//只有一个节点
        children: [
            { path: '/dashbord', component: dashbord, name: 'Dashbord' }
        ]
    },
    {
        path: '/',
        component: Home,
        name: '配置管理',
        iconCls: 'fa el-icon-setting',//图标样式class
        children: [
            { path: '/main', component: Main, name: '主页', hidden: true },
			{ path: '/applist', component: applist, name: '应用列表' },
			{ path: '/nodelist', component: nodelist, name: '节点管理' },
			{ path: '/template', component: template, name: '模板管理' },
			{ path: '/masterconfig', component: MasterConfig, name: '主配置'}
        ]
    },
    {
        path: '/',
        component: Home,
        name: '',
        iconCls: 'fa fa-id-card-o',
		leaf: true,
        children: [
            { path: '/flushcache', component: FlushCache, name: '缓存刷新' }
        ]
    },
    {
        path: '/',
        component: Home,
        name: '',
        iconCls: 'fa el-icon-date',
        leaf: true,//只有一个节点
        children: [
            { path: '/auth', component: auth, name: '权限管理' }
        ]
    },
	{
	    path: '/',
	    component: Home,
	    name: '日志审计',
	    iconCls: 'fa el-icon-view',
	    children: [
            { path: '/index', component: appLog, name: '应用日志' },
            { path: '/nodelog', component: nodeLog, name: '节点日志' },
            { path: '/templatelog', component: templateLog, name: '模板日志' },
            { path: '/masterlog', component: masterLog, name: '主配置日志' },
	    ]
	},
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;