import axios from 'axios';

let base = 'http://10.6.85.178:8001';
let appList = `${base}`+ "/" + "appList/"

// export const removeNode = params => { return axios.delete(`${base}/node/{params}`); };

// export const addNode = params => { return axios.post(`${base}/node/`, { params: params }); };

// export const requestLogin = {'username':'admin', 'password': '123456'}.then(res => res.data)
export const requestLogin = params => { return axios.post(`${base}/login/`, params).then(res => res.data); };

// appList
export const getAppList = params => { return axios.get(`${base}/appList.json`, { params: params }); };

export const deleteApplist = params => { return axios.delete(`${base}/appList/` + params.id) };

export const updateApplist = params => { return axios.patch(`${base}/appList/` + params.id, params) };

export const addApplist = params => { return axios.post(`${appList}`, params) };

// export const updateMasterConfig = params => { return axios.patch(`${base}/masterConfig/2`, params) };

// varnish
export const getVarnishList = params => { return axios.get(`${base}/varnishList.json`, { params: params }); };

// node
export const getNodelist = params => { return axios.get(`${base}/node.json`, { params: params }); };

export const addNode = params => { return axios.post(`${base}/node/`, params) };

export const updateNode = params => { return axios.patch(`${base}/node/` + params.id, params) };

export const deleteNode = params => { return axios.delete(`${base}/node/` + params.id) };

// update status
export const postStatus = params => { return axios.post(`${base}/update_status/`, params) };

// template
export const getTemplatelist = params => { return axios.get(`${base}/template.json`, { params: params }); };

export const addTemplate = params => { return axios.post(`${base}/template/`, params) };

export const updateTemplate = params => { return axios.patch(`${base}/template/` + params.id, params) };

export const deleteTemplate = params => { return axios.delete(`${base}/template/` + params.id) };

// masteritem
export const getMasterlist = params => { return axios.get(`${base}/masterItem.json`, { params: params }); };

export const addMaster = params => { return axios.post(`${base}/masterItem/`, params) };

export const updateMaster = params => { return axios.patch(`${base}/masterItem/` + params.id, params) };

export const deleteMaster = params => { return axios.delete(`${base}/masterItem/` + params.id) };

// masterconfig
export const getMasterConfig = params => { return axios.get(`${base}/masterConfig.json`, { params: params }) };

export const updateMasterConfig = params => { return axios.patch(`${base}/masterConfig/` + params.id, params) }

// flushcache
export const postAdd = params => { return axios.post(`${base}/flushCache/`, params) };

// logs
export const getApplog = params => { return axios.get(`${base}/log/app/`, { params: params }) }

export const getItemlog = params => { return axios.get(`${base}/log/item/`, { params: params }) }

export const getNodelog = params => { return axios.get(`${base}/log/node/`, { params: params }) }

export const getTemplatelog = params => { return axios.get(`${base}/log/template/`, { params: params }) }

// user and group
export const getUserList = params => { return axios.get(`${base}/user/`, { params: params }) }

export const getGroupList = params => { return axios.get(`${base}/group/`, { params: params }) }
