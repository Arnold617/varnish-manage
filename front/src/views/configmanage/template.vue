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
					<el-button type="primary" v-on:click="get_templatelist">查询</el-button>
				</el-form-item>
			</el-form>
		</el-col>

		<!-- 列表 -->
		<el-table :data="templateList" highlight-current-row v-loading="listLoading" style="width: 100%;">
			<el-table-column type="index" label="ID" width="200px"></el-table-column>
			<el-table-column prop="name" label="名称" min-width="30%" sortable></el-table-column>
			<el-table-column prop="describe" label="描述" min-width="30%" sortable></el-table-column>
			<el-table-column label="操作" min-width="20%">
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
				<el-form-item label="名称" prop="name">
					<el-input v-model="editForm.name" auto-complete="off"></el-input>
				</el-form-item>
				<el-form-item label="描述" prop="describe">
					<el-input v-model="editForm.describe"></el-input>
				</el-form-item>
				<el-form-item label="内容" prop="content">
					<el-input type="textarea" v-model="editForm.content" style="50%" />
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
				<el-form-item label="名称" prop="name">
					<el-input v-model="addForm.name" auto-complete="off" placeholder="项目名称"></el-input>
				</el-form-item>
				<el-form-item label="描述" prop="describe">
					<el-input v-model="addForm.describe" placeholder="模板描述"></el-input>
				</el-form-item>
				<el-form-item label="内容" prop="content">
					<el-input type="textarea" placeholder="输入内容" v-model="addForm.content" style="50%" />
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
		addTemplate, getTemplatelist, updateTemplate, deleteTemplate
	} from '@/api/api';
	export default {
		data() {
			return {
				templateList: [],
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
					name: '',
					describe: '',
					content: '',
				},
				addFormVisible: false, //新增界面是否显示
				addLoading: false,
				addFormRules: {
					name: [{
						required: true,
						message: '请输入',
						trigger: 'blur'
					}]
				},
				//新增界面数据
				addForm: {
					"id": 0,
					name: '',
					describe: '',
					content: ''
				},
			}
		},

		created() {
			this.get_templatelist()
		},

		methods: {
			handleCurrentChange(val) {
				this.page = val;
				this.get_templatelist();
			},
			get_templatelist() {
				this.listLoading = true;
				const params = {
        page: this.page,
        name: this.filters.name
      }
				getTemplatelist(params)
					.then(res => {
						this.templateList = res.data.data;
						this.total = res.data.count;
						this.listLoading = false;
					})
			},
			// 显示编辑界面
			handleEdit: function(index, row) {
				this.editFormVisible = true;
				// this.ipAddrList = row.ip.split(',')   //编辑页面的数据重整
				this.editForm = Object.assign({}, row);
			},
			// 显示新增界面
			handleAdd: function() {
				this.addFormVisible = true;
				this.addForm = {
					"id": '',
					"name": '',
					"describe": '',
					"content": ''
				}
			},
			//删除
			handleDel: function(index, row) {
				this.$confirm('确认删除该记录吗?', '提示', {
					type: 'warning',
				}).then(() => {
					this.listLoading = true;
					let params = { id: row.id}
					deleteTemplate(params)
						.then((res) => {
							this.listLoading = false;
							//NProgress.done();
							this.$message({
								message: '删除成功',
								type: 'success'
							});
							this.get_templatelist();
						});
				}).catch(() => {});
			},
			//编辑
			editSubmit: function() {
				this.$refs.editForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.editLoading = true;
							const params = Object.assign({}, this.editForm);
							updateTemplate(params)
								.then((res) => {
									this.editLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['editForm'].resetFields();
									this.editFormVisible = false;
									this.get_templatelist();
								});
						});
					}
				});
			},

			//新增
			addSubmit: function() {
				this.$refs.addForm.validate((valid) => {
					if (valid) {
						this.$confirm('确认提交吗？', '提示', {}).then(() => {
							this.addLoading = true;
							let params = Object.assign({}, this.addForm);
							addTemplate(params)
								.then((res) => {
									this.addLoading = false;
									this.$message({
										message: '提交成功',
										type: 'success'
									});
									this.$refs['addForm'].resetFields();
									this.addFormVisible = false;
									this.get_templatelist();
									// this.ipAddrList = []
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
