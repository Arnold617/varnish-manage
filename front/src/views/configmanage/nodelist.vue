<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-button type="primary" @click="handleAdd"> + </el-button>
				</el-form-item>
				<el-form-item>
					<el-input v-model="filters.name" style="width: 300px" placeholder="模糊匹配"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="get_nodelist">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!-- 列表 -->
		<el-table :data="nodeList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="100px"></el-table-column>
			<el-table-column prop="room" label="机房" width="200px" sortable></el-table-column>
			<el-table-column prop="name" label="位置" min-width="20%" sortable></el-table-column>
			<el-table-column prop="ip" label="节点" min-width="40%" sortable></el-table-column>
			<el-table-column label="操作" width="150px">
				<template slot-scope="scope">
					<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
		
		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination @current-change="handleCurrentChange" :page-size="15" layout="total, prev, pager, next" :total="total">
			</el-pagination>
		</el-col>

		<!--编辑界面-->
		<el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
			<el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
				<el-form-item label="ID" prop="id">
					<el-input v-model="editForm.id" readonly></el-input>
				</el-form-item>
				<el-form-item label="机房" prop="room">
					<el-input v-model="editForm.room" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="位置">
					<el-input v-model="editForm.name"></el-input>
				</el-form-item>
				<el-form-item v-if="add_type==0" label="节点IP" prop="ip">
					<!-- <el-input v-model="plusForm.ip_address" style="width:200px" size="small"></el-input> -->
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
				<el-button @click.native="editFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--新增界面-->
		<el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
			<el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
				<el-form-item label="机房" prop="room">
					<el-input v-model="addForm.room" auto-complete="off" placeholder="机房名称"></el-input>
				</el-form-item>
				<el-form-item label="位置" prop="name">
					<el-input v-model="addForm.name" placeholder="机房具体位置"></el-input>
				</el-form-item>
				<el-form-item v-if="add_type==0" label="节点IP" prop="ip">
					<!-- <el-input v-model="plusForm.ip_address" style="width:200px" size="small"></el-input> -->
					<el-tag v-for="(tag,key) in ipAddrList" :key="tag" :disable-transitions="false" closable style="margin-right:3px"
					 @close="deleteIpAddr(tag,key)" type="primary">
						{{ tag }}
					</el-tag>
					<el-input v-if="ipInputVisible" ref="saveIpInput" v-model="ipInputVal" style="width:100px" size="small"
					 @keyup.enter.native="addIpAddr" @blur="addIpAddr" />
					<el-button v-else size="small" type="primary" @click="showIpInput">+ IP</el-button>
					<br>
					<span v-show="ipAddrList.length==0" style="color:red;font-size:12px">**注意：IP不可为空</span>
				</el-form-item>
				<el-form-item v-else label="CNAME" prop="ip_address">
					<el-input v-model="plusForm.ip_address" style="width:200px" size="small" />
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
		addNode, getNodelist, updateNode, deleteNode, postStatus,
	} from '@/api/api';

	export default {
		data() {
			return {
				nodeList: [],
				total: 0,
				listLoading: false,
				editFormVisible: false, //编辑界面是否显示
				editFormRules: {
					name: [{
						required: true,
						message: '请输入',
						trigger: 'blur'
					}]
				},
				editLoading: false,
				filters: {
				name: ''
				},
				//编辑界面数据
				editForm: {
					id: 0,
					room: '',
					name: '',
					// ip: '',
				},
				addFormVisible: false, //新增界面是否显示
				addLoading: false,
				addFormRules: {
					name: [{
						required: true,
						message: '请输入姓名',
						trigger: 'blur'
					}]
				},
				//新增界面数据
				addForm: {
					"id": 0,
					room: '',
					name: '',
					ip: ''
				},
				add_type: 0,
				ipInputVisible: false, // ip 输入框
				ipAddrList: [], // ip列表
				ipInputVal: null, // 新增ip

			}
		},

		created() {
			this.get_nodelist()
		},

		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.get_nodelist();
			},
			get_nodelist() {
				this.listLoading = true;
				const params = {
        page: this.page,
        name: this.filters.name
      }
				getNodelist(params)
					.then(res => {
						this.nodeList = res.data.data;
						this.total = res.data.count;
						this.listLoading = false;
					})
				// console.log(res)
			},
			// 显示编辑界面
			handleEdit: function(index, row) {
				this.editFormVisible = true;
				this.ipAddrList = row.ip.split(',')   //编辑页面的数据重整
				this.editForm = Object.assign({}, row); 
			},
			// 显示新增界面
			handleAdd: function() {
				this.addFormVisible = true;
				this.addForm = {
					"id": '',
					"room": '',
					"name": '',
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
							params.ip = this.ipAddrList.join(',')
							addNode(params)
								.then((res) => {
									this.addLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['addForm'].resetFields();
									this.addFormVisible = false;
									this.get_nodelist();
								});
								let para = {'status': 1}
								setTimeout(function(){
									postStatus(para)
									}, 2000)
						});
					}
				});
			},

			//编辑
			editSubmit: function() {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							//NProgress.start();
							const params = Object.assign({}, this.editForm);
							params.ip = this.ipAddrList.join(',')
							updateNode(params)
								.then((res) => {
									this.editLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['editForm'].resetFields();
									this.editFormVisible = false;
									this.get_nodelist();
								});
								let para = {'status': 1}
								setTimeout(function(){
									postStatus(para)
									}, 2000)
						});
					}
				});
			},

			// 删除ip
			deleteIpAddr(val, key) {
				// console.log(val, key)
				this.ipAddrList.splice(key, 1)
			},

			// 添加ip
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
			// 显示ip输入框
			showIpInput() {
				this.ipInputVisible = true
				this.$nextTick(_ => {
					this.$refs.saveIpInput.$refs.input.focus()
				})
			},

			//删除
			handleDel: function(index, row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					let params = { id: row.id}
					deleteNode(params)
						.then((res) => {
							this.listLoading = false;
							this.$message({
								message: '删除成功',
								type: 'success'
							});
							this.get_nodelist();
						});
				}).catch(() => {});
			},
		}
	}
</script>

<style>
</style>
