<template>
  <div
    style="background-color: rgba(64, 158, 255, 1);position: fixed;top: 0;right: 0;bottom: 0;left: 0">
    <Card shadow
          style=
            "display: inline-block;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%,-50%);
            text-align: center;"
    >
      <Form ref="form" :model="form" :rules="rule">
        <FormItem prop="user">
          <label>
            <Input type="text" v-model="form.userName" placeholder="Username">
              <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
          </label>
        </FormItem>
        <FormItem prop="password">
          <label>
            <Input type="password" v-model="form.password" @on-enter="handleSubmit('form')" placeholder="Password">
              <Icon type="ios-lock-outline" slot="prepend"></Icon>
            </Input>
          </label>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="handleSubmit('form')">SignIn</Button>
        </FormItem>
      </Form>
    </Card>
  </div>
</template>

<script>
import { Notification } from 'element-ui'
import {
  Input,
  Form,
  FormItem,
  Button,
  Icon,
  Card
} from 'iview'
export default {
  name: 'Login',
  components: {
    'Input': Input,
    'Form': Form,
    'FormItem': FormItem,
    'Button': Button,
    'Icon': Icon,
    'Card': Card
  },
  data () {
    return {
      form: {
        userName: '',
        password: ''
      },
      rule: {
        userName: [
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
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
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
      this.$axios.post('/api/sessions', this.form)
        .then(response => {
          console.log(response.data.token)
          this.$cookie.set('Token', response.data.token, 1)
          this.$store.dispatch('setToken', response.data.token)
            .then(() => {
              this.$router.push({ path: '/' })
            })
        })
        .catch(error => {
          Notification({
            title: '登录失败',
            message: '用户名或密码有误',
            type: 'error'
          })
          this.form.userName = ''
          this.form.password = ''
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
</style>
