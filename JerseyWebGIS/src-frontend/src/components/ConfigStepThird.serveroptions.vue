<script setup>
import { useConfigStepNext, useConfigStepPre, useConfig } from '@/logic/setupconfig'
import { ArrowRight, ArrowLeft } from '@element-plus/icons-vue'

const config = useConfig()

const protocolOptions = [
	{ label: 'http', value: 'http' },
	{ label: 'https', value: 'https' }
]

const dbOptions = [
	{ label: 'sqlite', value: 'sqlite' }
]
</script>

<template>
	<div id="configOptions">
		<div id="info">
			<el-row>
				<h1 id="header">填写配置参数</h1>
			</el-row>
			<el-row>
				<h3 id="subheader">ServerOptions</h3>
			</el-row>
			<el-row>
				<p id="description" style="margin-top: .3rem;">
					此处填写的是您发布WebGIS服务的相关配置参数，包括访问域名、端口等。
					<br>
					下方选项填写会附带相关参数的说明。
				</p>
			</el-row>
		</div>

		<div id="component">
			<el-row>
				<el-form class="toBeCenter" style="width:60%" size="large" label-position="left">
					<el-form-item label="服务发布域名">
						<el-input v-model="config.options.domain" placeholder="即您当前服务器的域名地址或ipv4地址" />
						<p class="comment">
							该参数用于配置您后续发布服务时的服务页面与服务器后端的数据通信。它应该是您当前使用主机的网络地址。
						</p>
						<p class="comment">
							例如，如果您只是作为学习在本地主机上尝试，那么填写localhost或者由ipconfig(windows)||ifconfig(linux)得到的主机本地ip即可。
						</p>
					</el-form-item>
					<el-form-item label="服务发布端口">
						<el-input v-model="config.options.port" placeholder="端口号" />
						<p class="comment">
							服务发布的端口号，它用于用于配置您后续发布服务时的服务页面与服务器后端的数据通信。
						</p>
						<p class="comment">
							如果您已为当前主机使用ngix等工具配置了端口转发，那么填写None即可。
						</p>
					</el-form-item>
					<el-form-item label="服务使用协议">
						<el-select v-model="config.options.protocol" placeholder="http/https" size="large"
							style="width:100%">
							<el-option v-for="item in protocolOptions" :key="item.value" :label="item.label"
								:value="item.value">
							</el-option>
						</el-select>
						<p class="comment">
							如果您有配置https，可启用https进行服务的访问。
						</p>
					</el-form-item>
					<el-form-item label="数据库类型　">
						<el-select v-model="config.options.database" placeholder="存储数据的数据库类型" size="large"
							style="width:100%">
							<el-option v-for="item in dbOptions" :key="item.value" :label="item.label"
								:value="item.value">
							</el-option>
						</el-select>
						<p class="comment">
							选择一个数据库用于管理您发布服务时所获得的数据与服务相关配置的存储。
							目前只支持sqlite。
						</p>
					</el-form-item>
				</el-form>
			</el-row>
		</div>

		<div id="actionButton">
			<el-row>
				<el-button-group class="toBeCenter">
					<el-button type="danger" size="large" @click="useConfigStepPre">
						<el-icon>
							<ArrowLeft></ArrowLeft>
						</el-icon> 上一步
					</el-button>
					<el-button type="success" size="large" @click="useConfigStepNext">下一步 <el-icon>
							<ArrowRight></ArrowRight>
						</el-icon>
					</el-button>
				</el-button-group>
			</el-row>

		</div>
	</div>
</template>

<style scoped>
.toBeCenter {
	margin: 0 auto;
}

.comment {
	font-size: .6rem;
	color: #476582;
	margin-block-start: 0;
	margin-block-end: 0;
	line-height: normal
}

#header {
	font-size: 1.5rem;
	color: #0B346E;
	margin-bottom: 0;
}

#subheader {
	font-size: 1.3rem;
	line-height: 1.2;
	margin-top: .25rem;
	color: #476582;
}

#description {
	font-size: 1rem;
	color: #476582;
}

#actionButton {
	margin-top: 2.5rem
}

#component {
	margin-top: 3rem;
	margin-right: auto;
}
</style>