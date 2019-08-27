<!--suppress JSUnusedGlobalSymbols, HtmlUnknownTarget, NpmUsedModulesInstalled -->
<template>
  <div class="full">
    <img src="@/assets/background.jpg" alt="" class="background">
    <el-card
      class="card"
      shadow="hover"
    >

      <div
        slot="header"
        class="card-header"
      >
        欢迎登陆百知课程管理系统
      </div>
      <div>
        <el-form
          ref="form"
          :model="form"
          label-position="right"
          label-width="80px"
          hide-required-asterisk
        >
          <el-form-item
            label="用户名："
            prop="username"
            :rules="[{ required: true, message: '请输入用户名', trigger: ['blur', 'change'] }]"
          >
            <el-autocomplete
              class="form-input"
              placeholder="请输入用户名"
              :fetch-suggestions="(queryString, cb)=>{cb([{ value: 'python'}])}"
              prefix-icon="el-icon-user"
              placement="top-start"
              v-model="form.username">
            </el-autocomplete>
          </el-form-item>
          <el-form-item
            label="密码："
            prop="password"
            :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]"
          >
            <el-input
              class="form-input"
              placeholder="请输入密码"
              show-password
              prefix-icon="el-icon-lock"
              @keydown.native.enter="submitHandler"
              v-model="form.password">
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              @click="submitHandler"
              class="button button-left"
            >
              登陆
            </el-button>
            <el-button
              @click="resetFields"
              class="button">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Notification, Card, Form, FormItem, Input, Autocomplete, Button } from 'element-ui'

import { postToken } from '@/api'

export default {
  name: 'Login',
  components: {
    'el-autocomplete': Autocomplete,
    'el-input': Input,
    'el-form': Form,
    'el-form-item': FormItem,
    'el-button': Button,
    'el-card': Card
  },
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      rule: {
        username: [
          { required: true, message: 'Please fill in the user name', trigger: 'blur' }
        ],
        password: [
          { required: true, message: 'Please fill in the password.', trigger: 'blur' },
          { type: 'string', min: 6, message: 'The password length cannot be less than 6 bits', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    resetFields () {
      this.$refs['form'].resetFields()
    },
    submitHandler () {
      this.$refs['form'].validate((valid) => {
        if (valid) {
          this.submit()
        } else {
          Notification({
            title: 'error',
            message: '请正确填写登录信息',
            type: 'error'
          })
        }
      })
    },
    submit () {
      postToken(this.form, new Date().getTime())
        .then(response => {
          this.$cookie.set('username', this.form.username, 1)
          this.$cookie.set('password', this.form.password, 1)
          this.$store.dispatch('setToken', response.data.token)
            .then(() => {
              this.$router.push({ path: '/schedule' })
            })
        })
        .catch(error => {
          Notification({
            title: '登录失败',
            message: '用户名或密码有误',
            type: 'error'
          })
          this.resetFields()
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
  .full {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }

  .background {
    min-width: 100%;
    min-height: 100%
  }

  .card {
    width: 400px;
    position: fixed;
    right: 160px;
    top: 50%;
    transform: translate(0, -50%);
    background-color: rgba(0, 0, 0, 0)
  }

  .card-header {
    text-align: center;
    font-size: x-large;
  }

  .card /deep/ * {
    color: white;
  }

  .form-input {
    width: 240px;
    background-color: rgba(0, 0, 0, 0)
  }

  .form-input /deep/ div, .form-input /deep/ input {
    background-color: rgba(0, 0, 0, 0)
  }

  .button {
    background-color: rgba(0, 0, 0, 0);
  }

  .button-left {
    margin-right: 50px;
  }

</style>
