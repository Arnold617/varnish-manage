<template>
	<section>
		<!-- 工具条 -->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<div class="grid-item">
								<span>搜索名称</span>
								<div style="display:inline-block">
									<el-select v-model="filterQuery" filterable placeholder="请选择">
										<el-option label="域名" value="domain"/>
                		<el-option label="ip" value="ip_address"/>
                		<el-option label="机房" value="room"/>
                		<el-option label="产品" value="product"/>
              		</el-select>
								</div>
							</div>
				</el-form-item>
				<el-form-item>
					<el-input v-model="filters.name" style="width: 300px" placeholder="模糊匹配"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="get_applist">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleAdd">新增</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="appList" :header-cell-style="{background:'#DFE6EC'}" highlight-current-row v-loading="listLoading" 
		element-loading-text="老板,不再等一下吗?" style="width:100%;font-size:14px" border fit>
			<el-table-column type="index" align="center" label="ID" width="66px"></el-table-column>
			<el-table-column prop="product" align="center" label="产品" min-width="10%">
			</el-table-column>
			<el-table-column prop="domain" align="center" label="域名" min-width="15%">
			</el-table-column>
			<el-table-column prop="name" align="center" label="名称" min-width="10%">
			</el-table-column>
			<el-table-column prop="room" align="center" label="机房" min-width="10%" sortable>
			</el-table-column>
			<el-table-column prop="ip_address" align="center" label="后端ip" min-width="30%" sortable>
			</el-table-column>
			<el-table-column prop="template" label="模板内容" v-if="false" ></el-table-column>
			<el-table-column label="操作" align="center" width="150px">
				<template slot-scope="scope">
					<el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<!-- <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button> -->
			<!-- <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :total="total" style="float:right;"> -->
			<el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination>
		</el-col>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="ID" prop="id">
					<el-input v-model="editForm.id" readonly></el-input>
				</el-form-item>
				<el-form-item label="产品" prop="product">
                                        <!-- <el-input v-model="editForm.product" auto-complete="off"></el-input> -->
                                        <el-select v-model="editForm.product" filterable size="small">
                                                <el-option label="test1" value="test1"></el-option>
                                                <el-option label="test2" value="test2"></el-option>
                                                <el-option label="test2" value="test3"></el-option>
                                        </el-select>
                                </el-form-item>
				<el-form-item label="域名" prop="domain">
					<el-input v-model="editForm.domain" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="名称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="机房" prop="room">
					<el-select v-model="editForm.room" value-key="id" multiple filterable style="width: 200px">
						<el-option v-for="(item,index) in nodeList" :key="index" :label="item.room" :value="item.room"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-if="add_type==0" label="后端IP" prop="ip_address">
					<el-tag v-for="(tag,key) in ipAddrList" :key="tag" :disable-transitions="false" closable style="margin-right:3px"
					 @close="deleteIpAddr(tag,key)" type="primary" effect="plain">
						{{ tag }}
					</el-tag>
					<el-input v-if="ipInputVisible" ref="saveIpInput" v-model="ipInputVal" style="width:100px" size="small"
					 @keyup.enter.native="addIpAddr" @blur="addIpAddr" />
					<el-button v-else size="small" type="primary" @click="showIpInput">+ IP</el-button>
					<br>
					<span v-show="ipAddrList.length==0" style="color:red;font-size:12px">**注意：IP不可为空</span>
				</el-form-item>
				<el-form-item label="模板内容" prop="template">
					<el-input type="textarea" v-model="editForm.template" style="50%" />
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--新增界面-->
		<el-dialog title="编辑" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
				<el-form-item label="产品" prop="product">
					<!-- <el-input v-model="editForm.product" auto-complete="off"></el-input> -->
					<el-select v-model="addForm.product" filterable size="small">
						<el-option label="test1" value="test1"></el-option>
						<el-option label="test2" value="test2"></el-option>
						<el-option label="test3" value="test3"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="域名" prop="domain">
					<el-input v-model="addForm.domain" auto-complete="off" placeholder="项目域名"></el-input>
				</el-form-item>
				<el-form-item label="名称" prop="name">
					<el-input v-model="addForm.name" auto-complete="off" placeholder="项目名称"></el-input>
				</el-form-item>
				<el-form-item label="机房" prop="room">
					<el-select v-model="addForm.room" value-key="id" multiple filterable style="width: 200px;">
						<el-option v-for="(item,index) in nodeList" :key="index" :label="item.room" :value="item.room"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="模板" prop="template">
					<el-select v-model="addForm.template" filterable style="width: 300px">
						<el-option v-for="(item,index) in templateList" :key="index" :label="item.name" :value="item.content"></el-option>
					</el-select>
				</el-form-item>
				<el-form-item v-if="add_type==0" label="后端IP" prop="ip_address">
					<el-tag v-for="(tag,key) in ipAddrList" :key="tag" :disable-transitions="false" closable style="margin-right:3px"
					 @close="deleteIpAddr(tag,key)" type="primary" effect="plain">
						{{ tag }}
					</el-tag>
					<el-input v-if="ipInputVisible" ref="saveIpInput" v-model="ipInputVal" style="width:100px" size="small"
					 @keyup.enter.native="addIpAddr" @blur="addIpAddr" />
					<el-button v-else size="small" type="primary" @click="showIpInput">+ IP</el-button>
					<br>
					<span v-show="ipAddrList.length==0" style="color:red;font-size:12px">**注意：IP不可为空</span>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="addFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
			</div>
		</el-dialog>

	</section>
</template>

<script>
import {
		getAppList, getNodelist, getTemplatelist, deleteApplist, updateApplist, addApplist
	} from '@/api/api';
	export default {
		data() {
			return {
				filters: {
					name: ''
				},
				appList: [],
				nodeList: [],
				templateList: [],
				total: 0,
				page: 1,
				listLoading: false,
				editFormVisible: false, //编辑界面是否显示
				editFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
					domain: [{
						required: true,
						message: '请输入域名',
						trigger: 'blur'
					}],
					template: [{
						required: true,
						message: '请选择模板',
						trigger: 'blur'
					}],
					ip_address: [{
						required: true,
						message: 'ip不可为空',
						trigger: 'change'
					}],
					product: [{
						required: true,
						message: '请选择产品',
						// trigger: 'blur
					}]
				},
				//编辑界面数据
				editForm: {
					id: 0,
					product: '',
					domain: '',
					name: '',
					room: '',
				},
				filterQuery: 'domain',
				editLoading: false,
				add_type: 0,
				ipInputVisible: false, // ip 输入框
				ipAddrList: [], // ip列表
				ipInputVal: null, // 新增ip

				addFormVisible: false, //新增界面是否显示
				addLoading: false,
				addFormRules: {
					name: [{
						required: true,
						message: '请输入名称',
						trigger: 'blur'
					}],
					domain: [{
						required: true,
						message: '请输入域名',
						trigger: 'blur'
					}],
					product: [{
						required: true,
						message: '请选择产品',
						// trigger: 'blur
					}]
				},
				//新增界面数据
				addForm: {
					template: '',
					product: '',
					domain: '',
					name: '',
					room: '',
				},
			}
		},
		created() {
			this.get_applist()
			this.get_templatelist()
			this.get_nodelist()
		},
		// mounted() {
		// 	this.get_applist();
		// },

		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.get_applist();
			},
			get_nodelist() {
				getNodelist()
					.then(res => {
						this.nodeList = res.data.data
					})
			},
			get_templatelist() {
				getTemplatelist()
					.then(res => {
						this.templateList = res.data.data
					})
			},
			get_applist() {
				const name = this.filterQuery
				let params = {
					page: this.page,
					// domain: this.filters.name
				};
				params[name] = this.filters.name
				this.listLoading = true;
				getAppList(params)
					.then(res => {
						this.appList = res.data.data
						this.total = res.data.count;
						this.listLoading = false;
					})
			},
			// 显示编辑界面
			handleEdit: function(index, row) {
				this.editFormVisible = true;
				row.room = row.room.split(',') // 多选框需要list格式
				this.ipAddrList = row.ip_address.split(',') //编辑页面的数据重整
				this.editForm = Object.assign({}, row);
			},

			//删除
			handleDel: function(index, row) {
				this.$confirm('确认删除该域名吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					let para = {'status': 1}
					updateMasterConfig(para)

					// this.$axios.delete(url)
					let params = { id: row.id}
					deleteApplist(params)
						.then((res) => {
							this.listLoading = false;
							//NProgress.done();
							this.$message({
								message: '删除成功',
								type: 'success'
							});
							this.get_applist();
						});
				}).catch(() => {});
			},
			// 显示ip输入框
			showIpInput() {
				this.ipInputVisible = true
				this.$nextTick(_ => {
					this.$refs.saveIpInput.$refs.input.focus()
				})
			},
			//编辑
			editSubmit: function() {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							const params = Object.assign({}, this.editForm);
							params.room = params.room.join(',')
							params.ip_address = this.ipAddrList.join(',')
							params.status = 1
							// console.log(params)
							// let url = 'http://10.6.85.178:8001/appList/' + params.id;
							// this.$axios.patch(url, params)
							updateApplist(params)
								.then((res) => {
									this.editLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['editForm'].resetFields();
									this.editFormVisible = false;
									this.get_applist();
								});
						});
					}
				});
			},
			// 添加ip和检验
			addIpAddr() {
				if (this.ipInputVal) {
					const reg =
						/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/
					if (reg.test(this.ipInputVal)) {
						const self = this
						const re = this.ipAddrList.find(function(inputArr) {
							return inputArr == self.ipInputVal
						})
						if (!re) {
							this.ipAddrList.push(this.ipInputVal)
							this.ipInputVisible = false
							this.ipInputVal = null
						} else {
							this.$message({
								message: this.ipInputVal + '已经存在',
								type: 'warning'
							})
							this.ipInputVisible = false
							this.ipInputVal = null
						}
					} else {
						this.$message({
							message: this.ipInputVal + '校验失败',
							type: 'warning'
						})
						this.ipInputVisible = false
						this.ipInputVal = null
					}
				}
			},

			// 删除ip
			deleteIpAddr(val, key) {
				// console.log(val, key)
				this.ipAddrList.splice(key, 1)
			},
			// 显示新增界面
			handleAdd: function() {
				// console.log(this.templateList);
				this.addFormVisible = true;
				this.addForm = {
					'product': '',
					'domain': '',
					'name': '',
					'room': [],
					// "ip": ''
				};
				this.ipAddrList = [];
			},
			//新增
			addSubmit: function() {
				this.$refs.addForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.addLoading = true;
							const params = Object.assign({}, this.addForm);
							params.room = params.room.join(',')
							params.ip_address = this.ipAddrList.join(',')
							params.status = 1
							let para = {'status': 1}
							updateMasterConfig(para)
							addApplist(params)
								.then((res) => {
									this.addLoading = false;
									// console.log(para.template)
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['addForm'].resetFields();
									this.addFormVisible = false;
									this.get_applist();
								});
						});
					}
				});
			},


		}
	}
</script>

<style>
</style>
